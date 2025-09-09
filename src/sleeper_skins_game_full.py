import requests
import pandas as pd
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from twilio.rest import Client
import schedule
import time

class SleeperSkinsGame:
    def __init__(self, league_id: str, config_file: str = "config.json"):
        """
        Initialize the Sleeper Skins Game automation
        
        Args:
            league_id: Your Sleeper league ID
            config_file: Path to configuration file
        """
        self.league_id = league_id
        self.base_url = "https://api.sleeper.app/v1"
        self.data_file = "skins_game_data.xlsx"
        
        # Load configuration
        self.config = self.load_config(config_file)
        
        # Initialize Twilio client if configured
        if self.config.get('twilio'):
            self.twilio_client = Client(
                self.config['twilio']['account_sid'],
                self.config['twilio']['auth_token']
            )
        
        # Skins game settings
        self.weekly_high_score_payout = 10
        self.weekly_underdog_payout = 3
        self.perfect_week_payout = 40
        
        # Initialize data storage
        self.init_data_storage()
        
        # Cache for user data
        self._users_cache = None
        self._rosters_cache = None
    
    def load_config(self, config_file: str) -> dict:
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config file {config_file} not found. Creating template...")
            self.create_config_template(config_file)
            return {}
    
    def create_config_template(self, config_file: str):
        """Create a template configuration file"""
        template = {
            "twilio": {
                "account_sid": "YOUR_TWILIO_ACCOUNT_SID",
                "auth_token": "YOUR_TWILIO_AUTH_TOKEN",
                "from_number": "+1234567890",
                "to_numbers": ["+1234567890", "+0987654321"]
            },
            "league_settings": {
                "current_season": 2025,
                "league_name": "Your League Name"
            },
            "odds": {
                "example_format": {
                    "1": {
                        "ARI": {"opponent": "LAR", "is_underdog": true},
                        "ATL": {"opponent": "PHI", "is_underdog": false},
                        "note": "Add all games for each week with underdog designation"
                    }
                }
            }
        }
        
        with open(config_file, 'w') as f:
            json.dump(template, f, indent=2)
        
        print(f"Created config template at {config_file}. Please update with your settings.")
    
    def init_data_storage(self):
        """Initialize Excel file for data storage"""
        if not os.path.exists(self.data_file):
            weeks_df = pd.DataFrame(columns=[
                'week', 'season', 'date_processed', 'high_score_winner', 'high_score_points',
                'underdog_winner', 'underdog_correct', 'perfect_week_winner', 'total_games',
                'high_score_payout', 'underdog_payout', 'perfect_week_payout'
            ])
            
            skins_df = pd.DataFrame(columns=[
                'week', 'season', 'high_score_skin_amount', 'underdog_skin_amount',
                'high_score_carried_over', 'underdog_carried_over'
            ])
            
            users_df = pd.DataFrame(columns=[
                'user_id', 'owner_id', 'username', 'display_name', 'total_high_score_wins',
                'total_underdog_wins', 'perfect_weeks', 'total_winnings'
            ])
            
            with pd.ExcelWriter(self.data_file, engine='openpyxl') as writer:
                weeks_df.to_excel(writer, sheet_name='Weekly_Results', index=False)
                skins_df.to_excel(writer, sheet_name='Skins_Tracking', index=False)
                users_df.to_excel(writer, sheet_name='User_Stats', index=False)
            
            print(f"Created data storage file: {self.data_file}")
    
    def get_league_info(self) -> dict:
        """Get league information including current week"""
        url = f"{self.base_url}/league/{self.league_id}"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get league info: {response.status_code}")
    
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
    
    def create_owner_to_user_mapping(self) -> Dict[str, str]:
        """Create mapping from owner_id to user_id"""
        rosters = self.get_rosters()
        return {roster['owner_id']: roster['owner_id'] for roster in rosters if roster.get('owner_id')}
    
    def get_current_week(self) -> Tuple[int, str]:
        """Get current week from league info"""
        league_info = self.get_league_info()
        current_leg = league_info.get('metadata', {}).get('current_pickem_leg_id', '')
        
        if current_leg:
            # Parse "v1:regular:18" to get week number
            parts = current_leg.split(':')
            if len(parts) >= 3:
                return int(parts[2]), current_leg
        
        raise Exception("Could not determine current week from league info")
    
    def calculate_high_score_winners(self, week: int) -> Tuple[List[str], float]:
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
    
    def calculate_underdog_winners(self, week: int, odds_data: Dict[str, dict]) -> Tuple[List[str], int, int]:
        """
        Calculate user(s) with most correct underdog picks
        
        Args:
            week: Week number
            odds_data: Dictionary with game odds/results for the week
                Format: {
                    "team": {"opponent": "OPP", "is_underdog": True/False, "won": True/False}
                }
        
        Returns:
            Tuple of (winner_owner_ids, max_correct_underdogs, total_underdog_games)
        """
        user_picks = self.get_week_picks(week)
        
        # Count underdog games and determine winners
        underdog_teams = [team for team, data in odds_data.items() if data.get('is_underdog', False)]
        underdog_winners = [team for team in underdog_teams if odds_data[team].get('won', False)]
        
        total_underdog_games = len(underdog_teams)
        
        user_underdog_correct = {}
        
        for owner_id, picks in user_picks.items():
            correct_underdogs = len([pick for pick in picks if pick in underdog_winners])
            user_underdog_correct[owner_id] = correct_underdogs
        
        if not user_underdog_correct:
            return [], 0, total_underdog_games
        
        max_correct = max(user_underdog_correct.values())
        winners = [owner_id for owner_id, correct in user_underdog_correct.items() if correct == max_correct]
        
        return winners, max_correct, total_underdog_games
    
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
    
    def load_current_skins(self) -> Dict[str, float]:
        """Load current skin amounts"""
        try:
            skins_df = pd.read_excel(self.data_file, sheet_name='Skins_Tracking')
            
            if skins_df.empty:
                return {'high_score': self.weekly_high_score_payout, 'underdog': self.weekly_underdog_payout}
            
            latest = skins_df.iloc[-1]
            return {
                'high_score': latest.get('high_score_skin_amount', self.weekly_high_score_payout),
                'underdog': latest.get('underdog_skin_amount', self.weekly_underdog_payout)
            }
        except:
            return {'high_score': self.weekly_high_score_payout, 'underdog': self.weekly_underdog_payout}
    
    def process_week(self, week: int, odds_data: Dict[str, dict], season: int = 2025):
        """
        Process results for a specific week
        
        Args:
            week: Week number to process
            odds_data: Dictionary with game odds and results
                Format: {
                    "ARI": {"opponent": "LAR", "is_underdog": True, "won": False},
                    "LAR": {"opponent": "ARI", "is_underdog": False, "won": True},
                    ...
                }
        """
        print(f"Processing Week {week}, Season {season}...")
        
        # Get users and create mapping
        users = self.get_users()
        
        # Calculate winners
        high_score_winners, high_score = self.calculate_high_score_winners(week)
        underdog_winners, underdog_correct, total_underdog_games = self.calculate_underdog_winners(week, odds_data)
        perfect_week_winners = self.check_perfect_week(week, odds_data)
        
        # Get current skin amounts
        current_skins = self.load_current_skins()
        
        # Determine payouts and carry-overs
        high_score_payout = current_skins['high_score']
        underdog_payout = current_skins['underdog']
        
        # Handle ties (carry over skins)
        high_score_carried = len(high_score_winners) != 1
        underdog_carried = len(underdog_winners) != 1
        
        next_high_score_skin = (high_score_payout + self.weekly_high_score_payout 
                               if high_score_carried else self.weekly_high_score_payout)
        next_underdog_skin = (underdog_payout + self.weekly_underdog_payout 
                             if underdog_carried else self.weekly_underdog_payout)
        
        # Save results
        self.save_week_results(
            week, season, high_score_winners, high_score, underdog_winners, 
            underdog_correct, perfect_week_winners, len(odds_data), high_score_payout, 
            underdog_payout, self.perfect_week_payout if perfect_week_winners else 0
        )
        
        # Save next week's skin amounts
        self.save_skin_amounts(week + 1, season, next_high_score_skin, next_underdog_skin, 
                              high_score_carried, underdog_carried)
        
        # Update user stats
        self.update_user_stats(high_score_winners, underdog_winners, perfect_week_winners,
                              high_score_payout, underdog_payout, users)
        
        # Send notifications
        self.send_notifications(week, season, high_score_winners, high_score, 
                              underdog_winners, underdog_correct, perfect_week_winners,
                              high_score_payout, underdog_payout, high_score_carried, 
                              underdog_carried, users, total_underdog_games)
        
        print(f"Week {week} processing complete!")
    
    def save_week_results(self, week: int, season: int, high_score_winners: List[str], 
                         high_score: float, underdog_winners: List[str], underdog_correct: int,
                         perfect_week_winners: List[str], total_games: int, 
                         high_score_payout: float, underdog_payout: float, perfect_week_payout: float):
        """Save week results to Excel"""
        
        weeks_df = pd.read_excel(self.data_file, sheet_name='Weekly_Results')
        
        new_row = {
            'week': week,
            'season': season,
            'date_processed': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'high_score_winner': ', '.join(high_score_winners) if high_score_winners else 'TIE',
            'high_score_points': high_score,
            'underdog_winner': ', '.join(underdog_winners) if underdog_winners else 'TIE',
            'underdog_correct': underdog_correct,
            'perfect_week_winner': ', '.join(perfect_week_winners) if perfect_week_winners else 'None',
            'total_games': total_games,
            'high_score_payout': high_score_payout if len(high_score_winners) == 1 else 0,
            'underdog_payout': underdog_payout if len(underdog_winners) == 1 else 0,
            'perfect_week_payout': perfect_week_payout
        }
        
        weeks_df = pd.concat([weeks_df, pd.DataFrame([new_row])], ignore_index=True)
        
        with pd.ExcelWriter(self.data_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            weeks_df.to_excel(writer, sheet_name='Weekly_Results', index=False)
    
    def save_skin_amounts(self, week: int, season: int, high_score_amount: float, 
                         underdog_amount: float, high_score_carried: bool, underdog_carried: bool):
        """Save skin amounts for upcoming week"""
        
        skins_df = pd.read_excel(self.data_file, sheet_name='Skins_Tracking')
        
        new_row = {
            'week': week,
            'season': season,
            'high_score_skin_amount': high_score_amount,
            'underdog_skin_amount': underdog_amount,
            'high_score_carried_over': high_score_carried,
            'underdog_carried_over': underdog_carried
        }
        
        skins_df = pd.concat([skins_df, pd.DataFrame([new_row])], ignore_index=True)
        
        with pd.ExcelWriter(self.data_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            skins_df.to_excel(writer, sheet_name='Skins_Tracking', index=False)
    
    def update_user_stats(self, high_score_winners: List[str], underdog_winners: List[str],
                         perfect_week_winners: List[str], high_score_payout: float,
                         underdog_payout: float, users: Dict[str, dict]):
        """Update cumulative user statistics"""
        
        users_df = pd.read_excel(self.data_file, sheet_name='User_Stats')
        
        # Process each user
        all_users = set(high_score_winners + underdog_winners + perfect_week_winners)
        for owner_id in all_users:
            user_info = users.get(owner_id, {})
            
            # Find existing user record or create new one
            user_row = users_df[users_df['owner_id'] == owner_id]
            
            if user_row.empty:
                # New user
                new_user = {
                    'user_id': user_info.get('user_id', owner_id),
                    'owner_id': owner_id,
                    'username': user_info.get('username', 'Unknown'),
                    'display_name': user_info.get('display_name', 'Unknown'),
                    'total_high_score_wins': 0,
                    'total_underdog_wins': 0,
                    'perfect_weeks': 0,
                    'total_winnings': 0
                }
                users_df = pd.concat([users_df, pd.DataFrame([new_user])], ignore_index=True)
                user_idx = len(users_df) - 1
            else:
                user_idx = user_row.index[0]
            
            # Update stats
            if owner_id in high_score_winners and len(high_score_winners) == 1:
                users_df.at[user_idx, 'total_high_score_wins'] += 1
                users_df.at[user_idx, 'total_winnings'] += high_score_payout
            
            if owner_id in underdog_winners and len(underdog_winners) == 1:
                users_df.at[user_idx, 'total_underdog_wins'] += 1
                users_df.at[user_idx, 'total_winnings'] += underdog_payout
            
            if owner_id in perfect_week_winners:
                users_df.at[user_idx, 'perfect_weeks'] += 1
                users_df.at[user_idx, 'total_winnings'] += self.perfect_week_payout
        
        # Save updated stats
        with pd.ExcelWriter(self.data_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            users_df.to_excel(writer, sheet_name='User_Stats', index=False)
    
    def send_notifications(self, week: int, season: int, high_score_winners: List[str], 
                          high_score: float, underdog_winners: List[str], underdog_correct: int,
                          perfect_week_winners: List[str], high_score_payout: float,
                          underdog_payout: float, high_score_carried: bool, 
                          underdog_carried: bool, users: Dict[str, dict], total_underdog_games: int):
        """Send text message notifications"""
        
        if not self.config.get('twilio'):
            print("Twilio not configured - skipping notifications")
            return
        
        # Build message
        message = f"🏈 WEEK {week} SKINS GAME RESULTS 🏈\n\n"
        
        # High Score Results
        if high_score_winners and not high_score_carried:
            winner_names = [users.get(uid, {}).get('display_name', 'Unknown') for uid in high_score_winners]
            message += f"💰 HIGH SCORE WINNER: {', '.join(winner_names)}\n"
            message += f"Score: {high_score} points\nPayout: ${high_score_payout}\n\n"
        elif high_score_carried:
            message += f"🔄 HIGH SCORE TIE ({len(high_score_winners)} players at {high_score} pts)\n"
            message += f"Skin carries over! Next week: ${high_score_payout + self.weekly_high_score_payout}\n\n"
        
        # Underdog Results
        if underdog_winners and not underdog_carried:
            winner_names = [users.get(uid, {}).get('display_name', 'Unknown') for uid in underdog_winners]
            message += f"🐕 UNDERDOG WINNER: {', '.join(winner_names)}\n"
            message += f"Correct underdogs: {underdog_correct}/{total_underdog_games}\nPayout: ${underdog_payout}\n\n"
        elif underdog_carried:
            message += f"🔄 UNDERDOG TIE ({len(underdog_winners)} players with {underdog_correct} correct)\n"
            message += f"Skin carries over! Next week: ${underdog_payout + self.weekly_underdog_payout}\n\n"
        
        # Perfect Week
        if perfect_week_winners:
            winner_names = [users.get(uid, {}).get('display_name', 'Unknown') for uid in perfect_week_winners]
            message += f"🎯 PERFECT WEEK! {', '.join(winner_names)}\n"
            message += f"Payout: ${self.perfect_week_payout}\n\n"
        
        # Next week info
        next_high = high_score_payout + self.weekly_high_score_payout if high_score_carried else self.weekly_high_score_payout
        next_under = underdog_payout + self.weekly_underdog_payout if underdog_carried else self.weekly_underdog_payout
        
        message += f"NEXT WEEK SKINS:\n💰 High Score: ${next_high}\n🐕 Underdog: ${next_under}"
        
        # Send notifications
        for phone_number in self.config['twilio'].get('to_numbers', []):
            try:
                self.twilio_client.messages.create(
                    body=message,
                    from_=self.config['twilio']['from_number'],
                    to=phone_number
                )
                print(f"Notification sent to {phone_number}")
            except Exception as e:
                print(f"Failed to send notification to {phone_number}: {e}")
    
    def get_week_summary(self, week: int) -> dict:
        """Get a summary of picks and scores for a week"""
        users = self.get_users()
        user_picks = self.get_week_picks(week)
        high_score_winners, high_score = self.calculate_high_score_winners(week)
        
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
    
    def create_odds_template(self, week: int) -> dict:
        """Create a template for manual odds input"""
        # This creates a template based on a typical NFL week
        # You'll fill this in manually each week
        template = {
            f"week_{week}_odds": {
                "ARI": {"opponent": "LAR", "is_underdog": True, "won": False},
                "LAR": {"opponent": "ARI", "is_underdog": False, "won": True},
                "ATL": {"opponent": "PHI", "is_underdog": True, "won": False},
                "PHI": {"opponent": "ATL", "is_underdog": False, "won": True},
                # Add all games for the week...
                "note": "Set is_underdog=True for underdogs, won=True for winners"
            }
        }
        
        filename = f"week_{week}_odds_template.json"
        with open(filename, 'w') as f:
            json.dump(template, f, indent=2)
        
        print(f"Created odds template: {filename}")
        print("Fill in all games, set underdogs and winners, then use in process_week()")
        
        return template


# Example usage and testing functions
def example_usage():
    """Example of how to use the system"""
    
    # Initialize
    league_id = "1137502853016403968"  # Your actual league ID
    skins_game = SleeperSkinsGame(league_id)
    
    # Get current week automatically
    try:
        current_week, _ = skins_game.get_current_week()
        print(f"Current week detected: {current_week}")
    except:
        print("Could not auto-detect current week")
        current_week = 18  # Fallback
    
    # Create odds template for manual input
    skins_game.create_odds_template(current_week)
    
    # Example odds data (you'll create this manually each week)
    example_odds = {
        "ARI": {"opponent": "LAR", "is_underdog": True, "won": False},
        "LAR": {"opponent": "ARI", "is_underdog": False, "won": True},
        "ATL": {"opponent": "PHI", "is_underdog": True, "won": True},  # Underdog win!
        "PHI": {"opponent": "ATL", "is_underdog": False, "won": False},
        # ... add all games for the week
    }
    
    # Process the week
    # skins_game.process_week(current_week, example_odds)
    
    # Get a summary of the week
    summary = skins_game.get_week_summary(current_week)
    print(f"\nWeek {current_week} Summary:")
    print(f"High Score: {summary['high_score']} points")
    
    for user_data in summary['user_data']:
        print(f"{user_data['display_name']}: {user_data['score']} pts, Picks: {user_data['picks']}")


if __name__ == "__main__":
    example_usage()
