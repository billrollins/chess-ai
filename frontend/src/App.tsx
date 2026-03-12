import { useState } from "react";
import { ChessBoard } from "./components/ChessBoard";
import { GameList } from "./components/GameList";
import { ReplayView } from "./components/ReplayView";
import { api } from "./api";

type View = "play" | "games" | "replay";
type GameMode = "2player" | "1vai" | "2ai";
type AiId = "random" | "greedy";

export default function App() {
  const [view, setView] = useState<View>("play");
  const [gameId, setGameId] = useState<string | null>(null);
  const [replayGameId, setReplayGameId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState<GameMode>("2player");
  const [aiId, setAiId] = useState<AiId>("greedy");

  const startNewGame = async () => {
    setLoading(true);
    try {
      const game = await api.createGame(mode, aiId);
      setGameId(game.id);
      setReplayGameId(null);
      setView("play");
    } finally {
      setLoading(false);
    }
  };

  const openGame = (id: string) => {
    setReplayGameId(id);
    setGameId(null);
    setView("replay");
  };

  return (
    <div style={{ padding: "1rem", maxWidth: 800, margin: "0 auto" }}>
      <header style={{ display: "flex", flexWrap: "wrap", gap: "1rem", marginBottom: "1rem", alignItems: "center" }}>
        <h1 style={{ margin: 0, fontSize: "1.5rem" }}>Chess AI</h1>
        <button onClick={() => { setView("play"); setReplayGameId(null); }} disabled={view === "play"}>
          Play
        </button>
        <button onClick={() => setView("games")} disabled={view === "games"}>
          Saved Games
        </button>
        <span style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
          <label>Mode:</label>
          <select value={mode} onChange={(e) => setMode(e.target.value as GameMode)}>
            <option value="2player">2-Player</option>
            <option value="1vai">1 vs AI</option>
            <option value="2ai">2 AI</option>
          </select>
        </span>
        {(mode === "1vai" || mode === "2ai") && (
          <span style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
            <label>AI:</label>
            <select value={aiId} onChange={(e) => setAiId(e.target.value as AiId)}>
              <option value="random">Random</option>
              <option value="greedy">Greedy</option>
            </select>
          </span>
        )}
        <button onClick={startNewGame} disabled={loading}>
          {loading ? "Loading..." : "New Game"}
        </button>
      </header>

      {view === "play" && (
        <ChessBoard
          gameId={gameId}
          mode={mode}
          onGameStart={startNewGame}
          onNoGame={() => setGameId(null)}
        />
      )}
      {view === "games" && <GameList onSelectGame={openGame} />}
      {view === "replay" && replayGameId && (
        <ReplayView gameId={replayGameId} onBack={() => setView("games")} />
      )}
    </div>
  );
}
