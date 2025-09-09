#!/usr/bin/env python3
"""
Debug script to see what picks users made and why perfect week detection isn't working
"""

from skins_game_mvp import SleeperSkinsGameMVP
import json

def debug_perfect_week():
    """Debug perfect week detection"""
    
    league_id = "1267183695911976960"
    skins_game = SleeperSkinsGameMVP(league_id)
    
    week = 1
    
    # Get user picks
    user_picks = skins_game.get_week_picks(week)
    print(f"📊 User picks for Week {week}:")
    
    for owner_id, picks in user_picks.items():
        if picks:  # Only show users who made picks
            users = skins_game.get_users()
            user_name = users.get(owner_id, {}).get('display_name', 'Unknown')
            print(f"  {user_name}: {picks}")
    
    # Load game results
    try:
        with open(f'week_{week}_game_results.json', 'r') as f:
            game_results = json.load(f)
        
        print(f"\n🎮 Game results for Week {week}:")
        winning_teams = [team for team, data in game_results.items() if data.get('won', False)]
        print(f"  Winning teams: {winning_teams}")
        
        # Check perfect week
        perfect_week_winners = skins_game.check_perfect_week(week, game_results)
        print(f"\n🎯 Perfect week winners: {perfect_week_winners}")
        
        if not perfect_week_winners:
            print("  No perfect weeks found. Reasons could be:")
            print("  - Users didn't pick all games")
            print("  - Users' picks don't match the game results")
            print("  - Game results don't reflect actual NFL results")
        
    except FileNotFoundError:
        print(f"❌ No game results file found for Week {week}")

if __name__ == "__main__":
    debug_perfect_week()
