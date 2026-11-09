import type messages from "../../messages/ko.json";
import type { routing } from "./routing";

// ko.json을 기준으로 메시지 키와 언어 코드를 타입 검사한다.
declare module "next-intl" {
  interface AppConfig {
    Locale: (typeof routing.locales)[number];
    Messages: typeof messages;
  }
}
