#!/usr/bin/env python3
"""
Example showing the difference between old and new underdog systems
"""

def demonstrate_percentage_system():
    print("🏈 UNDERDOG SYSTEM COMPARISON 🏈")
    print("=" * 50)
    
    print("📊 Example Scenario:")
    print("Total underdog games: 8")
    print("Underdog wins: 2 (LAC, CAR)")
    print()
    
    # Example user picks
    users = {
        "Player A": {
            "underdog_picks": ["DAL", "LAC", "CAR", "MIA"],  # 4 picks
            "correct_picks": ["LAC", "CAR"],  # 2 correct
            "percentage": 50.0
        },
        "Player B": {
            "underdog_picks": ["DAL", "LAC", "CAR", "MIA", "CLE", "ATL", "TB", "NYJ"],  # 8 picks
            "correct_picks": ["LAC", "CAR"],  # 2 correct
            "percentage": 25.0
        },
        "Player C": {
            "underdog_picks": ["LAC"],  # 1 pick
            "correct_picks": ["LAC"],  # 1 correct
            "percentage": 100.0
        }
    }
    
    print("👥 User Results:")
    print("=" * 30)
    
    for player, data in users.items():
        print(f"{player}:")
        print(f"  Underdog picks: {len(data['underdog_picks'])}")
        print(f"  Correct picks: {len(data['correct_picks'])}")
        print(f"  Percentage: {data['percentage']:.1f}%")
        print(f"  Picks: {data['underdog_picks']}")
        print(f"  Correct: {data['correct_picks']}")
        print()
    
    print("🏆 WINNER DETERMINATION:")
    print("=" * 30)
    
    print("OLD SYSTEM (Raw Count):")
    print("  Player A: 2 correct")
    print("  Player B: 2 correct")
    print("  Player C: 1 correct")
    print("  → TIE between Player A and Player B")
    print()
    
    print("NEW SYSTEM (Percentage):")
    print("  Player A: 50.0%")
    print("  Player B: 25.0%")
    print("  Player C: 100.0%")
    print("  → WINNER: Player C")
    print()
    
    print("✅ BENEFITS OF PERCENTAGE SYSTEM:")
    print("  • Prevents gaming the system by picking all underdogs")
    print("  • Rewards quality over quantity")
    print("  • More strategic decision making")
    print("  • Fairer competition")

if __name__ == "__main__":
    demonstrate_percentage_system()
