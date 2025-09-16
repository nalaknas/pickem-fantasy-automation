#!/usr/bin/env python3
"""
Generate Week 1 Apple Shortcuts Data
====================================

Creates Apple Shortcuts data specifically for Week 1 results.
"""

import json
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.apple_shortcuts import AppleShortcutsIntegration

def main():
    """Generate Week 1 data for Apple Shortcuts"""
    print("📱 GENERATING WEEK 1 APPLE SHORTCUTS DATA")
    print("=" * 50)
    
    # Load Week 1 results
    try:
        with open('data/skins_game_results.json', 'r') as f:
            results = json.load(f)
    except FileNotFoundError:
        print("❌ No results file found at data/skins_game_results.json")
        print("   Run 'python3 main.py' first to process a week")
        return
    except json.JSONDecodeError as e:
        print(f"❌ Error reading results file: {e}")
        print("   The file may be corrupted or invalid JSON")
        return
    
    # Find Week 1 results
    week1_results = None
    for result in results:
        if result.get('week') == 1:
            week1_results = result
            break
    
    if not week1_results:
        print("❌ No Week 1 results found")
        return
    
    print(f"✅ Found Week 1 results")
    print(f"Week: {week1_results.get('week')}")
    print(f"Season: {week1_results.get('season')}")
    
    # Create Apple Shortcuts integration
    integration = AppleShortcutsIntegration()
    
    # Format the data
    formatted_data = integration.format_for_shortcuts(week1_results)
    
    # Save to file
    os.makedirs('shortcuts', exist_ok=True)
    with open('shortcuts/shortcuts_week1.json', 'w') as f:
        json.dump(formatted_data, f, indent=2)
    
    print(f"✅ Week 1 data saved to shortcuts/shortcuts_week1.json")
    
    # Show preview
    print(f"\n📝 Message preview:")
    print("-" * 40)
    print(formatted_data['message_text'])
    print("-" * 40)
    
    print(f"\n📱 Next steps:")
    print(f"1. Transfer shortcuts/shortcuts_week1.json to your iPhone")
    print(f"2. Run your Apple Shortcut")
    print(f"3. Send to your group chat")

if __name__ == "__main__":
    main()
