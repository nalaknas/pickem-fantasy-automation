#!/usr/bin/env python3
"""
Test the underdog calculation specifically
"""

from skins_game_mvp import SleeperSkinsGameMVP
from secure_config import config
import json

def test_underdog_calc():
    print("🔍 TESTING UNDERDOG CALCULATION")
    print("=" * 40)
    
    # Use 2025 league ID
    league_id = config.sleeper_league_id
    skins_game = SleeperSkinsGameMVP(league_id)
    
    try:
        # Load odds data
        with open('week_1_odds_template.json', 'r') as f:
            full_data = json.load(f)
            odds_data = full_data['week_1_odds']
        
        # Remove note field
        if 'note' in odds_data:
            del odds_data['note']
        
        print(f"Loaded {len(odds_data)} games")
        
        # Test underdog calculation
        print("Testing calculate_underdog_winners...")
        underdog_winners, underdog_percentage, total_underdog_games = skins_game.calculate_underdog_winners(1, odds_data)
        
        print(f"✅ Underdog calculation successful!")
        print(f"Winners: {underdog_winners}")
        print(f"Percentage: {underdog_percentage:.1f}%")
        print(f"Total underdog games: {total_underdog_games}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_underdog_calc()
