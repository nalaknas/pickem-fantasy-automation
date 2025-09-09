#!/usr/bin/env python3
"""
Debug script to check the Sleeper API data for the new league ID
"""

import requests
from secure_config import config
import json

def debug_league_data():
    league_id = config.sleeper_league_id
    base_url = "https://api.sleeper.app/v1"
    
    print(f"🔍 Debugging League ID: {league_id}")
    print("=" * 50)
    
    # Check league info
    try:
        url = f"{base_url}/league/{league_id}"
        response = requests.get(url)
        
        if response.status_code == 200:
            league_info = response.json()
            print("✅ League Info Retrieved:")
            print(f"  Name: {league_info.get('name', 'Unknown')}")
            print(f"  Season: {league_info.get('season', 'Unknown')}")
            print(f"  Status: {league_info.get('status', 'Unknown')}")
            print(f"  Current Pickem Leg: {league_info.get('metadata', {}).get('current_pickem_leg_id', 'None')}")
            print()
        else:
            print(f"❌ Failed to get league info: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error getting league info: {e}")
        return
    
    # Check users
    try:
        url = f"{base_url}/league/{league_id}/users"
        response = requests.get(url)
        
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Users Retrieved: {len(users)} users")
            print("  Sample users:")
            for i, user in enumerate(users[:5]):
                print(f"    {i+1}. {user.get('display_name', 'Unknown')} (ID: {user.get('user_id', 'Unknown')})")
            print()
        else:
            print(f"❌ Failed to get users: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error getting users: {e}")
        return
    
    # Check rosters
    try:
        url = f"{base_url}/league/{league_id}/rosters"
        response = requests.get(url)
        
        if response.status_code == 200:
            rosters = response.json()
            print(f"✅ Rosters Retrieved: {len(rosters)} rosters")
            
            # Check for pickem data
            print("  Checking for pickem data...")
            for i, roster in enumerate(rosters[:3]):
                if roster is None:
                    print(f"    Roster {i+1}: None/Empty")
                    continue
                    
                owner_id = roster.get('owner_id')
                metadata = roster.get('metadata', {})
                points_by_leg = metadata.get('points_by_leg', {}) if metadata else {}
                previous_picks = metadata.get('previous_picks', {}) if metadata else {}
                
                print(f"    Roster {i+1} (Owner: {owner_id}):")
                print(f"      Points by leg: {len(points_by_leg)} entries")
                print(f"      Previous picks: {len(previous_picks)} entries")
                
                if points_by_leg:
                    print(f"      Sample points: {dict(list(points_by_leg.items())[:2])}")
                if previous_picks:
                    print(f"      Sample picks: {dict(list(previous_picks.items())[:2])}")
            print()
        else:
            print(f"❌ Failed to get rosters: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error getting rosters: {e}")
        return
    
    print("🎯 Summary:")
    print(f"  League: {league_info.get('name', 'Unknown')}")
    print(f"  Season: {league_info.get('season', 'Unknown')}")
    print(f"  Users: {len(users)}")
    print(f"  Rosters: {len(rosters)}")
    print(f"  Current Week: {league_info.get('metadata', {}).get('current_pickem_leg_id', 'Unknown')}")

if __name__ == "__main__":
    debug_league_data()
