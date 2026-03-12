# Chess AI — Base Context

This is the single entry point for AI-assisted development on this project. Read this file first; drill into extended context files only as needed for the task at hand.

## Project Overview

Chess platform with 2-player hot-seat, 1vAI, 2AI modes. Custom AI players (Random, Greedy). Game storage as PGN + SQLite. Replay viewer. Built for future trainable AI and tournaments.

## Tech Stack

- **Backend:** FastAPI, python-chess, SQLite
- **Frontend:** React 18, TypeScript, Vite, react-chessboard, chess.js
- **Ports:** Backend 8001, Frontend 5174

## Key Paths

| Area | Path |
|------|------|
| Game logic | `backend/app/game/manager.py` |
| API routes | `backend/app/api/routes.py` |
| AI players | `backend/app/players/` |
| Storage | `backend/app/storage/game_storage.py` |
| Frontend app | `frontend/src/App.tsx` |
| Chess board | `frontend/src/components/ChessBoard.tsx` |
| API client | `frontend/src/api.ts` |

## Run

- `PlayChess.bat` — starts both servers, opens browser
- Or: `scripts/_start_backend.bat`, `scripts/_start_vite.bat`

## Version & Changelog

- `VERSION` — current version string (project root)
- `CHANGELOG.md` — rolling changelog with `[Unreleased]` section (project root)

---

## .ai Folder Guide

The `.ai/` folder holds context, plans, and protocols for AI-assisted development.

```
.ai/
  context/
    context_base.md            <-- you are here
    .last_update               <-- git hash of last context sync
    context_extended/          <-- detailed docs by topic
  plans/
    _index.md                  <-- current focus and plan list
    plan_*.md                  <-- one file per plan
  protocols/                   <-- prompt files for routine tasks
```

### Reading Protocol

1. **Always start here** (`context_base.md`) for project overview and folder orientation.
2. **For a specific task**, read the relevant extended context file(s) from the table below.
3. **For planned work**, check `plans/_index.md` for current focus, then the referenced plan file.
4. **For routine tasks** (review, version bump, session start), read the relevant protocol in `protocols/`.

### Extended Context

Detailed docs split by topic under `context_extended/`:

| File | Contents |
|------|----------|
| [architecture.md](context_extended/architecture.md) | High-level architecture, data flow, state management |
| [game_engine.md](context_extended/game_engine.md) | GameManager, game lifecycle, modes |
| [api_routes.md](context_extended/api_routes.md) | REST endpoints, request/response shapes |
| [ai_players.md](context_extended/ai_players.md) | Player abstraction, registry, RandomAI, GreedyAI |
| [frontend.md](context_extended/frontend.md) | React structure, ChessBoard, mode selection |
| [storage.md](context_extended/storage.md) | PGN files, SQLite schema, replay |
| [scripts_tooling.md](context_extended/scripts_tooling.md) | PlayChess.bat, kill_servers, dev workflow |

Context describes **current state** of the code. For future work, see plans.

### Plans

Backlog and future work live in `plans/`. Separate from context (which describes how things work now).

- **`_index.md`** — Overview of all plans, current focus, next actions.
- **`plan_*.md`** — One file per plan. Each has steps with status and handoff notes.

**Step statuses:** done, in progress, on deck, backlog.

**Workflow:**
1. Pick a plan and steps from `_index.md`
2. Read relevant context; implement
3. Verify, commit, push
4. Update plan status; move to next steps
5. Repeat

### Protocols

Prompt files for AI-assisted routine tasks. Feed the file contents to the AI to execute:

- **`start_session.md`** — Cold-start orientation: read context, check plans, load relevant docs.
- **`review_and_update.md`** — Review changed code + update context docs. Uses `.last_update` git hash to diff only what changed since last sync.
- **`version_bump.md`** — Evaluate `[Unreleased]` changelog entries and bump `VERSION` (patch/minor/major).

### Scripts

Git and server management in `scripts/`:

- **`commit.bat`** — Reads `commit_message.txt`, runs git add + commit, resets message to placeholder.
- **`commit_message.txt`** — Write your commit message here before running `commit.bat`. Placeholder: `---`.
- **`kill_servers.bat`** — Kills backend (8001) and frontend (5174) processes.
- **`_start_backend.bat`** — Activates venv, starts uvicorn on 8001.
- **`_start_vite.bat`** — Starts Vite dev server on 5174.

---

## Maintenance

- After feature work: run `protocols/review_and_update.md` to review code and sync context.
- Every ~3 sessions: run `protocols/version_bump.md` to evaluate a version bump.
- Before large tasks: read this file + relevant extended context files.
- To commit: write message to `scripts/commit_message.txt`, then run `scripts/commit.bat`.
