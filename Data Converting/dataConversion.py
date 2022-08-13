import chess

import chess.engine
import re
import asyncio

import os
cwd = os.getcwd()
path = cwd + "\\Data Converting\\Data\\stockfish_15_win_x64_avx2\\stockfish_15_win_x64_avx2\\stockfish_15_x64_avx2.exe"
engine = chess.engine.SimpleEngine.popen_uci(path)


chessBoard = chess.Board()



def getBoardString(board):
    boardString = str(board)
    boardString = boardString.replace(" ", "")
    boardString = boardString.replace("\n", "")
    return boardString


def getInputArray(board):
    boardString = getBoardString(board)
    array = [0] * 64
    valueDict = {"." : 0, "P": 1/12, "p" : 2/12, "N": 3/12, "n": 4/12, "B" : 5/12, "b" : 6/12, "R": 7/12, "r" : 8/12, "Q": 9/12, "q" : 10/12, "K": 11/12, "k" : 12/12}

    for i in range(64):
        key = boardString[i]
        array[i] = valueDict[key]
    
    return array



def gamesToMovesArray(gamePGN):
    # Turnss a pgn string into an array of moves
    moves = re.split("  *|[0-9]*[.]", game)
    moves = list(filter(None, moves))

    # remove the '\n' at the end
    moves.pop()
    return moves














# TODO: Make eval into label function, then add all at once.


# Takes an eval string, and outputs the neural network equivalent
def evalToLabel(evalString):
    if(evalString.charAt(0) == '#'): # we have a forced mate
        mateIn = int(evalString[1:])

        if(mateIn < 0):
            return abs(mateIn)  # black has a forced mate in abs(mateIn) moves
        else:
            return 229 - mateIn # white has a forced mate in 229 - mateIn moves

        



    num = int(evalString)

    # any evaluation higher than 10 gets limited by the range of the neural network. 
    if(abs(num) >= 10):
        if(num > 0):
            return 10
        else:
            return -10
    

    return 10 * num + 215



def finish(gamePGN):
    moves = gamesToMovesArray(gamePGN)
    board = chess.Board()



    for move in moves:
        board.push_san(move)
    
    print(board)

    info = engine.analyse(board, chess.engine.Limit(time=0.01, depth=20))


    eval = str(info['score'].white())
    print(eval)



    if(eval[0] != '#' and abs(int(eval)) < 500): ## no forced mate and eval < 500 centipawns
        return moves
    
    
    while not board.is_game_over():
        result = engine.play(board, chess.engine.Limit(time=0.1))
        producesan = board.san(result.move)
        board.push(result.move)
        moves.append(producesan)


    return moves




games = open("Data Converting\\Data\\InputGames.pgn", "r")

game = games.readline()

game = "e4 e5 Qh5 Nc6 Bc4 Nf6 \n"

print(game)

print(finish(game))    
engine.quit()