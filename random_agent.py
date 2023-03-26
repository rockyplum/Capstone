import random
import chess

board = chess.Board()

print("Enter 0 if you would like to play as White, and 1 if you would like to play as Black: ")
colour = int(input())

if (colour == 0):
    while (not board.is_checkmate()):
        player_move = input()
        board.push_san(player_move)
        
        legal = [m for m in board.legal_moves]
        
        engine_move = random.choice(legal)
        board.san_and_push(engine_move)
        print(engine_move)
    print("The winner is: " + board.outcome().winner)
        
else:
    while (not board.is_checkmate()):
        engine_move = random.choice(board.legal_moves)
        board.push_san(engine_move)
        print(engine_move)
        
        player_move = input()
        board.push_san(player_move)
    print("The winner is: " + board.outcome().winner)
    
print("Thank you for playing")