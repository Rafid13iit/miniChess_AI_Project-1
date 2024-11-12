from .board import Board
from .ai import MinichessAI
import time

class MinichessGame:
    def __init__(self, player1_type='human', player2_type='ai', player1_depth=3, player2_depth=3):
        """
        Initialize a Minichess game object.

        Parameters:
            player1_type (str): The type of player 1 ('human' or 'ai'). Defaults to 'human'.
            player2_type (str): The type of player 2 ('human' or 'ai'). Defaults to 'ai'.
            player1_depth (int): The depth of search for player 1 if they are an AI. Defaults to 3.
            player2_depth (int): The depth of search for player 2 if they are an AI. Defaults to 3.
        """
        # Initialize the game board
        self.board = Board()
        
        # Determine whose turn it is. There are only two players in Minichess, so we
        # just switch between 'white' and 'black'.
        self.current_player = 'white'
        
        # Is the game running? If this is False, the game is over.
        self.game_running = True
        
        # Initialize the players dictionary. The keys are the player colors, and
        # the values are the player objects. If a player is human, the value is
        # None.
        self.players = {
            'white': self.create_player(player1_type, 'white', player1_depth),
            'black': self.create_player(player2_type, 'black', player2_depth)
        }

    def create_player(self, player_type, color, depth):
        # Check if the player type is 'human' (case insensitive)
        if player_type.lower() == 'human':
            # Return None for human players as they don't need an AI object
            return None
        # For AI players, create and return a MinichessAI object with the specified color and search depth
        return MinichessAI(color, depth)

    def parse_position(self, pos_str):
        """
        Convert algebraic notation to board coordinates.

        Algebraic notation is a way of representing positions on a chessboard using
        letters and numbers. The column is represented by a letter (a-h), and the
        row is represented by a number (1-8). This function takes a string in
        algebraic notation and returns the corresponding coordinates on the board.

        For example, the string 'e4' would be converted to the coordinates (4, 3),
        which correspond to the square in the 5th column and 4th row of the board.

        If the input string is not in algebraic notation, or if the coordinates
        are not valid, this function returns None.

        :param pos_str: A string in algebraic notation representing a position on the board.
        :return: The coordinates of the position on the board, or None if the input is invalid.
        """
        # Check that the input string is two characters long
        if len(pos_str) != 2:
            return None

        # Convert the column letter to a number
        col = ord(pos_str[0].lower()) - ord('a')

        # Convert the row number to an integer
        row = int(pos_str[1]) - 1

        # Check if the position is valid
        if self.board.is_position_valid((col, row)):
            # Return the coordinates
            return (col, row)

        # If the position is not valid, return None
        return None

    def play_turn(self):
        # Display the current state of the board
        self.board.display()

        # Check if the current player is in checkmate
        if self.board.is_checkmate(self.current_player):
            # Determine the winner based on the current player
            winner = 'Black' if self.current_player == 'white' else 'White'
            # Announce the winner
            print(f"Checkmate! {winner} wins!")
            # End the game as it's over
            self.game_running = False
            return False

        # Check if the game is in a stalemate for the current player
        elif self.board.is_stalemate(self.current_player):
            # Announce the draw due to stalemate
            print(f"Stalemate! It's a draw.")
            # End the game as no moves are possible
            self.game_running = False
            return False

        # Announce whose turn it is
        print(f"\n{self.current_player.capitalize()}'s turn")

        # Check if the current player is an AI
        if self.players[self.current_player]:  # AI player
            # Add a delay to make AI moves visible to players
            time.sleep(1)
            # Get the best move from the AI
            start_pos, end_pos = self.players[self.current_player].get_best_move(self.board)
            # Attempt to move the piece on the board
            if self.board.move_piece(start_pos, end_pos):
                # Announce the move made by the AI
                print(f"AI moves from {chr(start_pos[0] + ord('a'))}{start_pos[1]+1} "
                      f"to {chr(end_pos[0] + ord('a'))}{end_pos[1]+1}")
            else:
                # Announce a failure in executing the AI move
                print("AI move failed.")
                # End the game as it encountered an error
                self.game_running = False
                return False

        else:  # Human player
            # Loop until a valid move is made
            while True:
                try:
                    # Prompt the human player for the start position
                    start = input("Enter start position (e.g., e2): ")
                    # Prompt the human player for the end position
                    end = input("Enter end position (e.g., e4): ")

                    # Parse the start and end positions from input
                    start_pos = self.parse_position(start)
                    end_pos = self.parse_position(end)

                    # Check if both start and end positions are valid
                    if start_pos and end_pos:
                        # Attempt to move the piece on the board
                        if self.board.move_piece(start_pos, end_pos):
                            # Break the loop if the move is successful
                            break
                    # Announce invalid move attempt
                    print("Invalid move. Try again.")
                except ValueError:
                    # Announce invalid input format
                    print("Invalid input format. Use letters a-e for columns and numbers 1-6 for rows.")

        # Switch the turn to the other player
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        return True

    def play_game(self):
        # Display welcome message and instructions for the game
        print("Welcome to Minichess!")
        print("White pieces are uppercase (PRNBQK)")
        print("Black pieces are lowercase (prnbqk)")
        print("Enter moves in algebraic notation (e.g., 'e2' to 'e4')")

        # Run the game loop as long as the game is running
        while self.game_running:
            # Play a turn and check if the game should continue
            if not self.play_turn():
                # Break the loop if the game is over
                break
            
        # Display game over message once the loop exits
        print("\nGame Over!")
        # Show the final state of the board
        self.board.display()
