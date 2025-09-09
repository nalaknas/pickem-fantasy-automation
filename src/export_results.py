#!/usr/bin/env python3
"""
CSV/Excel Export Module for Sleeper Fantasy Pickem Skins Game
"""

import pandas as pd
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict

class SkinsGameExporter:
    def __init__(self, results_file: str = "data/skins_game_results.json"):
        """
        Initialize the exporter
        
        Args:
            results_file: Path to the results JSON file
        """
        self.results_file = results_file
        self.export_file_csv = "skins_game_season_report.csv"
        self.export_file_xlsx = "skins_game_season_report.xlsx"
    
    def load_results(self) -> List[dict]:
        """Load results from JSON file"""
        try:
            with open(self.results_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Results file not found: {self.results_file}")
            return []
    
    def create_weekly_breakdown(self, results: List[dict]) -> pd.DataFrame:
        """Create weekly breakdown DataFrame"""
        weekly_data = []
        processed_weeks = set()  # Track processed weeks to avoid duplicates
        
        for result in results:
            week_key = (result['week'], result['season'])
            if week_key in processed_weeks:
                continue  # Skip duplicates
            processed_weeks.add(week_key)
            
            week_data = {
                'Week': result['week'],
                'Season': result['season'],
                'Date_Processed': result.get('date_processed', ''),
                'Highest_Scorer': ', '.join(result['winner_names']['highest']),
                'Highest_Score': result['scores']['highest'],
                'Second_Highest': ', '.join(result['winner_names']['second_highest']) if result['rankings']['second_highest'] else '',
                'Second_Score': result['scores']['second_highest'] if result['rankings']['second_highest'] else '',
                'Third_Highest': ', '.join(result['winner_names']['third_highest']) if result['rankings']['third_highest'] else '',
                'Third_Score': result['scores']['third_highest'] if result['rankings']['third_highest'] else '',
                'Lowest_Scorer': ', '.join(result['winner_names']['lowest']),
                'Lowest_Score': result['scores']['lowest'],
                'No_Picks': ', '.join(result['winner_names']['no_picks']) if result['rankings'].get('no_picks') else '',
                'Perfect_Week': ', '.join(result['winner_names']['perfect_week']) if result['perfect_week_winners'] else '',
                'Perfect_Week_Count': len(result['perfect_week_winners'])
            }
            weekly_data.append(week_data)
        
        return pd.DataFrame(weekly_data)
    
    def create_season_scores(self, results: List[dict]) -> pd.DataFrame:
        """Create season scores DataFrame with all user scores"""
        # Collect all unique users across all weeks
        all_users = set()
        for result in results:
            all_users.update(result['rankings']['highest'])
            all_users.update(result['rankings']['second_highest'])
            all_users.update(result['rankings']['third_highest'])
            all_users.update(result['rankings']['lowest'])
            all_users.update(result['rankings'].get('no_picks', []))
        
        # Create DataFrame with users as rows and weeks as columns
        weeks = sorted([r['week'] for r in results])
        season_data = []
        
        for user_id in sorted(all_users):
            user_row = {'User_ID': user_id}
            
            # Get user display name from any result
            display_name = 'Unknown'
            for result in results:
                if user_id in result['rankings']['highest']:
                    display_name = result['winner_names']['highest'][result['rankings']['highest'].index(user_id)]
                    break
                elif user_id in result['rankings']['second_highest']:
                    display_name = result['winner_names']['second_highest'][result['rankings']['second_highest'].index(user_id)]
                    break
                elif user_id in result['rankings']['third_highest']:
                    display_name = result['winner_names']['third_highest'][result['rankings']['third_highest'].index(user_id)]
                    break
                elif user_id in result['rankings']['lowest']:
                    display_name = result['winner_names']['lowest'][result['rankings']['lowest'].index(user_id)]
                    break
                elif user_id in result['rankings'].get('no_picks', []):
                    display_name = result['winner_names']['no_picks'][result['rankings']['no_picks'].index(user_id)]
                    break
            
            user_row['Display_Name'] = display_name
            
            # Add scores for each week
            for week in weeks:
                week_result = next((r for r in results if r['week'] == week), None)
                if week_result:
                    if user_id in week_result['rankings']['highest']:
                        user_row[f'Week_{week}_Score'] = week_result['scores']['highest']
                        user_row[f'Week_{week}_Rank'] = '1st'
                    elif user_id in week_result['rankings']['second_highest']:
                        user_row[f'Week_{week}_Score'] = week_result['scores']['second_highest']
                        user_row[f'Week_{week}_Rank'] = '2nd'
                    elif user_id in week_result['rankings']['third_highest']:
                        user_row[f'Week_{week}_Score'] = week_result['scores']['third_highest']
                        user_row[f'Week_{week}_Rank'] = '3rd'
                    elif user_id in week_result['rankings']['lowest']:
                        user_row[f'Week_{week}_Score'] = week_result['scores']['lowest']
                        user_row[f'Week_{week}_Rank'] = 'Last'
                    elif user_id in week_result['rankings'].get('no_picks', []):
                        user_row[f'Week_{week}_Score'] = 0
                        user_row[f'Week_{week}_Rank'] = 'No Picks'
                    else:
                        user_row[f'Week_{week}_Score'] = ''
                        user_row[f'Week_{week}_Rank'] = ''
                else:
                    user_row[f'Week_{week}_Score'] = ''
                    user_row[f'Week_{week}_Rank'] = ''
            
            # Calculate season totals
            total_score = 0
            wins = 0
            perfect_weeks = 0
            
            for week in weeks:
                week_result = next((r for r in results if r['week'] == week), None)
                if week_result and f'Week_{week}_Score' in user_row and user_row[f'Week_{week}_Score'] != '':
                    total_score += user_row[f'Week_{week}_Score']
                    if user_row[f'Week_{week}_Rank'] == '1st':
                        wins += 1
                    if user_id in week_result['perfect_week_winners']:
                        perfect_weeks += 1
            
            user_row['Total_Score'] = total_score
            user_row['Total_Wins'] = wins
            user_row['Perfect_Weeks'] = perfect_weeks
            
            season_data.append(user_row)
        
        return pd.DataFrame(season_data)
    
    def create_user_picks_data(self, results: List[dict]) -> pd.DataFrame:
        """Create user picks DataFrame (if picks data is available)"""
        picks_data = []
        
        for result in results:
            week = result['week']
            season = result['season']
            
            # This would need to be implemented based on how picks are stored
            # For now, we'll create a placeholder structure
            for user_id in result['rankings']['highest'] + result['rankings']['second_highest'] + result['rankings']['third_highest'] + result['rankings']['lowest']:
                picks_row = {
                    'Week': week,
                    'Season': season,
                    'User_ID': user_id,
                    'Picks': 'N/A',  # Placeholder - would need actual picks data
                    'Score': result['scores']['highest'] if user_id in result['rankings']['highest'] else 
                            result['scores']['second_highest'] if user_id in result['rankings']['second_highest'] else
                            result['scores']['third_highest'] if user_id in result['rankings']['third_highest'] else
                            result['scores']['lowest'] if user_id in result['rankings']['lowest'] else 0
                }
                picks_data.append(picks_row)
        
        return pd.DataFrame(picks_data)
    
    def export_to_csv(self, results: List[dict]) -> bool:
        """Export results to CSV file"""
        try:
            # Create weekly breakdown
            weekly_df = self.create_weekly_breakdown(results)
            
            # Create season scores
            season_df = self.create_season_scores(results)
            
            # Combine dataframes
            with open(self.export_file_csv, 'w', newline='', encoding='utf-8') as f:
                # Write weekly breakdown
                f.write("=== WEEKLY BREAKDOWN ===\n")
                weekly_df.to_csv(f, index=False)
                f.write("\n\n=== SEASON SCORES ===\n")
                season_df.to_csv(f, index=False)
            
            print(f"✅ CSV export completed: {self.export_file_csv}")
            return True
            
        except Exception as e:
            print(f"❌ CSV export failed: {e}")
            return False
    
    def export_to_excel(self, results: List[dict]) -> bool:
        """Export results to Excel file with multiple sheets"""
        try:
            # Create dataframes
            weekly_df = self.create_weekly_breakdown(results)
            season_df = self.create_season_scores(results)
            picks_df = self.create_user_picks_data(results)
            
            # Create Excel file with multiple sheets
            with pd.ExcelWriter(self.export_file_xlsx, engine='openpyxl') as writer:
                weekly_df.to_excel(writer, sheet_name='Weekly_Breakdown', index=False)
                season_df.to_excel(writer, sheet_name='Season_Scores', index=False)
                picks_df.to_excel(writer, sheet_name='User_Picks', index=False)
                
                # Add summary sheet
                summary_data = {
                    'Metric': ['Total Weeks', 'Total Users', 'Total Perfect Weeks', 'Export Date'],
                    'Value': [
                        len(results),
                        len(set().union(*[r['rankings']['highest'] + r['rankings']['second_highest'] + r['rankings']['third_highest'] + r['rankings']['lowest'] for r in results])),
                        sum(len(r['perfect_week_winners']) for r in results),
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    ]
                }
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            print(f"✅ Excel export completed: {self.export_file_xlsx}")
            return True
            
        except Exception as e:
            print(f"❌ Excel export failed: {e}")
            return False
    
    def export_all(self) -> bool:
        """Export both CSV and Excel formats"""
        results = self.load_results()
        
        if not results:
            print("❌ No results to export")
            return False
        
        print(f"📊 Exporting {len(results)} weeks of data...")
        
        csv_success = self.export_to_csv(results)
        excel_success = self.export_to_excel(results)
        
        return csv_success and excel_success

def main():
    """Main function for testing the exporter"""
    exporter = SkinsGameExporter()
    exporter.export_all()

if __name__ == "__main__":
    main()
