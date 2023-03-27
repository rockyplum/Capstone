import keras
import numpy as np
import chess

start_model = keras.models.load_model('start_net')
end_model = keras.models.load_model('end_net')

print('models loaded')
print(start_model.summary())

def get_net_input(fen):
    
    input = []
    last = False
    
    for c in fen:
        
        # B or W to move
        if last:
            
            if c == 'w':
                input.append(0)
            else:
                input.append(1)
            break
        
        # ignore
        if (c == '/'):
            continue
        
        # just before to move information
        elif (c == ' '):
            last = True
            continue
        
        # data about square
        else:
            
            vec = np.zeros(13) # empty square, K, Q, B, N, R, P, k, q, b, n, r, p
            
            # empty square
            try:
                
                x = int(c)
                
                vec[0] = 1
                for i in range(x):
                    for n in vec:
                        input.append(int(n))
                    
            # piece
            except:
                
                if (c == 'K'):
                    vec[1] = 1
                elif (c == 'Q'):
                    vec[2] = 1
                elif (c == 'B'):
                    vec[3] = 1
                elif (c == 'N'):
                    vec[4] = 1
                elif (c == 'R'):
                    vec[5] = 1
                elif (c == 'P'):
                    vec[6] = 1
                elif (c == 'k'):
                    vec[7] = 1
                elif (c == 'q'):
                    vec[8] = 1
                elif (c == 'b'):
                    vec[9] = 1
                elif (c == 'n'):
                    vec[10] = 1
                elif (c == 'r'):
                    vec[11] = 1
                elif (c == 'p'):
                    vec[12] = 1
                
                for n in vec:
                    input.append(int(n))
    
    return input

def get_move(board):
    
    wrong_start = False
    
    # get starting square
    
    fen = board.fen()
    x_start = get_net_input(fen)
    
    y_start = start_model.predict([x_start])
    start_square_list = y_start[0]
    
    for i in range(64):
        x_start.append(0)
    
    while True:
    
        start_square_index = np.argmax(start_square_list)
        start_square = chess.SQUARE_NAMES[start_square_index]
        
        # modify x
        
        x_start[833 + start_square_index] = 1
        
        # get end square
        
        y_end = end_model.predict([x_start])
        end_square_list = y_end[0]
        
        while True:
        
            if wrong_start:
                break
        
            end_square_index = np.argmax(end_square_list)
            end_square = chess.SQUARE_NAMES[end_square_index]
            
            move = start_square + end_square
            
            try:
                board.push_uci(move)
                return move
            except:
                
                try:
                    board.push_uci(move + "Q")
                    return move + "Q"
                except:
                    pass
                
                if end_square_list[end_square_index] <= 0:
                    wrong_start = True
                else: 
                    end_square_list[end_square_index] = 0
                
                continue
        
        start_square_list[start_square_index] = 0
        x_start[833 + start_square_index] = 0
        wrong_start = False
    
board = chess.Board()

print("Enter 0 if you would like to play as White, and 1 if you would like to play as Black: ")
colour = int(input())

if (colour == 0):
    
    while (not board.is_checkmate()):
        
        try:
            player_move = input()
            board.push_san(player_move)
        except:
            print("invalid move, try again")
            continue
        
        engine_move = get_move(board)
        print(engine_move)
        
    print("The winner is: " + board.outcome().winner)
        
else:
    
    while (not board.is_checkmate()):
        
        engine_move = get_move(board)
        print(engine_move)
        
        try:
            player_move = input()
            board.push_san(player_move)
        except:
            print("invalid move, try again")
            continue
        
    print("The winner is: " + board.outcome().winner)
    
print("Thank you for playing")