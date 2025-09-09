#!/usr/bin/env python3
"""
Test Weekly Runner with Your Filled Week 1 Data
"""

from skins_game_mvp import SleeperSkinsGameMVP
import json

def test_with_your_week1_data():
    print("🏈 TESTING WITH YOUR WEEK 1 DATA 🏈")
    print("=" * 50)
    
    # Use last season's league ID for testing (since it has data)
    old_league_id = "1137502853016403968"  # Last season
    skins_game = SleeperSkinsGameMVP(old_league_id)
    
    try:
        # Force week 1 for testing
        test_week = 1
        print(f"📅 Testing Week: {test_week}")
        
        # Get league info
        league_info = skins_game.get_league_info()
        print(f"League: {league_info.get('name', 'Unknown')}")
        print(f"Season: {league_info.get('season', 'Unknown')}")
        
        # Load your filled-in odds data
        odds_filename = f"week_{test_week}_odds_template.json"
        print(f"📊 Loading odds data from {odds_filename}...")
        
        with open(odds_filename, 'r') as f:
            odds_data = json.load(f)[f'week_{test_week}_odds']
        
        # Remove the note field for processing
        if 'note' in odds_data:
            del odds_data['note']
        
        print(f"✅ Loaded {len(odds_data)} games")
        
        # Show some sample data
        print(f"\n📋 Sample Games:")
        game_count = 0
        for team, data in odds_data.items():
            if game_count < 4:  # Show first 4 games
                opponent = data['opponent']
                result = "✅ WON" if data['won'] else "❌ LOST"
                underdog = "🐕 UNDERDOG" if data['is_underdog'] else "🏆 FAVORITE"
                print(f"  {team} vs {opponent}: {result} ({underdog})")
                game_count += 1
        
        # Calculate underdog statistics
        underdog_teams = [team for team, data in odds_data.items() if data.get('is_underdog', False)]
        underdog_winners = [team for team in underdog_teams if odds_data[team].get('won', False)]
        
        print(f"\n📈 UNDERDOG STATISTICS:")
        print(f"  Total underdog games: {len(underdog_teams)}")
        print(f"  Underdog wins: {len(underdog_winners)}")
        print(f"  Underdog win rate: {len(underdog_winners)/len(underdog_teams)*100:.1f}%")
        print(f"  Underdog winners: {underdog_winners}")
        
        # Process the week
        print(f"\n🔄 Processing Week {test_week}...")
        result = skins_game.process_week(test_week, odds_data)
        
        # Show results summary
        print(f"\n🎉 WEEK {test_week} RESULTS PROCESSED!")
        print(f"📊 High Score Winner(s): {', '.join(result['winner_names']['high_score'])} - {result['high_score']} points")
        if 'underdog_percentage' in result:
            print(f"🐕 Underdog Winner(s): {', '.join(result['winner_names']['underdog'])} - {result['underdog_percentage']:.1f}% correct")
        else:
            print(f"🐕 Underdog Winner(s): {', '.join(result['winner_names']['underdog'])} - {result.get('underdog_correct', 0)}/{result['total_underdog_games']} correct")
        
        # Show all stored results
        print(f"\n📈 ALL STORED RESULTS:")
        skins_game.view_all_results()
        
        print(f"\n✅ Week {test_week} processing complete!")
        print(f"📁 Results saved to: skins_game_results.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_with_your_week1_data()
