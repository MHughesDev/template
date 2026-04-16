# apps/web/AGENTS.md

<!-- Per spec §26.8 item 233 — optional web profile -->

**Purpose:** Scoped agent instructions for web frontend development. Active only when the web profile is enabled. Supplements root AGENTS.md — root remains supreme for all repo-wide policy.

## Scope

This file governs everything under `apps/web/`. When the web profile is disabled, `apps/web/` contains only this file and a `README.md` placeholder — do not scaffold components or pages until `scripts/profiles/enable-web.sh` has run.

## Framework conventions

This project uses **Next.js (App Router)** with TypeScript. After initialization, confirm the framework in `idea.md §3` and update this section if a different framework was selected (e.g. Vite+React).

### Directory structure

```
apps/web/
├── app/                  # Next.js App Router — layouts, pages, loading states
│   ├── (auth)/           # Auth-gated route group
│   ├── (public)/         # Public route group
│   └── layout.tsx        # Root layout (fonts, providers)
├── components/           # Shared UI components (never import from app/ directly)
│   ├── ui/               # Primitive components (button, input, modal)
│   └── <domain>/         # Domain-specific components (InvoiceCard, TenantSelector)
├── lib/                  # Non-component utilities
│   ├── api/              # Generated API client (from OpenAPI spec)
│   ├── auth/             # Auth token handling (see Auth patterns below)
│   └── hooks/            # Custom React hooks
├── public/               # Static assets
└── tests/                # Vitest unit tests; Playwright e2e tests
```

### Component conventions

- Use **React Server Components** (RSC) by default. Add `"use client"` only when you need browser APIs, event handlers, or useState/useEffect.
- Keep page components thin — data fetching in RSC, logic in `lib/`, display in `components/`.
- Co-locate styles: use **Tailwind CSS** utility classes. No CSS Modules or styled-components.
- All components must be TypeScript with explicit prop types — no implicit `any`.

### File naming

| Type | Convention | Example |
|------|-----------|---------|
| Pages | `page.tsx` inside route folder | `app/(auth)/invoices/page.tsx` |
| Layouts | `layout.tsx` inside route folder | `app/(auth)/layout.tsx` |
| Client components | `*.client.tsx` suffix or `"use client"` top | `InvoiceForm.client.tsx` |
| Hooks | `use*.ts` | `useInvoices.ts` |
| Utilities | `*.ts` | `formatCurrency.ts` |

## API integration patterns

### Generated client

The API client is generated from the FastAPI OpenAPI spec. **Never hand-write fetch calls** — use the generated client.

```bash
make codegen:web-client   # regenerates apps/web/lib/api/ from /api/v1/openapi.json
```

Re-run codegen whenever `apps/api/src/*/router.py` or schemas change.

### Auth token handling

- Tokens are stored in **HttpOnly cookies** set by the API `/auth/token` endpoint.
- Never read or write tokens from `localStorage` or `sessionStorage`.
- The API client automatically includes the cookie on same-origin requests.
- For cross-origin (separate domain) deployments, use the `Authorization: Bearer` header with a token from a secure in-memory store — see `lib/auth/token-store.ts`.

### Correlation IDs

Propagate the `X-Correlation-ID` header from the API response back to subsequent requests:

```typescript
// lib/api/middleware.ts
export const correlationMiddleware: Middleware = {
  onResponse(response) {
    const id = response.headers.get("X-Correlation-ID");
    if (id) sessionStorage.setItem("correlationId", id);
  },
  onRequest(request) {
    const id = sessionStorage.getItem("correlationId");
    if (id) request.headers.set("X-Correlation-ID", id);
  },
};
```

### Error handling

- HTTP 401 → redirect to `/login`.
- HTTP 403 → show "Access denied" toast; do not redirect.
- HTTP 422 → map field errors from `detail[].loc` to form field errors.
- HTTP 5xx → show generic error message; log to console with correlation ID.

## Testing

### Unit tests (Vitest)

Test location: `apps/web/tests/unit/`

```bash
pnpm test:unit          # vitest run
pnpm test:unit:watch    # vitest watch
```

Test hooks and utility functions in isolation — mock API calls with `vi.mock`.

### Component tests (Vitest + Testing Library)

Test location: `apps/web/tests/components/`

```bash
pnpm test:components
```

Render components with `render()` from `@testing-library/react`. Assert on visible text and ARIA roles — not on class names or internal state.

### E2E tests (Playwright)

Test location: `apps/web/tests/e2e/`

```bash
pnpm test:e2e           # headed
pnpm test:e2e:ci        # headless (used in CI)
```

E2E tests should cover the happy-path user journeys: sign up, log in, core domain action (create invoice, place order, etc.), log out. Keep E2E count low — prefer unit and component tests.

## Build and deploy

### Environment variables

| Variable | Required | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | Yes | Base URL of the FastAPI backend |
| `NEXT_PUBLIC_APP_ENV` | Yes | `development`, `staging`, or `production` |
| `NEXT_PUBLIC_SENTRY_DSN` | No | Sentry DSN for error tracking |

Never prefix server-only secrets with `NEXT_PUBLIC_`. Only values safe for the browser get that prefix.

### Docker

The web profile Dockerfile is `apps/web/Dockerfile` (created by `scripts/profiles/enable-web.sh`). It uses:
- Stage 1: `node:20-alpine` — install deps + build Next.js.
- Stage 2: `node:20-alpine` — copy `.next/standalone` output only.

Build with: `docker build -t app-web apps/web/`

### CI

The web CI job (`web-test` in `.github/workflows/ci.yml`) runs:
1. `pnpm install --frozen-lockfile`
2. `pnpm lint`
3. `pnpm tsc --noEmit`
4. `pnpm test:unit`
5. `pnpm build`

E2E tests run only in the `e2e` CI job (separate, slower).

## Accessibility

- All interactive elements must have accessible names (aria-label or visible text).
- Use semantic HTML elements (`<button>`, `<nav>`, `<main>`, `<section>`).
- Keyboard navigation must work for all interactive elements.
- Color contrast ratio ≥ 4.5:1 for normal text (WCAG AA).
- Run `pnpm a11y` (axe-core) on any new page before merging.

## Security

- Never render user-supplied content with `dangerouslySetInnerHTML` without sanitisation.
- CSP headers are set in `next.config.js` → `headers()`.
- No API keys or secrets in client-side code — use server-side API routes for any secrets.
- See `docs/security/threat-model-stub.md` for the full frontend attack surface.
