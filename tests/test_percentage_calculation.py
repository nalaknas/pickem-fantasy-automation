#!/usr/bin/env python3
"""
Test the new percentage-based underdog calculation
"""

from skins_game_mvp import SleeperSkinsGameMVP
import json

def test_percentage_calculation():
    print("🏈 TESTING PERCENTAGE-BASED UNDERDOG CALCULATION 🏈")
    print("=" * 60)
    
    # Use last season's league ID for testing
    old_league_id = "1137502853016403968"
    skins_game = SleeperSkinsGameMVP(old_league_id)
    
    try:
        test_week = 1
        print(f"📅 Testing Week: {test_week}")
        
        # Create example odds data with different scenarios
        example_odds = {
            # Game 1: DAL (underdog) vs PHI (favorite)
            "DAL": {"opponent": "PHI", "is_underdog": True, "won": False},
            "PHI": {"opponent": "DAL", "is_underdog": False, "won": True},
            
            # Game 2: KC (favorite) vs LAC (underdog) - UNDERDOG WINS!
            "KC": {"opponent": "LAC", "is_underdog": False, "won": False},
            "LAC": {"opponent": "KC", "is_underdog": True, "won": True},
            
            # Game 3: TB (favorite) vs ATL (underdog)
            "TB": {"opponent": "ATL", "is_underdog": False, "won": True},
            "ATL": {"opponent": "TB", "is_underdog": True, "won": False},
            
            # Game 4: CIN (favorite) vs CLE (underdog)
            "CIN": {"opponent": "CLE", "is_underdog": False, "won": True},
            "CLE": {"opponent": "CIN", "is_underdog": True, "won": False},
            
            # Game 5: MIA (underdog) vs IND (favorite)
            "MIA": {"opponent": "IND", "is_underdog": True, "won": False},
            "IND": {"opponent": "MIA", "is_underdog": False, "won": True},
            
            # Game 6: CAR (underdog) vs JAX (favorite) - UNDERDOG WINS!
            "CAR": {"opponent": "JAX", "is_underdog": True, "won": True},
            "JAX": {"opponent": "CAR", "is_underdog": False, "won": False},
        }
        
        print("📊 Example Games:")
        underdog_teams = [team for team, data in example_odds.items() if data.get('is_underdog', False)]
        underdog_winners = [team for team in underdog_teams if example_odds[team].get('won', False)]
        
        print(f"  Total underdog games: {len(underdog_teams)}")
        print(f"  Underdog wins: {len(underdog_winners)}")
        print(f"  Underdog winners: {underdog_winners}")
        
        for team in underdog_teams:
            result = "✅ WON" if example_odds[team]['won'] else "❌ LOST"
            print(f"    {team}: {result}")
        
        # Get user picks to simulate different scenarios
        user_picks = skins_game.get_week_picks(test_week)
        
        print(f"\n👥 User Underdog Pick Analysis:")
        print("=" * 40)
        
        user_underdog_stats = {}
        
        for owner_id, picks in user_picks.items():
            if not picks:  # Skip users with no picks
                continue
                
            # Count underdog picks and correct ones
            user_underdog_picks = [pick for pick in picks if pick in underdog_teams]
            user_underdog_correct = [pick for pick in user_underdog_picks if pick in underdog_winners]
            
            if len(user_underdog_picks) > 0:
                percentage = len(user_underdog_correct) / len(user_underdog_picks) * 100
                user_underdog_stats[owner_id] = {
                    'total_underdog_picks': len(user_underdog_picks),
                    'correct_underdog_picks': len(user_underdog_correct),
                    'percentage': percentage,
                    'picks': user_underdog_picks,
                    'correct_picks': user_underdog_correct
                }
        
        # Sort by percentage
        sorted_users = sorted(user_underdog_stats.items(), key=lambda x: x[1]['percentage'], reverse=True)
        
        print("Ranking by Underdog Pick Percentage:")
        for i, (owner_id, stats) in enumerate(sorted_users[:5], 1):  # Show top 5
            user_info = skins_game.get_users().get(owner_id, {})
            display_name = user_info.get('display_name', 'Unknown')
            
            print(f"  {i}. {display_name}: {stats['correct_underdog_picks']}/{stats['total_underdog_picks']} = {stats['percentage']:.1f}%")
            print(f"     Picks: {stats['picks']}")
            print(f"     Correct: {stats['correct_picks']}")
        
        # Test the actual calculation
        print(f"\n🔄 Testing MVP Calculation...")
        underdog_winners, underdog_percentage, total_underdog_games = skins_game.calculate_underdog_winners(test_week, example_odds)
        
        print(f"✅ MVP Results:")
        print(f"  Winners: {underdog_winners}")
        print(f"  Percentage: {underdog_percentage:.1f}%")
        print(f"  Total underdog games: {total_underdog_games}")
        
        # Show the difference between old and new system
        print(f"\n📈 SYSTEM COMPARISON:")
        print("OLD SYSTEM (Raw Count):")
        # Calculate old way
        user_underdog_correct_old = {}
        for owner_id, picks in user_picks.items():
            if picks:
                correct_underdogs = len([pick for pick in picks if pick in underdog_winners])
                user_underdog_correct_old[owner_id] = correct_underdogs
        
        if user_underdog_correct_old:
            max_correct_old = max(user_underdog_correct_old.values())
            winners_old = [owner_id for owner_id, correct in user_underdog_correct_old.items() if correct == max_correct_old]
            print(f"  Winners: {winners_old} (with {max_correct_old} correct)")
        
        print("NEW SYSTEM (Percentage):")
        print(f"  Winners: {underdog_winners} (with {underdog_percentage:.1f}% correct)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_percentage_calculation()
