import chess

import chess.engine
import re

import os
cwd = os.getcwd()


path = cwd + "\\Data Converting\\Data\\stockfish_15_win_x64_avx2\\stockfish_15_win_x64_avx2\\stockfish_15_x64_avx2.exe"



engine = chess.engine.SimpleEngine.popen_uci(path)

engine.quit()
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
    # Turn all games into an array of moves.
    moves = re.split("  *|[0-9]*[.]", game)
    moves = list(filter(None, moves))


games = open("Data Converting\\Data\\InputGames.pgn", "r")

game = games.readline()





print(moves)



