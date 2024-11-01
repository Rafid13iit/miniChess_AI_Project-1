from .board import Board
from .ai import MinichessAI

class MinichessGame:
    def __init__(self, player1_type='human', player2_type='ai'):
        self.board = Board()
        self.current_player = 'white'
        
        self.players = {
            'white': self.create_player(player1_type, 'white'),
            'black': self.create_player(player2_type, 'black')
        }

    def create_player(self, player_type, color):
        if player_type.lower() == 'human':
            return None
        return MinichessAI(color)

    def parse_position(self, pos_str):
        if len(pos_str) != 2:
            return None
        col = ord(pos_str[0].lower()) - ord('a')
        row = int(pos_str[1]) - 1
        if 0 <= col < 5 and 0 <= row < 6:  # Updated ranges
            return (col, row)
        return None

    def play_turn(self):
        self.board.display()
        
        if self.board.is_checkmate(self.current_player):
            winner = 'Black' if self.current_player == 'white' else 'White'
            print(f"Checkmate! {winner} wins!")
            return False
            
        print(f"\n{self.current_player.capitalize()}'s turn")
        
        if self.players[self.current_player]:  # AI player
            start_pos, end_pos = self.players[self.current_player].get_best_move(self.board)
            self.board.move_piece(start_pos, end_pos)
            print(f"AI moves from {chr(start_pos[0] + ord('a'))}{start_pos[1]+1} "
                  f"to {chr(end_pos[0] + ord('a'))}{end_pos[1]+1}")
        else:  # Human player
            while True:
                try:
                    start = input("Enter start position (e.g., e2): ")
                    end = input("Enter end position (e.g., e4): ")
                    
                    start_pos = self.parse_position(start)
                    end_pos = self.parse_position(end)
                    
                    if start_pos and end_pos:
                        if self.board.move_piece(start_pos, end_pos):
                            break
                    print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid input format. Use letters a-f for columns and numbers 1-5 for rows.")
                    
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        return True

    def play_game(self):
        print("Welcome to Minichess!")
        print("White pieces are uppercase (PRNBQK)")
        print("Black pieces are lowercase (prnbqk)")
        print("Enter moves in algebraic notation (e.g., 'e2' to 'e4')")
        
        while True:
            if not self.play_turn():
                break
            
        print("\nGame Over!")
        self.board.display()
