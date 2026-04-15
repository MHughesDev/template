# scripts/idea-parser.py
"""Parse idea.md into a deterministic init-manifest.json (stdlib only)."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

PARSER_VERSION = "2.0"
MIN_IDEA_VERSION = "2.0"

# Profiles that, when enabled, scaffold into packages/ (via enable-<stem>.sh)
PACKAGE_PROFILE_STEMS: set[str] = {
    "workers", "ai-rag", "billing", "email", "file-storage",
    "search", "analytics", "scheduled-jobs",
}

# Declarative profile constraint rules
PROFILE_REQUIRES: dict[str, list[str]] = {
    "billing": ["multi_tenancy"],
    "multi_tenancy": [],
    "websocket": [],
    "ai_rag": [],
}

PROFILE_CONFLICTS: dict[str, list[str]] = {
    # No hard conflicts currently — used for future extension
}

ARCHETYPE_DEFAULTS: dict[str, dict[str, bool]] = {
    "api_service": {
        "web_frontend": False,
        "mobile": False,
        "workers": False,
        "ai_rag": False,
        "multi_tenancy": False,
        "websocket": False,
        "scheduled_jobs": False,
        "file_storage": False,
        "email_notifications": False,
        "search": False,
        "billing": False,
        "analytics": False,
    },
    "full_stack_web": {
        "web_frontend": True,
        "mobile": False,
        "workers": False,
        "ai_rag": False,
        "multi_tenancy": False,
        "websocket": False,
        "scheduled_jobs": False,
        "file_storage": False,
        "email_notifications": True,
        "search": False,
        "billing": False,
        "analytics": False,
    },
    "full_stack_mobile": {
        "web_frontend": True,
        "mobile": True,
        "workers": False,
        "ai_rag": False,
        "multi_tenancy": False,
        "websocket": True,
        "scheduled_jobs": False,
        "file_storage": True,
        "email_notifications": True,
        "search": False,
        "billing": False,
        "analytics": True,
    },
    "platform_internal": {
        "web_frontend": False,
        "mobile": False,
        "workers": True,
        "ai_rag": False,
        "multi_tenancy": False,
        "websocket": False,
        "scheduled_jobs": True,
        "file_storage": False,
        "email_notifications": False,
        "search": False,
        "billing": False,
        "analytics": False,
    },
    "data_pipeline": {
        "web_frontend": False,
        "mobile": False,
        "workers": True,
        "ai_rag": False,
        "multi_tenancy": False,
        "websocket": False,
        "scheduled_jobs": True,
        "file_storage": True,
        "email_notifications": False,
        "search": False,
        "billing": False,
        "analytics": True,
    },
    "ai_ml_service": {
        "web_frontend": False,
        "mobile": False,
        "workers": True,
        "ai_rag": True,
        "multi_tenancy": False,
        "websocket": False,
        "scheduled_jobs": False,
        "file_storage": True,
        "email_notifications": False,
        "search": True,
        "billing": False,
        "analytics": True,
    },
    "marketplace": {
        "web_frontend": True,
        "mobile": False,
        "workers": True,
        "ai_rag": False,
        "multi_tenancy": True,
        "websocket": True,
        "scheduled_jobs": True,
        "file_storage": True,
        "email_notifications": True,
        "search": True,
        "billing": True,
        "analytics": True,
    },
    "saas_product": {
        "web_frontend": True,
        "mobile": False,
        "workers": True,
        "ai_rag": False,
        "multi_tenancy": True,
        "websocket": False,
        "scheduled_jobs": True,
        "file_storage": True,
        "email_notifications": True,
        "search": False,
        "billing": True,
        "analytics": True,
    },
}

# Order matches §5 table rows (profile key -> enable script stem)
PROFILE_ROW_KEYS: list[tuple[str, str]] = [
    ("web_frontend", "web"),
    ("mobile", "mobile"),
    ("workers", "workers"),
    ("ai_rag", "ai-rag"),
    ("multi_tenancy", "multi-tenancy"),
    ("websocket", "websocket"),
    ("scheduled_jobs", "scheduled-jobs"),
    ("file_storage", "file-storage"),
    ("email_notifications", "email"),
    ("search", "search"),
    ("billing", "billing"),
    ("analytics", "analytics"),
]

ARCHETYPE_ROW_TO_KEY: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"^\*\*API service\*\*", re.I), "api_service"),
    (re.compile(r"Full-stack web app", re.I), "full_stack_web"),
    (re.compile(r"Full-stack with mobile", re.I), "full_stack_mobile"),
    (re.compile(r"Platform / internal", re.I), "platform_internal"),
    (re.compile(r"Data pipeline", re.I), "data_pipeline"),
    (re.compile(r"AI / ML service", re.I), "ai_ml_service"),
    (re.compile(r"Marketplace", re.I), "marketplace"),
    (re.compile(r"SaaS product", re.I), "saas_product"),
]


def _parse_init_meta(text: str) -> dict[str, str | None]:
    m = re.search(
        r"<!--\s*INIT_META\s*(.*?)-->",
        text,
        re.DOTALL | re.IGNORECASE,
    )
    if not m:
        return {}
    block = m.group(1)
    out: dict[str, str | None] = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip()
        if v in ("null", '""', "''"):
            out[k] = None
        else:
            out[k] = v.strip('"').strip("'")
    return out


def _check_version_compat(meta: dict[str, str | None]) -> list[str]:
    """Warn when idea.md declares an init_version older than this parser supports."""
    errs: list[str] = []
    raw = meta.get("init_version")
    if not raw:
        return errs
    try:
        major_idea = int(str(raw).split(".")[0])
        major_parser = int(PARSER_VERSION.split(".")[0])
        if major_idea < major_parser:
            errs.append(
                f"INIT_META init_version is '{raw}' but this parser requires >= {MIN_IDEA_VERSION}. "
                "Update your idea.md template to the current version before re-initializing."
            )
    except ValueError:
        errs.append(f"INIT_META init_version '{raw}' is not a valid version string.")
    return errs


def _table_after_heading(text: str, heading_re: re.Pattern[str]) -> list[list[str]]:
    lines = text.splitlines()
    start = -1
    for i, line in enumerate(lines):
        if heading_re.match(line.strip()):
            start = i
            break
    if start < 0:
        return []
    rows: list[list[str]] = []
    for line in lines[start + 1 :]:
        if line.strip().startswith("|") and "|" in line[1:]:
            if re.match(r"^\|\s*[-:]+", line):
                continue
            parts = [p.strip() for p in line.split("|")]
            parts = [p for p in parts if p != ""]
            if parts:
                rows.append(parts)
        elif line.startswith("## "):
            break
    return rows


def _section_lines(text: str, section_num: int) -> str:
    pat = re.compile(rf"^##\s+{section_num}\.", re.MULTILINE)
    m = pat.search(text)
    if not m:
        return ""
    start = m.start()
    rest = text[start:]
    m2 = re.compile(r"^##\s+", re.MULTILINE).search(rest[1:])
    if m2:
        return rest[: m2.start() + 1]
    return rest


def _parse_identity(text: str) -> dict[str, str]:
    sec = _section_lines(text, 1)
    rows = _table_after_heading(sec, re.compile(r"^##\s+1\."))
    out: dict[str, str] = {}
    for row in rows:
        if len(row) < 2:
            continue
        key = row[0].lower()
        val = row[1].strip().strip("`")
        if "project name" in key:
            out["project_name"] = val
        elif "display name" in key:
            out["display_name"] = val
        elif "one-line" in key or "pitch" in key:
            out["one_line_pitch"] = val
        elif "repository slug" in key or "slug" in key:
            out["repository_slug"] = val
    return out


def _parse_archetype(text: str) -> tuple[str | None, list[str]]:
    sec = _section_lines(text, 3)
    rows = _table_after_heading(sec, re.compile(r"^##\s+3\."))
    selected: list[str] = []
    archetype_key: str | None = None
    for row in rows:
        if len(row) < 2:
            continue
        label = row[0]
        select_cell = row[1] if len(row) > 1 else ""
        if "[x]" in select_cell.lower() or "[X]" in select_cell:
            selected.append(label)
            for pat, key in ARCHETYPE_ROW_TO_KEY:
                if pat.search(label):
                    archetype_key = key
                    break
    return archetype_key, selected


def _profile_key_from_label(label: str) -> str | None:
    """Map first-column label from §5 table to internal profile key."""
    low = label.lower()
    if "web frontend" in low:
        return "web_frontend"
    if "mobile app" in low or low.strip().startswith("**mobile"):
        return "mobile"
    if "background workers" in low:
        return "workers"
    if "ai" in low and "rag" in low:
        return "ai_rag"
    if "multi-tenancy" in low:
        return "multi_tenancy"
    if "websocket" in low or "real-time" in low:
        return "websocket"
    if "scheduled jobs" in low or ("cron" in low and "scheduled" in low):
        return "scheduled_jobs"
    if "file uploads" in low or ("file" in low and "storage" in low):
        return "file_storage"
    if "email" in low and "notifications" in low:
        return "email_notifications"
    if "search" in low and "full-text" in low:
        return "search"
    if "billing" in low or "payments" in low:
        return "billing"
    if "analytics" in low:
        return "analytics"
    return None


def _parse_profiles(text: str) -> tuple[dict[str, str], list[str]]:
    """Return per-profile state: 'unanswered' | 'yes' | 'no', and parse errors."""
    sec = _section_lines(text, 5)
    lines = sec.splitlines()
    in_table = False
    header_seen = False
    states: dict[str, str] = {k: "unanswered" for k, _ in PROFILE_ROW_KEYS}
    errs: list[str] = []
    for line in lines:
        if "| Profile |" in line or ("Profile" in line and "Enable?" in line):
            in_table = True
            continue
        if not in_table:
            continue
        if "|---" in line or line.strip().startswith("|---"):
            header_seen = True
            continue
        if not header_seen or "|" not in line:
            continue
        if not line.strip().startswith("|"):
            break
        parts = [p.strip() for p in line.split("|")]
        parts = [p for p in parts if p != ""]
        if len(parts) < 2:
            continue
        label = parts[0].strip("*").strip()
        enable_cell = parts[1]
        key = _profile_key_from_label(label)
        if key is None:
            continue
        if re.search(r"\[x\]\s*yes", enable_cell, re.I):
            states[key] = "yes"
        elif re.search(r"\[x\]\s*no", enable_cell, re.I):
            states[key] = "no"
        elif re.search(r"\[\s*\]", enable_cell) and "[x]" not in enable_cell.lower():
            states[key] = "unanswered"
        else:
            errs.append(
                f"Profile '{key}': Enable? must be `[x] yes`, `[x] no`, or `[ ]` (unanswered)."
            )
    return states, errs


def _parse_bounded_contexts(text: str) -> tuple[list[dict[str, str]], list[str]]:
    sec = _section_lines(text, 4)
    lines = sec.splitlines()
    sub_start = -1
    for i, line in enumerate(lines):
        if re.match(r"^###\s+4\.2", line):
            sub_start = i
            break
    if sub_start < 0:
        return [], ["Could not find §4.2 Bounded contexts table."]
    rows: list[list[str]] = []
    header_seen = False
    for line in lines[sub_start + 1 :]:
        if line.startswith("### "):
            break
        if line.strip().startswith("|") and "|" in line[1:]:
            if "Context name" in line and "Entities" in line:
                header_seen = True
                continue
            if re.match(r"^\|\s*[-:]+", line):
                continue
            if not header_seen:
                continue
            parts = [p.strip() for p in line.split("|")]
            parts = [p for p in parts if p != ""]
            if len(parts) >= 3:
                rows.append(parts)
    contexts: list[dict[str, str]] = []
    names: list[str] = []
    errs: list[str] = []
    for row in rows:
        if len(row) < 3:
            continue
        name = row[0].strip().strip("`")
        if not name or name.startswith("<!--") or "e.g." in name.lower():
            continue
        if "<!--" in name:
            continue
        contexts.append(
            {
                "name": name,
                "entities": row[1].strip(),
                "description": row[2].strip(),
            }
        )
        names.append(name.lower())
    dupes = {n for n in names if names.count(n) > 1}
    if dupes:
        errs.append(f"Duplicate bounded context names: {sorted(dupes)}")
    return contexts, errs


def _parse_primary_db(text: str) -> str | None:
    sec = _section_lines(text, 7)
    rows = _table_after_heading(sec, re.compile(r"^##\s+7\."))
    for row in rows:
        if len(row) < 2:
            continue
        if "primary database" in row[0].lower():
            cell = row[1].lower()
            if "postgres" in cell:
                return "postgresql"
            if "sqlite" in cell:
                return "sqlite"
            return None
    return None


def _parse_queue_section_12(text: str) -> list[dict[str, str]]:
    lines = text.splitlines()
    in_section = False
    header_seen = False
    rows: list[dict[str, str]] = []
    for line in lines:
        if re.match(r"^##\s+12\.(\s|$)", line):
            in_section = True
            continue
        if in_section and line.startswith("## ") and not re.match(r"^##\s+12\.", line):
            break
        if not in_section:
            continue
        if "Priority" in line and "Category" in line and "Summary" in line:
            header_seen = True
            continue
        if "|---" in line or line.strip().startswith("|---"):
            continue
        if not header_seen or "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) < 3:
            continue
        priority, category, summary = parts[0], parts[1], parts[2]
        if priority.startswith("<!--") or "add rows" in priority.lower():
            continue
        if not summary or summary.startswith("<!--"):
            continue
        rows.append(
            {
                "priority": priority.strip(),
                "category": category.strip(),
                "summary": summary.strip(),
            }
        )
    return rows


def _parse_open_questions(text: str) -> list[str]:
    sec = _section_lines(text, 16)
    out: list[str] = []
    for line in sec.splitlines():
        m = re.match(r"^\s*(\d+)\.\s+(.+)$", line)
        if not m:
            continue
        item = m.group(2).strip()
        if item.startswith("<!--") or not item:
            continue
        out.append(item)
    return out


def _placeholder_in_required_sections(text: str) -> list[str]:
    """Sections 1,3,4,6,7,9 — report <!-- blocks."""
    errs: list[str] = []
    for num in (1, 3, 4, 6, 7, 9):
        sec = _section_lines(text, num)
        if "<!--" in sec:
            errs.append(
                f"Section {num} still contains HTML comment placeholders (`<!--`)."
            )
    return errs


def _resolve_profile_states(
    archetype_key: str,
    raw_states: dict[str, str],
) -> tuple[dict[str, bool], dict[str, str], list[str]]:
    """Returns enabled map, source map (explicit|resolved_by_archetype), archetype_resolved_fields."""
    defaults = ARCHETYPE_DEFAULTS.get(archetype_key, {})
    enabled: dict[str, bool] = {}
    source: dict[str, str] = {}
    resolved_fields: list[str] = []
    for key, _script in PROFILE_ROW_KEYS:
        st = raw_states.get(key, "unanswered")
        if st == "yes":
            enabled[key] = True
            source[key] = "explicit"
        elif st == "no":
            enabled[key] = False
            source[key] = "explicit"
        else:
            # unanswered — use archetype default (not inferred from prose)
            d = defaults.get(key, False)
            enabled[key] = d
            source[key] = "resolved_by_archetype"
            resolved_fields.append(key)
    return enabled, source, resolved_fields


def _validate_profile_constraints(
    enabled_map: dict[str, bool],
) -> list[str]:
    """Check PROFILE_REQUIRES and PROFILE_CONFLICTS rules against resolved profile map."""
    errs: list[str] = []
    for profile, required in PROFILE_REQUIRES.items():
        if not enabled_map.get(profile):
            continue
        for dep in required:
            if not enabled_map.get(dep):
                errs.append(
                    f"Profile '{profile}' requires '{dep}' to also be enabled — "
                    f"enable '{dep}' in §5 or disable '{dep}' in §5."
                )
    for profile, conflicts in PROFILE_CONFLICTS.items():
        if not enabled_map.get(profile):
            continue
        for conflict in conflicts:
            if enabled_map.get(conflict):
                errs.append(
                    f"Profile '{profile}' conflicts with '{conflict}' — "
                    "they cannot both be enabled."
                )
    return errs


def _resolve_module_placement(
    contexts: list[dict[str, str]],
    profiles_enabled: list[str],
) -> list[dict[str, Any]]:
    """
    Assign module_placement ('api_module' or 'shared_package') to each bounded context.

    When a context name matches a profile that scaffolds into packages/, mark it as
    'shared_package' so the orchestrator skips double-scaffolding into apps/api/src/.
    """
    result: list[dict[str, Any]] = []
    for ctx in contexts:
        name = ctx["name"].strip().lower().replace(" ", "_")
        name_dash = name.replace("_", "-")
        # Profile script stems that create packages/ (e.g. 'billing', 'search')
        overlaps_package_profile = (
            name_dash in PACKAGE_PROFILE_STEMS or name in PACKAGE_PROFILE_STEMS
        ) and (name_dash in profiles_enabled or any(
            s.replace("-", "_") == name for s in profiles_enabled
        ))
        placement = "shared_package" if overlaps_package_profile else "api_module"
        result.append({**ctx, "module_placement": placement})
    return result


def _infer_queue_dependencies(
    queue_rows: list[dict[str, Any]],
    contexts: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """
    Infer dependency edges between queue rows from domain relationships.

    If context B's entities or description mentions context A's name,
    add context A's queue ID as a dependency of context B's queue ID.
    """
    if len(queue_rows) < 2:
        return queue_rows

    # Build a map: context name → queue row index (0-based)
    ctx_names = [c["name"].strip().lower() for c in contexts]
    id_for_name: dict[str, str] = {}
    for i, ctx in enumerate(contexts):
        name = ctx["name"].strip().lower()
        if i < len(queue_rows):
            id_for_name[name] = queue_rows[i]["id"]

    updated: list[dict[str, Any]] = []
    for i, row in enumerate(queue_rows):
        ctx = contexts[i] if i < len(contexts) else None
        if ctx is None:
            updated.append(row)
            continue
        description = (ctx.get("entities", "") + " " + ctx.get("description", "")).lower()
        deps: list[str] = []
        for j, other_name in enumerate(ctx_names):
            if j == i:
                continue
            if other_name in description and j < len(queue_rows):
                dep_id = queue_rows[j]["id"]
                if dep_id not in deps:
                    deps.append(dep_id)
        new_row = dict(row)
        if deps:
            existing = new_row.get("dependencies", "").strip()
            merged = (existing + " " + " ".join(deps)).strip() if existing else " ".join(deps)
            new_row["dependencies"] = merged
        updated.append(new_row)
    return updated


def _empty_resolved_decisions() -> dict[str, Any]:
    return {
        "compose_services": ["api"],
        "python_dependencies": [],
        "env_vars": {},
        "modules_to_scaffold": [],
        "profiles_enabled": [],
        "profiles_discarded": [],
        "queue_seed_rows": [],
        "ci_additions": [],
        "use_postgres": False,
        "archetype_resolved_fields": [],
        "open_questions": [],
    }


def _add_unique(lst: list[str], item: str) -> None:
    if item not in lst:
        lst.append(item)


def _merge_env(d: dict[str, str], updates: dict[str, str]) -> None:
    for k, v in updates.items():
        if k not in d:
            d[k] = v


def _merge_deps(lst: list[str], items: list[str]) -> None:
    for it in items:
        if it not in lst:
            lst.append(it)


def apply_web_frontend_decisions(
    _manifest: dict[str, Any], decisions: dict[str, Any]
) -> None:
    _add_unique(decisions["compose_services"], "nginx")
    _merge_env(
        decisions["env_vars"],
        {"VITE_API_URL": "http://localhost:8000"},
    )


def apply_mobile_decisions(
    _manifest: dict[str, Any], decisions: dict[str, Any]
) -> None:
    _merge_env(
        decisions["env_vars"],
        {"EXPO_PUBLIC_API_URL": "http://localhost:8000"},
    )


def apply_workers_decisions(
    _manifest: dict[str, Any], decisions: dict[str, Any]
) -> None:
    for s in ("redis", "worker"):
        _add_unique(decisions["compose_services"], s)
    _merge_deps(decisions["python_dependencies"], ["celery[redis]", "redis"])
    _merge_env(
        decisions["env_vars"],
        {
            "CELERY_BROKER_URL": "redis://localhost:6379/0",
            "CELERY_RESULT_BACKEND": "redis://localhost:6379/1",
        },
    )


def apply_ai_rag_decisions(
    _manifest: dict[str, Any], decisions: dict[str, Any]
) -> None:
    _add_unique(decisions["compose_services"], "chroma")
    _merge_deps(decisions["python_dependencies"], ["chromadb", "sentence-transformers"])
    _merge_env(
        decisions["env_vars"],
        {
            "CHROMA_HOST": "localhost",
            "CHROMA_PORT": "8001",
            "AI_KILL_SWITCH": "false",
        },
    )


def apply_multi_tenancy_decisions(
    _manifest: dict[str, Any], decisions: dict[str, Any]
) -> None:
    _merge_env(decisions["env_vars"], {"TENANT_ISOLATION_MODEL": "row_level"})
    _add_unique(decisions["ci_additions"], "tenant_isolation_integration_test")


def apply_websocket_decisions(
    _manifest: dict[str, Any], decisions: dict[str, Any]
) -> None:
    _merge_deps(decisions["python_dependencies"], ["websockets"])
    _merge_env(decisions["env_vars"], {"WS_HEARTBEAT_INTERVAL": "30"})


def apply_scheduled_jobs_decisions(
    _manifest: dict[str, Any], decisions: dict[str, Any]
) -> None:
    _merge_deps(decisions["python_dependencies"], ["apscheduler"])
    _merge_env(decisions["env_vars"], {"SCHEDULER_ENABLED": "true"})


def apply_file_storage_decisions(
    _manifest: dict[str, Any], decisions: dict[str, Any]
) -> None:
    _merge_deps(decisions["python_dependencies"], ["boto3"])
    _merge_env(
        decisions["env_vars"],
        {
            "STORAGE_PROVIDER": "local",
            "STORAGE_BUCKET": "local-dev",
            "AWS_ACCESS_KEY_ID": "REPLACE_ME",
            "AWS_SECRET_ACCESS_KEY": "REPLACE_ME",
            "AWS_REGION": "us-east-1",
        },
    )


def apply_email_notifications_decisions(
    _manifest: dict[str, Any], decisions: dict[str, Any]
) -> None:
    _merge_deps(decisions["python_dependencies"], ["sendgrid"])
    _merge_env(
        decisions["env_vars"],
        {
            "EMAIL_PROVIDER": "smtp",
            "SMTP_HOST": "localhost",
            "SMTP_PORT": "1025",
            "SMTP_FROM": "noreply@example.com",
        },
    )


def apply_search_decisions(
    _manifest: dict[str, Any], decisions: dict[str, Any]
) -> None:
    _merge_deps(decisions["python_dependencies"], ["meilisearch"])
    _merge_env(
        decisions["env_vars"],
        {
            "SEARCH_PROVIDER": "meilisearch",
            "MEILISEARCH_URL": "http://localhost:7700",
            "MEILISEARCH_API_KEY": "REPLACE_ME",
        },
    )


def apply_billing_decisions(
    _manifest: dict[str, Any], decisions: dict[str, Any]
) -> None:
    _merge_deps(decisions["python_dependencies"], ["stripe"])
    _merge_env(
        decisions["env_vars"],
        {
            "STRIPE_SECRET_KEY": "sk_test_REPLACE_ME",
            "STRIPE_WEBHOOK_SECRET": "whsec_REPLACE_ME",
            "STRIPE_PUBLISHABLE_KEY": "pk_test_REPLACE_ME",
        },
    )


def apply_analytics_decisions(
    _manifest: dict[str, Any], decisions: dict[str, Any]
) -> None:
    _merge_env(
        decisions["env_vars"],
        {
            "ANALYTICS_ENABLED": "false",
            "ANALYTICS_WRITE_KEY": "REPLACE_ME",
        },
    )


def apply_primary_db_decisions(use_postgres: bool, decisions: dict[str, Any]) -> None:
    if use_postgres:
        _add_unique(decisions["compose_services"], "db")
        _merge_deps(decisions["python_dependencies"], ["asyncpg"])
        _merge_env(
            decisions["env_vars"],
            {
                "DATABASE_URL": "postgresql+asyncpg://user:password@localhost:5432/dbname",
            },
        )
        decisions["use_postgres"] = True
    else:
        _merge_env(
            decisions["env_vars"],
            {"DATABASE_URL": "sqlite+aiosqlite:///./dev.db"},
        )
        decisions["use_postgres"] = False


PROFILE_APPLIERS: dict[str, Any] = {
    "web_frontend": apply_web_frontend_decisions,
    "mobile": apply_mobile_decisions,
    "workers": apply_workers_decisions,
    "ai_rag": apply_ai_rag_decisions,
    "multi_tenancy": apply_multi_tenancy_decisions,
    "websocket": apply_websocket_decisions,
    "scheduled_jobs": apply_scheduled_jobs_decisions,
    "file_storage": apply_file_storage_decisions,
    "email_notifications": apply_email_notifications_decisions,
    "search": apply_search_decisions,
    "billing": apply_billing_decisions,
    "analytics": apply_analytics_decisions,
}


def _build_queue_seed_rows(
    queue_items: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """Map §12 rows to queue.csv schema dicts."""
    out: list[dict[str, Any]] = []
    for i, item in enumerate(queue_items, start=1):
        qid = f"IDEA-{i:03d}"
        out.append(
            {
                "id": qid,
                "batch": "1",
                "phase": item.get("priority", "1") or "1",
                "category": item.get("category", "init") or "init",
                "summary": item["summary"],
                "dependencies": "",
                "notes": "seeded from idea.md §12 via init-manifest",
                "created_date": datetime.now(tz=UTC).date().isoformat(),
            }
        )
    return out


def build_manifest(
    text: str, idea_path: Path
) -> tuple[dict[str, Any] | None, list[str]]:
    errors: list[str] = []
    meta = _parse_init_meta(text)
    if not meta:
        errors.append("INIT_META block is missing (expected <!-- INIT_META ... -->).")

    init_meta_errors: list[str] = []
    if meta:
        init_meta_errors.extend(_check_version_compat(meta))

    init_val = meta.get("initialized", "false") if meta else None
    if init_val is not None and str(init_val).lower() not in ("false", "no", "0"):
        init_meta_errors.append(
            "INIT_META initialized is not false — set initialized: false to parse a new manifest."
        )

    identity = _parse_identity(text)
    for field in ("project_name", "display_name", "one_line_pitch", "repository_slug"):
        if not identity.get(field) or "<!--" in identity.get(field, ""):
            errors.append(f"§1 {field.replace('_', ' ')} is missing or placeholder.")

    errors.extend(_placeholder_in_required_sections(text))

    archetype_key, selected = _parse_archetype(text)
    if len(selected) != 1:
        errors.append(
            f"§3 Archetype: require exactly one row with [x] in Select column; found {len(selected)}."
        )
    if archetype_key is None and len(selected) == 1:
        errors.append(
            "§3 Archetype: could not map selected row to a known archetype key."
        )

    profile_states, profile_parse_errs = _parse_profiles(text)
    errors.extend(profile_parse_errs)

    contexts, ctx_errs = _parse_bounded_contexts(text)
    errors.extend(ctx_errs)
    if not contexts:
        errors.append(
            "§4.2 Bounded contexts: at least one non-placeholder row is required."
        )

    queue_items = _parse_queue_section_12(text)
    if not queue_items:
        errors.append(
            "§12 Initial queue items: at least one non-placeholder row is required."
        )

    primary_db = _parse_primary_db(text)
    if primary_db not in ("postgresql", "sqlite"):
        errors.append(
            "§7 Primary database: specify PostgreSQL or SQLite in the table cell (required)."
        )

    open_q = _parse_open_questions(text)

    if errors or init_meta_errors:
        errors = init_meta_errors + errors
        return None, errors

    assert archetype_key is not None
    assert primary_db is not None

    enabled_map, source_map, arche_resolved = _resolve_profile_states(
        archetype_key, profile_states
    )

    # Profile constraint validation (requires/conflicts)
    constraint_errors = _validate_profile_constraints(enabled_map)
    if constraint_errors:
        errors.extend(constraint_errors)
        return None, errors

    decisions = _empty_resolved_decisions()
    decisions["archetype_resolved_fields"] = arche_resolved
    decisions["open_questions"] = open_q

    profiles_enabled: list[str] = []
    profiles_discarded: list[str] = []
    for key, script_stem in PROFILE_ROW_KEYS:
        if enabled_map.get(key):
            profiles_enabled.append(script_stem)
        else:
            profiles_discarded.append(script_stem)

    decisions["profiles_enabled"] = profiles_enabled
    decisions["profiles_discarded"] = profiles_discarded

    for key, enabled in enabled_map.items():
        if enabled and key in PROFILE_APPLIERS:
            PROFILE_APPLIERS[key]({}, decisions)

    apply_primary_db_decisions(primary_db == "postgresql", decisions)

    # Resolve module placement: skip scaffolding into apps/api/src/ when a profile
    # already creates packages/<name>/ for the same bounded context
    contexts_with_placement = _resolve_module_placement(contexts, profiles_enabled)
    mod_names = [
        c["name"].strip().lower().replace(" ", "_")
        for c in contexts_with_placement
        if c.get("module_placement") == "api_module"
    ]
    decisions["modules_to_scaffold"] = [m for m in mod_names if m]

    # Build queue rows then infer dependency edges from domain relationships
    raw_queue_rows = _build_queue_seed_rows(queue_items)
    decisions["queue_seed_rows"] = _infer_queue_dependencies(raw_queue_rows, contexts)

    profile_details: list[dict[str, Any]] = []
    for key, script_stem in PROFILE_ROW_KEYS:
        en = enabled_map.get(key, False)
        profile_details.append(
            {
                "profile_key": key,
                "script": script_stem,
                "enabled": en,
                "source": source_map.get(key, "explicit"),
            }
        )

    manifest: dict[str, Any] = {
        "meta": {
            "init_version": meta.get("init_version", "2.0") if meta else "2.0",
            "idea_path": str(idea_path),
            "parsed_at": datetime.now(tz=UTC).isoformat(),
            "initialized": False,
            "init_manifest_hash": None,
        },
        "project": {
            "project_name": identity["project_name"],
            "display_name": identity["display_name"],
            "one_line_pitch": identity["one_line_pitch"],
            "repository_slug": identity["repository_slug"],
        },
        "archetype": archetype_key,
        "primary_database": primary_db,
        "profiles": profile_details,
        "bounded_contexts": contexts_with_placement,
        "resolved_decisions": decisions,
    }

    meta_without_hash = dict(manifest["meta"])
    meta_without_hash.pop("init_manifest_hash", None)
    manifest_for_hash = {**manifest, "meta": meta_without_hash}
    raw = json.dumps(manifest_for_hash, sort_keys=True, ensure_ascii=False).encode()
    manifest["meta"]["init_manifest_hash"] = hashlib.sha256(raw).hexdigest()
    return manifest, []


def print_summary(manifest: dict[str, Any]) -> None:
    rd = manifest["resolved_decisions"]
    print("--- Resolved decisions summary ---")
    print(f"Archetype: {manifest['archetype']}")
    print(f"Primary DB: {manifest['primary_database']}")
    print(f"Profiles enabled (scripts): {', '.join(rd['profiles_enabled'])}")
    print(f"Profiles discarded: {', '.join(rd['profiles_discarded'])}")
    print(f"Compose services: {', '.join(rd['compose_services'])}")
    print(f"Python dependencies: {', '.join(rd['python_dependencies'])}")
    print(f"Env vars (keys): {', '.join(sorted(rd['env_vars']))}")
    print(f"Modules to scaffold: {', '.join(rd['modules_to_scaffold'])}")
    print(f"Queue rows to seed: {len(rd['queue_seed_rows'])}")
    print(f"CI additions: {', '.join(rd['ci_additions'])}")
    if rd.get("archetype_resolved_fields"):
        print(
            "Resolved by archetype defaults: "
            + ", ".join(rd["archetype_resolved_fields"])
        )
    if rd.get("open_questions"):
        print(f"Open questions (non-blocking): {len(rd['open_questions'])}")
    print("--- End summary ---")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Parse idea.md into init-manifest.json"
    )
    parser.add_argument("--idea", type=Path, default=Path("idea.md"))
    parser.add_argument("--out", type=Path, default=Path("init-manifest.json"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = Path.cwd()
    idea_path = args.idea if args.idea.is_absolute() else root / args.idea
    if not idea_path.is_file():
        print(f"ERROR: idea file not found: {idea_path}", file=sys.stderr)
        return 1
    text = idea_path.read_text(encoding="utf-8")
    manifest, errors = build_manifest(text, idea_path)
    if errors:
        print("Validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        return 1
    assert manifest is not None
    print_summary(manifest)
    out_path = args.out if args.out.is_absolute() else root / args.out
    serialized = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    if args.dry_run:
        print(serialized)
    else:
        out_path.write_text(serialized, encoding="utf-8")
        print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
