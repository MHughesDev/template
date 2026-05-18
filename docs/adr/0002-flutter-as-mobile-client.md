---
doc_id: "7.4"
title: "ADR-0002 flutter as mobile client"
section: "ADR"
status: "current"
updated: "2026-05-17"
---

# 7.4 — ADR-0002: Flutter as the mobile client; no Flutter for web

**Status:** Accepted

**Date:** 2026-05-17

## Context

The template ships a working full-stack baseline of **FastAPI** (`apps/api/`) and **React 19** (`apps/web/`). Products initialized from this template will increasingly need a mobile presence on **iOS phones and tablets** and **Android phones and tablets**.

Three architectural questions had to be answered before any product enables a mobile profile, so that every initialized product converges on the same answer rather than re-litigating it per project:

1. **What technology drives mobile?** Native (Swift + Kotlin) duplicates effort across iOS and Android. React Native shares language with `apps/web/` but its UI fidelity, animation performance, and platform-API surface lag Flutter in 2026. Flutter ships a single Dart codebase to both stores with Impeller as default renderer and an official MVVM architecture (released January 2026 by the Flutter team).
2. **What relationship does mobile have to the backend?** The mobile app must not own business logic, must not duplicate auth rules, and must not bypass the API contract that web already consumes.
3. **Should the web frontend also be replaced by Flutter Web** to achieve a literal "one codebase, every surface" outcome?

This decision freezes those answers so future contributors and AI agents stop reopening them.

## Decision

### 1. Mobile (iOS phones, iPads, Android phones, Android tablets) uses Flutter

A new optional client profile, `apps/mobile/`, is the only sanctioned location for mobile code. It is built with:

- **Flutter (stable channel) + Dart 3.x**
- **Material 3** as the base design system, with **Cupertino** widgets applied selectively for navigation transitions, pickers, action sheets, switches, and pull-to-refresh (full enumeration in `docs/architecture/mobile.md`)
- **Riverpod** (with `@riverpod` code generation) for state management
- **Feature-first organization + official MVVM layering** — `presentation/`, `application/`, `domain/`, `data/` — with dependency direction inward only
- **`go_router`** for navigation, **Dio** for HTTP, **`drift`** for typed SQLite caching, **`flutter_secure_storage`** for tokens

### 2. Mobile is a thin client to the FastAPI backend

The mobile app holds **zero business logic**. It is, by contract, a presentation and interaction layer over the same FastAPI service that `apps/web/` consumes:

- The FastAPI backend remains the single source of truth for data, validation, authorization, and integration rules.
- The same OpenAPI 3.1 schema produced by FastAPI is consumed by **both** clients. React uses `openapi-ts`; Flutter uses **`degenerate`** (chosen over `swagger_to_dart` and `florval` after evaluation — see Alternatives).
- Auth uses the same JWT access + refresh token scheme. Only the storage primitive differs: `httpOnly` cookies / `localStorage` fallback on web, Keychain (iOS) / encrypted SharedPreferences + Keystore (Android) on mobile via `flutter_secure_storage`.
- Error code taxonomy and API versioning policy are shared. Mobile cannot ship a feature that depends on an endpoint behavior that web has not also seen.

### 3. Web stays on React. Flutter Web is **not** adopted

`apps/web/` (React 19 + Vite + TanStack + Tailwind v4 + shadcn/ui) remains the only supported browser/desktop-browser experience. Flutter Web is explicitly rejected for the template default because:

- SEO and accessibility on Flutter Web (CanvasKit) materially trail DOM-based React.
- Initial bundle size and time-to-interactive on Flutter Web are unacceptable for a general-purpose web product.
- The existing React baseline is production-tested and integrates with the rest of the repo's conventions (Biome, Playwright, generated client, Vite).
- The marginal code-sharing benefit between Flutter mobile and Flutter web does not offset the worse web experience.

Desktop applications (macOS, Windows) are **out of scope** for this ADR. If a product later needs a true native desktop shell, the default path is React inside Tauri or Electron, re-using `apps/web/`. Flutter Desktop targets remain unsupported by the template until a separate ADR enables them.

### 4. Mobile lives behind an optional profile, like web

`apps/mobile/` is enabled per-product when `idea.md` includes mobile in the scope. The presence of the directory does not force every initialized product to ship mobile builds, just as the presence of `apps/web/` does not force every product to ship a web client.

### 5. Locked technical decisions

To prevent decision drift across products and across agent sessions, the following are **locked at the template level** (changing any of them requires a new ADR):

| Concern | Locked choice |
|---|---|
| Architecture pattern | Feature-first + official Flutter MVVM (presentation / application / domain / data) |
| State management | Riverpod with `@riverpod` codegen |
| Navigation | `go_router` |
| HTTP client | Dio with `QueuedInterceptor` for token refresh |
| OpenAPI client generator | `degenerate` |
| Local DB | `drift` (typed SQLite) |
| Secure storage | `flutter_secure_storage` |
| Renderer | Impeller (default; do not disable) |
| Lint set | `very_good_analysis` |
| DI | Riverpod first; `get_it` only for non-reactive sync services |
| i18n | `flutter_localizations` + ARB from day one |
| Testing | Pyramid: unit ≥70% / widget ~20% / integration ~10%; goldens for design-system components only |
| Build flavors | `dev`, `staging`, `prod` via `--dart-define-from-file` |
| Forbidden | `GetX`, raw `SharedPreferences` for tokens, hand-written API models, hand-edits to `lib/generated/`, business logic in widgets |

## Consequences

**Easier**

- One mobile codebase deploys to iOS and Android without duplicating screens, navigation, or models.
- The same backend serves web and mobile — no parallel API, no shadow business rules, no auth divergence.
- AI agents operating in `apps/mobile/` have a fully-enumerated set of locked decisions to follow; they cannot silently introduce GetX, plain HTTP, or hand-rolled API models.
- Cross-platform UI coherence between iOS and Android is achievable because Material 3 anchors the design system while Cupertino widgets handle only the moments where platform expectations would otherwise feel wrong.

**Harder**

- The template now maintains a third runtime (Dart toolchain, Xcode for iOS builds, Android SDK for Android builds) in addition to Python and Node. CI macOS runner minutes become a real cost when mobile is enabled.
- Apple Developer Program enrollment and store review timelines are pre-requisites that no amount of code can shorten.
- Generated Dart client must stay in sync with the FastAPI schema; a backend breaking change now fans out to two consumers instead of one.
- Designers must understand the Material-3-with-Cupertino-accents model rather than designing two parallel mocks.

**Risks accepted**

- Some platform-specific edge cases (e.g. iOS-only widgets like `CupertinoContextMenu`) require per-platform code in `core/adaptive/`. This is tolerated; the alternative — fighting the platform — produces worse UX.
- Flutter's upgrade cadence (Dart language, Flutter SDK, dependency churn) requires periodic maintenance work. The template will track stable channel; products on long-LTS schedules can pin via ADR.
- `degenerate` is a younger package than `openapi-generator`. The team has accepted the trade-off for FastAPI/OpenAPI 3.1 ergonomics; rotation to a different generator requires a new ADR.

**Follow-up work**

- Per-product ADRs inside initialized products will record product-specific mobile decisions (analytics vendor, crash reporter, push notification provider, biometric unlock policy).
- A future ADR may revisit Flutter Web if web bundle performance and SEO close the gap meaningfully, or if a specific product type (e.g. internal admin tools, app-like SaaS dashboards) is added to the template.
- A future ADR may add Flutter Desktop targets if a product genuinely requires a native desktop shell beyond what React + Tauri/Electron provides.

## Alternatives considered

| Alternative | Rejected because |
|---|---|
| **React Native** for mobile to share TypeScript with `apps/web/` | UI fidelity, animation performance, and platform-API parity lag Flutter in 2026. The promised "share JS with web" benefit erodes once you account for navigation libraries, state libraries, native modules, and platform-specific UI code that diverge anyway. |
| **Native Swift + Native Kotlin** (separate codebases) | Doubles engineering surface, doubles AI-agent context, doubles release pipelines, and produces drift between platforms within months. Acceptable only for products with extreme platform-specific requirements — not for the template default. |
| **Flutter for web as well** (single Flutter codebase across mobile + web) | Flutter Web's CanvasKit payload, SEO weakness, and desktop-browser UX patterns make it a worse default than React for general-purpose web. The remaining UI-sharing benefit with mobile is small once adaptive web widgets are factored in. |
| **`swagger_to_dart`** as the Dart OpenAPI generator | Strong FastAPI awareness with Freezed + Retrofit output, but `degenerate` offers broader OpenAPI 3.1 spec compatibility and pluggable HTTP clients, which better fits a template that future products will customize. Re-evaluate if `degenerate` quality regresses. |
| **`florval`** as the Dart OpenAPI generator | Tight Riverpod integration is attractive but couples generated code to a specific state-management library; `degenerate` keeps generated code library-agnostic so Riverpod providers can live in `application/` rather than `generated/`. |
| **BLoC** instead of Riverpod for state management | Excellent for >20-engineer enterprise apps with audit/replay requirements, but boilerplate cost is too high for the template's default scale. Riverpod with codegen wins on ergonomics for the typical initialized product. |
| **Clean Architecture** as the layering pattern | Strong dependency boundaries but over-engineered for typical product scope. Feature-first + MVVM (the Flutter team's official 2026 recommendation) reaches the same goals with less ceremony. |
| **`Provider`** (legacy) for state management | Predates Riverpod; same author has since deprecated it for new projects in favor of Riverpod's compile-time safety. |
| **`SharedPreferences`** for token storage | Unencrypted on both platforms. Non-negotiable security failure for auth tokens. |

## References

- Architecture document: [`docs/architecture/mobile.md`](../architecture/mobile.md)
- Optional client profile: [`docs/optional-clients/mobile.md`](../optional-clients/mobile.md)
- Mobile agent scope: [`apps/mobile/AGENTS.md`](../../apps/mobile/AGENTS.md)
- Sibling web client scope: [`apps/web/AGENTS.md`](../../apps/web/AGENTS.md)
- Founding architecture ADR: [`docs/adr/0001-initial-template-architecture.md`](0001-initial-template-architecture.md)
- ADR template: [`docs/adr/template.md`](template.md)
- External: Flutter team's official MVVM architecture guide (January 2026)
- External: `degenerate` Dart package — pub.dev/packages/degenerate
