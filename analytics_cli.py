#!/usr/bin/env python3
"""
Command-line interface for the Sleeper Analytics Dashboard
"""

import argparse
import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from analytics_dashboard import SleeperAnalyticsDashboard


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Sleeper Pickem League Analytics Dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analytics_cli.py --full-dashboard
  python analytics_cli.py --summary-only
  python analytics_cli.py --predict-player "nalaknas"
  python analytics_cli.py --charts-only --output-dir ./my_analytics
        """
    )
    
    parser.add_argument(
        '--full-dashboard',
        action='store_true',
        help='Generate complete analytics dashboard with all charts and summary'
    )
    
    parser.add_argument(
        '--summary-only',
        action='store_true',
        help='Generate only the performance summary text'
    )
    
    parser.add_argument(
        '--charts-only',
        action='store_true',
        help='Generate only the charts without summary'
    )
    
    parser.add_argument(
        '--predict-player',
        type=str,
        help='Predict next week performance for a specific player (by display name)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='analytics_output',
        help='Output directory for generated files (default: analytics_output)'
    )
    
    parser.add_argument(
        '--league-id',
        type=str,
        help='Sleeper league ID (optional, will use config if not provided)'
    )
    
    args = parser.parse_args()
    
    # Initialize dashboard
    try:
        dashboard = SleeperAnalyticsDashboard(league_id=args.league_id)
        print(f"🏈 Initialized analytics dashboard for league: {dashboard.league_id}")
    except Exception as e:
        print(f"❌ Error initializing dashboard: {e}")
        return 1
    
    # Execute requested actions
    try:
        if args.full_dashboard:
            print("🚀 Generating full analytics dashboard...")
            dashboard.generate_full_dashboard(args.output_dir)
            
        elif args.summary_only:
            print("📝 Generating performance summary...")
            dashboard.extract_player_data()
            dashboard.calculate_league_analytics()
            summary = dashboard.generate_performance_summary()
            print(summary)
            
            # Save to file
            os.makedirs(args.output_dir, exist_ok=True)
            with open(f"{args.output_dir}/performance_summary.txt", "w") as f:
                f.write(summary)
            print(f"💾 Summary saved to: {args.output_dir}/performance_summary.txt")
            
        elif args.charts_only:
            print("📊 Generating charts only...")
            dashboard.extract_player_data()
            dashboard.calculate_league_analytics()
            
            os.makedirs(args.output_dir, exist_ok=True)
            
            chart_paths = {
                "weekly_trends": f"{args.output_dir}/weekly_trends.png",
                "score_distribution": f"{args.output_dir}/score_distribution.png",
                "top_performers": f"{args.output_dir}/top_performers.png",
                "improvement_trends": f"{args.output_dir}/improvement_trends.png"
            }
            
            dashboard.create_weekly_trends_chart(chart_paths["weekly_trends"])
            dashboard.create_score_distribution_chart(chart_paths["score_distribution"])
            dashboard.create_top_performers_chart(chart_paths["top_performers"])
            dashboard.create_improvement_trends_chart(chart_paths["improvement_trends"])
            
            print("✅ Charts generated successfully!")
            for name, path in chart_paths.items():
                print(f"   • {name}: {path}")
                
        elif args.predict_player:
            print(f"🔮 Predicting performance for player: {args.predict_player}")
            dashboard.extract_player_data()
            
            # Find player by display name
            users = dashboard.get_users()
            player_id = None
            for uid, user_info in users.items():
                if user_info.get('display_name', '').lower() == args.predict_player.lower():
                    player_id = uid
                    break
            
            if not player_id:
                print(f"❌ Player '{args.predict_player}' not found")
                print("Available players:")
                for user_info in users.values():
                    print(f"   • {user_info.get('display_name', 'Unknown')}")
                return 1
            
            prediction = dashboard.predict_next_week_performance(player_id)
            player_name = users[player_id]['display_name']
            
            print(f"\n🎯 PREDICTION FOR {player_name.upper()}:")
            print(f"   Predicted Score: {prediction['predicted_score']:.2f}")
            print(f"   Confidence: {prediction['confidence']:.2f}")
            print(f"   Trend: {prediction['trend']:+.2f}")
            print(f"   Next Week: {prediction['next_week']}")
            
        else:
            # Default: show summary
            print("📊 Generating performance summary...")
            dashboard.extract_player_data()
            dashboard.calculate_league_analytics()
            summary = dashboard.generate_performance_summary()
            print(summary)
            
    except Exception as e:
        print(f"❌ Error during execution: {e}")
        return 1
    
    print("\n✅ Analytics completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main())
