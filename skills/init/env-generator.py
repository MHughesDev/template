# skills/init/env-generator.py
"""

PURPOSE:
Generates .env.example content based on enabled profiles. Each profile has a
defined set of required environment variables with defaults and documentation
comments. The generated .env.example is profile-appropriate: only includes
vars for enabled features.

DEPENDS ON:
- pathlib (stdlib) — file paths
- argparse (stdlib) — CLI (--profiles list)
- sys (stdlib) — stdout output

DEPENDED ON BY:
- skills/init/env-generator.md — references as machinery
- scripts/generate-env.sh — uses this to generate .env.example at init time

CONSTANTS:

  BASE_VARS: dict[str, dict] — vars always included regardless of profile.
    Each entry: {default: str, comment: str, section: str}
    Includes: DATABASE_URL, JWT_SECRET_KEY, JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_REFRESH_TOKEN_EXPIRE_DAYS, API_HOST, API_PORT, API_DEBUG, API_CORS_ORIGINS,
    API_PREFIX, API_ALLOWED_HOSTS, LOG_LEVEL, LOG_FORMAT

  PROFILE_VARS: dict[str, dict[str, dict]] — vars added per profile.
    - "ai_rag": AI_ENABLED, CHROMA_HOST, CHROMA_PORT, CHROMA_COLLECTION, EMBEDDING_PROVIDER, OPENAI_API_KEY
    - "workers": BROKER_URL, RESULT_BACKEND_URL
    - "multi_tenancy": MULTI_TENANCY_ENABLED
    - "billing": STRIPE_API_KEY, STRIPE_WEBHOOK_SECRET
    - "email": SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, FROM_EMAIL
    - "web": FRONTEND_URL, VITE_API_BASE_URL (for frontend .env)
    - "search": SEARCH_PROVIDER, MEILISEARCH_URL, MEILISEARCH_API_KEY

FUNCTIONS:

  generate_section(
    section_name: str,
    vars_dict: dict[str, dict]
  ) -> str:
    PURPOSE: Generate a section of .env.example content.
    STEPS:
      1. Add section header comment: # === SECTION_NAME ===
      2. For each var: add comment line, then VAR_NAME=default line
      3. Add blank line after section
    RETURNS: Section content string

  generate_env_example(enabled_profiles: list[str]) -> str:
    PURPOSE: Generate complete .env.example for given profiles.
    STEPS:
      1. Start with BASE_VARS sections
      2. For each enabled profile: add PROFILE_VARS sections
      3. Add DEVELOPMENT ONLY section at bottom
      4. Add file header comment (§1.7 title comment + purpose note)
    RETURNS: Complete .env.example content

  main() -> None:
    PURPOSE: CLI entry point.
    STEPS:
      1. Parse args: --profiles (comma-separated list or "all")
      2. Generate env example
      3. Write to stdout (caller redirects to file)
      4. Optionally: --output path to write directly

DESIGN DECISIONS:
- Output to stdout by default: caller redirects (> .env.example) for flexibility
- Unknown profile names: warn but don't fail (graceful degradation)
- Section ordering: Base → Auth → API → per-profile → Observability → Dev-only
- All default values use CHANGEME or safe defaults (never real secrets)
"""
