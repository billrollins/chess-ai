import { useState, useEffect, useCallback, useRef } from "react";
import { Chessboard } from "react-chessboard";
import { api, GameState } from "../api";

interface ChessBoardProps {
  gameId: string | null;
  mode: string;
  onGameStart: () => void;
  onNoGame: () => void;
}

function isAITurn(game: GameState): boolean {
  const currentPlayer = game.turn === "white" ? game.white_player : game.black_player;
  return currentPlayer !== "human";
}

export function ChessBoard({ gameId, onGameStart, onNoGame, mode }: ChessBoardProps) {
  const [game, setGame] = useState<GameState | null>(null);
  const [loading, setLoading] = useState(false);
  const [aiThinking, setAiThinking] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const aiRequestInFlight = useRef(false);

  const fetchGame = useCallback(async (id: string) => {
    setLoading(true);
    setError(null);
    try {
      const g = await api.getGame(id);
      setGame(g);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load game");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (gameId) {
      fetchGame(gameId);
    } else {
      setGame(null);
    }
  }, [gameId, fetchGame]);

  useEffect(() => {
    if (!gameId || !game || game.result || aiRequestInFlight.current) return;
    if (!isAITurn(game)) return;

    const runAIMove = () => {
      aiRequestInFlight.current = true;
      setAiThinking(true);
      setError(null);
      api
        .getAIMove(gameId!, false)
        .then((updated) => setGame(updated))
        .catch((e) => setError(e instanceof Error ? e.message : "AI move failed"))
        .finally(() => {
          setAiThinking(false);
          aiRequestInFlight.current = false;
        });
    };

    const delay = mode === "2ai" ? 400 : 0;
    const id = setTimeout(runAIMove, delay);
    return () => clearTimeout(id);
  }, [gameId, game?.fen, game?.moves?.length, mode]);

  const onDrop = (sourceSquare: string, targetSquare: string, piece: string) => {
    if (!gameId || !game || game.result || isAITurn(game)) return false;
    setError(null);
    const isPromotion = piece.toLowerCase() === "p" &&
      ((piece === "wP" && targetSquare[1] === "8") || (piece === "bP" && targetSquare[1] === "1"));
    const promotion = isPromotion ? "q" : undefined;
    api
      .makeMove(gameId, sourceSquare, targetSquare, promotion)
      .then((updated) => setGame(updated))
      .catch((e) => setError(e instanceof Error ? e.message : "Invalid move"));
    return false;
  };

  if (!gameId) {
    return (
      <div style={{ textAlign: "center", padding: "3rem" }}>
        <p>No active game. Select mode and click &quot;New Game&quot;.</p>
        <button onClick={onGameStart}>New Game</button>
      </div>
    );
  }

  if (loading && !game) {
    return <div style={{ padding: "2rem", textAlign: "center" }}>Loading...</div>;
  }

  if (error && !game) {
    return (
      <div style={{ padding: "2rem", textAlign: "center", color: "#c00" }}>
        <p>{error}</p>
        <button onClick={onNoGame}>Back</button>
      </div>
    );
  }

  if (!game) return null;

  const isGameOver = !!game.result && game.result !== "*";

  return (
    <div>
      {error && (
        <div style={{ color: "#c00", marginBottom: "0.5rem", fontSize: "0.9rem" }}>
          {error}
        </div>
      )}
      <div style={{ marginBottom: "0.5rem", fontSize: "0.9rem" }}>
        {isGameOver ? (
          <span>Game over: {game.result}</span>
        ) : aiThinking ? (
          <span>AI thinking...</span>
        ) : (
          <span>Turn: {game.turn === "white" ? "White" : "Black"}</span>
        )}
      </div>
      <div style={{ maxWidth: 480, margin: "0 auto" }}>
        <Chessboard
          position={game.fen}
          onPieceDrop={onDrop}
          boardOrientation="white"
          arePiecesDraggable={!isGameOver && !aiThinking && !isAITurn(game)}
          boardWidth={480}
        />
      </div>
      {isGameOver && (
        <div style={{ marginTop: "1rem", textAlign: "center" }}>
          <button onClick={onGameStart}>New Game</button>
        </div>
      )}
    </div>
  );
}
