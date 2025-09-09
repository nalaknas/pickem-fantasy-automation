#!/usr/bin/env python3
"""
Example usage of the Sleeper Skins Game MVP

This script demonstrates how to:
1. Pull league data from Sleeper API
2. Calculate highest scorer and underdog winners
3. Store results for future reference
"""

from skins_game_mvp import SleeperSkinsGameMVP
import json

def main():
    # Initialize with your league ID
    # league_id = "1137502853016403968"  # Old league ID (commented out)
    league_id = "1267183695911976960"  # Current season league ID
    skins_game = SleeperSkinsGameMVP(league_id)
    
    print("🏈 SLEEPER SKINS GAME MVP 🏈")
    print("=" * 40)
    
    try:
        # Get current week
        current_week = skins_game.get_current_week()
        print(f"Current week: {current_week}")
        
        # Get league info
        league_info = skins_game.get_league_info()
        print(f"League: {league_info.get('name', 'Unknown')}")
        
        # Get users
        users = skins_game.get_users()
        print(f"League members: {len(users)}")
        
        # Show current week summary
        summary = skins_game.get_week_summary(current_week)
        print(f"\nWeek {current_week} Summary:")
        print(f"High Score: {summary['high_score']} points")
        
        # Show all users and their scores
        print("\nAll Users:")
        for user_data in summary['user_data']:
            print(f"  {user_data['display_name']}: {user_data['score']} pts")
        
        # Show highest scorer
        high_score_winners, high_score = skins_game.calculate_highest_scorer(current_week)
        print(f"\n🏆 HIGHEST SCORER: {high_score} points")
        for winner_id in high_score_winners:
            winner_name = users.get(winner_id, {}).get('display_name', 'Unknown')
            print(f"  Winner: {winner_name}")
        
        # Create odds template for manual input
        print(f"\n📝 Creating odds template for week {current_week}...")
        skins_game.create_odds_template(current_week)
        
        print("\n✅ MVP is working! Next steps:")
        print("1. Fill in the odds template with actual game results")
        print("2. Use process_week() to calculate and store results")
        print("3. View stored results with view_all_results()")
        
        # Example of how to process a week (commented out)
        print("\n📋 Example usage:")
        print("""
        # Load your odds data
        with open('week_18_odds_template.json', 'r') as f:
            odds_data = json.load(f)['week_18_odds']
        
        # Process the week
        result = skins_game.process_week(current_week, odds_data)
        
        # View all results
        skins_game.view_all_results()
        """)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your league ID is correct and the Sleeper API is accessible.")

if __name__ == "__main__":
    main()
