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

---

## .ai Folder Guide

The `.ai/` folder holds all context, plans, and protocols for AI-assisted development. Structure:

```
.ai/
  context/
    context_base.md            <-- you are here
    context_extended/          <-- detailed docs by topic
  plans/
    _index.md                  <-- current focus and plan list
    plan_*.md                  <-- one file per plan
  protocols/                   <-- prompt files for routine tasks
  versions/                    <-- version tracking and change log
```

### Reading Protocol

1. **Always start here** (`context_base.md`) for project overview and folder orientation.
2. **For a specific task**, read the relevant extended context file(s) from the table below.
3. **For planned work**, check `plans/_index.md` for current focus, then the referenced plan file.
4. **For routine tasks** (commit, review, context refresh), read the relevant protocol in `protocols/`.

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

Prompt files for routine tasks. Feed the file contents to the AI to execute:

- **`review_code.txt`** — Review code for correctness, consistency, security.
- **`update_context.txt`** — Refresh `.ai/context/` to match current codebase.
- **`commit.txt`** — Run git add, commit using message from `versions/commit message.txt`.

### Versions

- **`.version`** — Current version string (e.g. 0.1.0).
- **`change_log.md`** — Manual log of notable changes.
- **`commit message.txt`** — Default commit message for the commit protocol.

---

## Maintenance

- After major feature changes: update relevant `context_extended/` files.
- After refactors: run `protocols/update_context.txt` or manually refresh.
- Before large tasks: read this file + relevant extended context files.
