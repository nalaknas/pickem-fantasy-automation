#!/usr/bin/env python3
"""
Test script for the simplified skins game system
"""

from skins_game_mvp import SleeperSkinsGameMVP
import json

def test_simplified_system():
    """Test the simplified ranking system"""
    
    # Initialize with your league ID
    league_id = "1267183695911976960"
    skins_game = SleeperSkinsGameMVP(league_id)
    
    try:
        # Get current week
        current_week = skins_game.get_current_week()
        print(f"Current week detected: {current_week}")
        
        # Test rankings calculation
        print(f"\nTesting rankings calculation for Week {current_week}...")
        rankings = skins_game.calculate_week_rankings(current_week)
        
        print(f"Rankings calculated:")
        print(f"  Highest: {len(rankings['highest'])} user(s)")
        print(f"  Second Highest: {len(rankings['second_highest'])} user(s)")
        print(f"  Third Highest: {len(rankings['third_highest'])} user(s)")
        print(f"  Lowest: {len(rankings['lowest'])} user(s)")
        
        # Test processing a week without game results
        print(f"\nTesting week processing without game results...")
        result = skins_game.process_week(current_week)
        
        print(f"✅ Week processing successful!")
        print(f"Result keys: {list(result.keys())}")
        
        # Test processing with game results (if example file exists)
        example_file = f"week_{current_week}_game_results_example.json"
        try:
            with open(example_file, 'r') as f:
                game_results = json.load(f)
            
            print(f"\nTesting week processing with game results...")
            result_with_games = skins_game.process_week(current_week, game_results)
            
            print(f"✅ Week processing with game results successful!")
            if result_with_games['perfect_week_winners']:
                print(f"Perfect week winners: {result_with_games['perfect_week_winners']}")
            else:
                print("No perfect week winners")
                
        except FileNotFoundError:
            print(f"📝 No example game results file found ({example_file})")
            print(f"   Perfect week detection test skipped")
        
        # View all results
        print(f"\n📊 All stored results:")
        skins_game.view_all_results()
        
        print(f"\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simplified_system()
