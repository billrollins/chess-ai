# Chess AI

A chess platform with 2-player hot-seat, game storage, and replay. Built for future AI integration and tournaments.

## Quick Start

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5174

## Features

- **2-player hot-seat** — Play on one device, take turns
- **Game storage** — Finished games saved as PGN + SQLite
- **Replay** — Step through saved games move by move

## Project Structure

```
chess-ai/
├── backend/          # FastAPI + python-chess
├── frontend/         # React + react-chessboard
├── games/            # PGN files (created on first save)
└── engines/          # Stockfish (Phase 2)
```

## API

- `POST /api/games` — Create game
- `GET /api/games/{id}` — Get game state
- `POST /api/games/{id}/move` — Make move
- `GET /api/games` — List saved games
- `GET /api/games/{id}/replay` — Get PGN for replay

## Next (Phase 2)

- Stockfish integration
- 1vAI and 2 AI modes
- `scripts/download_stockfish.py`
