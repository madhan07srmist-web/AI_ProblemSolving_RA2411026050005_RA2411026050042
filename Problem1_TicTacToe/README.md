# Tic Tac Toe (Flask)

A web-based Tic Tac Toe game where you play as **X** against an AI opponent (**O**).

The AI supports:
- Minimax
- Alpha-Beta Pruning

## Features

- Interactive browser UI
- Backend move validation and game-state checks
- AI decision making with algorithm statistics (nodes explored and response time)

## Project Structure

- `app.py` - Flask backend and AI logic
- `templates/index.html` - Frontend UI

## Requirements

- Python 3.10+
- pip

## Setup and Run

1. Open a terminal in this folder.
2. (Optional) Create and activate a virtual environment:

   **Windows (PowerShell):**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the app:

   ```bash
   python app.py
   ```

5. Open your browser at:

   `http://127.0.0.1:5000`

## API

### POST /move

Request JSON:

```json
{
  "board": ["", "", "", "", "", "", "", "", ""],
  "index": 0,
  "algorithm": "minimax"
}
```

- `board`: List of 9 cells, each one of `""`, `"X"`, `"O"`
- `index`: Player move index (0-8)
- `algorithm`: `"minimax"` or `"alphabeta"`

## Notes

- The app runs with Flask debug mode enabled in `app.py`.
- For production, use a production WSGI server and disable debug mode.
