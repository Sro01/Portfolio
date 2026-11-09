import { describe, expect, it } from "vitest";
import de from "../../messages/de.json";
import en from "../../messages/en.json";
import ja from "../../messages/ja.json";
import ko from "../../messages/ko.json";

// 모든 언어가 기준 언어(ko)와 같은 메시지 키를 갖는지 확인한다.
function keys(value: unknown, prefix = ""): string[] {
  if (typeof value !== "object" || value === null) return [prefix];
  return Object.entries(value).flatMap(([key, child]) =>
    keys(child, prefix ? `${prefix}.${key}` : key),
  );
}

describe("messages", () => {
  const base = keys(ko).sort();

  it.each(Object.entries({ en, ja, de }))(
    "%s has the same keys as ko",
    (_, messages) => {
      expect(keys(messages).sort()).toEqual(base);
    },
  );
});
