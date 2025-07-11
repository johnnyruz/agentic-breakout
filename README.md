# Breakout - IMPROVING

A classic Breakout game implemented in Python using Pygame, where the blocks form the word "IMPROVING" in blue colors.

## Features

- **Classic Breakout gameplay** - Control a paddle to bounce a ball and break blocks
- **Custom block arrangement** - Blocks are arranged to spell out "IMPROVING"
- **Blue color scheme** - All blocks are colored in blue tones as requested
- **Smooth physics** - Ball bounces with realistic physics, including angle changes based on paddle hit position
- **Timer system** - Track how long it takes to complete the level
- **Game states** - Win condition when all blocks are destroyed, restart functionality
- **Responsive controls** - Use left/right arrow keys to move the paddle

## Installation

1. Install Python 3.6+ if not already installed
2. Install Pygame:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install Pygame directly:
   ```bash
   pip install pygame
   ```

## How to Run

```bash
python breakout_improving.py
```

## Controls

- **Left/Right Arrow Keys**: Move paddle left and right
- **R**: Restart game (when game over or won)
- **ESC**: Exit game

## Game Rules

1. Use the paddle to bounce the ball upward
2. Break all blue blocks that spell "IMPROVING"
3. Don't let the ball fall off the bottom of the screen
4. Win by destroying all blocks!

## Game Mechanics

- **Paddle Physics**: The ball's bounce angle depends on where it hits the paddle
- **Timer System**: Track your completion time with a running clock
- **Wall Bouncing**: Ball bounces off top and side walls
- **Win Condition**: Destroy all blocks to win and see your completion time
- **Loss Condition**: Ball falls off the bottom of the screen

## Code Structure

- `Ball` class: Handles ball movement and physics
- `Paddle` class: Manages paddle movement and controls
- `Block` class: Individual block objects with collision detection
- `Game` class: Main game logic, rendering, and game loop
- Block patterns are defined as 2D arrays to form each letter

The word "IMPROVING" is created using custom letter patterns where each letter is defined as a 5-row grid pattern, with blocks arranged to form readable letters.

Enjoy breaking out and improving your skills!