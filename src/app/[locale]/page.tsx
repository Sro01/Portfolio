import type { Locale } from "next-intl";
import { setRequestLocale } from "next-intl/server";

export default async function HomePage({ params }: PageProps<"/[locale]">) {
  const { locale } = await params;
  // 지원 언어 검증은 [locale]/layout.tsx에서 한다.
  setRequestLocale(locale as Locale);
  return <main />;
}
