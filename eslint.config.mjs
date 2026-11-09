import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";
import prettier from "eslint-config-prettier/flat";

// docs/frontend-conventions.md의 규칙 중 기계적으로 검사할 수 있는 것을 여기서 강제한다.

const PALETTE =
  "slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose|black|white";
const COLOR_UTILS =
  "bg|text|border|ring|outline|fill|stroke|from|via|to|shadow|divide|decoration|accent|caret|placeholder";

const classNameRules = [
  {
    // bg-blue-500, text-white 같은 기본 팔레트 대신 의미 기반 토큰을 쓴다.
    selector: `Literal[value=/(^|[\\s:])(${COLOR_UTILS})-(${PALETTE})(-\\d{2,3})?(?![\\w-])/]`,
    message:
      "기본 팔레트 색상 대신 의미 기반 토큰(bg-primary, text-muted-foreground 등)을 사용하세요.",
  },
  {
    // p-[13px], text-[#333] 같은 임의값 대신 @theme 토큰을 등록한다.
    selector: "Literal[value=/(^|[\\s:])[a-z-]+-\\[[^\\]]+\\](?=$|\\s)/]",
    message: "임의값 대신 globals.css의 @theme에 토큰을 등록해 사용하세요.",
  },
  {
    selector: "Literal[value=/(^|[\\s:])space-[xy]-/]",
    message: "space-x/y 대신 flex·grid와 gap-*을 사용하세요.",
  },
];

// import 방향: app → features → components → lib. 역방향과 기능 간 import를 막는다.
const layerImports = (patterns) => ({
  "no-restricted-imports": ["error", { patterns }],
});
const PRIMITIVES = {
  group: ["@base-ui/react", "@base-ui/react/*", "@radix-ui/*"],
  message: "프리미티브는 components/ui/의 shadcn 컴포넌트를 거쳐 사용하세요.",
};

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,
  prettier,
  {
    files: ["src/**/*.{ts,tsx}"],
    ignores: ["src/components/ui/**"],
    rules: {
      "no-restricted-syntax": ["error", ...classNameRules],
      // UI 문구는 messages/에 두고 next-intl로 불러온다.
      "react/jsx-no-literals": [
        "error",
        { noStrings: false, ignoreProps: true },
      ],
    },
  },
  {
    files: ["src/app/**/*.{ts,tsx}"],
    rules: layerImports([PRIMITIVES]),
  },
  {
    files: ["src/features/**/*.{ts,tsx}"],
    rules: layerImports([
      PRIMITIVES,
      { group: ["@/app/*"], message: "features는 app을 import하지 않습니다." },
      {
        group: ["@/features/*", "../*"],
        message:
          "기능끼리 import하지 않습니다. 공유가 필요하면 components/나 lib/로 옮기세요. 같은 기능 안에서는 ./ 경로를 씁니다.",
      },
    ]),
  },
  {
    files: ["src/components/**/*.{ts,tsx}"],
    ignores: ["src/components/ui/**"],
    rules: layerImports([
      PRIMITIVES,
      {
        group: ["@/app/*", "@/features/*"],
        message: "components는 app·features를 import하지 않습니다.",
      },
    ]),
  },
  {
    files: ["src/components/ui/**/*.{ts,tsx}"],
    rules: layerImports([
      {
        group: ["@/app/*", "@/features/*"],
        message: "components는 app·features를 import하지 않습니다.",
      },
    ]),
  },
  {
    files: ["src/lib/**/*.{ts,tsx}"],
    rules: layerImports([
      {
        group: ["@/app/*", "@/features/*", "@/components/*"],
        message: "lib는 다른 계층을 import하지 않습니다.",
      },
    ]),
  },
  globalIgnores([
    ".next/**",
    "out/**",
    "build/**",
    "next-env.d.ts",
    // 개인 기록·조사 자료 (Git 제외)
    "archive/**",
  ]),
]);

export default eslintConfig;
