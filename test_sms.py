#!/usr/bin/env python3
"""
SMS Test Script for Sleeper Skins Game
=====================================

Quick script to test SMS notifications before using them in production.

Usage:
    python3 test_sms.py                    # Test with configured numbers
    python3 test_sms.py +1234567890       # Test with specific number
    python3 test_sms.py +1234567890,+0987654321  # Test with multiple numbers

"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.sms_notifications import SMSNotifier

def main():
    print("📱 SMS NOTIFICATION TEST SCRIPT")
    print("=" * 40)
    
    # Initialize SMS notifier
    notifier = SMSNotifier()
    
    # Check if SMS is configured
    if not notifier.is_configured():
        print("❌ SMS notifications not configured!")
        print("\nTo configure SMS notifications:")
        print("1. Sign up for Twilio at https://www.twilio.com/")
        print("2. Get your Account SID and Auth Token from the console")
        print("3. Purchase a phone number for sending SMS")
        print("4. Add these to your .env file:")
        print("   TWILIO_ACCOUNT_SID=your_account_sid")
        print("   TWILIO_AUTH_TOKEN=your_auth_token")
        print("   TWILIO_FROM_NUMBER=+1234567890")
        print("   TWILIO_TO_NUMBERS=+1234567890,+0987654321")
        print("\n5. Run this script again to test!")
        return
    
    print("✅ SMS notifications configured")
    print(f"📞 From number: {notifier.twilio_config['from_number']}")
    print(f"📞 Configured recipients: {notifier.get_configured_numbers()}")
    
    # Check for command line test numbers
    test_numbers = None
    if len(sys.argv) > 1:
        test_numbers = [num.strip() for num in sys.argv[1].split(',')]
        print(f"📞 Using test numbers: {test_numbers}")
    
    # Show sample message
    print("\n📝 Sample message that will be sent:")
    print("-" * 50)
    
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
    
    sample_message = notifier.format_results_message(sample_result, 1, 2025)
    print(sample_message)
    print("-" * 50)
    
    # Ask for confirmation
    print(f"\n🤔 Ready to send test message?")
    if test_numbers:
        print(f"   Recipients: {test_numbers}")
    else:
        print(f"   Recipients: {notifier.get_configured_numbers()}")
    
    confirm = input("   Send test message? (y/N): ").strip().lower()
    
    if confirm in ['y', 'yes']:
        print("\n📱 Sending test message...")
        success = notifier.send_test_message(test_numbers)
        
        if success:
            print("\n🎉 Test completed successfully!")
            print("   Check your phone for the test message.")
            print("   If you received it, SMS notifications are working!")
        else:
            print("\n❌ Test failed!")
            print("   Check your Twilio configuration and try again.")
    else:
        print("❌ Test cancelled")
    
    print(f"\n💡 Next steps:")
    print(f"   1. If test was successful, you can now use SMS notifications")
    print(f"   2. Run: python3 main.py test-sms")
    print(f"   3. Or process a week: python3 main.py")
    print(f"   4. The system will ask if you want to send SMS after processing")

if __name__ == "__main__":
    main()
