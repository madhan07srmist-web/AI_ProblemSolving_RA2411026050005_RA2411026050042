# AI Projects Repository

This repository contains two Python projects that demonstrate game-tree search and decision-making techniques using Minimax and Alpha-Beta Pruning.

## 1. Tic-Tac-Toe AI (tictactoe.py)

### Problem Description
This project builds an AI opponent for the classic Tic-Tac-Toe game.  
The goal is to choose the optimal move at every turn so the AI never loses against a rational player.

### Algorithm Used
The AI uses Minimax to evaluate all possible future game states and select the move with the best guaranteed outcome.  
Alpha-Beta Pruning is used as an optimization to skip branches that cannot improve the final decision, reducing search time.

### How to Run
```bash
python app.py
```

### Sample Output
```text
Current board:
X | O | X
---------
O | X |  
---------
  |   | O

AI is thinking using Alpha-Beta Pruning...
Best move selected: position 7
Result: Draw
```

## 2. Smart Job Scheduling (job_scheduler.py)

### Problem Description
This project models job scheduling as a sequential decision-making problem.  
The objective is to choose the best next job based on priority, deadline, and expected utility to maximize overall scheduling quality.

### Algorithm Used
The scheduler uses Minimax-style decision making to evaluate possible scheduling choices and their future impact.  
At each step, it scores candidate decisions and selects the option with the best worst-case outcome.

### How to Run
```bash
python app.py
```

### Sample Output
```text
Jobs loaded: 5
Evaluating best schedule...
Selected order: J3 -> J1 -> J4 -> J2 -> J5
Total utility score: 87
Late jobs: 1
```

## Notes
- Python 3.x is required.
- Keep both scripts in the repository root or update command paths accordingly.
