#!/usr/bin/env python3
"""
SMS Notifications Module for Sleeper Skins Game
===============================================

Handles sending SMS notifications via Twilio for weekly results.
Includes confirmation prompts and test functionality.

"""

from typing import Dict, List, Optional
import json

# Handle both relative and absolute imports
try:
    from .secure_config import config
except ImportError:
    from secure_config import config

class SMSNotifier:
    """Handles SMS notifications for skins game results"""
    
    def __init__(self):
        """Initialize SMS notifier with Twilio configuration"""
        self.twilio_config = config.twilio_config
        self.twilio_client = None
        
        if self.twilio_config:
            try:
                from twilio.rest import Client
                self.twilio_client = Client(
                    self.twilio_config['account_sid'],
                    self.twilio_config['auth_token']
                )
                print("✅ Twilio SMS client initialized")
            except ImportError:
                print("⚠️  Twilio package not installed. Install with: pip install twilio")
            except Exception as e:
                print(f"⚠️  Failed to initialize Twilio client: {e}")
        else:
            print("⚠️  No Twilio configuration found. SMS notifications disabled.")
    
    def is_configured(self) -> bool:
        """Check if SMS notifications are properly configured"""
        return self.twilio_client is not None and self.twilio_config is not None
    
    def format_results_message(self, result: Dict, week: int, season: int) -> str:
        """
        Format weekly results into a readable SMS message
        
        Args:
            result: The processed week result from process_week()
            week: Week number
            season: Season year
        
        Returns:
            Formatted message string
        """
        league_name = config.league_name
        
        message = f"🏈 {league_name} - Week {week} Results 🏈\n\n"
        
        # High Score Results
        if result['rankings']['highest']:
            winner_names = ', '.join(result['winner_names']['highest'])
            score = result['scores']['highest']
            message += f"🥇 HIGHEST SCORER: {winner_names}\n"
            message += f"Score: {score} points\n\n"
        
        # Second Highest
        if result['rankings']['second_highest']:
            winner_names = ', '.join(result['winner_names']['second_highest'])
            score = result['scores']['second_highest']
            message += f"🥈 SECOND HIGHEST: {winner_names}\n"
            message += f"Score: {score} points\n\n"
        
        # Third Highest
        if result['rankings']['third_highest']:
            winner_names = ', '.join(result['winner_names']['third_highest'])
            score = result['scores']['third_highest']
            message += f"🥉 THIRD HIGHEST: {winner_names}\n"
            message += f"Score: {score} points\n\n"
        
        # Lowest Scorer
        if result['rankings']['lowest']:
            winner_names = ', '.join(result['winner_names']['lowest'])
            score = result['scores']['lowest']
            message += f"📉 LOWEST SCORER: {winner_names}\n"
            message += f"Score: {score} points\n\n"
        
        # No Picks
        if result['rankings']['no_picks']:
            winner_names = ', '.join(result['winner_names']['no_picks'])
            message += f"❌ NO PICKS SUBMITTED: {winner_names}\n\n"
        
        # Perfect Week
        if result['perfect_week_winners']:
            winner_names = ', '.join(result['winner_names']['perfect_week'])
            message += f"🎯 PERFECT WEEK: {winner_names}\n"
            message += f"Congratulations! 🎉\n\n"
        
        # Season info
        message += f"Season {season} • Week {week}\n"
        message += f"Good luck next week! 🍀"
        
        return message
    
    def send_test_message(self, test_numbers: List[str] = None) -> bool:
        """
        Send a test message to verify SMS functionality
        
        Args:
            test_numbers: List of phone numbers to send test to (optional)
        
        Returns:
            True if successful, False otherwise
        """
        if not self.is_configured():
            print("❌ SMS not configured. Cannot send test message.")
            return False
        
        # Use provided test numbers or default to configured numbers
        numbers_to_test = test_numbers or self.twilio_config.get('to_numbers', [])
        
        if not numbers_to_test:
            print("❌ No phone numbers configured for testing.")
            return False
        
        test_message = "🧪 TEST MESSAGE 🧪\n\nThis is a test message from your Sleeper Skins Game automation system.\n\nIf you received this, SMS notifications are working correctly! ✅"
        
        success_count = 0
        total_count = len(numbers_to_test)
        
        print(f"📱 Sending test message to {total_count} number(s)...")
        
        for phone_number in numbers_to_test:
            try:
                self.twilio_client.messages.create(
                    body=test_message,
                    from_=self.twilio_config['from_number'],
                    to=phone_number
                )
                print(f"✅ Test message sent to {phone_number}")
                success_count += 1
            except Exception as e:
                print(f"❌ Failed to send test message to {phone_number}: {e}")
        
        if success_count == total_count:
            print(f"🎉 All test messages sent successfully!")
            return True
        else:
            print(f"⚠️  {success_count}/{total_count} test messages sent successfully")
            return False
    
    def send_results_notification(self, result: Dict, week: int, season: int, 
                                 phone_numbers: List[str] = None) -> bool:
        """
        Send weekly results notification via SMS
        
        Args:
            result: The processed week result
            week: Week number
            season: Season year
            phone_numbers: List of phone numbers to send to (optional)
        
        Returns:
            True if all messages sent successfully, False otherwise
        """
        if not self.is_configured():
            print("❌ SMS not configured. Cannot send notifications.")
            return False
        
        # Use provided numbers or default to configured numbers
        numbers_to_notify = phone_numbers or self.twilio_config.get('to_numbers', [])
        
        if not numbers_to_notify:
            print("❌ No phone numbers configured for notifications.")
            return False
        
        # Format the message
        message = self.format_results_message(result, week, season)
        
        print(f"📱 Sending results notification to {len(numbers_to_notify)} number(s)...")
        print(f"📝 Message preview:")
        print("-" * 40)
        print(message)
        print("-" * 40)
        
        # Ask for confirmation
        confirm = input("\n🤔 Send this message? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("❌ Message sending cancelled.")
            return False
        
        success_count = 0
        total_count = len(numbers_to_notify)
        
        for phone_number in numbers_to_notify:
            try:
                self.twilio_client.messages.create(
                    body=message,
                    from_=self.twilio_config['from_number'],
                    to=phone_number
                )
                print(f"✅ Results notification sent to {phone_number}")
                success_count += 1
            except Exception as e:
                print(f"❌ Failed to send notification to {phone_number}: {e}")
        
        if success_count == total_count:
            print(f"🎉 All notifications sent successfully!")
            return True
        else:
            print(f"⚠️  {success_count}/{total_count} notifications sent successfully")
            return False
    
    def get_configured_numbers(self) -> List[str]:
        """Get list of configured phone numbers"""
        if self.twilio_config:
            return self.twilio_config.get('to_numbers', [])
        return []
    
    def add_test_numbers(self, test_numbers: List[str]) -> None:
        """
        Temporarily add test numbers for testing (doesn't modify config)
        
        Args:
            test_numbers: List of phone numbers to use for testing
        """
        if not self.twilio_config:
            self.twilio_config = {
                'account_sid': 'test',
                'auth_token': 'test',
                'from_number': '+1234567890',  # Dummy number
                'to_numbers': test_numbers
            }
        else:
            # Add test numbers to existing config temporarily
            self.twilio_config['to_numbers'] = test_numbers


def main():
    """Test the SMS notification system"""
    print("📱 SMS NOTIFICATION TEST")
    print("=" * 30)
    
    notifier = SMSNotifier()
    
    if not notifier.is_configured():
        print("❌ SMS notifications not configured.")
        print("\nTo configure SMS notifications:")
        print("1. Set up Twilio account and get credentials")
        print("2. Add to your .env file:")
        print("   TWILIO_ACCOUNT_SID=your_account_sid")
        print("   TWILIO_AUTH_TOKEN=your_auth_token")
        print("   TWILIO_FROM_NUMBER=+1234567890")
        print("   TWILIO_TO_NUMBERS=+1234567890,+0987654321")
        return
    
    print("✅ SMS notifications configured")
    print(f"📞 Configured numbers: {notifier.get_configured_numbers()}")
    
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
    test_confirm = input("\n🤔 Send test message to configured numbers? (y/N): ").strip().lower()
    if test_confirm in ['y', 'yes']:
        notifier.send_test_message()
    else:
        print("✅ Test completed without sending messages")


if __name__ == "__main__":
    main()
