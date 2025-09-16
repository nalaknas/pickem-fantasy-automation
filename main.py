#!/usr/bin/env python3
"""
Main entry point for Sleeper Fantasy Pickem Skins Game Automation
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.weekly_runner import main as run_weekly, quick_status
from src.view_results import view_results, view_season_summary
from src.export_results import SkinsGameExporter
from src.sms_notifications import SMSNotifier

def main():
    """Main entry point with command line argument handling"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "status":
            quick_status()
        elif sys.argv[1] == "view":
            view_results()
        elif sys.argv[1] == "export":
            print("📊 Exporting season report...")
            exporter = SkinsGameExporter()
            if exporter.export_all():
                print("✅ Export completed successfully!")
            else:
                print("❌ Export failed!")
        elif sys.argv[1] == "summary":
            view_season_summary()
        elif sys.argv[1] == "test-sms":
            print("📱 Testing SMS notifications...")
            notifier = SMSNotifier()
            if notifier.is_configured():
                # Check if test numbers provided
                test_numbers = None
                if len(sys.argv) > 2:
                    test_numbers = [num.strip() for num in sys.argv[2].split(',')]
                    print(f"📞 Using test numbers: {test_numbers}")
                
                notifier.send_test_message(test_numbers)
            else:
                print("❌ SMS notifications not configured")
                print("   Configure Twilio settings in your .env file first")
        else:
            # Pass arguments to weekly runner
            run_weekly()
    else:
        # Default: run weekly processing
        run_weekly()

if __name__ == "__main__":
    main()
