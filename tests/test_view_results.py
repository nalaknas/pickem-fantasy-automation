#!/usr/bin/env python3
"""
Test view_all_results method
"""

from skins_game_mvp import SleeperSkinsGameMVP
import json

def test_view_results():
    print("🔍 TESTING VIEW_ALL_RESULTS")
    print("=" * 30)
    
    league_id = "1267183695911976960"
    skins_game = SleeperSkinsGameMVP(league_id)
    
    try:
        print("Calling view_all_results...")
        skins_game.view_all_results()
        print("✅ Success!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_view_results()
