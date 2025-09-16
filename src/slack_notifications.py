#!/usr/bin/env python3
"""
Slack Notifications Module for Sleeper Skins Game
================================================

Handles sending notifications via Slack webhooks for weekly results.
Great for workplace or team group chats.

"""

import requests
import json
from typing import Dict, List, Optional

# Handle both relative and absolute imports
try:
    from .secure_config import config
except ImportError:
    from secure_config import config

class SlackNotifier:
    """Handles Slack notifications for skins game results"""
    
    def __init__(self):
        """Initialize Slack notifier with webhook configuration"""
        self.webhook_url = config.slack_webhook_url if hasattr(config, 'slack_webhook_url') else None
        
        if self.webhook_url:
            print("✅ Slack webhook configured")
        else:
            print("⚠️  Slack webhook not configured")
    
    def is_configured(self) -> bool:
        """Check if Slack notifications are properly configured"""
        return self.webhook_url is not None
    
    def format_results_message(self, result: Dict, week: int, season: int) -> str:
        """
        Format weekly results into a Slack message
        
        Args:
            result: The processed week result from process_week()
            week: Week number
            season: Season year
        
        Returns:
            Formatted message string
        """
        league_name = config.league_name
        
        message = f"🏈 *{league_name} - Week {week} Results* 🏈\n\n"
        
        # High Score Results
        if result['rankings']['highest']:
            winner_names = ', '.join(result['winner_names']['highest'])
            score = result['scores']['highest']
            message += f"🥇 *Highest Scorer:* {winner_names} - {score} points\n"
        
        # Second Highest
        if result['rankings']['second_highest']:
            winner_names = ', '.join(result['winner_names']['second_highest'])
            score = result['scores']['second_highest']
            message += f"🥈 *Second Highest:* {winner_names} - {score} points\n"
        
        # Third Highest
        if result['rankings']['third_highest']:
            winner_names = ', '.join(result['winner_names']['third_highest'])
            score = result['scores']['third_highest']
            message += f"🥉 *Third Highest:* {winner_names} - {score} points\n"
        
        # Lowest Scorer
        if result['rankings']['lowest']:
            winner_names = ', '.join(result['winner_names']['lowest'])
            score = result['scores']['lowest']
            message += f"📉 *Lowest Scorer:* {winner_names} - {score} points\n"
        
        # No Picks
        if result['rankings']['no_picks']:
            winner_names = ', '.join(result['winner_names']['no_picks'])
            message += f"❌ *No Picks Submitted:* {winner_names}\n"
        
        # Perfect Week
        if result['perfect_week_winners']:
            winner_names = ', '.join(result['winner_names']['perfect_week'])
            message += f"🎯 *Perfect Week:* {winner_names} 🎉\n"
        
        # Season info
        message += f"\nSeason {season} • Week {week}\n"
        message += f"Good luck next week! 🍀"
        
        return message
    
    def send_results_notification(self, result: Dict, week: int, season: int) -> bool:
        """
        Send weekly results notification via Slack
        
        Args:
            result: The processed week result
            week: Week number
            season: Season year
        
        Returns:
            True if message sent successfully, False otherwise
        """
        if not self.is_configured():
            print("❌ Slack webhook not configured. Cannot send notifications.")
            return False
        
        # Format the message
        message = self.format_results_message(result, week, season)
        
        # Create message payload
        payload = {
            "text": message,
            "username": "Skins Game Bot",
            "icon_emoji": ":football:"
        }
        
        print(f"📱 Sending Slack notification...")
        print(f"📝 Message preview:")
        print("-" * 40)
        print(message)
        print("-" * 40)
        
        # Ask for confirmation
        confirm = input("\n🤔 Send this message to Slack? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("❌ Message sending cancelled.")
            return False
        
        try:
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
            print("✅ Slack notification sent successfully!")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to send Slack notification: {e}")
            return False
    
    def send_test_message(self) -> bool:
        """Send a test message to verify Slack functionality"""
        if not self.is_configured():
            print("❌ Slack webhook not configured. Cannot send test message.")
            return False
        
        test_message = "🧪 *Test Message*\n\nThis is a test message from your Sleeper Skins Game automation system.\n\n✅ Slack notifications are working correctly!"
        
        payload = {
            "text": test_message,
            "username": "Skins Game Bot",
            "icon_emoji": ":football:"
        }
        
        print("📱 Sending Slack test message...")
        
        try:
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
            print("✅ Slack test message sent successfully!")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to send Slack test message: {e}")
            return False


def main():
    """Test the Slack notification system"""
    print("📱 SLACK NOTIFICATION TEST")
    print("=" * 40)
    
    notifier = SlackNotifier()
    
    if not notifier.is_configured():
        print("❌ Slack notifications not configured.")
        print("\nTo configure Slack notifications:")
        print("1. Go to your Slack workspace")
        print("2. Go to Apps → Incoming Webhooks")
        print("3. Create a new webhook")
        print("4. Copy the webhook URL")
        print("5. Add to your .env file:")
        print("   SLACK_WEBHOOK_URL=your_webhook_url_here")
        return
    
    print("✅ Slack notifications configured")
    
    # Test with a sample result
    sample_result = {
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
    
    print("\n🧪 Testing message formatting...")
    message = notifier.format_results_message(sample_result, 1, 2025)
    print("📝 Sample message:")
    print("-" * 40)
    print(message)
    print("-" * 40)
    
    # Ask if user wants to send test message
    test_confirm = input("\n🤔 Send test message to Slack? (y/N): ").strip().lower()
    if test_confirm in ['y', 'yes']:
        notifier.send_test_message()
    else:
        print("✅ Test completed without sending messages")


if __name__ == "__main__":
    main()
