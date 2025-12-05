# ASCII Space Invaders 👾 - Pygame

[![Version](https://img.shields.io/badge/Version-1.0.0-green.svg)]() 

A retro ASCII-style implementation of the classic Space Invaders arcade game built with Python and Pygame. Features authentic terminal-style graphics with procedurally generated sound effects. Detailed manual compile instructions. Building from source may work on Mac and Linux.

<img width="794" height="616" alt="Screenshot 2025-12-05 042854" src="https://github.com/user-attachments/assets/7bcd8c3b-6044-49c6-b6b0-9cf6b5a6728b" />


## Features
- Classic Space Invaders mechanics: defend Earth from alien invasion!
- Retro ASCII graphics with terminal aesthetic
- Animated aliens that alternate between frames
- Simple keyboard controls for movement and shooting
- Score tracking system (+10 points per alien destroyed)
- Aliens shoot back and move faster as you destroy them
- Procedurally generated sound effects (no audio files required!)
- Game over when aliens reach you or hit you with bullets
- Win condition: destroy all aliens
- Clean UI with ASCII art player, aliens, and projectiles
- Smooth physics with increasing difficulty

## Requirements
- **Python 3.11** (recommended for best compatibility)
- Pygame (`pygame==2.6.1`)
- NumPy (for sound generation)
- All other requirements are in the requirements.txt

## Compiled setup
Windows users can use the Release .exe in the Releases section. **ONLY do this if you trust the source.** I recommend reading the code from this repo first before running any compiled executable.
  
## Manual Installation & Setup
### Step 1: Create Virtual Environment / Clone repo

**Download and extract this repo, Install Python 3.11 - ensure you check 'Add to PATH' in the installer. Open CMD from the extracted folder:**

```bash
python -m venv space_invaders_venv

# Or create venv using Python 3.11 explicitly:
python -m venv space_invaders_venv --system-site-packages
```

### Step 2: Activate Virtual Environment
```powershell
# Windows (PowerShell):
.\space_invaders_venv\Scripts\activate.ps1

# Windows (CMD):
.\space_invaders_venv\Scripts\activate.bat

# Linux/Mac:
source space_invaders_venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt

# Or install manually:
pip install --user pygame==2.6.1 numpy
```

> ⚠️ **Important**: The wheel file requires Python 3.11. If you're using a different version, download the correct wheel or install from PyPI.

## Running the Game
```bash
# From inside the folder where space_invaders.py exists:
python space_invaders.py
```
Or download the self-contained Windows build in Releases (only do this if you trust the source).

### Controls
| Key | Action |
|-----|--------|
| LEFT ARROW / A  | Move Left |
| RIGHT ARROW / D | Move Right |
| SPACE  | Shoot |
| R  | Restart (after game over) |
| ESC  | Quit Game |

**RULES:** You are the ASCII defender (`/|\`). Destroy all alien invaders by shooting them before they reach Earth! Dodge alien bullets and prevent them from landing. The aliens speed up as you destroy more of them!

## Technical Details
- Built using **Python 3.11** for compatibility with pygame
- Uses NumPy for procedural sound generation (no audio files!)
- Physics-based movement with increasing alien speed
- Score increases by 10 points for each alien destroyed
- Game ends when aliens reach the player or player is hit by alien bullet
- Retro ASCII aesthetic with green terminal colors
- Player sprite: `/|\` and `/_|_\` characters
- Alien sprites: `/o\` and `\o/` characters (animated)
- Bullets: `|` (player) and `v` (alien)
- Clean, readable code with modular class structure
- 3 rows × 7 columns of aliens (21 total)
- Aliens move in formation and shoot randomly

## Sound Effects
The game features procedurally generated sound effects:
- **Player Shoot**: Descending tone (800Hz → 200Hz)
- **Alien Shoot**: Ascending tone (200Hz → 600Hz)
- **Alien Movement**: Low beep (150Hz) that speeds up as aliens are destroyed

All sounds are generated in real-time using NumPy sine waves - no audio files required!

## Building Single-File Executable

### Windows .exe
To build on Windows:
```bash
# Automated (double-click this file)
compile_to_exe.bat

# OR Manual
pip install pyinstaller
pyinstaller --onefile --name "space_invaders" space_invaders.py
```
Output: `dist/space_invaders.exe`

### Linux Binary
To build on Linux:
```bash
# Manual
pip install pyinstaller
pyinstaller --onefile --name "space_invaders" space_invaders.py

# Output: dist/space_invaders (binary)
```

### Important: Cross-Platform Limitations
⚠️ **PyInstaller cannot cross-compile!**
- Windows builds only work on Windows
- Linux builds only work on Linux
- You must build on each target platform

---

## Gameplay Tips
- Keep moving to avoid alien bullets
- Focus on clearing one column at a time
- The last few aliens are the hardest - they move very fast!
- Listen to the movement sound - it speeds up as danger increases
- You can only have one bullet on screen at a time, so aim carefully!

## Troubleshooting
**Game won't start:**
- Make sure pygame and numpy are installed: `pip install pygame numpy`
- Verify Python 3.11 is installed: `python --version`

**No sound:**
- Check your system volume
- Ensure NumPy is installed for sound generation
- Try running with `python -u space_invaders.py` for unbuffered output

**Import errors:**
- Activate your virtual environment first
- Reinstall dependencies: `pip install -r requirements.txt`

---

**Note**: This implementation uses procedurally generated sounds via NumPy, eliminating the need for external audio files. The game is fully self-contained!

**Windows users can use the Release .exe in the Releases section. ONLY do this if you trust the source.** I recommend reading the code from this repo first.

## Attribution

This project is licensed under Apache 2.0. See the LICENSE file for details.

Version: 1.0 | Date: 05/12/25

GitHub: https://github.com/captainzero93/
