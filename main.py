from src.game import MinichessGame

def main():
    print("Welcome to Minichess!")
    print("1. Human vs Human")
    print("2. Human vs AI")
    print("3. AI vs AI")
    
    while True:
        try:
            choice = int(input("Select game mode (1-3): "))
            if choice in [1, 2, 3]:
                break
            print("Please enter 1, 2, or 3.")
        except ValueError:
            print("Please enter a valid number.")

    game_modes = {
        1: ('human', 'human'),
        2: ('human', 'ai'),
        3: ('ai', 'ai')
    }
    
    player1_type, player2_type = game_modes[choice]
    game = MinichessGame(player1_type, player2_type)
    game.play_game()

if __name__ == "__main__":
    main()
