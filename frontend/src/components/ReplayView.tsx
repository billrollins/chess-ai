import { useState, useEffect } from "react";
import { Chessboard } from "react-chessboard";
import { Chess } from "chess.js";
import { api } from "../api";

interface ReplayViewProps {
  gameId: string;
  onBack: () => void;
}

export function ReplayView({ gameId, onBack }: ReplayViewProps) {
  const [pgn, setPgn] = useState<string | null>(null);
  const [metadata, setMetadata] = useState<Record<string, unknown> | null>(null);
  const [currentMoveIndex, setCurrentMoveIndex] = useState(-1);
  const [fen, setFen] = useState<string>("start");
  const [moves, setMoves] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .getReplay(gameId)
      .then(({ pgn: p, metadata: m }) => {
        setPgn(p);
        setMetadata(m);
        const chess = new Chess();
        const game = new Chess();
        try {
          game.loadPgn(p);
          const hist = game.history();
          setMoves(hist);
          if (hist.length === 0) {
            setFen(chess.fen());
          } else {
            setFen(game.fen());
            setCurrentMoveIndex(hist.length - 1);
          }
        } catch {
          setFen(chess.fen());
        }
      })
      .catch((e) => setError(e instanceof Error ? e.message : "Failed to load"))
      .finally(() => setLoading(false));
  }, [gameId]);

  const goToMove = (idx: number) => {
    if (idx < 0) {
      setFen(new Chess().fen());
      setCurrentMoveIndex(-1);
      return;
    }
    if (!pgn || moves.length === 0) return;
    const chess = new Chess();
    try {
      for (let i = 0; i <= idx && i < moves.length; i++) {
        chess.move(moves[i]);
      }
      setFen(chess.fen());
      setCurrentMoveIndex(idx);
    } catch {
      // ignore
    }
  };

  if (loading) return <div style={{ padding: "2rem" }}>Loading replay...</div>;
  if (error) return <div style={{ color: "#c00", padding: "2rem" }}>{error}</div>;

  return (
    <div>
      <div style={{ marginBottom: "0.5rem", display: "flex", alignItems: "center", gap: "1rem" }}>
        <button onClick={onBack}>Back to list</button>
        {metadata?.result != null && <span>Result: {String(metadata.result)}</span>}
      </div>
      <div style={{ marginBottom: "0.5rem", display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
        <button onClick={() => goToMove(-1)} disabled={currentMoveIndex < 0}>
          Start
        </button>
        <button
          onClick={() => goToMove(currentMoveIndex - 1)}
          disabled={currentMoveIndex < 0}
        >
          Prev
        </button>
        <button
          onClick={() => goToMove(currentMoveIndex + 1)}
          disabled={currentMoveIndex >= moves.length - 1}
        >
          Next
        </button>
        <button
          onClick={() => goToMove(moves.length - 1)}
          disabled={currentMoveIndex >= moves.length - 1 || moves.length === 0}
        >
          End
        </button>
        <span style={{ alignSelf: "center", fontSize: "0.9rem" }}>
          Move {currentMoveIndex + 1} / {moves.length || 1}
        </span>
      </div>
      <div style={{ maxWidth: 480, margin: "0 auto" }}>
        <Chessboard
          position={fen}
          boardOrientation="white"
          arePiecesDraggable={false}
          boardWidth={480}
        />
      </div>
      {moves.length > 0 && (
        <div style={{ marginTop: "1rem", fontSize: "0.9rem" }}>
          <strong>Moves:</strong>{" "}
          {moves.map((m, i) => (
            <button
              key={i}
              onClick={() => goToMove(i)}
              style={{
                margin: "0 0.25rem 0.25rem 0",
                padding: "0.2rem 0.4rem",
                background: i === currentMoveIndex ? "#ccc" : "#eee",
                border: "1px solid #999",
                borderRadius: 4,
                cursor: "pointer",
              }}
            >
              {m}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
