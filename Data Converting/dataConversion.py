import chess

chessBoard = chess.Board()

def getBoardString(board):
    boardString = str(board)
    boardString = boardString.replace(" ", "")
    boardString = boardString.replace("\n", "")
    return boardString


    

print(getBoardString(chessBoard))
