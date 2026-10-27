# ART-TI-FICIAL

A Pictionary-style drawing game where AI judges your artwork!

**Winner of Best Game at UNC-Chapel Hill's HACK110 2025 Hackathon**, competing against 30+ teams.

## About

ART-TI-FICIAL is a drawing game built in just 24 hours during UNC-Chapel Hill's HACK110 2025 Hackathon using Python and Pygame. Players are given a word to draw within a time limit, and once time runs out, OpenAI's GPT-4o-mini analyzes their drawing and scores how closely it matches the original prompt.

The game consists of three rounds with increasing difficulty (easy, medium, and hard). Each round has a different time limit, and players can earn up to 5,000 points per drawing.

Rather than checking drawings against predefined images, the game uses AI to interpret what the player actually drew, making each evaluation a little different.

## Tech Stack

- **Python** — Game logic
- **Pygame** — Drawing canvas and game interface
- **OpenAI API (GPT-4o-mini)** — Image recognition and scoring
- **Pillow & NumPy** — Image processing
- **CSV** — Word lists for each difficulty

## How It Works

1. The player receives a randomly selected word and draws it on the canvas.
2. When the timer ends, the drawing is captured and converted into an image.
3. The image is sent to GPT-4o-mini, which identifies what was drawn without knowing the target word.
4. The AI's interpretation is compared with the original word to generate a score between 0 and 5,000.
5. After three rounds, the player's total score is displayed.

## Team

Developed by **Frank Lin** and **Yao Luo** for HACK110 2025.
