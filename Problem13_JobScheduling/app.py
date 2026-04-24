from functools import lru_cache
from typing import Any

from flask import Flask, jsonify, render_template, request, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "smart-scheduling-secret-key"

DEFAULT_TASKS = [3, 7, 2, 9, 5]


def _parse_tasks(payload: Any) -> list[int]:
    """Parse and validate incoming task values from JSON payload."""
    tasks = payload.get("tasks") if isinstance(payload, dict) else None

    if tasks is None:
        return DEFAULT_TASKS.copy()

    if not isinstance(tasks, list) or len(tasks) == 0:
        raise ValueError("Tasks must be a non-empty list of integers.")

    parsed: list[int] = []
    for item in tasks:
        try:
            parsed.append(int(item))
        except (TypeError, ValueError) as exc:
            raise ValueError("All task values must be integers.") from exc

    return parsed


def _new_state(tasks: list[int]) -> dict[str, Any]:
    return {
        "initial_tasks": tasks.copy(),
        "remaining_tasks": tasks.copy(),
        "user_tasks": [],
        "ai_tasks": [],
        "user_score": 0,
        "ai_score": 0,
        "log": [],
        "turn": "user",
        "completed": False,
    }


@lru_cache(maxsize=None)
def _solve_state(remaining: tuple[int, ...], ai_turn: bool, diff: int) -> int:
    """Return optimal terminal score difference (AI - User) from this state."""
    if not remaining:
        return diff

    if ai_turn:
        best = -10**9
        for i, value in enumerate(remaining):
            nxt = remaining[:i] + remaining[i + 1 :]
            candidate = _solve_state(nxt, False, diff + value)
            if candidate > best:
                best = candidate
        return best

    best = 10**9
    for i, value in enumerate(remaining):
        nxt = remaining[:i] + remaining[i + 1 :]
        candidate = _solve_state(nxt, True, diff - value)
        if candidate < best:
            best = candidate
    return best


def _get_ai_choice(remaining: list[int], user_score: int, ai_score: int) -> int:
    """Choose the AI move that maximizes final outcome using Minimax."""
    rem = tuple(remaining)
    base_diff = ai_score - user_score
    best_index = 0
    best_eval = -10**9

    for i, value in enumerate(rem):
        nxt = rem[:i] + rem[i + 1 :]
        score = _solve_state(nxt, False, base_diff + value)

        # Deterministic tie-breakers: higher immediate value, then lower index.
        if (
            score > best_eval
            or (score == best_eval and value > rem[best_index])
            or (
                score == best_eval
                and value == rem[best_index]
                and i < best_index
            )
        ):
            best_eval = score
            best_index = i

    return best_index


def _state_response(state: dict[str, Any]) -> dict[str, Any]:
    if state["ai_score"] > state["user_score"]:
        outcome = "AI Scheduler has higher score"
    elif state["ai_score"] < state["user_score"]:
        outcome = "User has higher score"
    else:
        outcome = "Draw"

    return {
        "initial_tasks": state["initial_tasks"],
        "remaining_tasks": state["remaining_tasks"],
        "user_tasks": state["user_tasks"],
        "ai_tasks": state["ai_tasks"],
        "user_score": state["user_score"],
        "ai_score": state["ai_score"],
        "log": state["log"],
        "turn": state["turn"],
        "completed": state["completed"],
        "outcome": outcome,
    }


@app.route("/")
def index() -> str:
    if "game_state" not in session:
        session["game_state"] = _new_state(DEFAULT_TASKS)
    return render_template("index.html")


@app.get("/api/state")
def get_state():
    if "game_state" not in session:
        session["game_state"] = _new_state(DEFAULT_TASKS)
    return jsonify({"ok": True, "state": _state_response(session["game_state"])})


@app.post("/api/initialize")
def initialize():
    try:
        tasks = _parse_tasks(request.get_json(silent=True) or {})
    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400

    session["game_state"] = _new_state(tasks)
    return jsonify({"ok": True, "state": _state_response(session["game_state"])})


@app.post("/api/user-move")
def user_move():
    state = session.get("game_state")
    if not state:
        state = _new_state(DEFAULT_TASKS)

    if state["completed"]:
        return jsonify({"ok": False, "error": "All tasks are already claimed."}), 400

    if state["turn"] != "user":
        return jsonify({"ok": False, "error": "It is not the user turn."}), 400

    payload = request.get_json(silent=True) or {}
    index = payload.get("index")

    if not isinstance(index, int):
        return jsonify({"ok": False, "error": "A valid task index is required."}), 400

    remaining = state["remaining_tasks"]
    if index < 0 or index >= len(remaining):
        return jsonify({"ok": False, "error": "Task index out of range."}), 400

    user_pick = remaining.pop(index)
    state["user_tasks"].append(user_pick)
    state["user_score"] += user_pick

    ai_pick = None
    if remaining:
        ai_index = _get_ai_choice(remaining, state["user_score"], state["ai_score"])
        ai_pick = remaining.pop(ai_index)
        state["ai_tasks"].append(ai_pick)
        state["ai_score"] += ai_pick

    state["log"].append(
        {
            "round": len(state["log"]) + 1,
            "user_pick": user_pick,
            "ai_pick": ai_pick,
            "remaining_after_round": remaining.copy(),
        }
    )

    if not remaining:
        state["turn"] = "done"
        state["completed"] = True
    else:
        state["turn"] = "user"

    session["game_state"] = state
    return jsonify({"ok": True, "state": _state_response(state)})


if __name__ == "__main__":
    app.run(debug=True)
