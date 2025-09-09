import requests
import json
from datetime import datetime
from typing import Dict, List, Optional

class SleeperAPIExplorer:
    def __init__(self, league_id: str):
        self.league_id = league_id
        self.base_url = "https://api.sleeper.app/v1"
        
    def pretty_print(self, data, title: str):
        """Pretty print JSON data with a title"""
        print(f"\n{'='*50}")
        print(f"{title}")
        print('='*50)
        print(json.dumps(data, indent=2))
        print()
    
    def save_to_file(self, data, filename: str):
        """Save data to a JSON file for detailed inspection"""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Data saved to {filename}")
    
    def explore_league_info(self):
        """Get basic league information"""
        print("🏈 EXPLORING LEAGUE INFO...")
        
        url = f"{self.base_url}/league/{self.league_id}"
        response = requests.get(url)
        
        if response.status_code == 200:
            league_data = response.json()
            self.pretty_print(league_data, "LEAGUE INFORMATION")
            self.save_to_file(league_data, "league_info.json")
            
            # Extract key info
            print("KEY LEAGUE DETAILS:")
            print(f"  Name: {league_data.get('name', 'N/A')}")
            print(f"  Season: {league_data.get('season', 'N/A')}")
            print(f"  Week: {league_data.get('leg', 'N/A')}")  # Current week
            print(f"  Status: {league_data.get('status', 'N/A')}")
            print(f"  Scoring Type: {league_data.get('scoring_type', 'N/A')}")
            print(f"  League Type: {league_data.get('type', 'N/A')}")
            
            return league_data
        else:
            print(f"❌ Failed to get league info: {response.status_code}")
            return None
    
    def explore_users(self):
        """Get all users in the league"""
        print("\n👥 EXPLORING LEAGUE USERS...")
        
        url = f"{self.base_url}/league/{self.league_id}/users"
        response = requests.get(url)
        
        if response.status_code == 200:
            users_data = response.json()
            self.pretty_print(users_data, "LEAGUE USERS")
            self.save_to_file(users_data, "users.json")
            
            print("USER SUMMARY:")
            for user in users_data:
                print(f"  {user.get('display_name', 'N/A')} (@{user.get('username', 'N/A')}) - ID: {user.get('user_id', 'N/A')}")
            
            return users_data
        else:
            print(f"❌ Failed to get users: {response.status_code}")
            return None
    
    def explore_rosters(self):
        """Get roster information"""
        print("\n📋 EXPLORING ROSTERS...")
        
        url = f"{self.base_url}/league/{self.league_id}/rosters"
        response = requests.get(url)
        
        if response.status_code == 200:
            rosters_data = response.json()
            self.pretty_print(rosters_data, "ROSTERS")
            self.save_to_file(rosters_data, "rosters.json")
            
            return rosters_data
        else:
            print(f"❌ Failed to get rosters: {response.status_code}")
            return None
    
    def explore_matchups(self, week: int):
        """Explore matchups for a specific week"""
        print(f"\n🏆 EXPLORING WEEK {week} MATCHUPS...")
        
        url = f"{self.base_url}/league/{self.league_id}/matchups/{week}"
        response = requests.get(url)
        
        if response.status_code == 200:
            matchups_data = response.json()
            self.pretty_print(matchups_data, f"WEEK {week} MATCHUPS")
            self.save_to_file(matchups_data, f"week_{week}_matchups.json")
            
            # Summarize matchup data
            print(f"WEEK {week} MATCHUP SUMMARY:")
            for matchup in matchups_data:
                roster_id = matchup.get('roster_id', 'N/A')
                points = matchup.get('points', 0)
                matchup_id = matchup.get('matchup_id', 'N/A')
                print(f"  Roster {roster_id}: {points} points (Matchup {matchup_id})")
            
            return matchups_data
        else:
            print(f"❌ Failed to get week {week} matchups: {response.status_code}")
            return None
    
    def explore_bracket(self):
        """Explore playoff bracket if applicable"""
        print("\n🏆 EXPLORING PLAYOFF BRACKET...")
        
        url = f"{self.base_url}/league/{self.league_id}/bracket/1"  # 1 is winners bracket
        response = requests.get(url)
        
        if response.status_code == 200:
            bracket_data = response.json()
            self.pretty_print(bracket_data, "PLAYOFF BRACKET")
            self.save_to_file(bracket_data, "playoff_bracket.json")
            return bracket_data
        else:
            print(f"❌ No playoff bracket data available: {response.status_code}")
            return None
    
    def explore_transactions(self):
        """Explore league transactions"""
        print("\n💰 EXPLORING TRANSACTIONS...")
        
        url = f"{self.base_url}/league/{self.league_id}/transactions/1"  # Week 1, adjust as needed
        response = requests.get(url)
        
        if response.status_code == 200:
            transactions_data = response.json()
            self.pretty_print(transactions_data, "TRANSACTIONS")
            self.save_to_file(transactions_data, "transactions.json")
            return transactions_data
        else:
            print(f"❌ No transaction data available: {response.status_code}")
            return None
    
    def explore_picks_endpoint(self, week: int):
        """Try to find pick-related endpoints"""
        print(f"\n🎯 EXPLORING PICKS/PREDICTIONS FOR WEEK {week}...")
        
        # Try various potential endpoints for picks
        potential_endpoints = [
            f"/league/{self.league_id}/picks/{week}",
            f"/league/{self.league_id}/predictions/{week}",
            f"/league/{self.league_id}/bracket/{week}",
            f"/league/{self.league_id}/week/{week}/picks",
            f"/league/{self.league_id}/week/{week}",
        ]
        
        for endpoint in potential_endpoints:
            url = f"{self.base_url}{endpoint}"
            print(f"Trying: {url}")
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ SUCCESS! Found data at {endpoint}")
                self.pretty_print(data, f"PICKS DATA - {endpoint}")
                self.save_to_file(data, f"picks_week_{week}_{endpoint.replace('/', '_')}.json")
                return data
            else:
                print(f"  ❌ {response.status_code}")
        
        print("No pick-related endpoints found in standard API")
        return None
    
    def explore_nfl_games(self, week: int, season: int = 2025):
        """Get NFL games for a specific week (this might help with spreads/underdogs)"""
        print(f"\n🏈 EXPLORING NFL GAMES - WEEK {week}, SEASON {season}...")
        
        url = f"{self.base_url}/games/nfl/{season}/{week}"
        response = requests.get(url)
        
        if response.status_code == 200:
            games_data = response.json()
            self.pretty_print(games_data, f"NFL GAMES - WEEK {week}")
            self.save_to_file(games_data, f"nfl_games_week_{week}.json")
            
            # Summarize games
            print(f"NFL GAMES WEEK {week} SUMMARY:")
            for game_id, game in games_data.items():
                home = game.get('home', 'N/A')
                away = game.get('away', 'N/A')
                spread = game.get('spread', 'N/A')
                status = game.get('status', 'N/A')
                print(f"  {away} @ {home} (Spread: {spread}, Status: {status})")
            
            return games_data
        else:
            print(f"❌ Failed to get NFL games: {response.status_code}")
            return None
    
    def explore_nfl_state(self, season: int = 2025):
        """Get current NFL state/week information"""
        print(f"\n📅 EXPLORING NFL STATE FOR SEASON {season}...")
        
        url = f"{self.base_url}/games/nfl/{season}"
        response = requests.get(url)
        
        if response.status_code == 200:
            state_data = response.json()
            self.pretty_print(state_data, f"NFL STATE - SEASON {season}")
            self.save_to_file(state_data, f"nfl_state_{season}.json")
            
            print("NFL STATE SUMMARY:")
            print(f"  Current Week: {state_data.get('leg', 'N/A')}")
            print(f"  Season Type: {state_data.get('season_type', 'N/A')}")
            print(f"  Season: {state_data.get('season', 'N/A')}")
            
            return state_data
        else:
            print(f"❌ Failed to get NFL state: {response.status_code}")
            return None
    
    def full_exploration(self, weeks_to_check: List[int] = [1, 2, 3]):
        """Run a complete exploration of the league"""
        print("🔍 STARTING FULL SLEEPER API EXPLORATION")
        print(f"League ID: {self.league_id}")
        print(f"Timestamp: {datetime.now()}")
        
        # Basic league info
        league_info = self.explore_league_info()
        
        # Users
        users = self.explore_users()
        
        # Rosters
        rosters = self.explore_rosters()
        
        # NFL state
        nfl_state = self.explore_nfl_state()
        
        # Check multiple weeks
        for week in weeks_to_check:
            print(f"\n{'🔸'*20} WEEK {week} {'🔸'*20}")
            
            # Matchups
            self.explore_matchups(week)
            
            # NFL Games
            self.explore_nfl_games(week)
            
            # Try to find picks
            self.explore_picks_endpoint(week)
        
        # Other endpoints
        self.explore_bracket()
        self.explore_transactions()
        
        print("\n✅ EXPLORATION COMPLETE!")
        print("Check the generated .json files for detailed data structures.")
        print("\nNext steps:")
        print("1. Review the JSON files to understand the data structure")
        print("2. Look for pick/prediction data in the league interface")
        print("3. Check if picks are stored in a separate system/spreadsheet")
        print("4. Map roster_id to user_id using the rosters data")


# Usage
if __name__ == "__main__":
    # Get league ID from secure configuration
    from .secure_config import config
    league_id = config.sleeper_league_id
    
    explorer = SleeperAPIExplorer(league_id)
    
    # Run full exploration
    explorer.full_exploration(weeks_to_check=[1, 2, 3, 4])
    
    # Or run individual explorations
    # explorer.explore_league_info()
    # explorer.explore_users()
    # explorer.explore_matchups(1)
    # explorer.explore_nfl_games(1)