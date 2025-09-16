# Sleeper Analytics Dashboard

A comprehensive analytics dashboard for Sleeper pickem leagues that provides insights into player performance, trends, and predictions.

## Features

### 📊 Performance Analytics
- **Week-over-week trend analysis** - Track how players perform across multiple weeks
- **Consistency scoring** - Identify players with stable vs. volatile performance
- **Improvement tracking** - Highlight players making significant improvements
- **Statistical analysis** - Mean, median, distribution analysis of league performance

### 🔮 Predictive Analytics
- **Performance prediction** - Predict next week's scores using linear regression
- **Confidence scoring** - Provide confidence levels for predictions
- **Trend analysis** - Identify improving vs. declining players

### 📈 Data Visualization
- **Weekly trends chart** - Line graph showing all players' weekly performance
- **Score distribution histogram** - Visual representation of score patterns
- **Top performers bar chart** - Highlight the league's best performers
- **Improvement trends chart** - Show which players are improving/declining

### 🎯 Key Metrics
- **Average score** - Overall performance metric
- **Consistency score** - Based on standard deviation (lower = more consistent)
- **Improvement trend** - Linear regression slope of performance over time
- **Perfect weeks** - Count of weeks with maximum possible score
- **Zero weeks** - Count of weeks with zero score

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure your `secure_config.py` is properly configured with your Sleeper league ID.

## Usage

### Command Line Interface

The analytics dashboard can be used via the command line interface:

```bash
# Generate full dashboard with all charts and summary
python analytics_cli.py --full-dashboard

# Generate only the performance summary
python analytics_cli.py --summary-only

# Generate only charts
python analytics_cli.py --charts-only

# Predict performance for a specific player
python analytics_cli.py --predict-player "player_name"

# Specify custom output directory
python analytics_cli.py --full-dashboard --output-dir ./my_analytics
```

### Programmatic Usage

```python
from src.analytics_dashboard import SleeperAnalyticsDashboard

# Initialize dashboard
dashboard = SleeperAnalyticsDashboard()

# Extract player data
player_data = dashboard.extract_player_data()

# Calculate league analytics
analytics = dashboard.calculate_league_analytics()

# Generate performance summary
summary = dashboard.generate_performance_summary()
print(summary)

# Predict next week performance for a player
prediction = dashboard.predict_next_week_performance("user_id")
print(f"Predicted score: {prediction['predicted_score']:.2f}")
print(f"Confidence: {prediction['confidence']:.2f}")

# Generate all charts
dashboard.generate_full_dashboard("output_directory")
```

## Output Files

The dashboard generates several output files:

- **performance_summary.txt** - Text summary of league performance
- **weekly_trends.png** - Line chart showing all players' weekly performance
- **score_distribution.png** - Histogram of score distribution
- **top_performers.png** - Bar chart of top performers
- **improvement_trends.png** - Chart showing improvement/decline trends

## Example Output

### Performance Summary
```
🏈 LEAGUE PERFORMANCE SUMMARY 🏈
==================================================

📊 OVERALL STATISTICS:
• Total Players: 35
• Weeks Analyzed: 2
• Average League Score: 5.11

🏆 TOP PERFORMERS (by average score):
1. PSekhar7: 7.00 avg
2. abhia: 6.50 avg
3. BCIB: 6.50 avg
4. rushp12345: 6.50 avg
5. crazylook3: 6.50 avg

📈 MOST IMPROVED PLAYERS:
1. nalaknas: 📈 +8.00 trend
2. abhia: 📈 +5.00 trend
3. BntObrn: 📈 +5.00 trend
4. janakshah: 📈 +5.00 trend
5. scooty11: 📈 +4.00 trend

🎯 MOST CONSISTENT PLAYERS:
1. shreykap: 1.000 consistency
2. tuanfinitynbeyond: 1.000 consistency
3. hugebeast1999: 1.000 consistency
4. dirtypoonjabi: 0.667 consistency
5. Jaysterseason: 0.667 consistency
```

### Prediction Example
```
🎯 PREDICTION FOR NALAKNAS:
   Predicted Score: 17.00
   Confidence: 0.90
   Trend: +8.00
   Next Week: 3
```

## Testing

Run the test suite to verify functionality:

```bash
python test_analytics.py
```

This will test:
- Data extraction from Sleeper API
- Analytics calculations
- Chart generation
- Prediction functionality

## Technical Details

### Data Sources
- **Sleeper API** - Fetches league data, user information, and roster data
- **Points by leg** - Weekly scoring data from roster metadata

### Analytics Methods
- **Consistency Score** - `1 / (standard_deviation + 1)` (higher = more consistent)
- **Improvement Trend** - Linear regression slope of scores over time
- **Prediction** - Linear regression extrapolation with confidence based on R-squared

### Performance Metrics
- **Total Score** - Sum of all weekly scores
- **Average Score** - Mean weekly performance
- **Perfect Weeks** - Count of maximum possible scores
- **Zero Weeks** - Count of zero scores

## Future Enhancements

Potential future features:
- **Machine learning predictions** - More sophisticated prediction models
- **Social features** - Player comparisons and rivalries
- **Historical analysis** - Multi-season performance tracking
- **Real-time updates** - Live score tracking during games
- **Export functionality** - CSV/Excel export of analytics data
- **Web dashboard** - Browser-based interface
- **Mobile app** - iOS/Android application

## Contributing

This analytics dashboard is part of the Sleeper Skins Game Automation project. To contribute:

1. Create a feature branch
2. Implement your changes
3. Add tests for new functionality
4. Submit a pull request

## License

This project is licensed under the same terms as the main Sleeper Skins Game Automation project.
