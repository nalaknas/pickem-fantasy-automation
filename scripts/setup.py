#!/usr/bin/env python3
"""
Secure Setup Script for Sleeper Fantasy League Automation
========================================================

This script helps you set up secure configuration for your league.
It will guide you through creating a secure .env file with your sensitive data.
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create a secure .env file from the template."""
    env_file = Path(".env")
    template_file = Path("config/env.template")
    
    if env_file.exists():
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if response != 'y':
            print("✅ Keeping existing .env file")
            return True
    
    if not template_file.exists():
        print("❌ config/env.template file not found!")
        return False
    
    print("🔒 Setting up secure configuration...")
    print("📝 Please provide your sensitive information:")
    print()
    
    # Read template
    with open(template_file, 'r') as f:
        template_content = f.read()
    
    # Get user input
    league_id = input("Enter your Sleeper League ID: ").strip()
    if not league_id:
        print("❌ League ID is required!")
        return False
    
    # Replace template values
    env_content = template_content.replace("your_league_id_here", league_id)
    
    # Optional Twilio setup
    print("\n📱 Twilio Configuration (optional - press Enter to skip):")
    twilio_sid = input("Twilio Account SID: ").strip()
    twilio_token = input("Twilio Auth Token: ").strip()
    twilio_from = input("Twilio From Number (+1234567890): ").strip()
    twilio_to = input("Twilio To Numbers (comma-separated): ").strip()
    
    if twilio_sid and twilio_token and twilio_from and twilio_to:
        env_content = env_content.replace("your_twilio_account_sid_here", twilio_sid)
        env_content = env_content.replace("your_twilio_auth_token_here", twilio_token)
        env_content = env_content.replace("your_twilio_phone_number_here", twilio_from)
        env_content = env_content.replace("comma_separated_phone_numbers_here", twilio_to)
    
    # Write .env file
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    # Set secure permissions (Unix only)
    if os.name != 'nt':  # Not Windows
        os.chmod(env_file, 0o600)  # Read/write for owner only
    
    print(f"\n✅ Secure .env file created!")
    print(f"🔒 File permissions set to owner-only access")
    print(f"📁 Location: {env_file.absolute()}")
    print()
    print("🚀 You're ready to use the automation securely!")
    print("💡 Run 'python main.py status' to test your configuration")
    
    return True

def verify_setup():
    """Verify that the setup is working correctly."""
    print("\n🔍 Verifying setup...")
    
    try:
        # Add src to path
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        
        from src.secure_config import config
        
        if config.is_secure():
            print("✅ Configuration is secure and valid!")
            print(f"🏈 League ID: {config.sleeper_league_id[:8]}...{config.sleeper_league_id[-4:]}")
            print(f"📁 Data directory: {config.data_directory}")
            return True
        else:
            print("❌ Configuration validation failed!")
            return False
            
    except Exception as e:
        print(f"❌ Setup verification failed: {e}")
        return False

def main():
    """Main setup function."""
    print("🏈 SLEEPER FANTASY LEAGUE AUTOMATION SETUP 🏈")
    print("=" * 50)
    print()
    print("This script will help you set up secure configuration.")
    print("Your sensitive data (league ID, API keys) will be stored")
    print("in a .env file that is NOT committed to version control.")
    print()
    
    if create_env_file():
        verify_setup()
    else:
        print("❌ Setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
