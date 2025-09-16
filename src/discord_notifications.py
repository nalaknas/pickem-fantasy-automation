#!/usr/bin/env python3
"""
Discord Notifications Module for Sleeper Skins Game
==================================================

Handles sending notifications via Discord webhooks for weekly results.
Great alternative to SMS for group chats.

"""

import requests
import json
from typing import Dict, List, Optional

# Handle both relative and absolute imports
try:
    from .secure_config import config
except ImportError:
    from secure_config import config

class DiscordNotifier:
    """Handles Discord notifications for skins game results"""
    
    def __init__(self):
        """Initialize Discord notifier with webhook configuration"""
        self.webhook_url = config.discord_webhook_url if hasattr(config, 'discord_webhook_url') else None
        
        if self.webhook_url:
            print("✅ Discord webhook configured")
        else:
            print("⚠️  Discord webhook not configured")
    
    def is_configured(self) -> bool:
        """Check if Discord notifications are properly configured"""
        return self.webhook_url is not None
    
    def format_results_embed(self, result: Dict, week: int, season: int) -> dict:
        """
        Format weekly results into a Discord embed
        
        Args:
            result: The processed week result from process_week()
            week: Week number
            season: Season year
        
        Returns:
            Discord embed object
        """
        league_name = config.league_name
        
        # Create embed
        embed = {
            "title": f"🏈 {league_name} - Week {week} Results",
            "color": 0x00ff00,  # Green color
            "fields": [],
            "footer": {
                "text": f"Season {season} • Week {week}"
            },
            "timestamp": result.get('date_processed', '')
        }
        
        # High Score Results
        if result['rankings']['highest']:
            winner_names = ', '.join(result['winner_names']['highest'])
            score = result['scores']['highest']
            embed['fields'].append({
                "name": "🥇 Highest Scorer",
                "value": f"**{winner_names}** - {score} points",
                "inline": True
            })
        
        # Second Highest
        if result['rankings']['second_highest']:
            winner_names = ', '.join(result['winner_names']['second_highest'])
            score = result['scores']['second_highest']
            embed['fields'].append({
                "name": "🥈 Second Highest",
                "value": f"**{winner_names}** - {score} points",
                "inline": True
            })
        
        # Third Highest
        if result['rankings']['third_highest']:
            winner_names = ', '.join(result['winner_names']['third_highest'])
            score = result['scores']['third_highest']
            embed['fields'].append({
                "name": "🥉 Third Highest",
                "value": f"**{winner_names}** - {score} points",
                "inline": True
            })
        
        # Lowest Scorer
        if result['rankings']['lowest']:
            winner_names = ', '.join(result['winner_names']['lowest'])
            score = result['scores']['lowest']
            embed['fields'].append({
                "name": "📉 Lowest Scorer",
                "value": f"**{winner_names}** - {score} points",
                "inline": True
            })
        
        # No Picks
        if result['rankings']['no_picks']:
            winner_names = ', '.join(result['winner_names']['no_picks'])
            embed['fields'].append({
                "name": "❌ No Picks Submitted",
                "value": f"**{winner_names}**",
                "inline": False
            })
        
        # Perfect Week
        if result['perfect_week_winners']:
            winner_names = ', '.join(result['winner_names']['perfect_week'])
            embed['fields'].append({
                "name": "🎯 Perfect Week!",
                "value": f"**{winner_names}** 🎉",
                "inline": False
            })
        
        return embed
    
    def send_results_notification(self, result: Dict, week: int, season: int) -> bool:
        """
        Send weekly results notification via Discord
        
        Args:
            result: The processed week result
            week: Week number
            season: Season year
        
        Returns:
            True if message sent successfully, False otherwise
        """
        if not self.is_configured():
            print("❌ Discord webhook not configured. Cannot send notifications.")
            return False
        
        # Format the embed
        embed = self.format_results_embed(result, week, season)
        
        # Create message payload
        payload = {
            "embeds": [embed],
            "content": f"📊 **Week {week} Results are in!** Good luck next week! 🍀"
        }
        
        print(f"📱 Sending Discord notification...")
        print(f"📝 Message preview:")
        print("-" * 40)
        print(f"Title: {embed['title']}")
        for field in embed['fields']:
            print(f"{field['name']}: {field['value']}")
        print("-" * 40)
        
        # Ask for confirmation
        confirm = input("\n🤔 Send this message to Discord? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("❌ Message sending cancelled.")
            return False
        
        try:
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
            print("✅ Discord notification sent successfully!")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to send Discord notification: {e}")
            return False
    
    def send_test_message(self) -> bool:
        """Send a test message to verify Discord functionality"""
        if not self.is_configured():
            print("❌ Discord webhook not configured. Cannot send test message.")
            return False
        
        test_embed = {
            "title": "🧪 Test Message",
            "description": "This is a test message from your Sleeper Skins Game automation system.",
            "color": 0x0099ff,  # Blue color
            "fields": [
                {
                    "name": "Status",
                    "value": "✅ Discord notifications are working correctly!",
                    "inline": False
                }
            ],
            "footer": {
                "text": "Test completed successfully"
            }
        }
        
        payload = {
            "embeds": [test_embed],
            "content": "🧪 **Test Message** - If you see this, Discord notifications are working!"
        }
        
        print("📱 Sending Discord test message...")
        
        try:
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
            print("✅ Discord test message sent successfully!")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to send Discord test message: {e}")
            return False


def main():
    """Test the Discord notification system"""
    print("📱 DISCORD NOTIFICATION TEST")
    print("=" * 40)
    
    notifier = DiscordNotifier()
    
    if not notifier.is_configured():
        print("❌ Discord notifications not configured.")
        print("\nTo configure Discord notifications:")
        print("1. Go to your Discord server")
        print("2. Go to Server Settings → Integrations → Webhooks")
        print("3. Create a new webhook")
        print("4. Copy the webhook URL")
        print("5. Add to your .env file:")
        print("   DISCORD_WEBHOOK_URL=your_webhook_url_here")
        return
    
    print("✅ Discord notifications configured")
    
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
        },
        'date_processed': '2025-01-09T12:00:00'
    }
    
    print("\n🧪 Testing message formatting...")
    embed = notifier.format_results_embed(sample_result, 1, 2025)
    print("📝 Sample embed:")
    print(f"Title: {embed['title']}")
    for field in embed['fields']:
        print(f"{field['name']}: {field['value']}")
    
    # Ask if user wants to send test message
    test_confirm = input("\n🤔 Send test message to Discord? (y/N): ").strip().lower()
    if test_confirm in ['y', 'yes']:
        notifier.send_test_message()
    else:
        print("✅ Test completed without sending messages")


if __name__ == "__main__":
    main()
