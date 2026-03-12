const API_BASE = "/api";

export interface GameState {
  id: string;
  mode: string;
  fen: string;
  turn: string;
  result: string | null;
  moves: string[];
  white_player: string;
  black_player: string;
}

export const api = {
  async createGame(mode: string = "2player", aiId: string = "random"): Promise<GameState> {
    const res = await fetch(`${API_BASE}/games`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mode, ai_id: aiId }),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getGame(gameId: string): Promise<GameState> {
    const res = await fetch(`${API_BASE}/games/${gameId}`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async makeMove(
    gameId: string,
    fromSquare: string,
    toSquare: string,
    promotion?: string
  ): Promise<GameState> {
    const res = await fetch(`${API_BASE}/games/${gameId}/move`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ from_square: fromSquare, to_square: toSquare, promotion }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || "Move failed");
    }
    return res.json();
  },

  async listGames(): Promise<{ games: Array<{ id: string; mode: string; result: string; created_at: string }>; total: number }> {
    const res = await fetch(`${API_BASE}/games`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async getAIMove(gameId: string, auto: boolean = false): Promise<GameState> {
    const res = await fetch(`${API_BASE}/games/${gameId}/ai-move?auto=${auto}&delay_ms=500`, {
      method: "POST",
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || "AI move failed");
    }
    return res.json();
  },

  async getReplay(gameId: string): Promise<{ metadata: Record<string, unknown>; pgn: string }> {
    const res = await fetch(`${API_BASE}/games/${gameId}/replay`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
};
