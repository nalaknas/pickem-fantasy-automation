#!/usr/bin/env python3
"""
Complete example showing how to process a week with underdog calculations
"""

from skins_game_mvp import SleeperSkinsGameMVP
import json

def process_week_example():
    """Example of processing a week with complete odds data"""
    
    # Initialize with correct league ID
    league_id = "1267183695911976960"
    skins_game = SleeperSkinsGameMVP(league_id)
    
    print("🏈 COMPLETE WEEK PROCESSING EXAMPLE 🏈")
    print("=" * 60)
    
    # Example of a complete week's odds data (you would fill this in manually)
    example_odds = {
        "ARI": {"opponent": "LAR", "is_underdog": True, "won": False},
        "LAR": {"opponent": "ARI", "is_underdog": False, "won": True},
        "ATL": {"opponent": "PHI", "is_underdog": True, "won": True},  # Underdog win!
        "PHI": {"opponent": "ATL", "is_underdog": False, "won": False},
        "BAL": {"opponent": "KC", "is_underdog": True, "won": False},
        "KC": {"opponent": "BAL", "is_underdog": False, "won": True},
        "DET": {"opponent": "GB", "is_underdog": True, "won": True},   # Another underdog win!
        "GB": {"opponent": "DET", "is_underdog": False, "won": False},
        "WAS": {"opponent": "TB", "is_underdog": False, "won": True},
        "TB": {"opponent": "WAS", "is_underdog": True, "won": False},
        "CLE": {"opponent": "DAL", "is_underdog": True, "won": False},
        "DAL": {"opponent": "CLE", "is_underdog": False, "won": True},
        "MIA": {"opponent": "BUF", "is_underdog": False, "won": True},
        "BUF": {"opponent": "MIA", "is_underdog": True, "won": False},
        "LAC": {"opponent": "LV", "is_underdog": False, "won": True},
        "LV": {"opponent": "LAC", "is_underdog": True, "won": False},
    }
    
    print("📊 Example Week 1 Odds Data:")
    print("Format: Team vs Opponent: Result (Underdog/Favorite)")
    print()
    
    # Group by game for better display
    games = []
    processed_teams = set()
    
    for team, data in example_odds.items():
        if team not in processed_teams:
            opponent = data['opponent']
            processed_teams.add(team)
            processed_teams.add(opponent)
            
            team_result = "✅ WON" if data['won'] else "❌ LOST"
            opponent_result = "✅ WON" if example_odds[opponent]['won'] else "❌ LOST"
            
            team_type = "🐕 UNDERDOG" if data['is_underdog'] else "🏆 FAVORITE"
            opponent_type = "🐕 UNDERDOG" if example_odds[opponent]['is_underdog'] else "🏆 FAVORITE"
            
            games.append(f"  {team} vs {opponent}:")
            games.append(f"    {team}: {team_result} ({team_type})")
            games.append(f"    {opponent}: {opponent_result} ({opponent_type})")
            games.append("")
    
    for game in games:
        print(game)
    
    # Calculate underdog statistics
    underdog_teams = [team for team, data in example_odds.items() if data.get('is_underdog', False)]
    underdog_winners = [team for team in underdog_teams if example_odds[team].get('won', False)]
    
    print(f"📈 UNDERDOG STATISTICS:")
    print(f"  Total underdog games: {len(underdog_teams)}")
    print(f"  Underdog wins: {len(underdog_winners)}")
    print(f"  Underdog win rate: {len(underdog_winners)/len(underdog_teams)*100:.1f}%")
    print(f"  Underdog winners: {underdog_winners}")
    
    print(f"\n🎯 HOW TO USE THIS DATA:")
    print("1. Save this odds data to week_1_odds_template.json")
    print("2. Run: skins_game.process_week(1, odds_data)")
    print("3. The system will calculate:")
    print("   - Highest scorer for the week")
    print("   - Most correct underdog picks")
    print("   - Store results for future reference")
    
    # Show what the processing would look like
    print(f"\n💻 CODE EXAMPLE:")
    print("""
# Load your odds data
with open('week_1_odds_template.json', 'r') as f:
    odds_data = json.load(f)['week_1_odds']

# Process the week
result = skins_game.process_week(1, odds_data)

# View results
skins_game.view_all_results()
""")
    
    # Save the example odds data
    example_data = {"week_1_odds": example_odds}
    with open('week_1_example_odds.json', 'w') as f:
        json.dump(example_data, f, indent=2)
    
    print(f"\n✅ Example odds data saved to: week_1_example_odds.json")
    print("   You can use this as a template for your actual Week 1 data")

if __name__ == "__main__":
    process_week_example()
