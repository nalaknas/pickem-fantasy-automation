#!/usr/bin/env python3
"""
Current League Status and Example Output
"""

from skins_game_mvp import SleeperSkinsGameMVP
import json

def show_current_league_status():
    # Initialize with correct league ID
    league_id = "1267183695911976960"  # Current season league ID
    skins_game = SleeperSkinsGameMVP(league_id)
    
    print("🏈 CURRENT LEAGUE STATUS 🏈")
    print("=" * 50)
    
    try:
        # Get league info
        league_info = skins_game.get_league_info()
        print(f"League: {league_info.get('name', 'Unknown')}")
        print(f"Season: {league_info.get('season', 'Unknown')}")
        print(f"Status: {league_info.get('status', 'Unknown')}")
        
        # Get current week
        current_week = skins_game.get_current_week()
        print(f"Current Week: {current_week}")
        
        # Get users
        users = skins_game.get_users()
        print(f"Total Users: {len(users)}")
        
        print("\n👥 LEAGUE MEMBERS:")
        for i, (user_id, user_info) in enumerate(users.items(), 1):
            display_name = user_info.get('display_name', 'Unknown')
            username = user_info.get('username', 'Unknown')
            print(f"  {i:2d}. {display_name} (@{username})")
        
        # Check if there's any pickem data
        rosters = skins_game.get_rosters()
        print(f"\n📊 PICKEM DATA STATUS:")
        print(f"Total Rosters: {len(rosters)}")
        
        # Check for any pickem data
        has_data = False
        for roster in rosters:
            if roster and roster.get('metadata'):
                metadata = roster['metadata']
                if metadata.get('points_by_leg') or metadata.get('previous_picks'):
                    has_data = True
                    break
        
        if has_data:
            print("✅ Pickem data found - can calculate results")
            # Show week summary
            summary = skins_game.get_week_summary(current_week)
            print(f"\nWeek {current_week} Summary:")
            print(f"High Score: {summary['high_score']} points")
            
            for user_data in summary['user_data']:
                if user_data['score'] > 0:  # Only show users with scores
                    print(f"  {user_data['display_name']}: {user_data['score']} pts")
        else:
            print("⚠️  No pickem data yet - league is just starting")
            print("   This is normal for Week 1 before games are played")
        
        # Create odds template for the current week
        print(f"\n📝 Creating odds template for Week {current_week}...")
        template = skins_game.create_odds_template(current_week)
        
        print("\n🎯 NEXT STEPS:")
        print("1. Wait for Week 1 games to be played")
        print("2. Fill in the odds template with actual results")
        print("3. Run the processing to calculate winners")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def demonstrate_underdog_calculation():
    """Show how underdog calculations would work with example data"""
    print("\n" + "="*50)
    print("🐕 UNDERDOG CALCULATION EXAMPLE")
    print("="*50)
    
    # Example odds data (you would fill this in manually)
    example_odds = {
        "ARI": {"opponent": "LAR", "is_underdog": True, "won": False},
        "LAR": {"opponent": "ARI", "is_underdog": False, "won": True},
        "ATL": {"opponent": "PHI", "is_underdog": True, "won": True},  # Underdog win!
        "PHI": {"opponent": "ATL", "is_underdog": False, "won": False},
        "BAL": {"opponent": "KC", "is_underdog": True, "won": False},
        "KC": {"opponent": "BAL", "is_underdog": False, "won": True},
        "DET": {"opponent": "GB", "is_underdog": True, "won": True},   # Another underdog win!
        "GB": {"opponent": "DET", "is_underdog": False, "won": False},
    }
    
    print("Example odds data:")
    for team, data in example_odds.items():
        status = "✅ WON" if data['won'] else "❌ LOST"
        underdog = "🐕 UNDERDOG" if data['is_underdog'] else "🏆 FAVORITE"
        print(f"  {team} vs {data['opponent']}: {status} ({underdog})")
    
    # Calculate underdog winners
    underdog_teams = [team for team, data in example_odds.items() if data.get('is_underdog', False)]
    underdog_winners = [team for team in underdog_teams if example_odds[team].get('won', False)]
    
    print(f"\nUnderdog teams: {underdog_teams}")
    print(f"Underdog winners: {underdog_winners}")
    print(f"Total underdog games: {len(underdog_teams)}")
    print(f"Underdog wins: {len(underdog_winners)}")
    
    print("\n📋 How to use this:")
    print("1. Fill in week_X_odds_template.json with actual game results")
    print("2. Set is_underdog=True for teams that were underdogs")
    print("3. Set won=True for teams that won their games")
    print("4. Run skins_game.process_week(week, odds_data)")

if __name__ == "__main__":
    success = show_current_league_status()
    if success:
        demonstrate_underdog_calculation()
