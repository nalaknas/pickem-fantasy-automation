#!/usr/bin/env python3
"""
Minimal test to isolate the exact error
"""

from skins_game_mvp import SleeperSkinsGameMVP
import json

def minimal_test():
    print("🔍 MINIMAL TEST")
    print("=" * 20)
    
    league_id = "1267183695911976960"
    skins_game = SleeperSkinsGameMVP(league_id)
    
    try:
        # Load odds data
        with open('week_1_odds_template.json', 'r') as f:
            full_data = json.load(f)
            odds_data = full_data['week_1_odds']
        
        # Remove note field
        if 'note' in odds_data:
            del odds_data['note']
        
        print("Calling process_week...")
        result = skins_game.process_week(1, odds_data)
        print("✅ Success!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    minimal_test()
