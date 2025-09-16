#!/usr/bin/env python3
"""
Email-to-SMS Gateway for Sleeper Skins Game
==========================================

Sends results via email to carrier SMS gateways.
Works with most US carriers for iPhone group chats.

"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional

# Handle both relative and absolute imports
try:
    from .secure_config import config
except ImportError:
    from secure_config import config

class EmailToSMSNotifier:
    """Handles email-to-SMS notifications for skins game results"""
    
    def __init__(self):
        """Initialize email-to-SMS notifier"""
        self.email_config = self._get_email_config()
        self.carrier_gateways = {
            'att': '@txt.att.net',
            'verizon': '@vtext.com',
            'tmobile': '@tmomail.net',
            'sprint': '@messaging.sprintpcs.com',
            'uscellular': '@email.uscc.net',
            'boost': '@smsmyboostmobile.com',
            'cricket': '@sms.cricketwireless.net',
            'metropcs': '@mymetropcs.com'
        }
        
        if self.email_config:
            print("✅ Email-to-SMS configured")
        else:
            print("⚠️  Email-to-SMS not configured")
    
    def _get_email_config(self) -> Optional[Dict]:
        """Get email configuration from environment"""
        import os
        
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = os.getenv('SMTP_PORT', '587')
        email_user = os.getenv('EMAIL_USER')
        email_password = os.getenv('EMAIL_PASSWORD')
        
        if all([smtp_server, email_user, email_password]):
            return {
                'smtp_server': smtp_server,
                'smtp_port': int(smtp_port),
                'email_user': email_user,
                'email_password': email_password
            }
        return None
    
    def is_configured(self) -> bool:
        """Check if email-to-SMS is properly configured"""
        return self.email_config is not None
    
    def format_results_message(self, result: Dict, week: int, season: int) -> str:
        """
        Format weekly results into a concise SMS message
        
        Args:
            result: The processed week result from process_week()
            week: Week number
            season: Season year
        
        Returns:
            Formatted message string (SMS length optimized)
        """
        league_name = config.league_name
        
        # Keep message short for SMS
        message = f"🏈 {league_name} W{week} Results\n\n"
        
        # High Score Results
        if result['rankings']['highest']:
            winner_names = ', '.join(result['winner_names']['highest'])
            score = result['scores']['highest']
            message += f"🥇 {winner_names}: {score}pts\n"
        
        # Second Highest
        if result['rankings']['second_highest']:
            winner_names = ', '.join(result['winner_names']['second_highest'])
            score = result['scores']['second_highest']
            message += f"🥈 {winner_names}: {score}pts\n"
        
        # Lowest Scorer
        if result['rankings']['lowest']:
            winner_names = ', '.join(result['winner_names']['lowest'])
            score = result['scores']['lowest']
            message += f"📉 {winner_names}: {score}pts\n"
        
        # Perfect Week
        if result['perfect_week_winners']:
            winner_names = ', '.join(result['winner_names']['perfect_week'])
            message += f"🎯 Perfect: {winner_names}\n"
        
        message += f"\nS{season}W{week} 🍀"
        
        return message
    
    def get_carrier_gateway(self, phone_number: str) -> Optional[str]:
        """
        Determine carrier gateway for a phone number
        
        Args:
            phone_number: Phone number in format +1234567890
        
        Returns:
            Email gateway address or None if unknown
        """
        # This is a simplified approach - in reality you'd need to lookup the carrier
        # For now, we'll use a common gateway (you can specify carrier in config)
        return 'txt.att.net'  # Default to AT&T
    
    def send_to_phone(self, phone_number: str, message: str) -> bool:
        """
        Send SMS to phone number via email gateway
        
        Args:
            phone_number: Phone number in format +1234567890
            message: Message to send
        
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.is_configured():
            print("❌ Email-to-SMS not configured")
            return False
        
        # Remove + and format for email
        clean_number = phone_number.replace('+', '').replace('-', '').replace(' ', '')
        if len(clean_number) == 10:
            clean_number = '1' + clean_number  # Add country code
        
        # Get carrier gateway
        gateway = self.get_carrier_gateway(phone_number)
        if not gateway:
            print(f"❌ Unknown carrier for {phone_number}")
            return False
        
        # Create email address
        email_address = f"{clean_number}@{gateway}"
        
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = self.email_config['email_user']
        msg['To'] = email_address
        msg['Subject'] = ""  # SMS doesn't use subject
        
        msg.attach(MIMEText(message, 'plain'))
        
        try:
            # Connect to SMTP server
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['email_user'], self.email_config['email_password'])
            
            # Send email
            text = msg.as_string()
            server.sendmail(self.email_config['email_user'], email_address, text)
            server.quit()
            
            print(f"✅ SMS sent to {phone_number} via {gateway}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send SMS to {phone_number}: {e}")
            return False
    
    def send_results_notification(self, result: Dict, week: int, season: int, 
                                 phone_numbers: List[str]) -> bool:
        """
        Send weekly results notification via email-to-SMS
        
        Args:
            result: The processed week result
            week: Week number
            season: Season year
            phone_numbers: List of phone numbers to send to
        
        Returns:
            True if all messages sent successfully, False otherwise
        """
        if not self.is_configured():
            print("❌ Email-to-SMS not configured. Cannot send notifications.")
            return False
        
        # Format the message
        message = self.format_results_message(result, week, season)
        
        print(f"📱 Sending email-to-SMS notifications to {len(phone_numbers)} number(s)...")
        print(f"📝 Message preview:")
        print("-" * 40)
        print(message)
        print("-" * 40)
        
        # Ask for confirmation
        confirm = input("\n🤔 Send these messages? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("❌ Message sending cancelled.")
            return False
        
        success_count = 0
        total_count = len(phone_numbers)
        
        for phone_number in phone_numbers:
            if self.send_to_phone(phone_number, message):
                success_count += 1
        
        if success_count == total_count:
            print(f"🎉 All notifications sent successfully!")
            return True
        else:
            print(f"⚠️  {success_count}/{total_count} notifications sent successfully")
            return False


def main():
    """Test the email-to-SMS notification system"""
    print("📱 EMAIL-TO-SMS NOTIFICATION TEST")
    print("=" * 50)
    
    notifier = EmailToSMSNotifier()
    
    if not notifier.is_configured():
        print("❌ Email-to-SMS notifications not configured.")
        print("\nTo configure email-to-SMS:")
        print("1. Use Gmail, Outlook, or any SMTP email service")
        print("2. Add to your .env file:")
        print("   SMTP_SERVER=smtp.gmail.com")
        print("   SMTP_PORT=587")
        print("   EMAIL_USER=your_email@gmail.com")
        print("   EMAIL_PASSWORD=your_app_password")
        print("\nNote: Gmail requires App Passwords for SMTP")
        return
    
    print("✅ Email-to-SMS notifications configured")
    
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
    
    # Ask for test phone number
    test_number = input("\n📞 Enter test phone number (+1234567890): ").strip()
    if test_number:
        test_confirm = input(f"🤔 Send test message to {test_number}? (y/N): ").strip().lower()
        if test_confirm in ['y', 'yes']:
            notifier.send_to_phone(test_number, message)
        else:
            print("✅ Test completed without sending messages")
    else:
        print("✅ Test completed without phone number")


if __name__ == "__main__":
    main()
