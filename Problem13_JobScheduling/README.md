# Smart Job Scheduling Decision System

A web-based interactive system that demonstrates intelligent job scheduling through a two-player game between humans and AI. The system uses algorithmic decision-making to optimize job selections and scoring.

##  Features

- **Interactive Web Interface**: Clean, user-friendly UI for job scheduling decisions
- **AI Decision Making**: Advanced algorithm for optimal job selection
- **Real-Time Scoring**: Live score calculation and comparison
- **Game State Management**: Track game progress, decisions, and outcomes
- **Responsive Design**: Works on desktop and tablet devices

##  Project Structure

```
Smart Job Scheduling Decision System/
├── app.py              # Flask backend application
├── templates/
│   └── index.html      # Web interface
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore file
└── README.md          # This file
```

##  Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/Smart-Job-Scheduling-Decision-System.git
   cd Smart-Job-Scheduling-Decision-System
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**
   
   On Windows:
   ```bash
   .venv\Scripts\activate
   ```
   
   On macOS/Linux:
   ```bash
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

##  Usage

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Open in browser**
   Navigate to `http://localhost:5000` in your web browser

3. **Play the game**
   - The system will present a list of jobs to schedule
   - Make strategic decisions to maximize your score
   - Compete against the AI's optimal strategy
   - View the results and learn from the decisions

## 🔧 How It Works

### Backend (app.py)
- Built with **Flask** web framework
- Implements game state management
- Uses dynamic programming algorithm for AI decision-making
- Provides REST API endpoints for game operations

### Frontend (index.html)
- Interactive user interface
- Real-time game board display
- Score tracking and comparison
- Move history and game log

##  Dependencies

The project uses the following Python packages:
- **Flask**: Web framework for building the application
- **Werkzeug**: WSGI utilities (installed with Flask)

See `requirements.txt` for the complete list.

##  Game Rules

1. Players take turns selecting jobs from the available list
2. Each job has an associated value/score
3. Selected jobs are removed from the pool
4. The game continues until all jobs are scheduled
5. Final score is calculated based on selected jobs
6. AI uses optimal strategy to maximize its advantage

##  Troubleshooting

**Port already in use?**
```bash
python app.py --port 8080
```

**Virtual environment not activating?**
- Make sure you're in the project directory
- Try using the full path: `.venv\Scripts\activate.bat`

**Module not found?**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

##  Notes for Beginners

- Always use a virtual environment to avoid Python package conflicts
- The `.venv/` folder is ignored by Git (see `.gitignore`)
- `requirements.txt` helps others reproduce your environment
- The `__pycache__/` folder is auto-generated and ignored

##  Contributing

Feel free to fork this project and submit pull requests for improvements!

##  License

This project is open source and available under the MIT License.

## ✨ Author

Created as an educational project for demonstrating AI decision-making and job scheduling algorithms.

---
