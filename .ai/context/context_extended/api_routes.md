# API Routes

All under `/api` prefix. REST only.

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | /games | Create game. Body: { mode, ai_id } |
| GET | /games/{id} | Get game state |
| POST | /games/{id}/move | Human move. Body: { from_square, to_square, promotion? } |
| POST | /games/{id}/ai-move | AI move(s). Query: auto, delay_ms |
| GET | /games | List saved games. Query: limit, offset |
| GET | /games/{id}/replay | Get PGN + metadata for replay |

## Game State Response

- id, mode, fen, turn, result, moves[], white_player, black_player

## Errors

- 404: Game not found
- 400: Illegal move, not your turn, not AI's turn
