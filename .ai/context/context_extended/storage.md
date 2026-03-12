# Storage

## PGN

- Path: `games/YYYY-MM-DD/{game_id}.pgn`
- Written on game end by _save_game_to_storage
- gitignored (games/*)

## SQLite

- Path: `chess.db` (project root)
- Table: games (id, mode, white_player, black_player, result, pgn_path, created_at)
- GameStorage in backend/app/storage/game_storage.py

## Replay

- GET /games/{id}/replay returns metadata + PGN content
- ReplayView parses PGN with chess.js, steps through moves
