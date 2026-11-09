import { createNavigation } from "next-intl/navigation";
import { routing } from "./routing";

// 언어 접두사를 유지하는 Link·redirect·router. next/link 대신 이것을 쓴다.
export const { Link, redirect, usePathname, useRouter, getPathname } =
  createNavigation(routing);
