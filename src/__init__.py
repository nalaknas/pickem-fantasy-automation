"""
Sleeper Fantasy Pickem Skins Game Automation

A Python package for automating fantasy football skins game calculations
using the Sleeper API.
"""

from .skins_game_mvp import SleeperSkinsGameMVP
from .weekly_runner import main as run_weekly
from .view_results import view_results, view_season_summary
from .export_results import SkinsGameExporter

__version__ = "1.0.0"
__author__ = "Sleeper Fantasy Automation"

__all__ = [
    "SleeperSkinsGameMVP",
    "run_weekly", 
    "view_results",
    "view_season_summary",
    "SkinsGameExporter"
]
