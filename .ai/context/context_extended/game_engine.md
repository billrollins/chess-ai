# Game Engine

## GameManager (backend/app/game/manager.py)

- **Storage:** `_games: dict[game_id, {...}]` in memory
- **Per game:** id, mode, ai_id, board (python-chess Board), moves[], result, white_player, black_player

## Modes

- **2player:** white=human, black=human
- **1vai:** white=human, black=ai_id
- **2ai:** white=ai_id, black=ai_id

## Methods

- `create_game(mode, ai_id)` — new Board, store players, return state dict
- `get_game(game_id)` — return state or None
- `make_move(game_id, from_square, to_square, promotion)` — human move; validates turn, applies, returns state
- `make_ai_move(game_id, auto, delay_ms)` — async; gets AI via get_ai_player, await player.get_move(board), push; if auto, loops until human turn or game over

## Game End

- `board.is_game_over()` → set result (1-0, 0-1, 1/2-1/2)
- Routes call _save_game_to_storage on game end
