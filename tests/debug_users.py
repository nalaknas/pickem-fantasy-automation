#!/usr/bin/env python3
"""
Debug the users data structure
"""

from skins_game_mvp import SleeperSkinsGameMVP
from secure_config import config

def debug_users():
    print("🔍 DEBUGGING USERS DATA STRUCTURE")
    print("=" * 40)
    
    league_id = config.sleeper_league_id
    skins_game = SleeperSkinsGameMVP(league_id)
    
    try:
        users = skins_game.get_users()
        print(f"Total users: {len(users)}")
        
        # Check first few users
        for i, (user_id, user_data) in enumerate(users.items()):
            if i < 3:  # Show first 3
                print(f"User {i+1}:")
                print(f"  ID: {user_id}")
                print(f"  Type: {type(user_data)}")
                print(f"  Data: {user_data}")
                print()
        
        # Test the problematic line
        high_score_winners = ['1005271556681232384']  # kvstabla
        print("Testing winner name extraction:")
        for uid in high_score_winners:
            user_info = users.get(uid, {})
            print(f"  User ID: {uid}")
            print(f"  User info type: {type(user_info)}")
            print(f"  User info: {user_info}")
            if isinstance(user_info, dict):
                display_name = user_info.get('display_name', 'Unknown')
                print(f"  Display name: {display_name}")
            else:
                print(f"  ERROR: User info is not a dict!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_users()
