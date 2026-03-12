# Scripts & Tooling

## PlayChess.bat

- Calls kill_servers, starts backend + frontend in new windows, opens browser
- Ports: 8001 (backend), 5174 (frontend)

## scripts/

- `kill_servers.bat` — kills processes on 8001, 5174 only (not dev.bat ports)
- `_start_backend.bat` — cd backend, venv activate, uvicorn
- `_start_vite.bat` — cd frontend, npm run dev

## engines/

- Empty. Planned for Stockfish (benchmarking only, not playable opponent)
