# Retro DOS Game

## Overview
This project is a retro-style game inspired by classic games from the 2000s that ran on MS DOS. The game features a cannon that can be moved left and right using the arrow keys.

## Project Structure
```
retro-dos-game
├── src
│   ├── main.py          # Entry point of the game
│   ├── game.py          # Main game logic
│   ├── entities
│   │   └── cannon.py    # Cannon entity definition
│   ├── input.py         # User input handling
│   ├── render.py        # Rendering logic
│   └── assets
│       └── fonts        # Font files for rendering text
├── tests
│   └── test_game.py     # Unit tests for game logic
├── requirements.txt      # Project dependencies
├── setup.py              # Packaging information
└── README.md             # Project documentation
```

## Getting Started

### Prerequisites
- Python 3.x
- Pygame library (or other dependencies listed in `requirements.txt`)

### Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/retro-dos-game.git
   ```
2. Navigate to the project directory:
   ```
   cd retro-dos-game
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running the Game
To start the game, run the following command:
```
python src/main.py
```

### Controls
- Use the left arrow key to move the cannon left.
- Use the right arrow key to move the cannon right.

## Contributing
Feel free to submit issues or pull requests to improve the game. 

## License
This project is licensed under the MIT License. See the LICENSE file for details.