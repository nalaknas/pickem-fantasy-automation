#!/usr/bin/env python3
"""
Apple Shortcuts Integration for Sleeper Skins Game
================================================

Creates a webhook endpoint that Apple Shortcuts can call to get results
and then send them via iMessage. This runs on your phone!

"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

# Handle both relative and absolute imports
try:
    from .secure_config import config
except ImportError:
    from secure_config import config

class AppleShortcutsIntegration:
    """Handles Apple Shortcuts integration for iMessage notifications"""
    
    def __init__(self):
        """Initialize Apple Shortcuts integration"""
        self.results_file = f"{config.data_directory}/{config.results_file}"
        print("✅ Apple Shortcuts integration ready")
    
    def get_latest_results(self) -> Optional[Dict]:
        """Get the latest week's results for Apple Shortcuts"""
        try:
            with open(self.results_file, 'r') as f:
                results = json.load(f)
            
            if not results:
                return None
            
            # Get the most recent result
            latest_result = max(results, key=lambda x: x.get('week', 0))
            return latest_result
            
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"Error loading results: {e}")
            return None
    
    def create_sample_results(self, week: int = 1) -> Dict:
        """Create sample results for testing Apple Shortcuts"""
        return {
            'week': week,
            'season': 2025,
            'date_processed': datetime.now().isoformat(),
            'rankings': {
                'highest': ['user1'],
                'second_highest': ['user2'],
                'third_highest': ['user3'],
                'lowest': ['user4'],
                'no_picks': []
            },
            'scores': {
                'highest': 12.0,
                'second_highest': 10.0,
                'third_highest': 8.0,
                'lowest': 2.0
            },
            'perfect_week_winners': [],
            'winner_names': {
                'highest': ['John'],
                'second_highest': ['Sarah'],
                'third_highest': ['Mike'],
                'lowest': ['Tom'],
                'no_picks': [],
                'perfect_week': []
            }
        }
    
    def format_for_shortcuts(self, result: Dict) -> Dict:
        """
        Format results for Apple Shortcuts consumption
        
        Args:
            result: The processed week result
        
        Returns:
            Dictionary with formatted data for Shortcuts
        """
        week = result.get('week', 'Unknown')
        season = result.get('season', 'Unknown')
        
        # Format winners
        winners = {
            'highest': ', '.join(result['winner_names']['highest']) if result['winner_names']['highest'] else 'None',
            'second_highest': ', '.join(result['winner_names']['second_highest']) if result['winner_names']['second_highest'] else 'None',
            'third_highest': ', '.join(result['winner_names']['third_highest']) if result['winner_names']['third_highest'] else 'None',
            'lowest': ', '.join(result['winner_names']['lowest']) if result['winner_names']['lowest'] else 'None',
            'perfect_week': ', '.join(result['winner_names']['perfect_week']) if result['winner_names']['perfect_week'] else 'None'
        }
        
        # Format scores
        scores = {
            'highest': result['scores']['highest'],
            'second_highest': result['scores']['second_highest'],
            'third_highest': result['scores']['third_highest'],
            'lowest': result['scores']['lowest']
        }
        
        # Create iMessage-ready text
        message_text = f"🏈 {config.league_name} - Week {week} Results 🏈\n\n"
        
        if winners['highest'] != 'None':
            message_text += f"🥇 Highest Scorer: {winners['highest']} - {scores['highest']} points\n"
        
        if winners['second_highest'] != 'None':
            message_text += f"🥈 Second Highest: {winners['second_highest']} - {scores['second_highest']} points\n"
        
        if winners['third_highest'] != 'None':
            message_text += f"🥉 Third Highest: {winners['third_highest']} - {scores['third_highest']} points\n"
        
        if winners['lowest'] != 'None':
            message_text += f"📉 Lowest Scorer: {winners['lowest']} - {scores['lowest']} points\n"
        
        if winners['perfect_week'] != 'None':
            message_text += f"🎯 Perfect Week: {winners['perfect_week']} 🎉\n"
        
        message_text += f"\nSeason {season} • Week {week}\nGood luck next week! 🍀"
        
        return {
            'week': week,
            'season': season,
            'winners': winners,
            'scores': scores,
            'message_text': message_text,
            'timestamp': datetime.now().isoformat()
        }
    
    def create_shortcuts_data(self, use_sample: bool = False) -> Dict:
        """Create data file for Apple Shortcuts to consume"""
        if use_sample:
            latest_result = self.create_sample_results()
        else:
            latest_result = self.get_latest_results()
        
        if not latest_result:
            return {
                'error': 'No results found',
                'message_text': 'No results available yet. Process a week first!',
                'timestamp': datetime.now().isoformat()
            }
        
        return self.format_for_shortcuts(latest_result)
    
    def save_shortcuts_data(self, output_file: str = "shortcuts_data.json", use_sample: bool = False) -> bool:
        """Save formatted data for Apple Shortcuts"""
        try:
            data = self.create_shortcuts_data(use_sample)
            
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Shortcuts data saved to {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save Shortcuts data: {e}")
            return False
    
    def save_shortcuts_data_for_week(self, output_file: str, week: int, result: Dict) -> bool:
        """Save formatted data for a specific week's results"""
        try:
            # Format the specific result data
            data = self.format_for_shortcuts(result)
            
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Week {week} shortcuts data saved to {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save Week {week} Shortcuts data: {e}")
            return False


def main():
    """Test the Apple Shortcuts integration"""
    print("📱 APPLE SHORTCUTS INTEGRATION TEST")
    print("=" * 50)
    
    integration = AppleShortcutsIntegration()
    
    # Test with sample data first
    print("\n🧪 Testing with sample data...")
    if integration.save_shortcuts_data("shortcuts_sample.json", use_sample=True):
        print("\n📝 Sample data for Apple Shortcuts:")
        
        data = integration.create_shortcuts_data(use_sample=True)
        print(f"Week: {data['week']}")
        print(f"Season: {data['season']}")
        print(f"\nMessage preview:")
        print("-" * 40)
        print(data['message_text'])
        print("-" * 40)
    
    # Test with real data
    print("\n📊 Testing with real data...")
    if integration.save_shortcuts_data("shortcuts_real.json", use_sample=False):
        data = integration.create_shortcuts_data(use_sample=False)
        if 'error' not in data:
            print(f"Week: {data['week']}")
            print(f"Season: {data['season']}")
            print(f"\nMessage preview:")
            print("-" * 40)
            print(data['message_text'])
            print("-" * 40)
        else:
            print(f"Error: {data['error']}")
    
    print(f"\n📱 Next steps for iPhone setup:")
    print(f"1. Transfer shortcuts_sample.json to your iPhone")
    print(f"2. Create an Apple Shortcut that reads this file")
    print(f"3. Use 'Send Message' action to send to your group chat")
    print(f"4. Run the shortcut whenever you want to send results")
    print(f"\n💡 Use shortcuts_sample.json for testing, shortcuts_real.json for actual results")


if __name__ == "__main__":
    main()