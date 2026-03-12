# Frontend

## Stack

- React 18, TypeScript, Vite
- react-chessboard (drag-drop board)
- chess.js (ReplayView PGN parsing)

## Structure

- `App.tsx` — mode selector (2player, 1vai, 2ai), AI selector (random, greedy), ChessBoard, GameList, ReplayView
- `ChessBoard.tsx` — board, move handling, AI turn detection, calls getAIMove when AI's turn
- `GameList.tsx` — list saved games
- `ReplayView.tsx` — step through saved game moves
- `api.ts` — fetch wrappers for all endpoints

## AI Turn Flow

- ChessBoard checks `isAITurn(game)` via white_player/black_player
- useEffect: when AI turn, call api.getAIMove(gameId, false)
- Disable drag when AI turn; show "AI thinking..."
- For 2AI: 400ms delay between moves for watchability
