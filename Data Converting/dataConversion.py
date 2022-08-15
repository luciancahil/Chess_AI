import chess

import chess.engine
import re
import asyncio

import os
cwd = os.getcwd()
path = cwd + "\\Data Converting\\Data\\stockfish_15_win_x64_avx2\\stockfish_15_win_x64_avx2\\stockfish_15_x64_avx2.exe"
engine = chess.engine.SimpleEngine.popen_uci(path)


chessBoard = chess.Board()







def gamesToMovesArray(gamePGN):
    # Turnss a pgn string into an array of moves
    moves = re.split("  *|[0-9]*[.]", game)
    moves = list(filter(None, moves))

    # remove the '\n' at the end
    moves.pop()
    return moves














# TODO: Make eval into label function, then add all at once.


# Takes an eval string, and outputs the neural network equivalent
# Will not work for positions where either side has been checkmated
def evalToLabel(evalString):
    if(evalString[0] == '#'): # we have a forced mate
        mateIn = int(evalString[1:])

        if(mateIn < 0):
            return abs(mateIn)  # black has a forced mate in abs(mateIn) moves
        else:
            return 229 - mateIn # white has a forced mate in 229 - mateIn moves

        



    num = int(evalString) / 100

    # any evaluation higher than 10 gets limited by the range of the neural network. 
    if(abs(num) >= 10):
        if(num > 0):
            return 214
        else:
            return 15
    

    return int(10 * num + 115)



def finish(gamePGN):
    moves = gamesToMovesArray(gamePGN)
    board = chess.Board()
    movesandEval = ""



    for move in moves:
        board.push_san(move)
        info = engine.analyse(board, chess.engine.Limit(time=0.01, depth=20))
        eval = str(info['score'].white())
        nextPart = move + ";" + str(evalToLabel(eval)) + ":"
        movesandEval += nextPart
    

    info = engine.analyse(board, chess.engine.Limit(time=0.01, depth=20))

    if(eval[0] != '#' and abs(int(eval)) < 500): ## no forced mate and eval < 500 centipawns
        return movesandEval
    

    
    while not board.is_game_over():
        result = engine.play(board, chess.engine.Limit(time=0.1))
        info = engine.analyse(board, chess.engine.Limit(time=0.01, depth=20))
        producesan = board.san(result.move)
        board.push(result.move)

        
        nextEval = str(evalToLabel(eval))

        # check for  adelivered mate
        if(board.outcome() != None):
            if(board.outcome().winner): #white won
                nextEval = "229"
            else: # black won
                nextEval = "0"

        nextPart = producesan + ";" + nextEval + ":"
        movesandEval += nextPart


    return movesandEval


#Outcome(termination=<Termination.CHECKMATE: 1>, winner=True)

games = open("Data Converting\\Data\\InputGames.pgn", "r")

gameLines = games.readlines()



f = open("Data Converting\\Data\\OutputGames.pgn", "w")
num = 0

for game in gameLines:
    line = finish(game) + "\n"
    f.write(line)
    num += 1
    if(num % 10 == 0):
        printing = "At "  + str(num)
        print(printing)
    
    if(num == 100):
        break

f.close()
games.close()
engine.quit()