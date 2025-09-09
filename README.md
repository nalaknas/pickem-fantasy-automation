# Sleeper Fantasy Pickem Skins Game Automation

A Python package for automating fantasy football skins game calculations using the Sleeper API.

## Project Structure

```
pickem_fantasy_automation/
├── src/                           # Core application code
│   ├── __init__.py               # Package initialization
│   ├── skins_game_mvp.py         # Main MVP implementation
│   ├── weekly_runner.py          # Weekly processing script
│   ├── view_results.py           # Results viewing utilities
│   ├── sleeper_skins_game_full.py # Full-featured implementation
│   ├── sleeper_testing_toolkit.py # Testing utilities
│   └── sleeper_api_explorer.py   # API exploration tools
├── tests/                        # Test files and debugging scripts
│   ├── test_*.py                 # Unit tests
│   ├── debug_*.py               # Debugging scripts
│   └── example_*.py              # Example usage scripts
├── data/                         # Data files
│   ├── skins_game_results.json   # Main results storage
│   ├── league_info.json          # League configuration
│   ├── users.json               # User data
│   ├── rosters.json             # Roster data
│   ├── week_*_*.json            # Weekly data files
│   └── *.xlsx                   # Excel data files
├── docs/                         # Documentation
│   ├── README_MVP.md             # MVP documentation
│   └── README_Weekly_Runner.md   # Weekly runner guide
├── backups/                      # Backup files
│   └── skins_game_results_backup_*.json
├── main.py                       # Main entry point
└── README.md                     # This file
```

## Quick Start

### Basic Usage

```bash
# Process the previous week automatically
python main.py

# Process a specific week
python main.py 5

# Check current status
python main.py status

# View all results
python main.py view

# View season summary
python main.py summary

# Export season report to CSV/Excel
python main.py export
```

### Programmatic Usage

```python
from src.skins_game_mvp import SleeperSkinsGameMVP

# Initialize with secure configuration (uses .env file)
skins_game = SleeperSkinsGameMVP()

# Or initialize with specific league ID
skins_game = SleeperSkinsGameMVP("your_league_id_here")

# Process a week
result = skins_game.process_week(1)

# View results
skins_game.view_all_results()
```

## Features

- **Automatic Week Detection**: Automatically detects current week and processes previous week
- **Rankings Calculation**: Calculates highest, second highest, third highest, and lowest scorers
- **Perfect Week Detection**: Identifies users with perfect weekly picks (requires game results)
- **Results Storage**: Persistent JSON storage of all weekly results
- **Clean Results Viewing**: Organized display of results by season and week
- **Flexible Processing**: Can process any week with or without game results
- **CSV/Excel Export**: Automatic export of season reports for easy sharing

## Configuration

### Secure Setup (Recommended)

The system now uses secure environment variables to protect your sensitive data:

1. **Run the setup script**: `python setup.py`
2. **Enter your league ID** when prompted
3. **Optionally configure Twilio** for notifications
4. **Your data is automatically secured** in a `.env` file

### Manual Configuration

If you prefer manual setup:

1. Copy `env.template` to `.env`
2. Fill in your `SLEEPER_LEAGUE_ID`
3. Optionally add Twilio credentials for notifications

**Important**: The `.env` file is automatically excluded from version control to keep your data secure.

## Data Files

- `data/skins_game_results.json`: Main results storage
- `data/week_X_game_results.json`: Optional game results for perfect week detection
- `data/league_info.json`: League configuration data
- `data/users.json`: User information
- `data/rosters.json`: Roster data

## Export Files

The system automatically generates comprehensive reports in the root directory:

- `skins_game_season_report.csv`: CSV format with weekly breakdown and season scores
- `skins_game_season_report.xlsx`: Excel format with multiple sheets:
  - **Weekly_Breakdown**: Week-by-week winners, scores, and perfect weeks
  - **Season_Scores**: Complete season scores for all users with rankings
  - **User_Picks**: Individual user picks (when available)
  - **Summary**: Season statistics and export information

These files are automatically updated every time you process a week and can be easily shared with league members.

## Testing

All test files are organized in the `tests/` directory:

- `test_*.py`: Unit tests for various components
- `debug_*.py`: Debugging scripts for troubleshooting
- `example_*.py`: Example usage scripts

## Backup Files

Backup files are stored in the `backups/` directory to keep the main data directory clean.

## Requirements

- Python 3.7+
- requests
- pandas (for full implementation)

## API Usage

This package uses the Sleeper API (https://api.sleeper.app/v1) to fetch:
- League information
- User data
- Roster data
- Pickem results

No API key is required as Sleeper provides a public API.
