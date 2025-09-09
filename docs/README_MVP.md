# Sleeper Skins Game MVP - Simplified Version

A simplified implementation for automating your Sleeper fantasy football pickem league's skins game.

## What it does

1. **Pulls league data** from Sleeper API using your league ID
2. **Calculates weekly rankings** - highest, second highest, third highest, and lowest scorers
3. **Detects perfect weeks** (optional, when you provide game results)
4. **Stores results** in JSON format for future reference

## Quick Start

1. **Run the MVP**:
   ```bash
   python3 skins_game_mvp.py
   ```

2. **Run the weekly processor**:
   ```bash
   python3 weekly_runner.py
   ```

3. **Test the system**:
   ```bash
   python3 test_simplified_system.py
   ```

## How to use

### 1. Basic Usage (No additional files needed)
The system automatically calculates rankings based on weekly scores:

```python
from skins_game_mvp import SleeperSkinsGameMVP

# Initialize
skins_game = SleeperSkinsGameMVP("1267183695911976960")

# Process any week (no additional data needed)
result = skins_game.process_week(week_number)
```

This will show:
- 🥇 Highest Scorer(s) and their points
- 🥈 Second Highest Scorer(s) and their points  
- 🥉 Third Highest Scorer(s) and their points
- 📉 Lowest Scorer(s) and their points

### 2. Perfect Week Detection (Optional)
To detect perfect weeks, create a game results file:

**Create `week_X_game_results.json`:**
```json
{
  "ARI": {"opponent": "LAR", "won": false},
  "LAR": {"opponent": "ARI", "won": true},
  "BUF": {"opponent": "MIA", "won": true},
  "MIA": {"opponent": "BUF", "won": false}
}
```

**Process with perfect week detection:**
```python
# Load game results
with open('week_1_game_results.json', 'r') as f:
    game_results = json.load(f)

# Process with perfect week detection
result = skins_game.process_week(week_number, game_results)
```

### 3. Weekly Runner
Use the automated weekly runner:

```bash
# Process previous week (auto-detected)
python3 weekly_runner.py

# Process specific week
python3 weekly_runner.py 1

# Check status
python3 weekly_runner.py status
```

## Files created

- `skins_game_results.json` - Stores all processed results
- `week_X_game_results.json` - Optional game results for perfect week detection

## Example Output

```
🏈 WEEK 1 RESULTS 🏈
🥇 Highest Scorer(s): Player1, Player2 - 12.0 points
🥈 Second Highest: Player3 - 11.0 points
🥉 Third Highest: Player4 - 10.0 points
📉 Lowest Scorer(s): Player5 - 3.0 points
🎯 Perfect Week: Player1
```

## What's Changed

- ❌ **Removed**: Underdog calculations and manual odds entry
- ❌ **Removed**: Complex odds templates and manual data entry
- ✅ **Added**: Simple ranking system (highest, second, third, lowest)
- ✅ **Retained**: Perfect week detection (optional)
- ✅ **Simplified**: No additional files needed for basic functionality

## Example Workflow

```python
from skins_game_mvp import SleeperSkinsGameMVP
import json

# Initialize
skins_game = SleeperSkinsGameMVP("1267183695911976960")

# Get current week
current_week = skins_game.get_current_week()

# Process week (basic rankings only)
result = skins_game.process_week(current_week)

# OR process with perfect week detection
# with open(f'week_{current_week}_game_results.json', 'r') as f:
#     game_results = json.load(f)
# result = skins_game.process_week(current_week, game_results)

# View all results
skins_game.view_all_results()
```
