import { useState, useEffect } from "react";
import { api } from "../api";

interface GameListProps {
  onSelectGame: (id: string) => void;
}

interface GameMeta {
  id: string;
  mode: string;
  result: string;
  created_at: string;
}

export function GameList({ onSelectGame }: GameListProps) {
  const [games, setGames] = useState<GameMeta[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .listGames()
      .then(({ games: g, total: t }) => {
        setGames(g);
        setTotal(t);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div style={{ padding: "2rem" }}>Loading saved games...</div>;

  if (games.length === 0) {
    return (
      <div style={{ padding: "2rem", textAlign: "center" }}>
        <p>No saved games yet. Finish a game to see it here.</p>
      </div>
    );
  }

  return (
    <div>
      <h2>Saved Games ({total})</h2>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {games.map((g) => (
          <li
            key={g.id}
            style={{
              padding: "0.5rem",
              marginBottom: "0.25rem",
              background: "#eee",
              borderRadius: 4,
              cursor: "pointer",
            }}
            onClick={() => onSelectGame(g.id)}
          >
            <span style={{ fontFamily: "monospace", fontSize: "0.85rem" }}>{g.id.slice(0, 8)}...</span>
            {" — "}
            {g.result}
            {" — "}
            {g.created_at ? new Date(g.created_at).toLocaleString() : ""}
          </li>
        ))}
      </ul>
      <p style={{ fontSize: "0.85rem", color: "#666" }}>
        Click a game to replay.
      </p>
    </div>
  );
}
