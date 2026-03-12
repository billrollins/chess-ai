import os
import sqlite3
from pathlib import Path
from datetime import datetime
from chess.pgn import StringExporter


class GameStorage:
    """Stores games as PGN files and metadata in SQLite."""

    def __init__(self, games_dir: str = "games", db_path: str = "chess.db"):
        self.games_dir = Path(games_dir)
        self.games_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS games (
                id TEXT PRIMARY KEY,
                mode TEXT NOT NULL,
                white_player TEXT DEFAULT 'human',
                black_player TEXT DEFAULT 'human',
                result TEXT,
                pgn_path TEXT,
                created_at TEXT
            )
        """)
        conn.commit()
        conn.close()

    def save_game(
        self,
        game_id: str,
        mode: str,
        white_player: str,
        black_player: str,
        result: str | None,
        pgn_content: str,
    ) -> str:
        """Save game to PGN file and DB. Returns path to PGN."""
        today = datetime.utcnow().strftime("%Y-%m-%d")
        day_dir = self.games_dir / today
        day_dir.mkdir(parents=True, exist_ok=True)
        pgn_path = day_dir / f"{game_id}.pgn"
        pgn_path.write_text(pgn_content, encoding="utf-8")

        rel_path = str(pgn_path.relative_to(self.games_dir))
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """
            INSERT OR REPLACE INTO games (id, mode, white_player, black_player, result, pgn_path, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (game_id, mode, white_player, black_player, result or "*", rel_path, datetime.utcnow().isoformat()),
        )
        conn.commit()
        conn.close()
        return str(pgn_path)

    def get_game_metadata(self, game_id: str) -> dict | None:
        conn = sqlite3.connect(self.db_path)
        row = conn.execute(
            "SELECT id, mode, white_player, black_player, result, pgn_path, created_at FROM games WHERE id = ?",
            (game_id,),
        ).fetchone()
        conn.close()
        if not row:
            return None
        return {
            "id": row[0],
            "mode": row[1],
            "white_player": row[2],
            "black_player": row[3],
            "result": row[4],
            "pgn_path": row[5],
            "created_at": row[6],
        }

    def get_pgn_content(self, game_id: str) -> str | None:
        meta = self.get_game_metadata(game_id)
        if not meta or not meta.get("pgn_path"):
            return None
        full_path = self.games_dir / meta["pgn_path"]
        if not full_path.exists():
            return None
        return full_path.read_text(encoding="utf-8")

    def list_games(self, limit: int = 50, offset: int = 0) -> list[dict]:
        conn = sqlite3.connect(self.db_path)
        rows = conn.execute(
            "SELECT id, mode, white_player, black_player, result, pgn_path, created_at FROM games ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (limit, offset),
        ).fetchall()
        conn.close()
        return [
            {
                "id": r[0],
                "mode": r[1],
                "white_player": r[2],
                "black_player": r[3],
                "result": r[4],
                "pgn_path": r[5],
                "created_at": r[6],
            }
            for r in rows
        ]

    def count_games(self) -> int:
        conn = sqlite3.connect(self.db_path)
        count = conn.execute("SELECT COUNT(*) FROM games").fetchone()[0]
        conn.close()
        return count
