import requests
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class SleeperSkinsGameMVP:
    def __init__(self, league_id: str):
        """
        Minimal MVP for Sleeper Skins Game automation
        
        Args:
            league_id: Your Sleeper league ID
        """
        self.league_id = league_id
        self.base_url = "https://api.sleeper.app/v1"
        self.results_file = "data/skins_game_results.json"
        
        # Cache for API data
        self._users_cache = None
        self._rosters_cache = None
        self._league_info_cache = None
    
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
    
    def get_current_week(self) -> int:
        """Get current week from league info"""
        league_info = self.get_league_info()
        current_leg = league_info.get('metadata', {}).get('current_pickem_leg_id', '')
        
        if current_leg:
            # Parse "v1:regular:18" to get week number
            parts = current_leg.split(':')
            if len(parts) >= 3:
                return int(parts[2])
        
        raise Exception("Could not determine current week from league info")
    
    def calculate_highest_scorer(self, week: int) -> Tuple[List[str], float]:
        """Calculate the highest scoring user(s) for a specific week"""
        rosters = self.get_rosters()
        week_key = f"v1:regular:{week}"
        
        user_scores = {}
        
        for roster in rosters:
            owner_id = roster.get('owner_id')
            if not owner_id:
                continue
            
            points_by_leg = roster.get('metadata', {}).get('points_by_leg', {})
            week_score = points_by_leg.get(week_key, 0)
            user_scores[owner_id] = float(week_score)
        
        if not user_scores:
            return [], 0
        
        max_score = max(user_scores.values())
        winners = [owner_id for owner_id, score in user_scores.items() if score == max_score]
        
        return winners, max_score
    
    def get_week_picks(self, week: int) -> Dict[str, List[str]]:
        """Get all user picks for a specific week"""
        rosters = self.get_rosters()
        week_key = f"v1:regular:{week}"
        
        user_picks = {}
        
        for roster in rosters:
            owner_id = roster.get('owner_id')
            if not owner_id:
                continue
            
            previous_picks = roster.get('metadata', {}).get('previous_picks', {})
            week_picks = previous_picks.get(week_key, [])
            user_picks[owner_id] = week_picks
        
        return user_picks
    
    def calculate_week_rankings(self, week: int) -> Dict[str, List[str]]:
        """
        Calculate rankings for all users for a specific week
        
        Args:
            week: Week number
        
        Returns:
            Dictionary with rankings: {
                'highest': [owner_ids],
                'second_highest': [owner_ids], 
                'third_highest': [owner_ids],
                'lowest': [owner_ids],
                'no_picks': [owner_ids]  # Users with 0 points and no picks
            }
        """
        rosters = self.get_rosters()
        week_key = f"v1:regular:{week}"
        
        user_scores = {}
        user_picks = {}
        
        for roster in rosters:
            owner_id = roster.get('owner_id')
            if not owner_id:
                continue
            
            points_by_leg = roster.get('metadata', {}).get('points_by_leg', {})
            week_score = points_by_leg.get(week_key, 0)
            user_scores[owner_id] = float(week_score)
            
            # Get picks for this user
            previous_picks = roster.get('metadata', {}).get('previous_picks', {})
            week_picks = previous_picks.get(week_key, [])
            user_picks[owner_id] = week_picks
        
        if not user_scores:
            return {'highest': [], 'second_highest': [], 'third_highest': [], 'lowest': [], 'no_picks': []}
        
        # Separate users with 0 points and no picks from those with actual scores
        users_with_picks = {}
        users_no_picks = []
        
        for owner_id, score in user_scores.items():
            if score == 0 and len(user_picks.get(owner_id, [])) == 0:
                users_no_picks.append(owner_id)
            else:
                users_with_picks[owner_id] = score
        
        # Sort scores in descending order (only for users with picks)
        sorted_scores = sorted(users_with_picks.items(), key=lambda x: x[1], reverse=True)
        
        # Group users by score
        score_groups = {}
        for owner_id, score in sorted_scores:
            if score not in score_groups:
                score_groups[score] = []
            score_groups[score].append(owner_id)
        
        # Get unique scores in order
        unique_scores = sorted(score_groups.keys(), reverse=True)
        
        rankings = {
            'highest': score_groups[unique_scores[0]] if unique_scores else [],
            'second_highest': score_groups[unique_scores[1]] if len(unique_scores) > 1 else [],
            'third_highest': score_groups[unique_scores[2]] if len(unique_scores) > 2 else [],
            'lowest': score_groups[unique_scores[-1]] if unique_scores else [],
            'no_picks': users_no_picks
        }
        
        return rankings
    
    def check_perfect_week(self, week: int, odds_data: Dict[str, dict]) -> List[str]:
        """Check if any user had a perfect week"""
        user_picks = self.get_week_picks(week)
        
        # Get all winning teams
        winning_teams = [team for team, data in odds_data.items() if data.get('won', False)]
        total_games = len(odds_data)
        
        perfect_week_users = []
        
        for owner_id, picks in user_picks.items():
            # Check if all picks were correct
            correct_picks = len([pick for pick in picks if pick in winning_teams])
            if correct_picks == total_games and len(picks) == total_games:
                perfect_week_users.append(owner_id)
        
        return perfect_week_users
    
    def load_results(self) -> List[dict]:
        """Load existing results from storage"""
        try:
            with open(self.results_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_results(self, results: List[dict]):
        """Save results to storage"""
        with open(self.results_file, 'w') as f:
            json.dump(results, f, indent=2)
    
    def process_week(self, week: int, odds_data: Dict[str, dict] = None, season: int = None):
        """
        Process results for a specific week and store them
        
        Args:
            week: Week number to process
            odds_data: Dictionary with game results (optional, only needed for perfect week detection)
                Format: {
                    "ARI": {"opponent": "LAR", "won": False},
                    "LAR": {"opponent": "ARI", "won": True},
                    ...
                }
            season: Season year (auto-detected if not provided)
        """
        # Get season from league info if not provided
        if season is None:
            league_info = self.get_league_info()
            season = league_info.get('season', 2025)
        
        print(f"Processing Week {week}, Season {season}...")
        
        # Get users for display names
        users = self.get_users()
        
        # Calculate rankings
        rankings = self.calculate_week_rankings(week)
        
        # Get scores for each ranking group
        scores = {}
        for ranking_type, owner_ids in rankings.items():
            if ranking_type == 'no_picks':
                scores[ranking_type] = 0  # No picks users always have 0 points
            elif owner_ids:
                scores[ranking_type] = self.get_user_score_for_week(owner_ids[0], week)
            else:
                scores[ranking_type] = 0
        
        # Check for perfect week if odds data is provided
        perfect_week_winners = []
        if odds_data:
            perfect_week_winners = self.check_perfect_week(week, odds_data)
        
        # Create result record
        result = {
            'week': week,
            'season': season,
            'date_processed': datetime.now().isoformat(),
            'rankings': rankings,
            'scores': scores,
            'perfect_week_winners': perfect_week_winners,
            'winner_names': {
                'highest': [users.get(uid, {}).get('display_name', 'Unknown') for uid in rankings['highest']],
                'second_highest': [users.get(uid, {}).get('display_name', 'Unknown') for uid in rankings['second_highest']],
                'third_highest': [users.get(uid, {}).get('display_name', 'Unknown') for uid in rankings['third_highest']],
                'lowest': [users.get(uid, {}).get('display_name', 'Unknown') for uid in rankings['lowest']],
                'no_picks': [users.get(uid, {}).get('display_name', 'Unknown') for uid in rankings['no_picks']],
                'perfect_week': [users.get(uid, {}).get('display_name', 'Unknown') for uid in perfect_week_winners]
            }
        }
        
        # Load existing results and add new one
        results = self.load_results()
        results.append(result)
        self.save_results(results)
        
        return result
    
    def get_week_summary(self, week: int) -> dict:
        """Get a summary of picks and scores for a week"""
        users = self.get_users()
        user_picks = self.get_week_picks(week)
        high_score_winners, high_score = self.calculate_highest_scorer(week)
        
        summary = {
            'week': week,
            'high_score': high_score,
            'high_score_winners': high_score_winners,
            'user_data': []
        }
        
        for owner_id, picks in user_picks.items():
            user_info = users.get(owner_id, {})
            summary['user_data'].append({
                'owner_id': owner_id,
                'display_name': user_info.get('display_name', 'Unknown'),
                'picks': picks,
                'score': self.get_user_score_for_week(owner_id, week)
            })
        
        return summary
    
    def get_user_score_for_week(self, owner_id: str, week: int) -> float:
        """Get a specific user's score for a specific week"""
        rosters = self.get_rosters()
        week_key = f"v1:regular:{week}"
        
        for roster in rosters:
            if roster.get('owner_id') == owner_id:
                points_by_leg = roster.get('metadata', {}).get('points_by_leg', {})
                return float(points_by_leg.get(week_key, 0))
        
        return 0.0
    
    
    def view_all_results(self):
        """Display all stored results"""
        results = self.load_results()
        
        if not results:
            print("No results stored yet.")
            return
        
        print("\n📊 ALL STORED RESULTS 📊")
        for result in results:
            print(f"\nWeek {result['week']} ({result['season']}):")
            
            # Handle new format
            if 'rankings' in result:
                print(f"  🥇 Highest: {', '.join(result['winner_names']['highest'])} - {result['scores']['highest']} pts")
                if result['rankings']['second_highest']:
                    print(f"  🥈 Second: {', '.join(result['winner_names']['second_highest'])} - {result['scores']['second_highest']} pts")
                if result['rankings']['third_highest']:
                    print(f"  🥉 Third: {', '.join(result['winner_names']['third_highest'])} - {result['scores']['third_highest']} pts")
                print(f"  📉 Lowest: {', '.join(result['winner_names']['lowest'])} - {result['scores']['lowest']} pts")
                
                if result['rankings'].get('no_picks'):
                    print(f"  ❌ No Picks: {', '.join(result['winner_names']['no_picks'])}")
                
                # Always show perfect week line, even if empty
                if result['perfect_week_winners']:
                    print(f"  🎯 Perfect Week: {', '.join(result['winner_names']['perfect_week'])}")
                else:
                    print(f"  🎯 Perfect Week: ")
            
            # Handle old format for backward compatibility
            else:
                print(f"  High Score: {', '.join(result['winner_names']['high_score'])} - {result['high_score']} pts")
                if 'underdog_percentage' in result:
                    print(f"  Underdog: {', '.join(result['winner_names']['underdog'])} - {result['underdog_percentage']:.1f}% correct")
                else:
                    print(f"  Underdog: {', '.join(result['winner_names']['underdog'])} - {result.get('underdog_correct', 0)}/{result['total_underdog_games']} correct")


def main():
    """Example usage of the MVP"""
    
    # Initialize with your league ID
    # league_id = "1137502853016403968"  # Old league ID (commented out)
    league_id = "1267183695911976960"  # Current season league ID
    skins_game = SleeperSkinsGameMVP(league_id)
    
    try:
        # Get current week
        current_week = skins_game.get_current_week()
        print(f"Current week detected: {current_week}")
        
        # Get a summary of the current week
        summary = skins_game.get_week_summary(current_week)
        print(f"\nWeek {current_week} Summary:")
        print(f"High Score: {summary['high_score']} points")
        
        for user_data in summary['user_data']:
            print(f"{user_data['display_name']}: {user_data['score']} pts, Picks: {user_data['picks']}")
        
        # Example of how to process a week (no odds data needed for basic rankings)
        # skins_game.process_week(current_week)
        
        # Example with perfect week detection (if you have game results)
        # example_game_results = {
        #     "ARI": {"opponent": "LAR", "won": False},
        #     "LAR": {"opponent": "ARI", "won": True},
        #     # ... add all games for the week
        # }
        # skins_game.process_week(current_week, example_game_results)
        
        # View all stored results
        skins_game.view_all_results()
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
