#!/usr/bin/env python3
"""
Test process_week method step by step
"""

from skins_game_mvp import SleeperSkinsGameMVP
import json

def test_process_week():
    print("🔍 TESTING PROCESS_WEEK METHOD")
    print("=" * 40)
    
    # Use 2025 league ID
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
        
        print(f"Loaded {len(odds_data)} games")
        
        # Test each step
        print("1. Testing get_users...")
        users = skins_game.get_users()
        print(f"✅ Got {len(users)} users")
        
        print("2. Testing calculate_highest_scorer...")
        high_score_winners, high_score = skins_game.calculate_highest_scorer(1)
        print(f"✅ High score: {high_score}, Winners: {high_score_winners}")
        
        print("3. Testing calculate_underdog_winners...")
        underdog_winners, underdog_percentage, total_underdog_games = skins_game.calculate_underdog_winners(1, odds_data)
        print(f"✅ Underdog: {underdog_percentage:.1f}%, Winners: {len(underdog_winners)}")
        
        print("4. Testing check_perfect_week...")
        perfect_week_winners = skins_game.check_perfect_week(1, odds_data)
        print(f"✅ Perfect week winners: {perfect_week_winners}")
        
        print("5. Testing process_week...")
        result = skins_game.process_week(1, odds_data)
        print(f"✅ Process week successful!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_process_week()
