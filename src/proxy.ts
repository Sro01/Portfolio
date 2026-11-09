import createMiddleware from "next-intl/middleware";
import { routing } from "./i18n/routing";

export default createMiddleware(routing);

export const config = {
  // API, Next 내부 경로, 확장자가 있는 정적 파일은 제외한다.
  matcher: "/((?!api|trpc|_next|_vercel|.*\\..*).*)",
};
