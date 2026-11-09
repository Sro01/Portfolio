---
version: alpha
name: Sage Green
description: A quiet sage shadcn/ui theme — low-chroma green, near-white stage, and a large radius by tweakcn.
colors:
  background: "#fdfdfd"
  foreground: "#000000"
  card: "#fdfdfd"
  primary: "#afbea5"
  primary-foreground: "#000000"
  secondary: "#edf0f4"
  secondary-foreground: "#080808"
  muted: "#f5f5f5"
  muted-foreground: "#878787"
  accent: "#495940"
  accent-foreground: "#ffffff"
  destructive: "#b3191f"
  border: "#e7e7ee"
  input: "#ebebeb"
  ring: "#afbea5"
  sidebar: "#f5f8fb"
  sidebar-foreground: "#000000"
  sidebar-primary: "#000000"
  sidebar-accent: "#e4eae1"
  chart-1: "#4ac885"
  chart-2: "#7033ff"
  chart-3: "#fd822b"
  chart-4: "#3276e4"
  chart-5: "#747474"
  dark-background: "#070503"
  dark-foreground: "#f9f8f7"
  dark-card: "#100d08"
  dark-primary: "#afbea5"
  dark-secondary: "#26211a"
  dark-muted: "#1e1a14"
  dark-muted-foreground: "#928f8a"
  dark-accent: "#495940"
  dark-border: "#2f281b"
  dark-sidebar: "#040302"
  dark-destructive: "#b3191f"
typography:
  display:
    fontFamily: Plus Jakarta Sans
    fontSize: 48px
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 36px
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: 600
    lineHeight: 1.25
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.65
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.65
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1.4
  sans-ui:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
  mono:
    fontFamily: IBM Plex Mono
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.5
rounded:
  xs: 16px
  sm: 18px
  md: 20px
  lg: 22px
  xl: 26px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  "2xl": 48px
  section: 64px
  gutter: 32px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.primary-foreground}"
    rounded: "{rounded.md}"
    padding: 12px
  button-secondary:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.secondary-foreground}"
    rounded: "{rounded.md}"
    padding: 12px
  button-outline:
    backgroundColor: transparent
    textColor: "{colors.foreground}"
    rounded: "{rounded.md}"
    padding: 12px
  card:
    backgroundColor: "{colors.card}"
    textColor: "{colors.foreground}"
    rounded: "{rounded.lg}"
    padding: 24px
  input:
    backgroundColor: "{colors.background}"
    textColor: "{colors.foreground}"
    rounded: "{rounded.md}"
    padding: 12px
  sidebar:
    backgroundColor: "{colors.sidebar}"
    textColor: "{colors.sidebar-foreground}"
---

# Sage Green

A premade shadcn/ui theme by [tweakcn](https://tweakcn.com). Install tokens with `npx shadcn@latest add @shadcnblocks/theme/sage-green`, then keep this DESIGN.md in the project root (or `.agents/`) so coding agents stay on-brand.

## Overview

Sage Green keeps chroma low. The primary (`#afbea5`) is a dusty sage, the accent (`#495940`) is a deeper herb green, and the stage is almost white (`#fdfdfd`). Corners are large, so the UI feels soft.

The system is **calm, wellness-adjacent, and editorial**. It suits quiet products, journals, and shells that should feel settled rather than energetic.

Typography uses **Plus Jakarta Sans** for display, UI chrome and reading text, with **Pretendard** for Korean (Pretendard JP for Japanese). **IBM Plex Mono** covers code. The theme's Lora serif is not loaded.

Emotional targets: soft, grown, unhurried — never electric lime, never clinical zinc.

## Colors

- **Primary (`#afbea5`):** Dusty sage — primary buttons with black text (`#000000`). It is a tint, not a neon. In dark mode the primary is `#afbea5`.
- **Accent (`#495940`):** Deeper herb green (`#495940`) with white text for the stronger emphasis when sage is too quiet.
- **Secondary (`#edf0f4`):** Supporting actions and quiet structure. Text `#080808`.
- **Foreground (`#000000`):** Body text. Do not swap it for a random gray.
- **Background (`#fdfdfd`):** Page stage.
- **Card (`#fdfdfd`):** Content surfaces.
- **Muted (`#f5f5f5`):** Quiet chrome. Muted text is `#878787`.
- **Border (`#e7e7ee`):** Structural lines. Prefer these over heavy shadows.
- **Destructive (`#b3191f` / dark `#b3191f`):** Errors only. Keep them distinct from the brand color.
- **Ring (`#afbea5`):** Focus ring.

Dark mode stage is `#070503`, cards `#100d08`, foreground `#f9f8f7`.

## Typography

**Plus Jakarta Sans** leads display, UI and reading text; Korean falls back to **Pretendard** (Japanese to Pretendard JP) through `--font-cjk`. **IBM Plex Mono** is for code.

- **Display / headlines:** Plus Jakarta Sans SemiBold, tight tracking.
- **Body / reading:** Plus Jakarta Sans + Pretendard Regular at 15–18px, line-height about 1.6.
- **UI chrome / labels:** Plus Jakarta Sans Medium or Regular. Sentence case.
- **Mono:** IBM Plex Mono for code, tokens, and IDs.

This site is mostly Korean, so a Latin serif body (Lora) would only touch English words and numbers inside Korean sentences. Keep body text in the sans stack; dates and numbers also use Plus Jakarta Sans with tabular figures, not the mono face.

## Layout

Use a **soft editorial shell**: lots of near-white, sage as a wash or a single button, herb green for links that must be found.

- Base spacing is an 8px scale. Section rhythm is about 64px.
- Prefer a readable prose column (~65–75ch) and a wider shell (~1200px) for app chrome.
- One primary action per view.

## Elevation & Depth

Depth is **gentle**. Large radius plus a light border. Dark mode goes nearly black-brown (`#070503`) and keeps the same sage.

- Prefer semantic surfaces: background, then card, then the primary action.
- Dark mode elevates with the dark card color, not bright white borders.

## Shapes

Radius is **large** — base `--radius` is `1.4rem` (22px). This is a soft theme; do not square it off.

- Controls: about 20px.
- Cards: about 22px.
- Full pills only for chips and avatars.

## Components

Built for the shadcn/ui token contract. Prefer semantic tokens (`bg-primary`, `text-muted-foreground`) over raw hex in component code.

- **Primary button:** `#afbea5` fill, `#000000` label.
- **Secondary button:** `#edf0f4` fill, `#080808` label.
- **Cards:** `#fdfdfd` surface, `#e7e7ee` border, padding about 24px.
- **Inputs:** stage or card fill, border `#e7e7ee`, focus ring `#afbea5`.
- **Sidebar:** `#f5f8fb` with `#000000` labels. Do not paint the whole nav in primary.
- **Charts:** `#4ac885`, `#7033ff`, `#fd822b`, `#3276e4`, `#747474` in that order.

## Do's and Don'ts

**Do**

- Do keep chroma low. If a color shouts, it is wrong.
- Do keep display, UI and body on Plus Jakarta Sans with Pretendard for Korean.
- Do use the herb accent sparingly.
- Do support light and dark with the same color story.
- Do use shadcn semantic tokens instead of one-off hex in components.

**Don't**

- Don't replace sage with lime or emerald.
- Don't shrink the radius to 4px.
- Don't switch body text to Lora or another serif; don't use the mono face for dates or labels.
- Don't invent extra brand colors when a token already exists.
