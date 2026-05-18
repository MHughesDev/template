<!-- README.md -->

# 🏗️ The Software Factory: Your AI-First Launchpad 🚀

Welcome to the **Software Factory**. This isn't just a repository; it's a high-performance engine designed to turn your wildest ideas into production-ready reality at terminal velocity. ⚡

If you've ever felt the pain of "re-litigating" the same setup decisions for the 100th time, or watched your AI agents get lost in a "what file should I touch?" loop—**this is your cure.** 💊

---

## 🌟 At a Glance (The "Easy Read")

The Software Factory is a **production-ready full-stack baseline** paired with a sophisticated **Agent Operating System**. We've automated the boring stuff so you (and your AI agents) can focus on building the future.

- **🤖 Agent-First:** Built from the ground up for Cursor and other AI coding agents.
- **🏭 Factory Precision:** Every workflow is a documented, reusable machine procedure.
- **📦 Full-Stack Power:** A modern, type-safe stack that scales from MVP to Enterprise.
- **🚦 Queue-Driven:** Decompose complex tasks into auditable, parallel-ready work items.

---

## 🛠️ The Engine Room (Our Tech Stack)

We don't just use tools; we use the *right* tools. The Software Factory is powered by a curated selection of modern technologies that play nice together.

### 🎨 The Face (Frontend)
A sleek, reactive, and lightning-fast user experience.
*   **React 19** (The bleeding edge of UI)
*   **Vite** (For that instant-refresh dev speed)
*   **TanStack** (Router & Query for state management perfection)
*   **Tailwind CSS v4** (Utility-first styling at its finest)
*   **shadcn/ui** (Beautiful, accessible components)

### 🧠 The Brain (Backend)
A robust, type-safe, and highly performant API layer.
*   **FastAPI** (Python 3.12+ speed and elegance)
*   **SQLModel** (The best of SQLAlchemy + Pydantic)
*   **Postgres 18** (The gold standard for data integrity)
*   **Alembic** (Smooth, versioned migrations)
*   **JWT Auth** (Secure, stateless authentication)

### 📱 The Reach (Mobile)
Native performance with a single codebase.
*   **Flutter** (Beautiful, high-performance mobile apps for iOS and Android)

---

## 🧬 Why a "Software Factory"?

In a traditional setup, you're a craftsman. You hand-forge every screw. In the **Software Factory**, you're the architect of an automated assembly line. 🛠️

We treat **recurring workflows** as **machine procedures**.
1.  **Skills & Prompts:** Instead of explaining things repeatedly, we encode knowledge into reusable `skills/` and `prompts/`.
2.  **The Queue:** Work isn't a messy todo list; it's a structured `queue/` that agents can execute with surgical precision.
3.  **Governance:** Built-in validations and self-audit checks ensure that as the factory runs faster, it doesn't break things.

---

## 🚀 Getting Started (The Fast Path)

Ready to fire up the assembly line? Follow these steps to get your first product moving.

### 1️⃣ The Blueprint
Fill out `IDEA.md`. This is your product contract. Don't skip it—it's the DNA of your project.

### 2️⃣ The Ignition
Ask your AI agent to run the initialization skill:
```text
"Hey agent, run skills/init/repo_initialize.md based on my IDEA.md"
```
This will generate your spec, design docs, and seed your initial MVP queue. **No code is written yet—just the perfect plan.** 📝

### 3️⃣ The Execution
Start knocking out queue items from `queue/queue.csv`. Each row is a bite-sized, context-rich task that your agents can handle while you sip your coffee. ☕

---

## 🔧 Operational Commands

The Factory comes with a powerful `Makefile` to keep things running smoothly.

| Command | What it does |
| :--- | :--- |
| `make dev` | Fire up the local dev environment (API + Web) |
| `make docker-up` | Spin up the full stack (DB, Adminer, Backend, Frontend) |
| `make lint` | Keep the code clean and shiny ✨ |
| `make test` | Run the full suite of backend tests |
| `make queue:top-item` | See what's next on the assembly line |
| `make audit:self` | Run a comprehensive health check on the repo |

---

## 🚦 Required Flow for Agents

If you are an AI agent operating in this factory, you have a contract to follow (see `AGENTS.md` for the full legal text):

1.  **Read this README** (You're doing it! Good job! 🤖)
2.  **Read AGENTS.md** (The authoritative policy).
3.  **Search for Skills** (`make skills:list`). Never guess when a procedure exists.
4.  **Follow the Queue** (`queue/QUEUE_INSTRUCTIONS.md`).

---

## 📜 License & Contribution

The Software Factory is open-source under the **MIT License**. We love contributions! Just keep them small, logical, and well-documented.

---

**Now go build something incredible. The factory is waiting.** 🏭💨
