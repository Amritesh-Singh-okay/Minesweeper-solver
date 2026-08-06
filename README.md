# Minesweeper Solver

A Python bot that plays Google Minesweeper automatically. It reads the board using OpenCV, deduces safe cells and mines using a 3-tier algorithm (basic constraints, subset subtraction, and probabilistic estimation), and clicks them using PyAutoGUI.

![Minesweeper Solver Demo](Demo.gif)

> **Note:** Currently Windows-only (uses `ctypes` for global hotkeys and `winsound` for audio feedback).

## Features

- **3-tier solver engine** — Basic constraints, subset subtraction logic, and probabilistic mine estimation
- **Difficulty selector** — Easy (10x8), Medium (18x14), Expert (24x20)
- **Screen calibration** — hover over two corners and press Spacebar to map the board region on any monitor
- **Emergency stop** — hold `ESC` at any time to halt the bot
- **Win/loss tracker** — logs games, wins, losses, and win rate to `stats.json`

## Solver Logic

- **Tier 1 (Basic Constraints)** — Flags obvious mines when unrevealed neighbors equal the cell number, and clicks safe cells when mine count is satisfied.
- **Tier 2 (Subset Subtraction)** — Compares overlapping cell sets to deduce hidden safe cells and mines that basic logic misses.
- **Tier 3 (Probability Guessing)** — Calculates mine probabilities across frontier cells when stuck to make the safest guess.

## Project Structure

```
Minesweeper/
├── solver/
│   ├── __init__.py    # Package marker
│   ├── constants.py   # Board dimensions, color ranges, calibration loader
│   ├── vision.py      # Screenshot capture and cell color detection
│   ├── solver.py      # Constraint solving and mouse click execution
│   └── stats.py       # Game result logger
├── calibrate.py       # Interactive Spacebar calibration tool
├── main.py            # Entry point
└── requirements.txt
```

## Getting Started

### Prerequisites

- Python 3.10+
- Windows OS
- A browser with [Google Minesweeper](https://www.google.com/search?q=minesweeper) open

### Install

```bash
git clone https://github.com/Amritesh-Singh-okay/Minesweeper-solver.git
cd Minesweeper-solver

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

### Run

```bash
python main.py
```

1. Pick a difficulty (1 = Easy, 2 = Medium, 3 = Expert).
2. If no calibration exists, it will ask you to hover over the **top-left** and **bottom-right** corners of the board and press **Spacebar** for each.
3. Switch to your browser. The solver starts automatically.
4. Hold **ESC** anytime to stop.

## License

MIT — see [LICENSE](LICENSE).
