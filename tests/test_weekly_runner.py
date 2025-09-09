#!/usr/bin/env python3
"""
Test Weekly Runner with Week 18 from Last Season
"""

from skins_game_mvp import SleeperSkinsGameMVP
import json
import os

def test_weekly_runner_with_week18():
    print("🏈 TESTING WEEKLY RUNNER WITH WEEK 18 🏈")
    print("=" * 50)
    
    # Use last season's league ID
    old_league_id = "1137502853016403968"  # Last season
    skins_game = SleeperSkinsGameMVP(old_league_id)
    
    try:
        # Force week 18 for testing
        test_week = 18
        print(f"📅 Testing Week: {test_week}")
        
        # Get league info
        league_info = skins_game.get_league_info()
        print(f"League: {league_info.get('name', 'Unknown')}")
        print(f"Season: {league_info.get('season', 'Unknown')}")
        
        # Check if odds file exists
        odds_filename = f"week_{test_week}_odds_template.json"
        
        if not os.path.exists(odds_filename):
            print(f"📝 Creating odds template for Week {test_week}...")
            skins_game.create_odds_template(test_week)
            print(f"✅ Created {odds_filename}")
        
        # Load odds data
        print(f"📊 Loading odds data from {odds_filename}...")
        with open(odds_filename, 'r') as f:
            odds_data = json.load(f)[f'week_{test_week}_odds']
        
        # Validate odds data
        if not odds_data or odds_data.get('note'):
            print(f"⚠️  {odds_filename} appears to be empty or just a template")
            print(f"   Using example data for testing...")
            
            # Create example odds data
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
            
            # Save example data
            example_data = {f"week_{test_week}_odds": example_odds}
            with open(odds_filename, 'w') as f:
                json.dump(example_data, f, indent=2)
            
            odds_data = example_odds
        
        # Process the week
        print(f"🔄 Processing Week {test_week}...")
        result = skins_game.process_week(test_week, odds_data)
        
        # Show results summary
        print(f"\n🎉 WEEK {test_week} RESULTS PROCESSED!")
        print(f"📊 High Score Winner(s): {', '.join(result['winner_names']['high_score'])} - {result['high_score']} points")
        print(f"🐕 Underdog Winner(s): {', '.join(result['winner_names']['underdog'])} - {result['underdog_correct']}/{result['total_underdog_games']} correct")
        
        # Show all stored results
        print(f"\n📈 ALL STORED RESULTS:")
        skins_game.view_all_results()
        
        print(f"\n✅ Week {test_week} processing complete!")
        print(f"📁 Results saved to: skins_game_results.json")
        
        # Show what the weekly runner would do
        print(f"\n🎯 WEEKLY RUNNER SIMULATION:")
        print(f"This is exactly what 'python3 weekly_runner.py' would do:")
        print(f"1. ✅ Detect current week: {test_week}")
        print(f"2. ✅ Load odds data from {odds_filename}")
        print(f"3. ✅ Process the week and calculate winners")
        print(f"4. ✅ Store results and display summary")
        print(f"5. ✅ Show all historical results")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_weekly_runner_with_week18()
