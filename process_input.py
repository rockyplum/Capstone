# creates one list of positions, and one list of the moves played in those positions

import chess
import numpy as np
import json

d = open("games.txt", "r")

boards = []
#moves = []
start_squares = []
end_squares = []

def to_vec_array(fen):
    
    vecs = []
    last = False
    
    for c in fen:
        
        # B or W to move
        if last:
            
            if c == 'w':
                vecs.append(0)
            else:
                vecs.append(1)
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
                    vecs.append(vec.astype(int).tolist())
                    
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
                
                vecs.append(vec.astype(int).tolist())
    
    #print(chars)
    
    return vecs

# skip past headers
for i in range(5):
    d.readline()

# iterate through games
for i in range(1000):
    
    if i % 10 == 0:
        print(i)
    
    game = d.readline() # game
    board = chess.Board() # new board
    
    try:
        
        game = game[game.index("W1"):] # get just the moves, skip other information
    
        for m in game.split(" ")[:-1]:
            
            vec_array = to_vec_array(board.fen())
            
            move = m[m.index('.')+1:] # move in algebraic notation
            
            uci = board.parse_san(move).uci()
            
            start = uci[0:2]
            end = uci[2:4]
    
            start = chess.SQUARE_NAMES.index(start)
            end = chess.SQUARE_NAMES.index(end)
            
            start_vec = np.zeros(64)
            start_vec[start] = 1
            
            end_vec = np.zeros(64)
            end_vec[end] = 1
            
            board.push_san(move)
            
            start_squares.append(start_vec.astype(int).tolist())
            end_squares.append(end_vec.astype(int).tolist())
            boards.append(vec_array)
            
    except Exception as e:
        print(e)
        print(game)

j = {'board' : boards, 'start' : start_squares, 'end' : end_squares}
f = open("boards.json", "w")
json.dump(j, f)

print("Done")