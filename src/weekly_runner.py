#!/usr/bin/env python3
"""
Weekly Skins Game Runner
========================

Simple script to run every week to process your Sleeper skins game results.
Just update the odds data and run this script!

Usage:
1. Fill in the odds template for the current week
2. Run: python3 weekly_runner.py
3. View your results!

"""

from .skins_game_mvp import SleeperSkinsGameMVP
from .export_results import SkinsGameExporter

# Handle both relative and absolute imports
try:
    from .secure_config import config
except ImportError:
    from secure_config import config

import json
import os
from datetime import datetime

def main():
    print("🏈 WEEKLY SKINS GAME RUNNER 🏈")
    print("=" * 50)
    
    # Initialize with secure configuration
    skins_game = SleeperSkinsGameMVP()
    
    try:
        # Check if week is specified as command line argument
        import sys
        if len(sys.argv) > 1 and sys.argv[1].isdigit():
            target_week = int(sys.argv[1])
            print(f"📅 Processing Week: {target_week} (specified)")
        else:
            # Get current week and process previous week
            current_week = skins_game.get_current_week()
            target_week = current_week - 1
            print(f"📅 Current Week: {current_week}")
            print(f"📅 Processing Previous Week: {target_week} (auto-detected)")
        
        # Check if game results file exists (optional, only needed for perfect week detection)
        game_results_filename = f"data/week_{target_week}_game_results.json"
        game_results_data = None
        
        if os.path.exists(game_results_filename):
            print(f"📊 Loading game results from {game_results_filename}...")
            with open(game_results_filename, 'r') as f:
                game_results_data = json.load(f)
            print(f"✅ Game results loaded for perfect week detection")
        else:
            print(f"📝 No game results file found ({game_results_filename})")
            print(f"   Perfect week detection will be skipped")
            print(f"   Rankings will still be calculated based on scores")
        
        # Process the week
        print(f"🔄 Processing Week {target_week}...")
        
        # Check if there's pickem data available
        try:
            # Try to get a summary to check if data exists
            summary = skins_game.get_week_summary(target_week)
            if summary['high_score'] == 0 and not any(user['score'] > 0 for user in summary['user_data']):
                print(f"⚠️  No pickem data available for Week {target_week}")
                print(f"   This is normal early in the season before games are played")
                print(f"   The system is ready to process once games are completed")
                return
        except Exception as e:
            print(f"⚠️  No pickem data available for Week {target_week}")
            print(f"   This is normal early in the season before games are played")
            print(f"   The system is ready to process once games are completed")
            return
        
        result = skins_game.process_week(target_week, game_results_data)
        
        # Show just the current week's results
        print(f"\n📈 CURRENT WEEK RESULTS:")
        
        # Handle new format
        if 'rankings' in result:
            print(f"🥇 Highest Scorer(s): {', '.join(result['winner_names']['highest'])} - {result['scores']['highest']} points")
            if result['rankings']['second_highest']:
                print(f"🥈 Second Highest: {', '.join(result['winner_names']['second_highest'])} - {result['scores']['second_highest']} points")
            if result['rankings']['third_highest']:
                print(f"🥉 Third Highest: {', '.join(result['winner_names']['third_highest'])} - {result['scores']['third_highest']} points")
            print(f"📉 Lowest Scorer(s): {', '.join(result['winner_names']['lowest'])} - {result['scores']['lowest']} points")
            
            if result['rankings'].get('no_picks'):
                print(f"❌ No Picks Submitted: {', '.join(result['winner_names']['no_picks'])}")
            
            # Always show perfect week line, even if empty
            if result['perfect_week_winners']:
                print(f"🎯 Perfect Week: {', '.join(result['winner_names']['perfect_week'])}")
            else:
                print(f"🎯 Perfect Week: ")
        
        # Handle old format for backward compatibility
        else:
            print(f"📊 High Score Winner(s): {', '.join(result['winner_names']['high_score'])} - {result['high_score']} points")
            if 'underdog_percentage' in result:
                print(f"🐕 Underdog Winner(s): {', '.join(result['winner_names']['underdog'])} - {result['underdog_percentage']:.1f}% correct")
            else:
                print(f"🐕 Underdog Winner(s): {', '.join(result['winner_names']['underdog'])} - {result.get('underdog_correct', 0)}/{result['total_underdog_games']} correct")
        
        print(f"\n✅ Week {target_week} processing complete!")
        print(f"📁 Results saved to: data/skins_game_results.json")
        
        # Export to CSV/Excel for easy sharing
        print(f"📊 Exporting season report...")
        exporter = SkinsGameExporter()
        if exporter.export_all():
            print(f"📈 Season report exported: skins_game_season_report.csv & .xlsx")
        else:
            print(f"⚠️  Export failed, but results are still saved")
        
        # Optional: Show all results if requested
        import sys
        if len(sys.argv) > 2 and sys.argv[2] == "--show-all":
            print(f"\n📈 ALL STORED RESULTS:")
            skins_game.view_all_results()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        print(f"\n🔧 Troubleshooting:")
        print(f"1. Make sure your league ID is correct")
        print(f"2. Verify your internet connection")
        print(f"3. Check that pickem data is available for the week")
        print(f"\n💡 Usage:")
        print(f"  python3 main.py                            # Process previous week (auto-detect)")
        print(f"  python3 main.py 1                          # Process Week 1")
        print(f"  python3 main.py 1 --show-all               # Process Week 1 and show all results")
        print(f"  python3 main.py status                     # Quick status check")
        print(f"\n📝 Optional: Create week_X_game_results.json for perfect week detection")

def quick_status():
    """Quick status check without processing"""
    print("🔍 QUICK STATUS CHECK")
    print("=" * 30)
    
    skins_game = SleeperSkinsGameMVP()
    
    try:
        current_week = skins_game.get_current_week()
        league_info = skins_game.get_league_info()
        
        print(f"League: {league_info.get('name', 'Unknown')}")
        print(f"Season: {league_info.get('season', 'Unknown')}")
        print(f"Current Week: {current_week}")
        
        # Check for game results file (optional)
        game_results_filename = f"data/week_{current_week}_game_results.json"
        if os.path.exists(game_results_filename):
            print(f"✅ Game results file exists: {game_results_filename}")
        else:
            print(f"📝 No game results file: {game_results_filename} (perfect week detection will be skipped)")
        
        # Check for results
        if os.path.exists("data/skins_game_results.json"):
            with open("data/skins_game_results.json", 'r') as f:
                results = json.load(f)
            print(f"📊 Stored results: {len(results)} weeks")
        else:
            print(f"📊 No stored results yet")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        quick_status()
    else:
        main()
