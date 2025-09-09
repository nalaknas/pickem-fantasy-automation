#!/usr/bin/env python3
"""
Simple test to isolate the error
"""

from skins_game_mvp import SleeperSkinsGameMVP
import json

def test_simple():
    print("🔍 SIMPLE TEST")
    print("=" * 20)
    
    # Use 2025 league ID
    league_id = "1267183695911976960"
    skins_game = SleeperSkinsGameMVP(league_id)
    
    try:
        # Get current week
        current_week = skins_game.get_current_week()
        print(f"Current Week: {current_week}")
        
        # Get league info
        league_info = skins_game.get_league_info()
        print(f"League: {league_info.get('name', 'Unknown')}")
        print(f"Season: {league_info.get('season', 'Unknown')}")
        
        # Try to get week summary
        print(f"\nTrying to get Week 1 summary...")
        summary = skins_game.get_week_summary(1)
        print(f"Week 1 summary: {summary}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple()
