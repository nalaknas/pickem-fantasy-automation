#!/usr/bin/env python3
"""
Test script for the Sleeper Analytics Dashboard
"""

import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from analytics_dashboard import SleeperAnalyticsDashboard


def test_analytics_dashboard():
    """Test the analytics dashboard functionality"""
    print("🧪 Testing Sleeper Analytics Dashboard...")
    
    try:
        # Initialize dashboard
        dashboard = SleeperAnalyticsDashboard()
        print("✅ Dashboard initialized successfully")
        
        # Test data extraction
        print("📊 Testing data extraction...")
        player_data = dashboard.extract_player_data()
        print(f"✅ Extracted data for {len(player_data)} players")
        
        # Test analytics calculation
        print("📈 Testing analytics calculation...")
        analytics = dashboard.calculate_league_analytics()
        print(f"✅ Calculated analytics for {analytics.total_players} players")
        
        # Test summary generation
        print("📝 Testing summary generation...")
        summary = dashboard.generate_performance_summary()
        print("✅ Summary generated successfully")
        
        # Test prediction (if we have players)
        if player_data:
            print("🔮 Testing prediction functionality...")
            first_player_id = list(player_data.keys())[0]
            prediction = dashboard.predict_next_week_performance(first_player_id)
            print(f"✅ Prediction generated: {prediction['predicted_score']:.2f}")
        
        print("\n🎉 All tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_chart_generation():
    """Test chart generation functionality"""
    print("\n📊 Testing chart generation...")
    
    try:
        dashboard = SleeperAnalyticsDashboard()
        dashboard.extract_player_data()
        dashboard.calculate_league_analytics()
        
        # Test each chart type
        test_dir = "outputs/test_charts"
        os.makedirs(test_dir, exist_ok=True)
        
        print("   • Testing weekly trends chart...")
        dashboard.create_weekly_trends_chart(f"{test_dir}/test_weekly_trends.png")
        
        print("   • Testing score distribution chart...")
        dashboard.create_score_distribution_chart(f"{test_dir}/test_score_distribution.png")
        
        print("   • Testing top performers chart...")
        dashboard.create_top_performers_chart(f"{test_dir}/test_top_performers.png")
        
        print("   • Testing improvement trends chart...")
        dashboard.create_improvement_trends_chart(f"{test_dir}/test_improvement_trends.png")
        
        print("✅ All charts generated successfully!")
        print(f"📁 Test charts saved to: {test_dir}/")
        return True
        
    except Exception as e:
        print(f"❌ Chart generation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function"""
    print("🚀 Starting Sleeper Analytics Dashboard Tests")
    print("=" * 50)
    
    # Run basic functionality tests
    basic_test_passed = test_analytics_dashboard()
    
    # Run chart generation tests
    chart_test_passed = test_chart_generation()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY:")
    print(f"   Basic Functionality: {'✅ PASSED' if basic_test_passed else '❌ FAILED'}")
    print(f"   Chart Generation: {'✅ PASSED' if chart_test_passed else '❌ FAILED'}")
    
    if basic_test_passed and chart_test_passed:
        print("\n🎉 ALL TESTS PASSED! Analytics dashboard is ready to use.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    exit(main())
