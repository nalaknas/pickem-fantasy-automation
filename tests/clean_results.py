#!/usr/bin/env python3
"""
Clean and organize the skins game results
"""

import json
from datetime import datetime
from collections import defaultdict

def clean_and_organize_results():
    """Clean up duplicate results and organize by week/season"""
    
    # Load current results
    try:
        with open('skins_game_results.json', 'r') as f:
            results = json.load(f)
    except FileNotFoundError:
        print("No results file found")
        return
    
    print(f"📊 Found {len(results)} total entries")
    
    # Group by week and season to find duplicates
    grouped_results = defaultdict(list)
    for result in results:
        key = f"{result['season']}-{result['week']}"
        grouped_results[key].append(result)
    
    # Keep only the most recent entry for each week/season
    cleaned_results = []
    duplicates_removed = 0
    
    for key, week_results in grouped_results.items():
        if len(week_results) > 1:
            # Sort by date_processed and keep the most recent
            week_results.sort(key=lambda x: x['date_processed'], reverse=True)
            duplicates_removed += len(week_results) - 1
            print(f"🔄 Week {week_results[0]['week']} ({week_results[0]['season']}): Removed {len(week_results) - 1} duplicate(s)")
        
        cleaned_results.append(week_results[0])
    
    # Sort by season and week
    cleaned_results.sort(key=lambda x: (int(x['season']), int(x['week'])))
    
    print(f"✅ Removed {duplicates_removed} duplicate entries")
    print(f"📈 Kept {len(cleaned_results)} unique entries")
    
    # Create backup
    backup_filename = f"skins_game_results_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(backup_filename, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"💾 Created backup: {backup_filename}")
    
    # Save cleaned results
    with open('skins_game_results.json', 'w') as f:
        json.dump(cleaned_results, f, indent=2)
    
    print(f"✨ Results cleaned and organized!")
    
    # Show summary
    print(f"\n📋 SUMMARY BY SEASON:")
    season_counts = defaultdict(int)
    for result in cleaned_results:
        season_counts[result['season']] += 1
    
    for season in sorted(season_counts.keys(), key=int):
        print(f"  {season}: {season_counts[season]} weeks")

if __name__ == "__main__":
    clean_and_organize_results()
