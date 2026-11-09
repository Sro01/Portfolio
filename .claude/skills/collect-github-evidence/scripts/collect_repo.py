#!/usr/bin/env python3
"""저장소 하나에서 본인이 작성한 커밋과 관련 PR을 수집해 원장 파일로 저장한다.

PR 여부와 무관하게 모든 브랜치의 커밋을 작성자 이메일로 찾고,
PR 커밋 목록·병합 커밋과 SHA로 대조해 전달 경로(PR/직접 push/브랜치 전용)를 표시한다.

필요한 것: git, 로그인된 gh CLI. 표준 라이브러리만 사용한다.

사용 예:
  python3 -I collect_repo.py --repo owner/name --login Sro01 \
      --out archive/research/github/2026-11-09/owner-name [--email a@b.c ...] [--numstat]
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

FIELD = "\x1f"
RECORD = "\x1e"
PR_COMMITS_API_LIMIT = 250  # GitHub API는 PR당 커밋을 250개까지만 돌려준다
CO_AUTHOR = re.compile(r"^co-authored-by:\s*(.+?)\s*<([^>]+)>\s*$", re.I | re.M)


def run(cmd: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"명령 실패: {' '.join(cmd)}\n{result.stderr.strip()}")
    return result.stdout


def gh_json(args: list[str]):
    return json.loads(run(["gh", *args]) or "null")


def clone(repo: str, work: Path) -> Path:
    dest = work / repo.replace("/", "__")
    if not dest.exists():
        run(["gh", "repo", "clone", repo, str(dest), "--", "--filter=blob:none", "--no-checkout", "-q"])
    run(["git", "fetch", "-q", "--prune", "origin", "+refs/heads/*:refs/remotes/origin/*"], cwd=dest)
    return dest


def read_commits(repo_dir: Path) -> list[dict]:
    fmt = FIELD.join(["%H", "%an", "%ae", "%aI", "%cn", "%ce", "%cI", "%P", "%s", "%b"]) + RECORD
    raw = run(["git", "log", "--all", f"--format={fmt}"], cwd=repo_dir)
    commits = []
    for chunk in raw.split(RECORD):
        chunk = chunk.strip("\n")
        if not chunk:
            continue
        sha, an, ae, aI, cn, ce, cI, parents, subject, body = chunk.split(FIELD)
        commits.append({
            "sha": sha, "author_name": an, "author_email": ae.lower(), "authored_at": aI,
            "committer_name": cn, "committer_email": ce.lower(), "committed_at": cI,
            "parents": parents.split(), "title": subject, "body": body.strip(),
        })
    return commits


def branch_membership(repo_dir: Path) -> dict[str, list[str]]:
    branches = [b.strip() for b in run(["git", "branch", "-r", "--format=%(refname:short)"], cwd=repo_dir).splitlines()]
    membership: dict[str, list[str]] = defaultdict(list)
    for branch in branches:
        if branch.endswith("/HEAD") or "/" not in branch:
            continue
        for sha in run(["git", "rev-list", branch], cwd=repo_dir).split():
            membership[sha].append(branch.split("/", 1)[1])
    return membership


def resolve_identities(repo: str, commits: list[dict], login: str, extra: list[str]) -> tuple[set[str], list[dict]]:
    """작성자 이메일마다 커밋 하나의 GitHub 계정을 확인해 본인 이메일을 찾는다."""
    by_email: dict[str, dict] = {}
    for c in commits:
        by_email.setdefault(c["author_email"], c)
    counts = Counter(c["author_email"] for c in commits)
    identities = {e.lower() for e in extra}
    table = []
    for email, sample in by_email.items():
        linked = gh_json(["api", f"repos/{repo}/commits/{sample['sha']}", "--jq", "{login: .author.login}"])
        linked_login = (linked or {}).get("login")
        mine = email in identities or (linked_login or "").lower() == login.lower()
        if mine:
            identities.add(email)
        table.append({
            "email": email, "name": sample["author_name"], "commits": counts[email],
            "github_login": linked_login, "counted_as_mine": mine,
            "reason": "user_provided" if email in {e.lower() for e in extra} else ("login_match" if mine else None),
        })
    return identities, sorted(table, key=lambda r: -r["commits"])


def read_prs(repo: str) -> tuple[list[dict], bool]:
    fields = "number,title,body,state,author,url,createdAt,mergedAt,closedAt,baseRefName,headRefName,mergeCommit,additions,deletions,changedFiles"
    prs = gh_json(["pr", "list", "-R", repo, "--state", "all", "--limit", "5000", "--json", fields]) or []
    truncated = False
    for pr in prs:
        shas = run(["gh", "api", "--paginate", f"repos/{repo}/pulls/{pr['number']}/commits", "--jq", ".[].sha"]).split()
        pr["commit_shas"] = shas
        pr["commit_list_truncated"] = len(shas) >= PR_COMMITS_API_LIMIT
        truncated = truncated or pr["commit_list_truncated"]
        pr["author"] = (pr.get("author") or {}).get("login")
        pr["merge_commit_sha"] = (pr.pop("mergeCommit", None) or {}).get("oid")
    return sorted(prs, key=lambda p: p["number"]), truncated


def numstat(repo_dir: Path, sha: str) -> dict:
    out = run(["git", "show", "--numstat", "--format=", sha], cwd=repo_dir)
    files, added, deleted = [], 0, 0
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        a, d, path = parts
        files.append(path)
        added += int(a) if a.isdigit() else 0
        deleted += int(d) if d.isdigit() else 0
    return {"files": files, "additions": added, "deletions": deleted}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="owner/name")
    ap.add_argument("--login", required=True, help="본인 GitHub 로그인")
    ap.add_argument("--email", action="append", default=[], help="본인 커밋 이메일(여러 번 지정 가능)")
    ap.add_argument("--out", required=True, help="결과를 저장할 폴더")
    ap.add_argument("--work", help="clone 위치(기본: 임시 폴더). archive 밖을 쓴다")
    ap.add_argument("--numstat", action="store_true", help="커밋별 변경 파일·줄 수 포함(파일 내용 일부를 추가로 받음)")
    args = ap.parse_args()

    out = Path(args.out)
    if (out / "commits.json").exists():
        sys.exit(f"이미 수집 결과가 있습니다: {out}. 덮어쓰지 않습니다. 다른 폴더를 지정하세요.")
    out.mkdir(parents=True, exist_ok=True)
    work = Path(args.work) if args.work else Path(tempfile.mkdtemp(prefix="collect-github-"))
    work.mkdir(parents=True, exist_ok=True)

    meta = gh_json(["repo", "view", args.repo, "--json", "nameWithOwner,isPrivate,defaultBranchRef,url"])
    default_branch = meta["defaultBranchRef"]["name"]
    repo_dir = clone(args.repo, work)

    all_commits = read_commits(repo_dir)
    identities, identity_table = resolve_identities(args.repo, all_commits, args.login, args.email)
    membership = branch_membership(repo_dir)
    prs, truncated = read_prs(args.repo)

    in_pr: dict[str, list[int]] = defaultdict(list)
    merged_by_pr: dict[str, int] = {}
    for pr in prs:
        for sha in pr["commit_shas"]:
            in_pr[sha].append(pr["number"])
        if pr["merge_commit_sha"]:
            merged_by_pr[pr["merge_commit_sha"]] = pr["number"]

    mine = []
    for c in all_commits:
        co_authors = [e.lower() for _, e in CO_AUTHOR.findall(c["body"])]
        if c["author_email"] in identities:
            role = "author"
        elif identities.intersection(co_authors):
            role = "co_author"
        else:
            continue
        branches = sorted(set(membership.get(c["sha"], [])))
        if c["sha"] in in_pr:
            delivery = "pr"
        elif c["sha"] in merged_by_pr:
            delivery = "pr_merge_commit"
        elif default_branch in branches:
            delivery = "direct_push"
        else:
            delivery = "branch_only"
        record = {
            "repository": args.repo, "sha": c["sha"], "url": f"{meta['url']}/commit/{c['sha']}",
            "authored_at": c["authored_at"], "committed_at": c["committed_at"], "title": c["title"],
            "body": c["body"], "role": role, "author_email": c["author_email"],
            "committer_email": c["committer_email"], "is_merge": len(c["parents"]) > 1,
            "branches": branches, "on_default_branch": default_branch in branches,
            "delivery": delivery, "prs": sorted(set(in_pr.get(c["sha"], []))) or
                ([merged_by_pr[c["sha"]]] if c["sha"] in merged_by_pr else []),
        }
        if args.numstat:
            record.update(numstat(repo_dir, c["sha"]))
        mine.append(record)
    mine.sort(key=lambda r: r["authored_at"])

    my_prs = [p for p in prs if (p["author"] or "").lower() == args.login.lower()]
    mine_shas = {c["sha"] for c in mine}
    related_prs = [p for p in prs if p in my_prs or mine_shas.intersection(p["commit_shas"])]

    (out / "commits.json").write_text(json.dumps(mine, ensure_ascii=False, indent=1))
    (out / "prs.json").write_text(json.dumps(related_prs, ensure_ascii=False, indent=1))
    with (out / "commits.csv").open("w", newline="") as f:
        cols = ["authored_at", "sha", "delivery", "prs", "role", "is_merge", "title"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in mine:
            w.writerow({k: (",".join(map(str, r[k])) if k == "prs" else r[k]) for k in cols})

    delivery_counts = Counter(r["delivery"] for r in mine)
    collection = {
        "repository": args.repo, "private": meta["isPrivate"], "default_branch": default_branch,
        "collected_at": dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds"),
        "login": args.login, "identities": identity_table,
        "totals": {
            "all_commits_all_branches": len(all_commits), "my_commits": len(mine),
            "my_commits_by_delivery": dict(delivery_counts),
            "my_co_authored": sum(r["role"] == "co_author" for r in mine),
            "branches": len({b for bs in membership.values() for b in bs}),
            "prs_total": len(prs), "prs_authored_by_me": len(my_prs), "prs_related": len(related_prs),
        },
        "period": {"first": mine[0]["authored_at"] if mine else None, "last": mine[-1]["authored_at"] if mine else None},
        "limits": {
            "pr_commit_list_truncated": truncated,
            "deleted_or_force_pushed_history": "확인 불가",
            "unlinked_emails": "identities에서 counted_as_mine=false인 이메일 중 본인 것이 있는지 사용자 확인 필요",
        },
        "tools": {"git": run(["git", "--version"]).strip(), "gh": run(["gh", "--version"]).splitlines()[0]},
    }
    (out / "collection.json").write_text(json.dumps(collection, ensure_ascii=False, indent=1))
    print(json.dumps({"out": str(out), **collection["totals"], "period": collection["period"],
                      "pr_commit_list_truncated": truncated, "clone": str(repo_dir)}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
