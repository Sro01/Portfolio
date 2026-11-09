import type { NextConfig } from "next";
import createMDX from "@next/mdx";
import createNextIntlPlugin from "next-intl/plugin";

const withNextIntl = createNextIntlPlugin("./src/i18n/request.ts");
// MDX는 페이지가 아니라 content/의 사례 본문으로만 쓰므로 pageExtensions는 바꾸지 않는다.
const withMDX = createMDX();

const nextConfig: NextConfig = {
  // AGENTS.md는 CLAUDE.md 안내만 유지한다. Next.js 문서 안내는 docs/frontend-conventions.md에 둔다.
  agentRules: false,
  cacheComponents: true,
  partialPrefetching: true,
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
};

export default withNextIntl(withMDX(nextConfig));
