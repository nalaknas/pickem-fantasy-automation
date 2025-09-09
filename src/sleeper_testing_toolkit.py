import requests
import json
from datetime import datetime
import pandas as pd
from typing import Dict, List
import os

class SleeperTestingToolkit:
    def __init__(self, league_id: str):
        self.league_id = league_id
        self.base_url = "https://api.sleeper.app/v1"
    
    def test_league_connection(self):
        """Test basic connection and get league overview"""
        print("🔗 TESTING SLEEPER CONNECTION...")
        print(f"League ID: {self.league_id}")
        
        try:
            # Test league info
            league_url = f"{self.base_url}/league/{self.league_id}"
            league_response = requests.get(league_url)
            
            if league_response.status_code != 200:
                print(f"❌ Failed to connect to league: {league_response.status_code}")
                return False
            
            league_data = league_response.json()
            
            print("✅ Successfully connected to league!")
            print(f"   League Name: {league_data.get('name', 'N/A')}")
            print(f"   Season: {league_data.get('season', 'N/A')}")
            print(f"   Status: {league_data.get('status', 'N/A')}")
            
            # Get current week info
            current_leg = league_data.get('metadata', {}).get('current_pickem_leg_id', '')
            latest_report = league_data.get('metadata', {}).get('latest_report_leg_id', '')
            
            if current_leg:
                current_week = int(current_leg.split(':')[2])
                print(f"   Current Week: {current_week}")
            
            if latest_report:
                latest_week = int(latest_report.split(':')[2])
                print(f"   Latest Completed Week: {latest_week}")
            
            return True
            
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def analyze_roster_data(self):
        """Deep dive into roster data structure"""
        print("\n📊 ANALYZING ROSTER DATA STRUCTURE...")
        
        url = f"{self.base_url}/league/{self.league_id}/rosters"
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"❌ Failed to get rosters: {response.status_code}")
            return
        
        rosters = response.json()
        
        print(f"Found {len(rosters)} rosters")
        
        # Analyze first roster in detail
        if rosters:
            sample_roster = rosters[0]
            print(f"\n📋 SAMPLE ROSTER STRUCTURE:")
            print(f"   Owner ID: {sample_roster.get('owner_id', 'N/A')}")
            print(f"   Roster ID: {sample_roster.get('roster_id', 'N/A')}")
            
            metadata = sample_roster.get('metadata', {})
            points_by_leg = metadata.get('points_by_leg', {})
            previous_picks = metadata.get('previous_picks', {})
            
            print(f"\n📈 POINTS BY WEEK:")
            for leg, points in sorted(points_by_leg.items()):
                week_num = leg.split(':')[2]
                print(f"   Week {week_num}: {points} points")
            
            print(f"\n🎯 RECENT PICKS:")
            for leg, picks in sorted(previous_picks.items()):
                week_num = leg.split(':')[2]
                print(f"   Week {week_num}: {len(picks)} picks - {picks}")
        
        # Check data consistency across all rosters
        print(f"\n🔍 DATA CONSISTENCY CHECK:")
        
        all_weeks_with_scores = set()
        all_weeks_with_picks = set()
        
        for roster in rosters:
            metadata = roster.get('metadata', {})
            points_by_leg = metadata.get('points_by_leg', {})
            previous_picks = metadata.get('previous_picks', {})
            
            all_weeks_with_scores.update(points_by_leg.keys())
            all_weeks_with_picks.update(previous_picks.keys())
        
        print(f"   Weeks with scores: {sorted([int(w.split(':')[2]) for w in all_weeks_with_scores])}")
        print(f"   Weeks with picks: {sorted([int(w.split(':')[2]) for w in all_weeks_with_picks])}")
        
        return rosters
    
    def create_user_mapping(self):
        """Create a comprehensive user mapping file"""
        print("\n👥 CREATING USER MAPPING...")
        
        # Get users
        users_url = f"{self.base_url}/league/{self.league_id}/users"
        users_response = requests.get(users_url)
        
        # Get rosters
        rosters_url = f"{self.base_url}/league/{self.league_id}/rosters"
        rosters_response = requests.get(rosters_url)
        
        if users_response.status_code != 200 or rosters_response.status_code != 200:
            print("❌ Failed to get user or roster data")
            return
        
        users = users_response.json()
        rosters = rosters_response.json()
        
        # Create mapping
        mapping = []
        
        for roster in rosters:
            owner_id = roster.get('owner_id')
            roster_id = roster.get('roster_id')
            
            # Find corresponding user
            user_info = next((u for u in users if u['user_id'] == owner_id), {})
            
            mapping.append({
                'owner_id': owner_id,
                'roster_id': roster_id,
                'user_id': user_info.get('user_id', 'N/A'),
                'username': user_info.get('username', 'N/A'),
                'display_name': user_info.get('display_name', 'N/A'),
                'avatar': user_info.get('avatar', 'N/A')
            })
        
        # Save to both JSON and Excel for easy viewing
        with open('user_mapping.json', 'w') as f:
            json.dump(mapping, f, indent=2)
        
        df = pd.DataFrame(mapping)
        df.to_excel('user_mapping.xlsx', index=False)
        
        print("✅ User mapping created!")
        print("   Files: user_mapping.json, user_mapping.xlsx")
        
        print(f"\n👥 USER MAPPING SUMMARY:")
        for user in mapping:
            print(f"   {user['display_name']} (@{user['username']}) - Owner ID: {user['owner_id']}")
        
        return mapping
    
    def analyze_specific_week(self, week: int):
        """Analyze data for a specific week in detail"""
        print(f"\n🔍 DETAILED ANALYSIS - WEEK {week}")
        
        rosters_url = f"{self.base_url}/league/{self.league_id}/rosters"
        rosters_response = requests.get(rosters_url)
        
        if rosters_response.status_code != 200:
            print(f"❌ Failed to get rosters")
            return
        
        rosters = rosters_response.json()
        users = self.get_users_dict()
        
        week_key = f"v1:regular:{week}"
        
        # Collect week data
        week_data = []
        
        for roster in rosters:
            owner_id = roster.get('owner_id')
            metadata = roster.get('metadata', {})
            
            # Get score for this week
            points_by_leg = metadata.get('points_by_leg', {})
            week_score = points_by_leg.get(week_key, 0)
            
            # Get picks for this week
            previous_picks = metadata.get('previous_picks', {})
            week_picks = previous_picks.get(week_key, [])
            
            # Get user info
            user_info = users.get(owner_id, {})
            
            week_data.append({
                'owner_id': owner_id,
                'display_name': user_info.get('display_name', 'Unknown'),
                'username': user_info.get('username', 'Unknown'),
                'score': float(week_score),
                'picks': week_picks,
                'num_picks': len(week_picks)
            })
        
        # Sort by score
        week_data.sort(key=lambda x: x['score'], reverse=True)
        
        print(f"\n🏆 WEEK {week} LEADERBOARD:")
        for i, user in enumerate(week_data, 1):
            print(f"   {i}. {user['display_name']}: {user['score']} pts ({user['num_picks']} picks)")
        
        print(f"\n🎯 WEEK {week} PICKS BREAKDOWN:")
        all_picks = set()
        for user in week_data:
            all_picks.update(user['picks'])
        
        print(f"   Teams picked: {sorted(list(all_picks))}")
        print(f"   Total unique teams: {len(all_picks)}")
        
        # Pick popularity
        pick_counts = {}
        for user in week_data:
            for pick in user['picks']:
                pick_counts[pick] = pick_counts.get(pick, 0) + 1
        
        print(f"\n📊 PICK POPULARITY:")
        for team, count in sorted(pick_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {team}: {count} picks")
        
        # Save detailed analysis
        df = pd.DataFrame(week_data)
        df.to_excel(f'week_{week}_analysis.xlsx', index=False)
        print(f"\n💾 Detailed analysis saved to week_{week}_analysis.xlsx")
        
        return week_data
    
    def get_users_dict(self) -> Dict[str, dict]:
        """Get users as a dictionary keyed by user_id"""
        users_url = f"{self.base_url}/league/{self.league_id}/users"
        response = requests.get(users_url)
        
        if response.status_code == 200:
            users = response.json()
            return {user['user_id']: user for user in users}
        else:
            return {}
    
    def test_skins_calculation(self, week: int, mock_odds: Dict[str, dict]):
        """Test the skins calculation with mock data"""
        print(f"\n🧪 TESTING SKINS CALCULATION - WEEK {week}")
        
        from sleeper_skins_game import SleeperSkinsGame  # Import your main class
        
        skins_game = SleeperSkinsGame(self.league_id)
        
        # Test high score calculation
        high_score_winners, high_score = skins_game.calculate_high_score_winners(week)
        print(f"   High Score: {high_score} points")
        print(f"   Winners: {len(high_score_winners)} player(s)")
        
        # Test underdog calculation
        underdog_winners, underdog_correct, total_underdog_games = skins_game.calculate_underdog_winners(week, mock_odds)
        print(f"   Underdog Games: {total_underdog_games}")
        print(f"   Most Correct: {underdog_correct}")
        print(f"   Winners: {len(underdog_winners)} player(s)")
        
        # Test perfect week
        perfect_week_winners = skins_game.check_perfect_week(week, mock_odds)
        print(f"   Perfect Weeks: {len(perfect_week_winners)} player(s)")
        
        return {
            'high_score_winners': high_score_winners,
            'high_score': high_score,
            'underdog_winners': underdog_winners,
            'underdog_correct': underdog_correct,
            'perfect_week_winners': perfect_week_winners
        }
    
    def generate_weekly_odds_helper(self, week: int):
        """Generate a helper for creating weekly odds manually"""
        print(f"\n📋 GENERATING ODDS HELPER FOR WEEK {week}")
        
        # Try to get NFL games data (might have some info)
        nfl_url = f"{self.base_url}/games/nfl/2025/{week}"
        response = requests.get(nfl_url)
        
        if response.status_code == 200:
            games_data = response.json()
            print(f"   Found {len(games_data)} NFL games for week {week}")
            
            # Create odds template with game matchups
            odds_template = {}
            
            for game_id, game in games_data.items():
                home_team = game.get('home')
                away_team = game.get('away')
                
                if home_team and away_team:
                    odds_template[away_team] = {
                        "opponent": home_team,
                        "is_underdog": None,  # You'll fill this in
                        "won": None  # You'll fill this in after games
                    }
                    odds_template[home_team] = {
                        "opponent": away_team,
                        "is_underdog": None,  # You'll fill this in
                        "won": None  # You'll fill this in after games
                    }
            
            # Save template
            filename = f"week_{week}_odds_to_fill.json"
            with open(filename, 'w') as f:
                json.dump(odds_template, f, indent=2)
            
            print(f"✅ Created odds template: {filename}")
            print("   Fill in 'is_underdog' and 'won' fields manually")
            
        else:
            print(f"   No NFL games data available for week {week}")
            print("   You'll need to create the odds file manually")
    
    def quick_week_overview(self, week: int):
        """Get a quick overview of any week"""
        print(f"\n⚡ QUICK OVERVIEW - WEEK {week}")
        
        rosters_url = f"{self.base_url}/league/{self.league_id}/rosters"
        response = requests.get(rosters_url)
        
        if response.status_code != 200:
            print(f"❌ Failed to get rosters")
            return
        
        rosters = response.json()
        users = self.get_users_dict()
        
        week_key = f"v1:regular:{week}"
        
        # Check if week has data
        has_scores = any(roster.get('metadata', {}).get('points_by_leg', {}).get(week_key) 
                        for roster in rosters)
        has_picks = any(roster.get('metadata', {}).get('previous_picks', {}).get(week_key) 
                       for roster in rosters)
        
        print(f"   Week {week} Data Available:")
        print(f"   ✅ Scores: {'Yes' if has_scores else 'No'}")
        print(f"   ✅ Picks: {'Yes' if has_picks else 'No'}")
        
        if has_scores:
            # Quick score summary
            scores = []
            for roster in rosters:
                owner_id = roster.get('owner_id')
                score = roster.get('metadata', {}).get('points_by_leg', {}).get(week_key, 0)
                user_info = users.get(owner_id, {})
                
                scores.append({
                    'name': user_info.get('display_name', 'Unknown'),
                    'score': float(score)
                })
            
            scores.sort(key=lambda x: x['score'], reverse=True)
            
            print(f"\n   🏆 Top 3 Scores:")
            for i, user in enumerate(scores[:3], 1):
                print(f"      {i}. {user['name']}: {user['score']} pts")
            
            # Check for ties at the top
            top_score = scores[0]['score']
            tied_users = [user for user in scores if user['score'] == top_score]
            if len(tied_users) > 1:
                print(f"   ⚠️  TIE ALERT: {len(tied_users)} players tied at {top_score} pts")
        
        return has_scores, has_picks
    
    def get_users_dict(self) -> Dict[str, dict]:
        """Get users dictionary"""
        users_url = f"{self.base_url}/league/{self.league_id}/users"
        response = requests.get(users_url)
        
        if response.status_code == 200:
            users = response.json()
            return {user['user_id']: user for user in users}
        else:
            return {}
    
    def interactive_week_processor(self):
        """Interactive tool to help process a week step by step"""
        print("\n🎮 INTERACTIVE WEEK PROCESSOR")
        print("This will guide you through processing a week step by step")
        
        # Step 1: Choose week
        try:
            week_input = input("\nEnter week number to process (or 'current' for auto-detect): ")
            
            if week_input.lower() == 'current':
                league_info_url = f"{self.base_url}/league/{self.league_id}"
                response = requests.get(league_info_url)
                if response.status_code == 200:
                    league_data = response.json()
                    latest_leg = league_data.get('metadata', {}).get('latest_report_leg_id', '')
                    if latest_leg:
                        week = int(latest_leg.split(':')[2])
                        print(f"Auto-detected week: {week}")
                    else:
                        print("Could not auto-detect. Please enter manually.")
                        return
                else:
                    print("Could not connect to league. Please enter manually.")
                    return
            else:
                week = int(week_input)
            
        except ValueError:
            print("Invalid week number")
            return
        
        # Step 2: Check data availability
        print(f"\n📊 Checking data for week {week}...")
        has_scores, has_picks = self.quick_week_overview(week)
        
        if not has_scores or not has_picks:
            print("❌ Week data not complete. Cannot process.")
            return
        
        # Step 3: Generate odds template
        print(f"\n📋 Generating odds template for week {week}...")
        self.generate_weekly_odds_helper(week)
        
        # Step 4: Instructions
        print(f"\n📝 NEXT STEPS:")
        print(f"   1. Open week_{week}_odds_to_fill.json")
        print(f"   2. For each team, set:")
        print(f"      - 'is_underdog': true/false (based on point spread)")
        print(f"      - 'won': true/false (based on actual game results)")
        print(f"   3. Save the file as week_{week}_odds_final.json")
        print(f"   4. Run: process_completed_week({week})")
        
        return week
    
    def process_completed_week(self, week: int):
        """Process a week that has been completed with manual odds input"""
        print(f"\n⚙️  PROCESSING COMPLETED WEEK {week}")
        
        # Look for odds file
        odds_file = f"week_{week}_odds_final.json"
        
        if not os.path.exists(odds_file):
            print(f"❌ Odds file not found: {odds_file}")
            print(f"   Please create this file with game results and underdogs")
            return
        
        # Load odds
        with open(odds_file, 'r') as f:
            odds_data = json.load(f)
        
        print(f"✅ Loaded odds data for {len(odds_data)} teams")
        
        # Import and use main skins game class
        try:
            from sleeper_skins_game import SleeperSkinsGame
            skins_game = SleeperSkinsGame(self.league_id)
            skins_game.process_week(week, odds_data)
            
            print(f"🎉 Week {week} processed successfully!")
            
        except ImportError:
            print("❌ Could not import SleeperSkinsGame class")
            print("   Make sure sleeper_skins_game.py is in the same directory")
        except Exception as e:
            print(f"❌ Error processing week: {e}")
    
    def validate_odds_file(self, odds_file: str):
        """Validate an odds file format"""
        print(f"\n✅ VALIDATING ODDS FILE: {odds_file}")
        
        if not os.path.exists(odds_file):
            print(f"❌ File not found: {odds_file}")
            return False
        
        try:
            with open(odds_file, 'r') as f:
                odds_data = json.load(f)
            
            issues = []
            
            for team, data in odds_data.items():
                if not isinstance(data, dict):
                    issues.append(f"Team {team}: Data should be a dictionary")
                    continue
                
                if 'is_underdog' not in data or data['is_underdog'] is None:
                    issues.append(f"Team {team}: Missing 'is_underdog' value")
                
                if 'won' not in data or data['won'] is None:
                    issues.append(f"Team {team}: Missing 'won' value")
                
                if 'opponent' not in data:
                    issues.append(f"Team {team}: Missing 'opponent' value")
            
            if issues:
                print(f"❌ Found {len(issues)} issues:")
                for issue in issues[:5]:  # Show first 5 issues
                    print(f"   - {issue}")
                if len(issues) > 5:
                    print(f"   ... and {len(issues) - 5} more")
                return False
            else:
                print(f"✅ Odds file is valid!")
                print(f"   - {len(odds_data)} teams")
                
                underdogs = [team for team, data in odds_data.items() if data.get('is_underdog')]
                winners = [team for team, data in odds_data.items() if data.get('won')]
                underdog_winners = [team for team in underdogs if odds_data[team].get('won')]
                
                print(f"   - {len(underdogs)} underdogs")
                print(f"   - {len(winners)} winners")
                print(f"   - {len(underdog_winners)} underdog winners")
                
                return True
                
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON format in {odds_file}")
            return False
        except Exception as e:
            print(f"❌ Error validating file: {e}")
            return False


# Main testing and usage functions
def main():
    """Main function for testing and daily use"""
    print("🏈 SLEEPER SKINS GAME TOOLKIT 🏈")
    print("=" * 50)
    
    # Get league ID
    league_id = input("Enter your Sleeper League ID: ").strip()
    
    if not league_id:
        print("❌ No league ID provided")
        return
    
    # Initialize toolkit
    toolkit = SleeperTestingToolkit(league_id)
    
    # Test connection
    if not toolkit.test_league_connection():
        return
    
    while True:
        print("\n🎯 WHAT WOULD YOU LIKE TO DO?")
        print("1. Analyze roster data structure")
        print("2. Create user mapping file")
        print("3. Analyze specific week")
        print("4. Interactive week processor")
        print("5. Validate odds file")
        print("6. Process completed week")
        print("7. Quick week overview")
        print("8. Exit")
        
        choice = input("\nEnter choice (1-8): ").strip()
        
        if choice == '1':
            toolkit.analyze_roster_data()
        
        elif choice == '2':
            toolkit.create_user_mapping()
        
        elif choice == '3':
            try:
                week = int(input("Enter week number: "))
                toolkit.analyze_specific_week(week)
            except ValueError:
                print("Invalid week number")
        
        elif choice == '4':
            toolkit.interactive_week_processor()
        
        elif choice == '5':
            odds_file = input("Enter odds file name: ").strip()
            toolkit.validate_odds_file(odds_file)
        
        elif choice == '6':
            try:
                week = int(input("Enter week number to process: "))
                toolkit.process_completed_week(week)
            except ValueError:
                print("Invalid week number")
        
        elif choice == '7':
            try:
                week = int(input("Enter week number: "))
                toolkit.quick_week_overview(week)
            except ValueError:
                print("Invalid week number")
        
        elif choice == '8':
            print("👋 Goodbye!")
            break
        
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
