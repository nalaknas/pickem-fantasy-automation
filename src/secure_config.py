"""
Secure configuration management for Sleeper Fantasy League automation.
Handles environment variables and sensitive data securely.
"""

import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

class SecureConfig:
    """Secure configuration manager for the Sleeper Fantasy League automation."""
    
    def __init__(self, env_file: str = ".env"):
        """
        Initialize secure configuration.
        
        Args:
            env_file: Path to environment file (default: .env)
        """
        self.env_file = env_file
        self._load_environment()
        self._validate_required_vars()
    
    def _load_environment(self):
        """Load environment variables from file."""
        if os.path.exists(self.env_file):
            load_dotenv(self.env_file)
        else:
            print(f"⚠️  Environment file {self.env_file} not found.")
            print(f"📝 Please copy env.template to {self.env_file} and configure your settings.")
            print("🔒 This ensures your sensitive data stays secure!")
    
    def _validate_required_vars(self):
        """Validate that required environment variables are set."""
        required_vars = ['SLEEPER_LEAGUE_ID']
        missing_vars = []
        
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
            print(f"📝 Please set these in your {self.env_file} file")
            raise ValueError(f"Missing required environment variables: {missing_vars}")
    
    @property
    def sleeper_league_id(self) -> str:
        """Get the Sleeper League ID."""
        league_id = os.getenv('SLEEPER_LEAGUE_ID')
        if not league_id:
            raise ValueError("SLEEPER_LEAGUE_ID not set in environment variables")
        return league_id
    
    @property
    def twilio_config(self) -> Optional[Dict[str, str]]:
        """Get Twilio configuration if available."""
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        from_number = os.getenv('TWILIO_FROM_NUMBER')
        to_numbers = os.getenv('TWILIO_TO_NUMBERS')
        
        if all([account_sid, auth_token, from_number, to_numbers]):
            return {
                'account_sid': account_sid,
                'auth_token': auth_token,
                'from_number': from_number,
                'to_numbers': [num.strip() for num in to_numbers.split(',')]
            }
        return None
    
    @property
    def data_directory(self) -> str:
        """Get data directory path."""
        return os.getenv('DATA_DIRECTORY', 'data')
    
    @property
    def results_file(self) -> str:
        """Get results file name."""
        return os.getenv('RESULTS_FILE', 'skins_game_results.json')
    
    @property
    def current_season(self) -> int:
        """Get current season year."""
        return int(os.getenv('CURRENT_SEASON', '2025'))
    
    @property
    def league_name(self) -> str:
        """Get league name."""
        return os.getenv('LEAGUE_NAME', 'Fantasy League')
    
    def get_all_config(self) -> Dict[str, Any]:
        """Get all configuration as a dictionary."""
        return {
            'sleeper_league_id': self.sleeper_league_id,
            'twilio_config': self.twilio_config,
            'data_directory': self.data_directory,
            'results_file': self.results_file,
            'current_season': self.current_season,
            'league_name': self.league_name
        }
    
    def is_secure(self) -> bool:
        """Check if configuration is properly secured."""
        try:
            self._validate_required_vars()
            return True
        except ValueError:
            return False

# Global config instance
config = SecureConfig()
