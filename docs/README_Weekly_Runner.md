# Weekly Skins Game Runner

Simple script to process your Sleeper skins game results every week.

## Quick Start

**Every week, just run:**
```bash
python3 weekly_runner.py
```

## How It Works

### 1. **First Time Setup**
The script will automatically:
- Detect your current week
- Create an odds template file (`week_X_odds_template.json`)
- Tell you what to do next

### 2. **Weekly Process**
1. **Fill in the odds template** with actual game results:
   - Set `is_underdog: true` for teams that were underdogs
   - Set `won: true` for teams that won their games

2. **Run the script**:
   ```bash
   python3 weekly_runner.py
   ```

3. **View your results** - the script will show:
   - Highest scorer for the week
   - Most correct underdog picks
   - All stored historical results

### 3. **Quick Status Check**
Check your league status without processing:
```bash
python3 weekly_runner.py status
```

## Example Workflow

**Week 1:**
```bash
$ python3 weekly_runner.py
📅 Current Week: 1
📝 Creating odds template for Week 1...
✅ Created week_1_odds_template.json

🎯 NEXT STEPS:
1. Fill in week_1_odds_template.json with actual game results
2. Set is_underdog=True for teams that were underdogs
3. Set won=True for teams that won their games
4. Run this script again: python3 weekly_runner.py
```

**After filling in odds:**
```bash
$ python3 weekly_runner.py
📅 Current Week: 1
📊 Loading odds data from week_1_odds_template.json...
🔄 Processing Week 1...

🎉 WEEK 1 RESULTS PROCESSED!
📊 High Score Winner(s): nalaknas - 10.0 points
🐕 Underdog Winner(s): scooty11 - 3/8 correct

📈 ALL STORED RESULTS:
Week 1 (2025):
  High Score: nalaknas - 10.0 pts
  Underdog: scooty11 - 3/8 correct

✅ Week 1 processing complete!
📁 Results saved to: skins_game_results.json
```

## Files Created

- `week_X_odds_template.json` - Template for each week's odds
- `skins_game_results.json` - All stored results
- `weekly_runner.py` - Main script to run

## Troubleshooting

**"Odds file appears to be empty"**
- Make sure you filled in the odds template with actual game results
- Remove the `"note"` field from the JSON

**"Failed to get league info"**
- Check your internet connection
- Verify the league ID is correct

**"No pickem data yet"**
- This is normal for Week 1 before games are played
- Wait until after the games to process results

## That's It!

Just run `python3 weekly_runner.py` every week after the games are played. The script handles everything else automatically!
