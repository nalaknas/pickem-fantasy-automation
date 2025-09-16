#!/usr/bin/env python3
"""
Apple Shortcuts Weekly Integration
=================================

Integrates Apple Shortcuts data generation into the weekly workflow.
Run this after processing a week to generate data for iPhone shortcuts.

Usage:
    python3 apple_shortcuts_weekly.py
    python3 apple_shortcuts_weekly.py --sample
"""

import sys
import os
import argparse

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.apple_shortcuts import AppleShortcutsIntegration

def main():
    """Main function for Apple Shortcuts weekly integration"""
    parser = argparse.ArgumentParser(description='Generate Apple Shortcuts data for weekly results')
    parser.add_argument('--sample', action='store_true', help='Generate sample data for testing')
    parser.add_argument('--output', default='shortcuts/shortcuts_data.json', help='Output filename')
    
    args = parser.parse_args()
    
    print("📱 APPLE SHORTCUTS WEEKLY INTEGRATION")
    print("=" * 50)
    
    integration = AppleShortcutsIntegration()
    
    if args.sample:
        print("🧪 Generating sample data for testing...")
        success = integration.save_shortcuts_data(args.output, use_sample=True)
        if success:
            print(f"✅ Sample data saved to {args.output}")
            print("📱 Transfer this file to your iPhone and test your shortcut!")
    else:
        print("📊 Generating data from latest results...")
        success = integration.save_shortcuts_data(args.output, use_sample=False)
        if success:
            print(f"✅ Results data saved to {args.output}")
            print("📱 Transfer this file to your iPhone and run your shortcut!")
    
    # Show preview
    data = integration.create_shortcuts_data(use_sample=args.sample)
    if 'error' not in data:
        print(f"\n📝 Message preview:")
        print("-" * 40)
        print(data['message_text'])
        print("-" * 40)
    else:
        print(f"\n⚠️  {data['error']}")
        print("   Run 'python3 main.py' first to process a week")
    
    print(f"\n📱 Next steps:")
    print(f"1. Transfer {args.output} to your iPhone")
    print(f"2. Run your Apple Shortcut")
    print(f"3. Send to your group chat")

if __name__ == "__main__":
    main()
