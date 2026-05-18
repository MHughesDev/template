# Idea Definition — DeviceLab

> **Purpose.** `idea.md` is the single human-authored input that drives repository initialization. This is the **end-state product definition** for **DeviceLab**, a local-first, open-source BYOC cloud device-orchestration platform exposing devices to humans (web UI) and AI agents (MCP) over the user's own AWS account.
>
> This file is **not** an MVP scope; it is the **target** the agent-driven build converges on over many queue rows. Where a section calls for "MVP", read it as "v1 shippable surface that already covers all seven device families and the AI-optimized MCP." Smaller seed slices for the queue are derived by `repo_initialize`.
>
> Research and decisions feeding this document live under [`docs/research/`](docs/research/) (notes, sources, **`open_ended_question.md`** decision table, **`reference/EXTERNAL_REFERENCE.md`** upstream registry). Cite `[Snnn]` in `docs/research/SOURCES.md` when referenced in implementation specs.

---

## 1. Product identity

| Field | Your answer |
|-------|-------------|
| Product name | **DeviceLab** |
| One-sentence concept | An open-source, local-first **BYOC cloud device lab** that lets humans and AI agents provision, stream, automate, and test Linux / Android / Windows / macOS / iOS Simulator / Real iOS / Browser devices in the user's own AWS account, exposed through a local web UI at `http://localhost:3000` and an MCP gateway designed for **minimal back-and-forth** AI control. |
| Repository slug | `devicelab` (default; user-owned fork-friendly) |
| License | **MIT** (project code). Third-party adapters/AMIs follow their own licenses (see `docs/research/reference/EXTERNAL_REFERENCE.md`). |

---

## 2. Target users

- **Primary user(s):**
  - **Solo developers and small QA teams** running DeviceLab on their own machine, attaching their own AWS account, and using both the web UI **and** AI coding agents (Cursor, Claude Code, Codex, Gemini CLI, Continue, etc.) over MCP to operate cloud devices.
  - **AI coding agents themselves** as first-class operators of the MCP tool surface. The MCP design is the **primary AI UX** and is benchmarked by round-trip count, not just feature parity.
- **Secondary user(s):**
  - **Mobile / web QA engineers** who want a BYOC alternative to BrowserStack / Sauce Labs for owned-app testing in the **user's** AWS account.
  - **Security researchers** running disposable, time-limited cloud devices with proxy/log capture for owned applications.
  - **Plugin authors** extending DeviceLab via the Adapter SPI for new platforms (Tizen, KaiOS, attached USB racks, alternative clouds).
- **Non-users (must not have access):**
  - **End-user consumers** of any kind. DeviceLab has **no hosted accounts**, **no SaaS billing**, and **no DeviceLab-operated multi-tenant servers**.
  - **Anonymous public users.** All control planes bind to `localhost` by default with MCP elicitation flows for confirmations; remote access is opt-in via the user's own infrastructure.

---

## 3. Core problem

Today, AI coding agents can write code but struggle to **operate full operating systems and real devices** end-to-end. Existing options force a choice: proprietary SaaS device clouds (expensive, marked-up, opaque, not BYOC, no MCP), heavyweight self-hosted device farms (operationally hostile), or chatty "computer-use" loops that burn tokens on screenshots and primitive `click(x,y)` / `type_text` calls. Solo developers and small teams who want to (a) use **their own AWS account** for cost transparency and data control, (b) hand both humans and AI agents access to a cohesive matrix of **Linux, Android, Windows, macOS, iOS Simulator, Real iOS, and Browser** runtimes, and (c) get **structured, low-round-trip AI control** instead of screenshot-by-screenshot loops, have no good option. Without DeviceLab they cobble together emulator scripts, ad-hoc EC2 setups, and brittle Playwright/Appium shims that no AI agent can drive reliably.

---

## 4. End-state product scope (replaces "MVP scope")

The end-state shippable surface of DeviceLab is the union of the bullets below. Each is **user-visible** and **independently testable**. Queue seeding will sub-divide them; this list is the contract.

1. **Local-first install** — a developer can install DeviceLab on macOS / Windows / Linux, run it (Docker Compose default; optional Tauri shell later), and reach a local web UI at `http://localhost:3000` plus a **local MCP gateway** that AI clients can attach to via stdio or Streamable HTTP (with `MCP-Session-Id` and elicitation).
2. **BYOC AWS connection** — a user can connect their own AWS account (CLI profile / SSO / `AssumeRole`; never long-lived root keys), run an **automated preflight** (credentials, quotas, regions, IAM, capacity, optional bootstrap stack), and see clear remediation links for anything missing.
3. **Seven first-class device families, end-to-end** — for each of **Linux, Android, Windows, macOS, iOS Simulator, Real iOS (Device Farm + future plugins), and Browser/Web**, a user can pick a template, profile, and region; create a device; see lifecycle progress; stream it interactively; and operate it through a uniform MCP tool surface.
4. **AI-optimized MCP surface** — a single MCP server exposes per-device, capability-aware tools organized into ~12 groups (`inventory`, `lifecycle`, `observe`, `interact`, `forms`, `read_content`, `recipes`, `subscribe`, `files`, `network`, `identity`, `cost_safety`). The default observation pyramid is **AX tree → OCR index → structured-vision (OmniParser-class) → full VLM (BYOK, gated)**; semantic actions (`click_text`, `type_into`, `fill_form`, `wait_until`, `assert_visible`) are the default surface, with primitives available as fallback.
5. **No-back-and-forth interaction primitives** — every observation returns a `screen_version`; every action accepts `wait_for` + `expected_screen_version`; agents can `subscribe()` to push events (screen-change, dialog, URL, log pattern); `run_steps([...])` batches actions in one RPC; `paste_text` / AX `setValue` / UIA `ValuePattern` / `setText` / element-handle typing bypass keystroke simulation when fields are addressable.
6. **Recipes & session recording** — declarative YAML recipes (sandboxed Jinja) run via `run_recipe`; an existing AI session can be **recorded** into a recipe (`record_recipe`) — Playwright codegen patterns for Browser, structured-action recorders for mobile/desktop in later phases.
7. **Identity Broker** — secrets live in the OS keychain (or cryptfile fallback on headless Linux) and resolve **by reference**; AI never sees raw values; sensitive prompts use MCP **elicitation (URL mode)** per spec; OAuth/browser cookie injection supported for browser-family recipes.
8. **Streaming + input split** — interactive devices stream over **WebRTC** (Selkies-class Linux, Amazon DCV where AWS-native fits Windows/Linux GPU, scrcpy-style for Android, macOS/iOS Simulator via Mac host), with a **separate data-channel for input** so mouse/keyboard latency is independent of frame rate. AX-only "headless AI" stream profile available for token-sensitive sessions.
9. **Cost guardrails (BYOC)** — every device shows live estimated hourly cost via AWS Pricing API; per-workspace soft + hard caps; explicit confirmation gates for **EC2 Mac Dedicated Hosts** (24-hour minimum), GPU instances, Device Farm sessions, large EBS, long-running idle devices; orphaned-resource sweeper and cleanup tools.
10. **Snapshots & forks** — async `snapshot_start` + `snapshot_status`; per-family strategies (EBS, VSS on Windows, AVD snapshots, simctl checkpoints, Device Farm session recordings where applicable); `fork_device_from_snapshot` for A/B experimentation.
11. **Tests & artifacts** — uniform test runner emitting **JUnit XML** + optional **Allure** reports; artifact bundles (logs, screenshots, video, HAR, AX dumps, diagnostics manifest) downloadable per run.
12. **Evidence / replay** — every MCP call records before/after AX + thumbnail + request/response under an `evidence_id`; the UI ships a **Replay** scrubber for any AI session.
13. **Plugin SPI** — third-party adapters (new clouds, new device families, alternative streaming/automation backends) load via Python entry points (`devicelab.plugins.*`) with versioned ABI; OSS repo never bundles proprietary AMIs (e.g. Genymotion) but documents subscribe-in-your-AWS-account flows.
14. **First-run wizard** — guided flow (credentials → region → preflight → bootstrap stack → first Linux desktop → copy MCP config + Cursor deeplink) so a new user reaches a streamable device and an AI-controllable session within minutes of install.

Ordering for queue seeding (top → bottom): **1 → 2 → 14 → 3 (Linux first, Browser next) → 4/5 (MCP gateway + observation tiers) → 6/7 → 8 → 9 → 3 (Android, Windows, macOS, iOS Sim, Real iOS) → 10 → 11 → 12 → 13.**

---

## 5. Explicitly out of scope

- **No DeviceLab-hosted SaaS, accounts system, billing, or "production users" tier.** No payments, no email signup, no DeviceLab-side credential storage, no DeviceLab-operated multi-tenant servers. Auth is for connecting the *user's own AWS* — not for using DeviceLab itself.
- **No reseller relationship with AWS or any cloud.** AWS bills the user directly. DeviceLab does not mark up, meter, or aggregate spend across users.
- **No replication of Anthropic/OpenAI/Google computer-use loops as the default.** Screenshot-loop control is supported but **never default**; structured observation always wins until it can't.
- **No proprietary-software bundling.** Genymotion, NICE/Amazon DCV licensing, AWS Marketplace AMIs are integrations the user accepts in **their** account — never redistributed by DeviceLab.
- **No public-facing inbound runtime ports by default.** All device control flows through SSM tunnels / WebRTC with user-owned TURN. Anything exposing the runtime publicly is opt-in and warned about.
- **No "jailbreak the world" promises.** TLS pinning bypass on hardened apps and bypassing modern bot detection are **recipe-level**, owned-estate-only, with explicit ethical banners. Real-iOS-on-arbitrary-hardware beyond Device Farm / future physical racks is out of scope (Corellium-class virtualization is a third-party plugin path, not built-in).
- **No browser/mobile-grade end-user product polish.** Mobile companion apps, marketing site, analytics dashboards are out of scope.
- **No queue / orchestration for non-device automation.** DeviceLab is not a Temporal/Airflow replacement — recipes are device-scoped workflows, not generic workflow engines.

---

## 6. User stories

### 6.1 Solo developer / QA engineer (human in browser)

- As a developer, I want to connect my AWS account in a 60-second wizard so I can provision cloud devices without learning the AWS console first.
- As a QA engineer, I want to spin up an Android emulator and immediately stream it in my browser so I can reproduce a bug a teammate filed.
- As a developer, I want to see the **live estimated hourly cost** for every running device so I never accidentally leave a Mac Dedicated Host running for a week.
- As a developer, I want to snapshot a configured device, fork it twice, and run two paths in parallel without redoing setup.
- As a QA engineer, I want a replay scrubber of any AI session that operated my device so I can audit what happened.

### 6.2 AI coding agent (MCP client)

- As an AI agent, I want to list devices, observe their AX trees, and act on labelled elements in **one round trip per intent** so I do not burn tokens on screenshot loops.
- As an AI agent, I want to `subscribe(events=[screen_change, dialog])` and block in a single call until the event fires so I avoid polling.
- As an AI agent, I want to `type_into(field="email", text="…")` and have DeviceLab pick the right injection mechanism (AX `setValue`, UIA `ValuePattern`, `setText`, paste, keystrokes) per device family — without me knowing which one.
- As an AI agent, I want to request a password by **reference** (`secret_ref="github.password"`) and have DeviceLab inject it directly into the field, never returning the value to my context.
- As an AI agent, I want capability discovery so the tool manifest reflects what *this specific device* can do (no `tap()` offered on Linux desktops, no `right_click` on iPhones).

### 6.3 Plugin author (extends DeviceLab)

- As a plugin author, I want a stable `DeviceAdapter` protocol with `provision/boot/observe/act/snapshot/teardown` plus versioned ABI so my adapter survives DeviceLab upgrades.

### 6.4 Security-conscious user

- As a user, I want all dangerous tools (terminate device, run shell, delete volume, enable VLM, exceed cost cap) gated behind MCP elicitation with audit trails so AI agents cannot quietly do harm.
- As a user, I want a downloadable diagnostics bundle that redacts AWS account IDs and secret refs by default.

---

## 7. Core workflows

### 7.1 First-run onboarding

1. User installs DeviceLab (Docker Compose pull or `uv tool install devicelab`).
2. Opens `http://localhost:3000`; wizard launches.
3. Wizard validates AWS credentials (profile / SSO / AssumeRole), picks region.
4. Wizard runs **preflight**: IAM permissions, service quotas (Mac, GPU, Device Farm), capacity probe, AMI availability per chosen template.
5. Wizard offers to deploy a **bootstrap CloudFormation stack** (lab VPC + subnets + endpoints, IAM role, SSM, S3 artifact bucket, optional `coturn`).
6. Wizard creates first device (default: Linux Desktop), watches lifecycle to `Ready`, opens stream.
7. Wizard generates MCP config with a **Cursor install deeplink** + Claude / Codex / generic JSON snippets; user copies/pastes into their AI client; MCP server appears and lists tools.

### 7.2 Human-driven device session

1. User clicks **Create Device** → picks family / template / profile / region → review screen shows estimated cost + warnings → confirm.
2. Lifecycle progresses through canonical states (`Draft → Provisioning → Booting → Ready → Running …`) with phase substrings (`waiting_for_ssm`, `installing_runtime`) shown in UI.
3. User opens device session: WebRTC stream center, status bar top, actions right, timeline bottom.
4. User uploads an APK / IPA / build artifact, installs it, taps around, captures screenshots, downloads a recording.
5. User stops device. UI shows final cost.

### 7.3 AI-driven session (round-trip-budget contract)

1. AI client connects to MCP gateway; **capability handshake** returns per-device tool manifest (filtered by family + permissions).
2. AI calls `inventory.get_running_devices()` → picks a Browser device.
3. AI calls `observe.get_screen_index(device_id)` → returns structured AX/DOM + bbox text (no pixels).
4. AI calls `forms.fill_form({email: "…", password: secret_ref})` → DeviceLab resolves secret, injects values, presses submit; returns one envelope with `screen_version_before/after`, `observation_delta`, `evidence_id`.
5. AI calls `subscribe(events=["url_change", "dialog"], timeout=15s)` — blocks until event.
6. Total round trips: **≤ 5 to complete a real login**. This is a measurable acceptance criterion (§16).

### 7.4 Recipe authoring & replay

1. User runs a session manually or via AI.
2. User clicks **Record recipe** → DeviceLab emits YAML (selectors + actions + waits) referencing session secrets by name.
3. User edits YAML; re-runs via `recipes.run_recipe(name="login_and_smoke", inputs={...})`.
4. Subsequent runs are deterministic; recipe artifacts attach to the test run.

### 7.5 Cost guardrail / cleanup

1. Background `cost_guardrail_service` polls Pricing API + active resources every minute.
2. Devices approaching workspace soft cap trigger a UI badge + MCP notification; hard cap stops new device creation.
3. Nightly `cleanup_service` lists orphaned resources (untagged or `DeviceLab=true` with no owner record), surfaces a one-click cleanup queue.

### 7.6 Diagnostics / handoff

1. User clicks **Download diagnostics** on a failed device → tarball includes redacted logs, AX dumps, CloudFormation events, agent versions, MCP call history.
2. User shares with maintainer or attaches to a GitHub issue.

---

## 8. Data and entities

Primary domain entities (local SQLite via SQLModel; Litestream optional for S3 backup).

| Entity | Description (one sentence) | Key fields | Relationships |
|--------|---------------------------|------------|---------------|
| `Workspace` | Top-level container for one local user/project. | `id`, `name`, `default_region`, `created_at` | has many CloudAccounts, Devices, Recipes |
| `User` | Local operator profile (always single-tenant per workspace v1). | `id`, `display_name`, `email`, `last_opened_at` | belongs to Workspace |
| `CloudAccount` | A connected AWS account. | `id`, `provider`, `aws_account_id`, `default_region`, `credential_method`, `connection_status`, `permission_status`, `bootstrap_status` | belongs to Workspace; has many Devices |
| `DeviceTemplate` | Catalog entry describing how to provision a family/profile combination. | `template_id`, `platform_family`, `runtime_type`, `instance_family`, `streaming_adapter`, `automation_adapter`, `mcp_tool_groups`, `cold_start_seconds_estimate`, `min_billable_minutes`, `warm_pool_supported`, `production_ready` | referenced by Device |
| `DeviceProfile` | Tier (Cheap/Balanced/Performance/Disposable/Persistent/CI/Interactive/Headless/AIOptimized/ManualQA). | `id`, `name`, `instance_size`, `auto_stop_minutes`, `snapshot_policy`, `stream_quality`, `mcp_permission_mode` | referenced by Device |
| `Device` | A provisioned device instance in some lifecycle state. | `id`, `name`, `template_id`, `profile_id`, `cloud_account_id`, `region`, `state`, `phase`, `flags{recording,testing,snapshotting,mcp_connected,stream_active,tunnel_active,warm_claimed,cleanup_pending}`, `error_code?`, `last_heartbeat_at`, `tags` | belongs to CloudAccount; has many Sessions, Snapshots, Tests, Artifacts |
| `Tunnel` | An SSM port-forward / WebRTC signaling channel. | `id`, `device_id`, `kind`, `local_port`, `remote_port`, `state` | belongs to Device |
| `Session` | An interactive (human or AI) attachment to a device. | `id`, `device_id`, `client_type` (human/mcp), `client_id`, `started_at`, `ended_at`, `lease_kind` | belongs to Device |
| `McpClient` | Tracked MCP attachment (Cursor, Claude, …). | `id`, `name`, `transport`, `auth_token_hash`, `allowed_tool_groups`, `last_seen_at` | has many Sessions |
| `Snapshot` | Versioned device state checkpoint. | `id`, `device_id`, `kind` (ebs/avd/simctl/vss/app), `status`, `progress`, `aws_snapshot_id?`, `parent_snapshot_id?`, `created_at`, `notes` | belongs to Device |
| `Recipe` | YAML/Python automation script. | `id`, `name`, `version`, `family_compat`, `inputs_schema`, `body`, `signed_by?`, `created_at` | many-to-many with Devices via TestRun |
| `TestRun` | An execution of a recipe / test / manual session. | `id`, `device_id`, `recipe_id?`, `kind`, `status`, `started_at`, `ended_at`, `evidence_ids[]`, `report_format`, `error_summary?`, `mcp_session_id?` | belongs to Device |
| `Artifact` | An uploaded or generated file (APK/IPA/HAR/screenshot/recording/diagnostics). | `id`, `device_id?`, `test_run_id?`, `kind`, `path`, `size_bytes`, `checksum`, `created_at` | belongs to Device or TestRun |
| `Evidence` | Per-MCP-call replay record. | `id`, `session_id`, `tool_name`, `request_json`, `response_json`, `screen_version_before`, `screen_version_after`, `thumb_path`, `ax_dump_path`, `created_at` | belongs to Session |
| `SecretRef` | Reference into the OS keychain. | `id`, `name`, `backend`, `requires_elicitation`, `last_used_at` | referenced by Session, Recipe inputs |
| `CostEstimate` | Cached AWS pricing snapshot. | `id`, `service_code`, `attributes_hash`, `hourly_usd`, `fetched_at`, `expires_at` | per CloudAccount/region |
| `AuditEvent` | Immutable record of dangerous-tool calls + confirmations. | `id`, `actor` (user/mcp_client), `tool`, `device_id?`, `confirmation_id?`, `outcome`, `at` | append-only |
| `WarmPoolSlot` | Pre-booted device awaiting claim. | `id`, `template_id`, `state` (Warming/Warm/Claimed), `device_id?`, `created_at` | optional, per template |

**Cardinality & isolation notes:** Single-tenant per local workspace v1; multi-account via `AssumeRole` chains is v2. Soft-delete on `Device`, `Snapshot`, `Artifact`; hard-delete is operator-gated. All AWS resources tagged `DeviceLab=true / DeviceLabWorkspace=… / DeviceLabDevice=… / DeviceLabTemplate=… / DeviceLabVersion=…`. `Evidence` and `AuditEvent` retention configurable, default 30 days.

---

## 9. Integrations

| Service | Direction | Purpose | MVP? |
|---------|-----------|---------|------|
| **AWS EC2** | outbound | Provision Linux/Windows/Android-host/Mac instances, snapshots, EBS volumes | **yes** |
| **AWS Systems Manager (SSM)** | outbound | Session Manager tunnels, Run Command for agent install/update, State Manager for drift | **yes** |
| **AWS CloudFormation** | outbound | Bootstrap IAM/VPC/S3/SSM stack only; per-device lifecycle uses direct boto3 | **yes** |
| **AWS CloudWatch Logs** | outbound | Cloud-side log aggregation (optional; local first) | yes |
| **AWS Pricing API** | outbound | Hourly cost estimation cache (endpoint region `us-east-1`/`ap-south-1`) | **yes** |
| **AWS Device Farm** | outbound | Real iOS / Android devices in `us-west-2` (150-min remote sessions; per-minute or slot pricing) | yes (limited family) |
| **AWS S3 (user-owned)** | outbound | Optional artifact storage + Litestream replication | post-MVP toggle |
| **AWS IAM / STS** | outbound | Profiles, SSO, AssumeRole | **yes** |
| **AWS Marketplace AMIs (e.g. Genymotion ARM Android)** | outbound | User-subscribed Android images; never bundled | post-MVP plugin |
| **OS keychain** (Keychain / DPAPI / libsecret / cryptfile fallback) | local | Identity Broker secret storage | **yes** |
| **MCP clients** (Cursor, Claude Code, Codex, Continue, Cline, Gemini CLI, Windsurf, …) | inbound (stdio / Streamable HTTP) | AI control plane | **yes** |
| **mitmproxy** (embedded) | local | Per-device HTTP/HTTPS/HTTP-3 interception + HAR + mocks | yes |
| **coturn** (deployed in user's AWS) | local network | TURN server for WebRTC NAT traversal | yes |
| **Playwright** | outbound (browser family) | Browser automation, codegen recipes, MV3 extension testing | **yes** |
| **Appium 3** + **uiautomator2 driver** + **xcuitest driver** + **windows driver** | outbound (mobile/desktop) | Cross-platform automation | **yes** |
| **OmniParser V2 (local model)** | local | Structured screen parsing tier; off by default | yes |
| **Optional VLM providers** (Anthropic / OpenAI / Google / local) | outbound | Vision escalation tier (BYOK, cost-gated) | post-MVP toggle |
| **OpenTelemetry collector (user-deployed)** | outbound | Local trace/metric export from MCP gateway | yes |
| **GitHub release attestations / Sigstore** | inbound (CI) | Signed releases + SBOM | yes |

---

## 10. Authentication and permissions assumptions

| Field | Your answer |
|-------|-------------|
| Sign-up model | **None for DeviceLab itself.** Local single-user per workspace. AWS auth = user's AWS CLI profile / SSO / AssumeRole. MCP clients authenticate to the local gateway via per-client tokens (rotatable). |
| Roles | Local **operator** (full UI/MCP); MCP **client roles** layered as `Observe / Interact / Test / Manage / Admin / Dangerous` permission **modes**, refined as `read_scope × write_scope × cost_tier` axes; dangerous tools default disabled. |
| Resource ownership rules | Every AWS resource carries DeviceLab tags; deletion gated by tag match + operator confirmation. Devices belong to one Workspace; AI sessions can only act on devices their MCP client was granted leases for (see lease model). |
| Multi-tenancy | **No.** Single workspace per local installation. Future: per-machine workspace switching; never SaaS multi-tenant. |
| Session/token style | MCP: spec-compliant (`MCP-Session-Id`, `MCP-Protocol-Version`); per-MCP-client bearer tokens; sensitive operations use MCP **elicitation** (form for non-secret confirmations; URL mode for secrets). Optional **mTLS** between local MCP gateway and the cloud `devicelab-agent` over the SSM tunnel for defense-in-depth. |

Note: baseline JWT password auth from the template **does not apply** — DeviceLab has no remote user accounts. The initializer should preserve the template's auth code as scaffolding but the public product surface is local-only.

---

## 11. Frontend expectations

| Field | Your answer |
|-------|-------------|
| Public surface | **None.** No marketing site, no signup, no landing page. The app is local. |
| Authenticated surface | Dashboard, Devices (table + card views), Create Device wizard, Device Session (stream + actions + timeline + replay scrubber), MCP page (status, allowed tools, deeplinks, audit), Artifacts, Tests, Recipes, Logs (grouped), Diagnostics, Cost, Settings (Account / Cloud / Devices / MCP / Streaming / Cost / Security / Data). |
| Mobile / responsive | Desktop-class browser only; responsive enough to render on a 13" laptop. **Not** a mobile-first UI. |
| Design system | **shadcn/ui + Tailwind v4** baseline, augmented by a small set of bespoke components for the stream viewport, AX tree explorer, replay scrubber, and per-family device cards. Calm, table-first, minimal cloud jargon. |
| Anything explicitly out-of-scope for the UI | No marketing, no in-app account/billing, no notifications inbox beyond cost/error banners, no embedded chat with an LLM (use your own MCP client), no public sharing links. |

The baseline frontend's **items CRUD** and **admin view** are replaced wholesale by Device + Workspace UIs. Login screen is replaced by a local "unlock workspace" gate (optional OS keychain bound). User settings remain as scaffolding for per-operator preferences.

---

## 12. Backend / API expectations

| Field | Your answer |
|-------|-------------|
| API style | **REST + OpenAPI** for the control plane (consumed by the local web UI's typed TS client). **MCP** (stdio + Streamable HTTP) for AI clients. **gRPC bidi-streaming** between the local MCP gateway and the cloud `devicelab-agent` over SSM tunnels (internal only; mTLS). **WebRTC** for device streams + a separate data channel for input. **SSE** for UI live updates. |
| Versioning | `/api/v1/` for REST. MCP protocol version negotiated per spec; tool surface versioned via capability handshake. gRPC services versioned by proto package. |
| Pagination | Offset for lists; cursor for high-volume streams (audit log, evidence). |
| Rate limiting needs | Local API: light per-process. MCP: per-client + per-tool rate limits + per-call cost ceilings (especially `vlm_*`). AWS calls: client-side budgets to avoid quota exhaustion. |
| Background work needs | Yes. In-process **asyncio supervisor** by default for provisioning orchestration, tunnel watchdog, cost polling, cleanup, snapshot polling, warm pool maintenance. Optional **Redis + Taskiq/Dramatiq** profile for heavy parallelism. State machines use the **`transitions`** library. |

Key endpoints (illustrative; full surface generated from typed routers):

| Method | Path | Purpose | Auth |
|--------|------|---------|------|
| `GET` | `/api/v1/workspace` | Get workspace + connected cloud account status | local |
| `POST` | `/api/v1/cloud-accounts` | Connect/validate AWS account (profile/SSO/AssumeRole) | local |
| `POST` | `/api/v1/cloud-accounts/{id}/preflight` | Run quota / IAM / region preflight | local |
| `GET` | `/api/v1/templates` | List device templates with capabilities | local |
| `POST` | `/api/v1/devices` | Create device (template + profile + region) | local |
| `GET` | `/api/v1/devices` | List devices (filter by state/family) | local |
| `GET` | `/api/v1/devices/{id}/events` | SSE stream of lifecycle/phase changes | local |
| `POST` | `/api/v1/devices/{id}/lifecycle/{action}` | start/stop/restart/snapshot/terminate | local + confirmation |
| `GET` | `/api/v1/devices/{id}/stream` | WebRTC offer endpoint | local |
| `POST` | `/api/v1/devices/{id}/recipes/run` | Run recipe by id with inputs | local |
| `GET` | `/api/v1/cost/summary` | Active cost, top spenders, orphaned resources | local |
| `GET` | `/api/v1/mcp/config` | Generate MCP client config / Cursor deeplink | local |
| `POST` | `/api/v1/mcp/clients/{id}/rotate` | Rotate MCP bearer token | local |
| `GET` | `/api/v1/audit` | Audit log (paginated) | local |
| (MCP) | tools | See §4 bullet 4 for tool groups; capability handshake filters per device | MCP token + elicitation |

---

## 13. Deployment expectations

| Field | Your answer |
|-------|-------------|
| Target environment(s) | **Local developer machine** (primary). macOS, Windows 11, Linux. Optionally on a long-running personal VM (Litestream replicates SQLite to S3). |
| Cloud provider / host | **The user's AWS account** for cloud devices. DeviceLab is **not** hosted by anyone but the user. |
| Domain & TLS plan | `http://localhost:3000` default. Optional self-signed cert for `https://devicelab.local` via a one-time cert install when DCV/WebAuthn flows require secure context. No public DNS. |
| CI/CD beyond default GitHub Actions | Release pipeline builds Docker images (multi-arch: `linux/amd64`, `linux/arm64`), publishes to GHCR, generates **CycloneDX SBOM**, attaches **Sigstore** signatures + provenance attestations. **Packer** pipelines build per-family AMIs across regions (golden image + family overlay layers). |
| Observability | **OpenTelemetry** by default for traces/metrics in the local FastAPI + MCP gateway; logs via OTLP when collector configured. **Sentry optional**. Local diagnostics tarball generator for support. |

---

## 14. Security and privacy constraints

| Field | Your answer |
|-------|-------------|
| Compliance regimes | **None enforced** by DeviceLab (no hosted side). User remains responsible for their AWS account compliance; DeviceLab provides **building blocks** (audit log, redaction, secret broker, tagging) that help downstream compliance work. |
| PII handled | DeviceLab itself stores **no end-user PII** beyond the local operator's display name/email (optional). Devices controlled by the user may contain PII — DeviceLab does not exfiltrate or aggregate it. |
| Data retention policy | All local data retained per workspace settings (default 30 days for evidence/audit; configurable). User can wipe workspace at any time. |
| Data residency | Determined by user's AWS region selections. DeviceLab pins region per workspace + per-device override + per-template allow/deny lists. |
| Secrets management | **OS keychain** primary (Keychain / DPAPI / libsecret); **cryptfile** fallback on headless Linux. Secrets are **never** stored in SQLite, env files, logs, or returned to MCP clients. Sensitive flows use MCP **elicitation URL mode**. Optional **HashiCorp Vault** integration as a plugin. |

**Hard constraints:**

- **No public inbound runtime ports by default.** SSM tunnels and WebRTC over user-owned TURN only.
- **No long-lived AWS root keys** in any code path. Profile / SSO / `AssumeRole` only.
- **No secrets in model context.** AI never sees raw secret values; only refs.
- **No silent escalation to VLM / cloud LLM providers.** All such calls require explicit BYOK config + per-call cost gate.
- **Redaction layer on outbound tool responses** (PII regex + AWS IDs + secret refs) before returning to MCP clients.
- **Audit every dangerous-tool call** (terminate, delete, shell, enable dangerous group, exceed cost cap).
- **mTLS** between local MCP gateway and cloud `devicelab-agent` inside the SSM tunnel (defense in depth).
- **All AWS resources tagged** with DeviceLab tag set; untagged resources are not managed.
- **Defensive prompt-injection filtering** on tool outputs scraped from web/mobile pages.
- **No `os.getenv()` outside the central Settings module** (inherits from repo policy).

---

## 15. Testing expectations

| Field | Your answer |
|-------|-------------|
| Unit test depth | Per service / per adapter. State-machine transitions, identity broker, cost estimator, AX tree compressor, recipe parser all unit-covered. |
| Integration tests | Per route group + per device-family adapter using mocked AWS (`moto`) + simulated runtime agent. Real-cloud integration tests gated behind opt-in env vars and a dedicated test AWS account. |
| End-to-end tests | **Playwright** against the React app for human flows. **MCP self-tests** that drive the gateway end-to-end against simulated devices. Per-family **smoke recipes** that provision-and-tear-down on a real CI AWS account nightly. |
| Coverage floor | Per `pyproject.toml`; ratchet upward as adapters land. |
| Performance / load | **Round-trip-budget tests** as first-class CI gates: documented tasks (e.g. "login to web app and click button") must complete within target MCP call counts (default `≤ 4` for the documented flow set). Streaming latency budget: input RTT `< 50ms p95` over local LAN. |

---

## 16. Acceptance criteria for "initialized"

When this repository is considered **initialized** for DeviceLab, all of the following are true (these become queue-row acceptance contracts):

- **Spec & docs** for DeviceLab exist under `spec/spec.md` and `docs/architecture/` reflecting the §4 end-state, with the device-family matrix, MCP tool-group catalog, lifecycle state machine, and cost guardrail rules documented.
- **Initial queue rows** are seeded in dependency order following §4 (local install → BYOC AWS → first-run wizard → Linux + Browser families → MCP gateway + observation tiers → recipes → identity broker → streaming → cost → remaining families → snapshots → tests → evidence → plugin SPI).
- The repo's **agent control plane** (AGENTS.md, skills/, prompts/, queue/, Makefile) names DeviceLab-specific procedures: `add-device-family`, `add-mcp-tool-group`, `add-template`, `bake-ami`, `validate-cost-guardrail`, `run-round-trip-budget`.
- A **first-run wizard happy path** is queued: from a user with valid AWS credentials, reaching a streamable Linux Desktop + working MCP attachment **within 10 minutes** of `make up`.
- **MCP capability handshake** is specified: per-device tool manifest, observation envelope schema, action result envelope schema, lease model — with at least one round-trip-budget test fixture.
- **Identity Broker** contract is specified end-to-end: keychain backends, secret-ref schema, elicitation flow, audit trail.
- **Decisions log** is captured (links `docs/research/open_ended_question.md` + `docs/research/SOURCES.md` + `docs/research/reference/EXTERNAL_REFERENCE.md`) so subsequent agents don't relitigate frozen choices (e.g. 35-state FSM rejected, screenshot-default rejected, `accomplish()` deferred to v2, MCP-to-AI-client transport stays spec-compliant).

---

## 17. Non-functional requirements

| Requirement | Target | Notes |
|-------------|--------|-------|
| Availability | Local app: 99% during active use. Cloud devices: best-effort per AWS SLA + warm pool buffering. | DeviceLab is opportunistic; not an HA service. |
| Latency (p95) | UI control-plane API: `< 150 ms` local. MCP **input action** RTT through tunnel: `< 50 ms` LAN / `< 150 ms` cross-region. MCP **observation (cached AX tree)**: `< 100 ms`. Stream end-to-end glass-to-glass: target `< 120 ms` over WebRTC LAN. | Achieved by Observation Hub cache + push events + separate input data channel. |
| Throughput | One workspace supports `≥ 25` concurrent devices and `≥ 5` concurrent MCP clients on a typical developer laptop without UI degradation. | Heavier loads use the Redis worker profile. |
| Scalability plan | Vertical first (single local process scales to dozens of devices). Plugin SPI + warm pool + future multi-account `AssumeRole` extends horizontally. No SaaS scaling. | |
| Backup RPO / RTO | Local SQLite via Litestream optional → S3 (user-owned). RPO `≤ 1 min` with Litestream; RTO `≤ 10 min` (restore + reattach AWS resources by tag). Without Litestream, daily file backup recommended; data is recoverable from AWS tags. | |
| Cost transparency | Every running device's hourly estimate within `±10%` of actual AWS bill for the supported families. | Driven by AWS Pricing API cache. |
| Round-trip budget | Documented flows (login, install APK + launch, screenshot diff, fill form) must complete within published RT budgets (`≤ 4–6` MCP calls). | First-class CI gate. |

---

## 18. Hard constraints

- **Open-source MIT** core; third-party adapters honor their own licenses.
- **BYOC.** DeviceLab never holds the user's cloud credentials remotely. AWS bills the user directly.
- **No SaaS, no DeviceLab-hosted servers, no payment / accounts system, no telemetry without opt-in.**
- **MCP is a first-class interface** — every device action is exposed through MCP, gated by capability handshake + permission mode + cost tier + (optionally) elicitation.
- **Structured observation is the default**; screenshots / VLM are escalation tiers, always cost-gated.
- **No public inbound runtime ports** by default; SSM tunnels + WebRTC over user-owned TURN.
- **All AWS resources tagged**; orphan-resource cleanup is built in.
- **Real iOS is honest about its limits** (Device Farm 150-min sessions, `us-west-2` only, no persistent state) — never marketed as if it were Simulator-grade.
- **EC2 Mac honors the 24-hour Dedicated Host minimum** and surfaces it in cost UI prominently.
- **Plugin SPI versioned by proto + semantic version** — never silently break adapter ABI.
- **Secrets never returned to MCP clients.** Identity Broker injects values runtime-side.
- **No `accomplish(natural-language)` mega-tool in v1.** Recipes only.

---

## 19. Open questions

(Cross-reference: full decision table with confidence levels lives in [`docs/research/open_ended_question.md`](docs/research/open_ended_question.md). Items listed here are the **operator decisions still pending** when initialization runs — the initializer should turn each into a blocked queue row or `docs/open-questions.md` entry rather than guess.)

1. **Tauri shell timing.** Default v1 install is Docker Compose + localhost; is a Tauri wrapper part of the initial roadmap or strictly post-v1? (low risk; doesn't block init).
2. **Runtime agent language.** Default direction is **Go** (single static binary, gRPC) for the cloud `devicelab-agent`; do we accept that choice or run a Go-vs-Rust spike before queue seeding?
3. **Default local VLM (when enabled).** OmniParser V2 is the recommended structured-vision tier; do we ship a bundled Moondream/SmolVLM stub for general VLM, or strictly BYOK?
4. **First Browser-family CDP backend.** Playwright + CDP confirmed; do we also ship WebDriver BiDi adapters in v1 or list it as post-v1 (BiDi still WD-status at W3C)?
5. **Warm pool defaults per family.** Empty by default is safe; do we ship suggested pre-warm counts per template, or leave operators to opt in?
6. **Recording recipe authoring fidelity.** YAML + Playwright codegen for Browser is committed; what level of cross-family recorder (mobile/desktop) ships in v1 vs phases later?
7. **Optional HashiCorp Vault plugin** for Identity Broker — v1 or v2?
8. **OpenTelemetry exporter defaults.** Ship with a local OTLP target preconfigured to a sample Grafana/Tempo Compose service, or leave the user to wire it?
9. **mTLS cert lifecycle ownership.** Short-lived certs between MCP gateway and runtime agent — managed by DeviceLab CA, or pluggable into user PKI?
10. **AWS multi-account support timing.** `AssumeRole` chains are post-v1 in the current plan; confirm before initialization seeds the queue.

---

## 20. Additional context

- **Research workspace** (decisions, sources, skim notes): [`docs/research/`](docs/research/)
  - [`docs/research/README.md`](docs/research/README.md) — folder map.
  - [`docs/research/open_ended_question.md`](docs/research/open_ended_question.md) — 81-question decision table with confidence levels.
  - [`docs/research/SOURCES.md`](docs/research/SOURCES.md) — bibliography (`[S001…]`).
  - [`docs/research/queries/queries-results.md`](docs/research/queries/queries-results.md) — web-search log.
  - [`docs/research/notes/`](docs/research/notes/) — themed synthesis notes (local stack, AWS, streaming, automation/OCR/VLM, network/recipes/testing, security/onboarding).
  - [`docs/research/reference/EXTERNAL_REFERENCE.md`](docs/research/reference/EXTERNAL_REFERENCE.md) — tracked upstream registry + direct-read digests (MCP spec/SDK, FastMCP, AWS Mac/DCV/Device Farm/Pricing, Playwright MCP, Appium drivers, pywinauto, OmniParser, Selkies, coturn, libimobiledevice, mitmproxy).

- **Design history (pre-init):**
  - Original draft (pre-research) lived in chat as the "DeviceLab Production System Design" memo. Every fact from that memo is preserved across `docs/research/notes/`, this `idea.md`, and the decision table.
  - Pass 1 (architecture improvements): added round-trip budget, recipes, identity broker, semantic action tools, persistent handles, event subscriptions, observation pyramid.
  - Pass 2 (gaps): warm pools, preflight quotas, multi-client coordination + leases, observation versioning, evidence/replay, plugin SPI, time/locale controls.
  - Research rounds: 50-query web search + direct-read digests of upstream READMEs/specs.

- **Decisions explicitly chosen against** (do not relitigate without an ADR):
  - 35-state device FSM → collapsed to 10 canonical states + orthogonal flags.
  - 60-endpoint runtime-agent REST API → verb/noun action API + event streams over gRPC.
  - Screenshot-default observation (Anthropic/OpenAI/Google CUA style) → structured AX/OCR-first; screenshots are escalation.
  - VLM as default observation tier → deferred to BYOK escalation only.
  - `gRPC` toward MCP clients → spec-compliant MCP transports only; gRPC stays internal to gateway↔agent.
  - `accomplish(natural-language)` super-tool → deferred to post-v1; recipes only in v1.
  - CloudFormation for every per-device stack → CFN only for one-time bootstrap; per-device lifecycle uses direct boto3.
  - Bundling Genymotion / proprietary AMIs in the OSS repo → never; users subscribe in their own AWS.

- **Reference competitor / inspiration set** (for capability checklists, **not** business model): BrowserStack App Live, Sauce Labs Real Device Cloud, AWS Device Farm, Genymotion Cloud, Kasm Workspaces (closest OSS analog), Microsoft Playwright MCP (gold-standard browser MCP), Microsoft OmniParser (structured screen parsing).

- **Naming clarifications:**
  - "DeviceLab" project name; "devicelab" repo slug; `devicelab-agent` is the cloud runtime agent name; tag prefix `DeviceLab*` on AWS resources.
  - The browser-based UI URL is `http://localhost:3000` (frontend); local API on `http://localhost:8000`; MCP gateway on a separate local port (configurable, default `19736`) for stdio + Streamable HTTP attachments.

---

**End of idea definition.**

> Once every applicable section above is filled out, ask an AI agent in this repo to run **`skills/init/repo_initialize.md`**. The skill is the single canonical initialization procedure — there is no `make idea:*` command. Initialization will produce: refreshed `spec/spec.md`, DeviceLab-specific docs under `docs/architecture/`, the initial queue with the §4 ordering, and updated `AGENTS.md` scope references. Decisions from `docs/research/open_ended_question.md` should be honored unless explicitly overridden in this `idea.md`.
