"""
Analytics Dashboard for Sleeper Pickem League
Provides comprehensive analytics and insights for league performance
"""

import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from collections import defaultdict, Counter
import numpy as np
from dataclasses import dataclass

# Handle both relative and absolute imports
try:
    from .secure_config import config
except ImportError:
    from secure_config import config


@dataclass
class PlayerPerformance:
    """Data class for player performance metrics"""
    user_id: str
    display_name: str
    weekly_scores: Dict[int, float]
    total_score: float
    average_score: float
    consistency_score: float
    improvement_trend: float
    perfect_weeks: int
    zero_weeks: int


@dataclass
class LeagueAnalytics:
    """Data class for league-wide analytics"""
    total_players: int
    weeks_analyzed: int
    average_league_score: float
    score_distribution: Dict[float, int]
    top_performers: List[PlayerPerformance]
    most_improved: List[PlayerPerformance]
    most_consistent: List[PlayerPerformance]


class SleeperAnalyticsDashboard:
    """Main analytics dashboard class for Sleeper pickem league"""
    
    def __init__(self, league_id: str = None):
        """
        Initialize the analytics dashboard
        
        Args:
            league_id: Your Sleeper league ID (optional, will use config if not provided)
        """
        self.league_id = league_id or config.sleeper_league_id
        self.base_url = "https://api.sleeper.app/v1"
        
        # Cache for API data
        self._users_cache = None
        self._rosters_cache = None
        self._league_info_cache = None
        
        # Analytics data
        self.player_performances = {}
        self.league_analytics = None
        
        # Set up plotting style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def get_league_info(self) -> dict:
        """Get league information including current week"""
        if self._league_info_cache is None:
            url = f"{self.base_url}/league/{self.league_id}"
            response = requests.get(url)
            
            if response.status_code == 200:
                self._league_info_cache = response.json()
            else:
                raise Exception(f"Failed to get league info: {response.status_code}")
        
        return self._league_info_cache
    
    def get_users(self) -> Dict[str, dict]:
        """Get all users in the league with caching"""
        if self._users_cache is None:
            url = f"{self.base_url}/league/{self.league_id}/users"
            response = requests.get(url)
            
            if response.status_code == 200:
                users = response.json()
                self._users_cache = {user['user_id']: user for user in users}
            else:
                raise Exception(f"Failed to get league users: {response.status_code}")
        
        return self._users_cache
    
    def get_rosters(self) -> List[dict]:
        """Get all rosters data with caching"""
        if self._rosters_cache is None:
            url = f"{self.base_url}/league/{self.league_id}/rosters"
            response = requests.get(url)
            
            if response.status_code == 200:
                self._rosters_cache = response.json()
            else:
                raise Exception(f"Failed to get rosters: {response.status_code}")
        
        return self._rosters_cache
    
    def extract_player_data(self) -> Dict[str, PlayerPerformance]:
        """Extract and process player performance data"""
        users = self.get_users()
        rosters = self.get_rosters()
        
        player_performances = {}
        
        for roster in rosters:
            owner_id = roster.get('owner_id')
            if not owner_id:
                continue
            
            user_info = users.get(owner_id, {})
            display_name = user_info.get('display_name', 'Unknown')
            
            # Extract weekly scores
            metadata = roster.get('metadata', {})
            points_by_leg = metadata.get('points_by_leg', {})
            
            weekly_scores = {}
            for leg_key, score in points_by_leg.items():
                # Parse "v1:regular:X" to get week number
                if 'regular:' in leg_key:
                    week_num = int(leg_key.split(':')[2])
                    weekly_scores[week_num] = float(score)
            
            if not weekly_scores:
                continue
            
            # Calculate performance metrics
            scores = list(weekly_scores.values())
            total_score = sum(scores)
            average_score = total_score / len(scores) if scores else 0
            
            # Calculate consistency (lower standard deviation = more consistent)
            consistency_score = 1 / (np.std(scores) + 1) if len(scores) > 1 else 1
            
            # Calculate improvement trend (slope of scores over time)
            weeks = sorted(weekly_scores.keys())
            if len(weeks) > 1:
                x = np.array(weeks)
                y = np.array([weekly_scores[w] for w in weeks])
                improvement_trend = np.polyfit(x, y, 1)[0]  # Linear regression slope
            else:
                improvement_trend = 0
            
            # Count perfect and zero weeks
            perfect_weeks = sum(1 for score in scores if score == max(scores))
            zero_weeks = sum(1 for score in scores if score == 0)
            
            player_performances[owner_id] = PlayerPerformance(
                user_id=owner_id,
                display_name=display_name,
                weekly_scores=weekly_scores,
                total_score=total_score,
                average_score=average_score,
                consistency_score=consistency_score,
                improvement_trend=improvement_trend,
                perfect_weeks=perfect_weeks,
                zero_weeks=zero_weeks
            )
        
        self.player_performances = player_performances
        return player_performances
    
    def calculate_league_analytics(self) -> LeagueAnalytics:
        """Calculate league-wide analytics"""
        if not self.player_performances:
            self.extract_player_data()
        
        # Basic league stats
        total_players = len(self.player_performances)
        all_scores = []
        for player in self.player_performances.values():
            all_scores.extend(player.weekly_scores.values())
        
        weeks_analyzed = len(set().union(*[p.weekly_scores.keys() for p in self.player_performances.values()]))
        average_league_score = np.mean(all_scores) if all_scores else 0
        
        # Score distribution
        score_distribution = Counter([round(score, 1) for score in all_scores])
        
        # Top performers (by average score)
        top_performers = sorted(
            self.player_performances.values(),
            key=lambda p: p.average_score,
            reverse=True
        )[:10]
        
        # Most improved (by improvement trend)
        most_improved = sorted(
            self.player_performances.values(),
            key=lambda p: p.improvement_trend,
            reverse=True
        )[:10]
        
        # Most consistent (by consistency score)
        most_consistent = sorted(
            self.player_performances.values(),
            key=lambda p: p.consistency_score,
            reverse=True
        )[:10]
        
        self.league_analytics = LeagueAnalytics(
            total_players=total_players,
            weeks_analyzed=weeks_analyzed,
            average_league_score=average_league_score,
            score_distribution=dict(score_distribution),
            top_performers=top_performers,
            most_improved=most_improved,
            most_consistent=most_consistent
        )
        
        return self.league_analytics
    
    def generate_performance_summary(self) -> str:
        """Generate a text summary of league performance"""
        if not self.league_analytics:
            self.calculate_league_analytics()
        
        analytics = self.league_analytics
        
        summary = f"""
🏈 LEAGUE PERFORMANCE SUMMARY 🏈
{'='*50}

📊 OVERALL STATISTICS:
• Total Players: {analytics.total_players}
• Weeks Analyzed: {analytics.weeks_analyzed}
• Average League Score: {analytics.average_league_score:.2f}

🏆 TOP PERFORMERS (by average score):
"""
        
        for i, player in enumerate(analytics.top_performers[:5], 1):
            summary += f"{i}. {player.display_name}: {player.average_score:.2f} avg\n"
        
        summary += "\n📈 MOST IMPROVED PLAYERS:\n"
        for i, player in enumerate(analytics.most_improved[:5], 1):
            trend_emoji = "📈" if player.improvement_trend > 0 else "📉"
            summary += f"{i}. {player.display_name}: {trend_emoji} {player.improvement_trend:+.2f} trend\n"
        
        summary += "\n🎯 MOST CONSISTENT PLAYERS:\n"
        for i, player in enumerate(analytics.most_consistent[:5], 1):
            summary += f"{i}. {player.display_name}: {player.consistency_score:.3f} consistency\n"
        
        return summary
    
    def create_weekly_trends_chart(self, save_path: str = None) -> None:
        """Create a chart showing weekly trends for all players"""
        if not self.player_performances:
            self.extract_player_data()
        
        plt.figure(figsize=(15, 10))
        
        # Plot each player's weekly scores
        for player in self.player_performances.values():
            weeks = sorted(player.weekly_scores.keys())
            scores = [player.weekly_scores[w] for w in weeks]
            
            plt.plot(weeks, scores, marker='o', label=player.display_name, alpha=0.7)
        
        plt.xlabel('Week')
        plt.ylabel('Score')
        plt.title('Weekly Performance Trends - All Players')
        plt.grid(True, alpha=0.3)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
        else:
            plt.show()
        
        plt.close()
    
    def create_score_distribution_chart(self, save_path: str = None) -> None:
        """Create a histogram of score distribution"""
        if not self.league_analytics:
            self.calculate_league_analytics()
        
        plt.figure(figsize=(12, 8))
        
        # Get all scores
        all_scores = []
        for player in self.player_performances.values():
            all_scores.extend(player.weekly_scores.values())
        
        # Create histogram
        plt.hist(all_scores, bins=20, alpha=0.7, edgecolor='black')
        plt.xlabel('Score')
        plt.ylabel('Frequency')
        plt.title('Score Distribution Across All Players')
        plt.grid(True, alpha=0.3)
        
        # Add statistics
        mean_score = np.mean(all_scores)
        median_score = np.median(all_scores)
        plt.axvline(mean_score, color='red', linestyle='--', label=f'Mean: {mean_score:.2f}')
        plt.axvline(median_score, color='green', linestyle='--', label=f'Median: {median_score:.2f}')
        plt.legend()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
        else:
            plt.show()
        
        plt.close()
    
    def create_top_performers_chart(self, save_path: str = None) -> None:
        """Create a bar chart of top performers"""
        if not self.league_analytics:
            self.calculate_league_analytics()
        
        plt.figure(figsize=(12, 8))
        
        top_10 = self.league_analytics.top_performers[:10]
        names = [player.display_name for player in top_10]
        scores = [player.average_score for player in top_10]
        
        bars = plt.bar(range(len(names)), scores, alpha=0.7)
        plt.xlabel('Players')
        plt.ylabel('Average Score')
        plt.title('Top 10 Performers (by Average Score)')
        plt.xticks(range(len(names)), names, rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for i, (bar, score) in enumerate(zip(bars, scores)):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                    f'{score:.2f}', ha='center', va='bottom')
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
        else:
            plt.show()
        
        plt.close()
    
    def create_improvement_trends_chart(self, save_path: str = None) -> None:
        """Create a chart showing improvement trends"""
        if not self.league_analytics:
            self.calculate_league_analytics()
        
        plt.figure(figsize=(12, 8))
        
        # Get improvement data
        players = list(self.player_performances.values())
        names = [player.display_name for player in players]
        trends = [player.improvement_trend for player in players]
        
        # Color bars based on trend direction
        colors = ['green' if trend > 0 else 'red' for trend in trends]
        
        bars = plt.bar(range(len(names)), trends, color=colors, alpha=0.7)
        plt.xlabel('Players')
        plt.ylabel('Improvement Trend')
        plt.title('Player Improvement Trends (Positive = Improving)')
        plt.xticks(range(len(names)), names, rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        plt.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        
        # Add value labels
        for i, (bar, trend) in enumerate(zip(bars, trends)):
            plt.text(bar.get_x() + bar.get_width()/2, 
                    bar.get_height() + (0.01 if trend > 0 else -0.01),
                    f'{trend:+.2f}', ha='center', 
                    va='bottom' if trend > 0 else 'top')
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
        else:
            plt.show()
        
        plt.close()
    
    def predict_next_week_performance(self, player_id: str) -> Dict[str, float]:
        """Predict next week's performance for a specific player"""
        if not self.player_performances:
            self.extract_player_data()
        
        if player_id not in self.player_performances:
            raise ValueError(f"Player {player_id} not found")
        
        player = self.player_performances[player_id]
        
        if len(player.weekly_scores) < 2:
            return {"predicted_score": player.average_score, "confidence": 0.1}
        
        # Simple linear regression prediction
        weeks = sorted(player.weekly_scores.keys())
        scores = [player.weekly_scores[w] for w in weeks]
        
        # Predict next week
        next_week = max(weeks) + 1
        
        # Linear regression
        x = np.array(weeks)
        y = np.array(scores)
        
        # Calculate slope and intercept
        slope, intercept = np.polyfit(x, y, 1)
        predicted_score = slope * next_week + intercept
        
        # Calculate confidence based on R-squared
        y_pred = slope * x + intercept
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        confidence = max(0.1, min(0.9, r_squared))
        
        return {
            "predicted_score": max(0, predicted_score),  # Ensure non-negative
            "confidence": confidence,
            "trend": slope,
            "next_week": next_week
        }
    
    def generate_full_dashboard(self, output_dir: str = "analytics_output") -> None:
        """Generate complete analytics dashboard with all charts and summary"""
        import os
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract data and calculate analytics
        print("📊 Extracting player data...")
        self.extract_player_data()
        
        print("📈 Calculating league analytics...")
        self.calculate_league_analytics()
        
        # Generate summary
        print("📝 Generating performance summary...")
        summary = self.generate_performance_summary()
        
        # Save summary to file
        with open(f"{output_dir}/performance_summary.txt", "w") as f:
            f.write(summary)
        
        print(summary)
        
        # Generate charts
        print("📊 Creating charts...")
        
        chart_paths = {
            "weekly_trends": f"{output_dir}/weekly_trends.png",
            "score_distribution": f"{output_dir}/score_distribution.png",
            "top_performers": f"{output_dir}/top_performers.png",
            "improvement_trends": f"{output_dir}/improvement_trends.png"
        }
        
        self.create_weekly_trends_chart(chart_paths["weekly_trends"])
        self.create_score_distribution_chart(chart_paths["score_distribution"])
        self.create_top_performers_chart(chart_paths["top_performers"])
        self.create_improvement_trends_chart(chart_paths["improvement_trends"])
        
        print(f"✅ Dashboard generated successfully!")
        print(f"📁 Output directory: {output_dir}")
        print(f"📊 Charts saved:")
        for name, path in chart_paths.items():
            print(f"   • {name}: {path}")
        print(f"📝 Summary: {output_dir}/performance_summary.txt")


# Example usage
if __name__ == "__main__":
    # Initialize dashboard
    dashboard = SleeperAnalyticsDashboard()
    
    # Generate full dashboard
    dashboard.generate_full_dashboard()
    
    # Example of individual predictions
    print("\n🔮 PREDICTION EXAMPLES:")
    users = dashboard.get_users()
    for user_id in list(users.keys())[:3]:  # Show predictions for first 3 users
        try:
            prediction = dashboard.predict_next_week_performance(user_id)
            user_name = users[user_id]['display_name']
            print(f"{user_name}: Predicted {prediction['predicted_score']:.2f} "
                  f"(confidence: {prediction['confidence']:.2f})")
        except Exception as e:
            print(f"Error predicting for user {user_id}: {e}")
