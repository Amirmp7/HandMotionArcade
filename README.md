# 🎮 Hand Motion Arcade

A hand-controlled arcade game using MediaPipe and Pygame.

Control the paddle with your hand via webcam, collect coins, avoid bombs, and compete for the highest score!

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.5.0-green.svg)](https://www.pygame.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.0-orange.svg)](https://mediapipe.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Features

- **Hand Tracking**: Control the paddle with your hand using MediaPipe.
- **Particle Effects**: Sparks on paddle hit, golden burst on coin collection, bomb explosion.
- **Sound Effects**: Bounce, coin, game over, and bomb sounds.
- **Customization**: Change ball color, paddle color, ball shape, background theme, and sound.
- **High Scores**: Save your best scores with your name.
- **Difficulty Levels**: Easy, Medium, and Hard with different speeds and bomb penalties.
- **Bombs**: Bombs appear randomly and deduct points (penalty depends on difficulty level).
- **Mouse Support**: Play with mouse if camera is not available.

---

## Quick Start (Run with Python)

### Prerequisites

- Python 3.10 or higher
- Webcam (for hand control)
- Git (optional, for cloning)

### Installation

1. **Clone the repository** (or download as ZIP):

   ```bash
   git clone https://github.com/Amirmp7/HandMotionArcade.git
   cd HandMotionArcade
   ```

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate      # On Linux/Mac
   venv\Scripts\activate         # On Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the game**:

   ```bash
   python main.py
   ```

---

## 🛠️ Build Executable (Optional)

If you want to build a standalone `.exe` file for Windows:

1. Install PyInstaller:

   ```bash
   pip install pyinstaller
   ```

2. Build using the provided spec file:

   ```bash
   pyinstaller HandMotionArcade.spec
   ```

3. The executable will be created in the `dist` folder.

> **Note**: Building may take several minutes. The spec file is configured to include all necessary MediaPipe resources.

---

## 🎮 How to Play

| Action | Key / Input |
|---------|-------------|
| **Start Game** | Click "Start Game" button |
| **Options** | Click "Options" button |
| **Pause/Resume** | Press `P` |
| **Quit** | Click "Quit" button |
| **Menu** | Click "Menu" button after Game Over |
| **Paddle Control** | Move your hand left/right in front of webcam |
| **Mouse Fallback** | Move mouse left/right (if camera unavailable) |

### Difficulty Levels

| Level | Ball Speed | Bomb Count | Bomb Penalty |
|-------|------------|------------|--------------|
| Easy | Slow | 2 | -1 point |
| Medium | Medium | 3 | -1 point |
| Hard | Fast | 5 | -2 points |

### Game Objects

- **Coins**: Collect to increase your score (+1 point each).
- **Bombs**: Avoid them! They deduct points based on difficulty level.
- **Paddle**: Controlled by your hand or mouse.

---

## ⚙️ Customization (Options Menu)

- **Ball Color**: Cycle through 6 colors (Red, Blue, Green, Orange, Purple, White).
- **Paddle Color**: Cycle through 5 colors.
- **Ball Shape**: Circle, Square, or Triangle.
- **Sound**: Turn ON/OFF.
- **Background**: Cycle through 6 themes (Deep Blue, Sunset, Forest, Midnight, Ocean, Lava).

---

## 📁 Project Structure

```text
HandMotionArcade/
├── main.py                  # Entry point
├── game.py                  # Main game loop and state management
├── config.py                # All configuration parameters
├── detector.py              # Hand detection with MediaPipe
├── objects.py               # Game objects (Paddle, Ball, Coin, Bomb)
├── physics.py               # Physics engine (collisions, movement)
├── renderer.py              # Rendering and UI
├── audio.py                 # Sound management
├── state.py                 # Game state machine
├── effects.py               # Particle system
├── highscore.py             # High score management
├── settings.py              # Player settings management
├── requirements.txt         # Python dependencies
├── HandMotionArcade.spec    # PyInstaller spec file for building .exe
├── assets/
│   └── sounds/
│       ├── bounce.wav
│       ├── coin.wav
│       ├── game_over.wav
│       └── bomb.wav
└── data/                    # (Empty) - stores highscore.json and settings.json
```

---

## 🔧 Troubleshooting

### Camera not working?

- Make sure your webcam is connected.
- Check camera permissions in Windows: `Settings > Privacy & Security > Camera`.
- If still not working, the game will fallback to mouse control.

### Game crashes on startup?

- Ensure all dependencies are installed correctly.
- Try running with `console=True` in the `.spec` file to see error logs.

### High scores not saving?

- The `data/` folder will automatically be created when you first play.
- Make sure the folder has write permissions.

---

## 📜 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgments

- [MediaPipe](https://mediapipe.dev/) for hand tracking
- [Pygame](https://www.pygame.org/) for game development
- [OpenCV](https://opencv.org/) for camera handling

---
