# apps/mobile/AGENTS.md

<!-- Per spec §26.8 item 235 — optional mobile profile -->

**Purpose:** Scoped agent instructions for mobile development (Expo/React Native). Active only when the mobile profile is enabled. Supplements root AGENTS.md — root remains supreme for all repo-wide policy.

## Scope

This file governs everything under `apps/mobile/`. When the mobile profile is disabled, `apps/mobile/` contains only this file and a `README.md` placeholder. Do not scaffold screens or navigation until `scripts/profiles/enable-mobile.sh` has run.

## Framework conventions

This project uses **Expo (SDK 51+)** with React Native and TypeScript. The router is **Expo Router** (file-based, analogous to Next.js App Router).

### Directory structure

```
apps/mobile/
├── app/                  # Expo Router — file-based routes
│   ├── (auth)/           # Auth-gated stack (requires token)
│   ├── (public)/         # Public screens (login, register, onboarding)
│   ├── _layout.tsx       # Root layout (Stack + AuthProvider)
│   └── +not-found.tsx    # 404 handler
├── components/           # Shared components
│   ├── ui/               # Primitive components (Button, TextInput, Modal)
│   └── <domain>/         # Domain-specific components (InvoiceRow, OrderCard)
├── lib/                  # Non-component utilities
│   ├── api/              # Generated API client (from OpenAPI spec)
│   ├── auth/             # Token storage (SecureStore — see Auth patterns)
│   └── hooks/            # Custom hooks
├── assets/               # Images, fonts, icons
└── __tests__/            # Jest unit and component tests
```

### Component conventions

- TypeScript with explicit prop types everywhere — no implicit `any`.
- Use React Native core components (`View`, `Text`, `Pressable`, `FlatList`) not web tags.
- Styling: **NativeWind** (Tailwind for React Native) — use `className` utility classes.
- Avoid inline styles unless animating with `Animated` or `react-native-reanimated`.
- Use `Pressable` instead of `TouchableOpacity` — better cross-platform behaviour.

### File naming

| Type | Convention | Example |
|------|-----------|---------|
| Screens | `index.tsx` or `[id].tsx` inside route folder | `app/(auth)/invoices/[id].tsx` |
| Layouts | `_layout.tsx` inside route folder | `app/(auth)/_layout.tsx` |
| Hooks | `use*.ts` | `useInvoices.ts` |
| Utilities | `*.ts` | `formatCurrency.ts` |

## Auth storage patterns

**Critical security rule:** Never store tokens in `AsyncStorage` — it is unencrypted and readable by any app on a jailbroken device.

Always use **Expo SecureStore**:

```typescript
// lib/auth/token-store.ts
import * as SecureStore from "expo-secure-store";

const ACCESS_TOKEN_KEY = "access_token";
const REFRESH_TOKEN_KEY = "refresh_token";

export async function saveTokens(access: string, refresh: string) {
  await SecureStore.setItemAsync(ACCESS_TOKEN_KEY, access);
  await SecureStore.setItemAsync(REFRESH_TOKEN_KEY, refresh);
}

export async function getAccessToken(): Promise<string | null> {
  return SecureStore.getItemAsync(ACCESS_TOKEN_KEY);
}

export async function clearTokens() {
  await SecureStore.deleteItemAsync(ACCESS_TOKEN_KEY);
  await SecureStore.deleteItemAsync(REFRESH_TOKEN_KEY);
}
```

### Token refresh

On 401 response: attempt silent refresh using the refresh token → if refresh fails, call `clearTokens()` and redirect to the login screen. Never expose the refresh token to third-party SDKs.

## API integration patterns

### Generated client

Use the same generated client as the web app — generated from the FastAPI OpenAPI spec:

```bash
make codegen:mobile-client   # regenerates apps/mobile/lib/api/ from /api/v1/openapi.json
```

Configure the base URL via `expo-constants` and `app.config.ts` extra:

```typescript
// lib/api/client.ts
import Constants from "expo-constants";

const BASE_URL = Constants.expoConfig?.extra?.apiUrl ?? "http://localhost:8000";
```

### Network error handling

- HTTP 401 → silent token refresh → retry → navigate to login if still 401.
- HTTP 403 → show "Access denied" Alert; stay on screen.
- HTTP 422 → map `detail[].loc` to field-level validation errors in forms.
- Network timeout / unreachable → show offline banner; retry with exponential backoff.

### Offline support

If offline support is required (check `idea.md §5` for the offline profile): use **React Query** with `cacheTime: Infinity` + `staleTime: 5 * 60 * 1000` and **MMKV** for the persisted cache. Do not implement custom cache logic.

## Testing

### Unit and component tests (Jest + React Native Testing Library)

```bash
npx jest                # all tests
npx jest --watch        # watch mode
npx jest --coverage     # with coverage report
```

Test location: `apps/mobile/__tests__/`

- Test hooks and utilities in isolation — mock `expo-secure-store` and API calls with `jest.mock`.
- Component tests: use `render()` from `@testing-library/react-native`. Assert on `getByText`, `getByRole` — not on component internals.

### Device testing

Before merging any change that touches navigation or UI:
1. Run on iOS Simulator: `npx expo run:ios`
2. Run on Android Emulator: `npx expo run:android`

CI runs Jest only. Device testing is manual pre-merge.

### API contract tests

Use the shared OpenAPI spec to validate that the mobile client's request/response shapes match the API. See `skills/testing/api-contract-testing.md` for the contract testing pattern.

## Build and deploy

### EAS Build

Managed builds via **EAS Build** (Expo Application Services):

```bash
eas build --platform ios --profile preview    # ad-hoc / TestFlight
eas build --platform android --profile preview # internal testing
eas build --platform all --profile production  # app store submission
```

EAS profiles are configured in `apps/mobile/eas.json`. Secrets (API keys, signing certificates) are stored in the EAS project — never commit them.

### Environment configuration

Use `app.config.ts` with `extra` for build-time config:

```typescript
// apps/mobile/app.config.ts
export default {
  extra: {
    apiUrl: process.env.API_URL ?? "https://api.example.com",
    appEnv: process.env.APP_ENV ?? "development",
  },
};
```

| Variable | Description |
|----------|-------------|
| `API_URL` | Base URL of FastAPI backend |
| `APP_ENV` | `development`, `staging`, or `production` |

### OTA updates (Expo Updates)

Over-the-air updates are configured in `app.config.ts → updates`. OTA updates can only change JavaScript — native code changes require a full EAS build. Use `eas update --branch production` to push a JS-only fix.

## Target platforms

Confirm targets in `idea.md §5`. Default: iOS 16+ and Android API 31+. Update `app.config.ts → ios.minimumOsVersion` and `android.minSdkVersion` to match.

## Security

- SecureStore for all tokens and secrets (see Auth patterns above).
- Certificate pinning: if the API is high-sensitivity, add `react-native-ssl-pinning` — document the cert rotation procedure in `docs/security/`.
- Deep link validation: validate all incoming deep link URLs before navigating.
- Jailbreak/root detection: optional — add `expo-device` checks for high-security deployments.
- Never log tokens, passwords, or PII to the console in production (`__DEV__` guard all debug logs).
- See `docs/security/threat-model-stub.md` for the full mobile attack surface.
