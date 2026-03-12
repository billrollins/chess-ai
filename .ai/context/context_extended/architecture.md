# Architecture

## Overview

- **Server:** Single source of truth. GameManager holds in-memory games.
- **Client:** React state mirrors server. No Redux. Sync via REST request/response.
- **No WebSockets.** All communication is REST.

## Data Flow

1. **Create game:** POST /api/games → GameManager.create_game → returns state
2. **Human move:** POST /api/games/{id}/move → GameManager.make_move → validate, push, return state
3. **AI move:** POST /api/games/{id}/ai-move → GameManager.make_ai_move → await player.get_move → push, return state
4. **Game end:** Routes call _save_game_to_storage → PGN file + SQLite row

## State Sync

- Client fetches game on load and after each move/AI response
- No polling. No WebSocket. Each action is request → response → setState

## Concurrency

- GameManager is a singleton. No locking.
- AI moves are async but run in request handler; no background tasks
- No Celery, Redis, or task queue
