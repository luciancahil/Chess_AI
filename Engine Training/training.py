import numpy as np
import torch
from cProfile import label
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader, TensorDataset
import chess


class CustomTextDataset(Dataset):
    def __init__(self, input, labels):
        self.labels = labels
        self.input = input

    def __len__(self):
            return len(self.labels)

    def __getitem__(self, idx):
            label = self.labels[idx]
            input = self.input[idx]
            sample = (input, label)
            return sample


# Turns a board into a string with no spaces or newlines
def getBoardString(board):
    boardString = str(board)
    boardString = boardString.replace(" ", "")
    boardString = boardString.replace("\n", "")
    return boardString

# accepts a chessboardObject as an input, and outputs the input layer of our neural netwrok
def getInputArray(board):
    boardString = getBoardString(board)
    array = [0] * 64
    valueDict = {"." : 0, "P": 1/12, "p" : 2/12, "N": 3/12, "n": 4/12, "B" : 5/12, "b" : 6/12, "R": 7/12, "r" : 8/12, "Q": 9/12, "q" : 10/12, "K": 11/12, "k" : 12/12}

    for i in range(64):
        key = boardString[i]
        array[i] = valueDict[key]
    
    return array




games = open("Engine Training\\Data\\InputGames.pgn", "r")

gameLines = games.readlines()


numGames = len(gameLines)
numTrainGames = 0.8 * numGames
gamesProcessed = 0
trainInputs = []
trainOutputs = []
testInputs = []
testOutputs = []


for gameLine in gameLines:
    if(gamesProcessed >= 10):
        break

    plyLabelPairs = gameLine.split(":") # split the string into move-ply pairs

    plyLabelPairs.pop() # remove the newline character

    chessBoard = chess.Board() #create a new chessboard in the starting position.

    for pair in plyLabelPairs:
        #Split the ply and label
        splitArr = pair.split(";")
        ply = splitArr[0]
        label = splitArr[1]
        chessBoard.push_san(ply)
        if(gamesProcessed <= numTrainGames):
            trainInputs.append(getInputArray(chessBoard))
            trainOutputs.append(int(label))
        else:
            testInputs.append(getInputArray(chessBoard))
            testOutputs.append(int(label))
    
    gamesProcessed += 1

train_dataset = TensorDataset(torch.tensor(trainInputs), torch.tensor(trainOutputs))
test_dataset = TensorDataset(torch.tensor(testInputs), torch.tensor(testOutputs))