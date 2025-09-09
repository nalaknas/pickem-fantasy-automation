#!/usr/bin/env python3
"""
Results Viewer - Clean organized view of skins game results
"""

import json
from datetime import datetime
from collections import defaultdict

def view_results():
    """Display organized results by season and week"""
    
    try:
        with open('data/skins_game_results.json', 'r') as f:
            results = json.load(f)
    except FileNotFoundError:
        print("❌ No results file found")
        return
    
    if not results:
        print("📊 No results stored yet")
        return
    
    # Group by season
    seasons = defaultdict(list)
    for result in results:
        seasons[result['season']].append(result)
    
    print("🏈 SKINS GAME RESULTS SUMMARY 🏈")
    print("=" * 50)
    
    for season in sorted(seasons.keys(), key=int):
        season_results = seasons[season]
        season_results.sort(key=lambda x: int(x['week']))
        
        print(f"\n📅 SEASON {season}")
        print("-" * 30)
        
        for result in season_results:
            week = result['week']
            print(f"\nWeek {week}:")
            
            # Handle new format
            if 'rankings' in result:
                print(f"  🥇 Highest: {', '.join(result['winner_names']['highest'])} - {result['scores']['highest']} pts")
                if result['rankings']['second_highest']:
                    print(f"  🥈 Second: {', '.join(result['winner_names']['second_highest'])} - {result['scores']['second_highest']} pts")
                if result['rankings']['third_highest']:
                    print(f"  🥉 Third: {', '.join(result['winner_names']['third_highest'])} - {result['scores']['third_highest']} pts")
                print(f"  📉 Lowest: {', '.join(result['winner_names']['lowest'])} - {result['scores']['lowest']} pts")
                
                if result['rankings'].get('no_picks'):
                    print(f"  ❌ No Picks: {', '.join(result['winner_names']['no_picks'])}")
                
                # Always show perfect week line, even if empty
                if result['perfect_week_winners']:
                    print(f"  🎯 Perfect Week: {', '.join(result['winner_names']['perfect_week'])}")
                else:
                    print(f"  🎯 Perfect Week: ")
            
            # Handle old format
            else:
                print(f"  📊 High Score: {', '.join(result['winner_names']['high_score'])} - {result['high_score']} pts")
                if 'underdog_percentage' in result:
                    print(f"  🐕 Underdog: {', '.join(result['winner_names']['underdog'])} - {result['underdog_percentage']:.1f}% correct")
                else:
                    print(f"  🐕 Underdog: {', '.join(result['winner_names']['underdog'])} - {result.get('underdog_correct', 0)}/{result['total_underdog_games']} correct")
            
            # Show processing date
            try:
                date_str = result['date_processed']
                if 'T' in date_str:
                    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    print(f"  📅 Processed: {date_obj.strftime('%Y-%m-%d %H:%M')}")
            except:
                pass

def view_season_summary():
    """Show summary statistics by season"""
    
    try:
        with open('data/skins_game_results.json', 'r') as f:
            results = json.load(f)
    except FileNotFoundError:
        print("❌ No results file found")
        return
    
    if not results:
        print("📊 No results stored yet")
        return
    
    # Group by season
    seasons = defaultdict(list)
    for result in results:
        seasons[result['season']].append(result)
    
    print("📊 SEASON SUMMARY")
    print("=" * 30)
    
    for season in sorted(seasons.keys(), key=int):
        season_results = seasons[season]
        print(f"\n🏈 Season {season}:")
        print(f"  📅 Weeks processed: {len(season_results)}")
        
        # Count winners by category
        high_score_winners = set()
        perfect_weeks = set()
        
        for result in season_results:
            if 'rankings' in result:
                high_score_winners.update(result['rankings']['highest'])
                perfect_weeks.update(result['perfect_week_winners'])
            else:
                high_score_winners.update(result['high_score_winners'])
        
        print(f"  🥇 Unique high score winners: {len(high_score_winners)}")
        print(f"  🎯 Perfect weeks achieved: {len(perfect_weeks)}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "summary":
        view_season_summary()
    else:
        view_results()
