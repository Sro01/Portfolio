import type { MDXComponents } from "mdx/types";

// App Router에서 @next/mdx를 쓰려면 이 파일이 필요하다.
// 사례 본문(content/projects/<slug>/<언어>.mdx) 전체에 적용할 요소 스타일·컴포넌트를 여기에 둔다.
const components: MDXComponents = {};

export function useMDXComponents(): MDXComponents {
  return components;
}
