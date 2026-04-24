from __future__ import annotations

import math
import time
from typing import List, Optional, Tuple

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

WIN_LINES: Tuple[Tuple[int, int, int], ...] = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


def check_winner(board: List[str]) -> Optional[str]:
    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if all(cell != "" for cell in board):
        return "Draw"
    return None


def available_moves(board: List[str]) -> List[int]:
    return [i for i, cell in enumerate(board) if cell == ""]


def terminal_score(winner: Optional[str]) -> Optional[int]:
    if winner == "O":
        return 1
    if winner == "X":
        return -1
    if winner == "Draw":
        return 0
    return None


def minimax(board: List[str], is_maximizing: bool, node_counter: List[int]) -> Tuple[int, Optional[int]]:
    node_counter[0] += 1
    winner = check_winner(board)
    score = terminal_score(winner)
    if score is not None:
        return score, None

    if is_maximizing:
        best_score = -math.inf
        best_move: Optional[int] = None
        for move in available_moves(board):
            board[move] = "O"
            eval_score, _ = minimax(board, False, node_counter)
            board[move] = ""
            if eval_score > best_score:
                best_score = eval_score
                best_move = move
        return best_score, best_move

    best_score = math.inf
    best_move = None
    for move in available_moves(board):
        board[move] = "X"
        eval_score, _ = minimax(board, True, node_counter)
        board[move] = ""
        if eval_score < best_score:
            best_score = eval_score
            best_move = move
    return best_score, best_move


def alpha_beta(
    board: List[str],
    is_maximizing: bool,
    alpha: float,
    beta: float,
    node_counter: List[int],
) -> Tuple[int, Optional[int]]:
    node_counter[0] += 1
    winner = check_winner(board)
    score = terminal_score(winner)
    if score is not None:
        return score, None

    if is_maximizing:
        best_score = -math.inf
        best_move: Optional[int] = None
        for move in available_moves(board):
            board[move] = "O"
            eval_score, _ = alpha_beta(board, False, alpha, beta, node_counter)
            board[move] = ""
            if eval_score > best_score:
                best_score = eval_score
                best_move = move
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score, best_move

    best_score = math.inf
    best_move = None
    for move in available_moves(board):
        board[move] = "X"
        eval_score, _ = alpha_beta(board, True, alpha, beta, node_counter)
        board[move] = ""
        if eval_score < best_score:
            best_score = eval_score
            best_move = move
        beta = min(beta, best_score)
        if beta <= alpha:
            break
    return best_score, best_move


def choose_ai_move(board: List[str], algorithm: str) -> Tuple[Optional[int], dict]:
    selected = (algorithm or "").strip().lower()
    node_counter = [0]
    start = time.perf_counter()

    if selected == "alphabeta":
        _, move = alpha_beta(board, True, -math.inf, math.inf, node_counter)
        algorithm_name = "Alpha-Beta Pruning"
    else:
        _, move = minimax(board, True, node_counter)
        algorithm_name = "Minimax"

    elapsed_ms = (time.perf_counter() - start) * 1000

    return move, {
        "algorithm": algorithm_name,
        "nodes_explored": node_counter[0],
        "time_ms": round(elapsed_ms, 3),
    }


def outcome_message(outcome: Optional[str]) -> str:
    if outcome == "X":
        return "You win!"
    if outcome == "O":
        return "AI wins."
    if outcome == "Draw":
        return "It's a draw."
    return "Your turn (X)"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/move", methods=["POST"])
def move():
    data = request.get_json(silent=True) or {}
    board = data.get("board")
    index = data.get("index")
    algorithm = data.get("algorithm", "minimax")

    if not isinstance(board, list) or len(board) != 9:
        return jsonify({"error": "Invalid board state."}), 400

    normalized_board: List[str] = []
    for cell in board:
        if cell not in ("", "X", "O"):
            return jsonify({"error": "Invalid board symbols."}), 400
        normalized_board.append(cell)

    if not isinstance(index, int) or index < 0 or index > 8:
        return jsonify({"error": "Invalid move index."}), 400

    current_outcome = check_winner(normalized_board)
    if current_outcome is not None:
        return jsonify(
            {
                "board": normalized_board,
                "status": current_outcome,
                "message": outcome_message(current_outcome),
                "game_over": True,
                "ai": None,
            }
        )

    if normalized_board[index] != "":
        return jsonify({"error": "That cell is already occupied."}), 400

    normalized_board[index] = "X"
    after_user = check_winner(normalized_board)
    if after_user is not None:
        return jsonify(
            {
                "board": normalized_board,
                "status": after_user,
                "message": outcome_message(after_user),
                "game_over": True,
                "ai": None,
            }
        )

    ai_move, ai_stats = choose_ai_move(normalized_board, algorithm)
    if ai_move is not None:
        normalized_board[ai_move] = "O"

    after_ai = check_winner(normalized_board)
    status = after_ai if after_ai is not None else "ongoing"

    return jsonify(
        {
            "board": normalized_board,
            "status": status,
            "message": outcome_message(after_ai),
            "game_over": after_ai is not None,
            "ai": ai_stats,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
