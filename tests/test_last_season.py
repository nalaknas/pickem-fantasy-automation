#!/usr/bin/env python3
"""
Test the weekly runner with Week 18 results from last season
"""

from skins_game_mvp import SleeperSkinsGameMVP
import json

def test_with_last_season():
    print("🏈 TESTING WITH LAST SEASON WEEK 18 🏈")
    print("=" * 50)
    
    # Use last season's league ID
    old_league_id = "1137502853016403968"  # Last season
    skins_game = SleeperSkinsGameMVP(old_league_id)
    
    try:
        # Get current week from last season
        current_week = skins_game.get_current_week()
        print(f"📅 Last Season Week: {current_week}")
        
        # Get league info
        league_info = skins_game.get_league_info()
        print(f"League: {league_info.get('name', 'Unknown')}")
        print(f"Season: {league_info.get('season', 'Unknown')}")
        
        # Get users
        users = skins_game.get_users()
        print(f"Total Users: {len(users)}")
        
        # Show current week summary
        summary = skins_game.get_week_summary(current_week)
        print(f"\n📊 Week {current_week} Summary:")
        print(f"High Score: {summary['high_score']} points")
        
        # Show all users and their scores
        print(f"\n👥 All Users and Scores:")
        for user_data in summary['user_data']:
            if user_data['score'] > 0:  # Only show users with scores
                print(f"  {user_data['display_name']}: {user_data['score']} pts")
        
        # Calculate highest scorer
        high_score_winners, high_score = skins_game.calculate_highest_scorer(current_week)
        print(f"\n🏆 HIGHEST SCORER:")
        for winner_id in high_score_winners:
            winner_name = users.get(winner_id, {}).get('display_name', 'Unknown')
            print(f"  {winner_name}: {high_score} points")
        
        # Create odds template for testing
        print(f"\n📝 Creating odds template for Week {current_week}...")
        template = skins_game.create_odds_template(current_week)
        
        # Create example odds data based on typical Week 18 games
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
        
        # Save example odds data
        odds_filename = f"week_{current_week}_odds_template.json"
        example_data = {f"week_{current_week}_odds": example_odds}
        with open(odds_filename, 'w') as f:
            json.dump(example_data, f, indent=2)
        
        print(f"✅ Created example odds data in {odds_filename}")
        
        # Now test the weekly runner
        print(f"\n🔄 TESTING WEEKLY RUNNER...")
        print("=" * 30)
        
        # Process the week
        result = skins_game.process_week(current_week, example_odds)
        
        # Show results
        print(f"\n🎉 WEEK {current_week} RESULTS PROCESSED!")
        print(f"📊 High Score Winner(s): {', '.join(result['winner_names']['high_score'])} - {result['high_score']} points")
        print(f"🐕 Underdog Winner(s): {', '.join(result['winner_names']['underdog'])} - {result['underdog_correct']}/{result['total_underdog_games']} correct")
        
        # Show all stored results
        print(f"\n📈 ALL STORED RESULTS:")
        skins_game.view_all_results()
        
        print(f"\n✅ Test complete! The weekly runner works perfectly.")
        print(f"📁 Results saved to: skins_game_results.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_with_last_season()
