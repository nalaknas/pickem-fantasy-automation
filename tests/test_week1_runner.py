#!/usr/bin/env python3
"""
Test Weekly Runner with Week 1 using Last Season Data
"""

from skins_game_mvp import SleeperSkinsGameMVP
import json
import os

def test_week1_with_old_league():
    print("🏈 TESTING WEEK 1 WITH LAST SEASON DATA 🏈")
    print("=" * 50)
    
    # Use last season's league ID for testing Week 1
    old_league_id = "1137502853016403968"  # Last season
    skins_game = SleeperSkinsGameMVP(old_league_id)
    
    try:
        target_week = 1
        print(f"📅 Processing Week: {target_week}")
        
        # Get league info
        league_info = skins_game.get_league_info()
        print(f"League: {league_info.get('name', 'Unknown')}")
        print(f"Season: {league_info.get('season', 'Unknown')}")
        
        # Check if odds file exists
        odds_filename = f"week_{target_week}_odds_template.json"
        
        if not os.path.exists(odds_filename):
            print(f"❌ {odds_filename} not found!")
            return
        
        # Load odds data
        print(f"📊 Loading odds data from {odds_filename}...")
        with open(odds_filename, 'r') as f:
            full_data = json.load(f)
            print(f"Debug: Keys in file: {list(full_data.keys())}")
            odds_data = full_data[f'week_{target_week}_odds']
            print(f"Debug: Loaded {len(odds_data)} games")
        
        # Remove the note field if it exists
        if 'note' in odds_data:
            del odds_data['note']
            print(f"Debug: Removed 'note' field, now {len(odds_data)} games")
        
        # Validate odds data
        if not odds_data:
            print(f"⚠️  {odds_filename} appears to be empty")
            return
        
        # Check if it's just a template (has only the note field)
        if len(odds_data) == 1 and odds_data.get('note'):
            print(f"⚠️  {odds_filename} appears to be just a template")
            return
        
        # Process the week
        print(f"🔄 Processing Week {target_week}...")
        result = skins_game.process_week(target_week, odds_data)
        
        # Show results summary
        print(f"\n🎉 WEEK {target_week} RESULTS PROCESSED!")
        print(f"📊 High Score Winner(s): {', '.join(result['winner_names']['high_score'])} - {result['high_score']} points")
        if 'underdog_percentage' in result:
            print(f"🐕 Underdog Winner(s): {', '.join(result['winner_names']['underdog'])} - {result['underdog_percentage']:.1f}% correct")
        else:
            # Handle old format for backward compatibility
            print(f"🐕 Underdog Winner(s): {', '.join(result['winner_names']['underdog'])} - {result.get('underdog_correct', 0)}/{result['total_underdog_games']} correct")
        
        # Show all stored results
        print(f"\n📈 ALL STORED RESULTS:")
        skins_game.view_all_results()
        
        print(f"\n✅ Week {target_week} processing complete!")
        print(f"📁 Results saved to: skins_game_results.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_week1_with_old_league()
