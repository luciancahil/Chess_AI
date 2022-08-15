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

print("done Reading")

numGames = 100
numTrainGames = 0.8 * numGames
gamesProcessed = 0
trainInputs = []
trainOutputs = []
testInputs = []
testOutputs = []


for gameLine in gameLines:
    if(gamesProcessed % 100 == 0):
        printStr = "Processed " + str(gamesProcessed)
        print(printStr)
    
    if(gamesProcessed == 100):
        break

    plyLabelPairs = gameLine.split(":") # split the string into move-ply pairs
    plyLabelPairs.pop() # remove the newline character
    chessBoard = chess.Board() #create a new chessboard in the starting position.

    for pair in plyLabelPairs:
        #Split the ply and label
        splitArr = pair.split(";")
        ply = splitArr[0]
        label = int(splitArr[1])

        # there was an error in creating data, where 215 was set as 0 centipawns instaed of 115
        # to fix it, subtract 100 from all non-mating and non-mating and non-fixed evaluations

        chessBoard.push_san(ply)
        if(gamesProcessed <= numTrainGames):
            trainInputs.append(getInputArray(chessBoard))
            trainOutputs.append(label)  # error with setting the 0 value at 215 rather than 115. Subtract 100 to fis
        else:
            testInputs.append(getInputArray(chessBoard))
            testOutputs.append(label)
    
    gamesProcessed += 1

train_dataset = TensorDataset(torch.tensor(trainInputs), torch.tensor(trainOutputs))
test_dataset = TensorDataset(torch.tensor(testInputs), torch.tensor(testOutputs))


# Hyper-parameters 
input_size = 64 # number of squares
hidden_size = 200 # number of pixels in hidden layer
num_classes = 230 
num_epochs = 2 # number of times we go through data
batch_size = 100
learning_rate = 0.001

# Data loader
train_loader = torch.utils.data.DataLoader(dataset=train_dataset, 
                                           batch_size=batch_size, 
                                           shuffle=True)

test_loader = torch.utils.data.DataLoader(dataset=test_dataset, 
                                          batch_size=batch_size, 
                                          shuffle=False)


# Fully connected neural network with one hidden layer
class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.input_size = input_size
        self.l1 = nn.Linear(input_size, hidden_size)  # connects the input layer to the first hidden layer
        self.relu = nn.ReLU() # relu function
        self.l2 = nn.Linear(hidden_size, hidden_size) # connects the first hidden layer to the second
        self.l3 = nn.Linear(hidden_size, num_classes) # connects the second hidden layer to the output layer


    def forward(self, x):
        out = self.l1(x) #runs input into hidden layer
        out = self.relu(out) # runs output of layer 1 through relu
        out = self.l2(out) # runs relu'd function through to the second hidden layer
        out = self.relu(out)
        out = self.l3(out) # runs the relu'd output of the 2nd hidden layer into the output layer
        return out


#no gpu
device = torch.device('cpu')

model = NeuralNet(input_size, hidden_size, num_classes).to(device)


# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)  


# Train the model
n_total_steps = len(train_loader)
for epoch in range(num_epochs):
    for i, (images, labels) in enumerate(train_loader):  
        # origin shape: [100, 1, 28, 28]
        # resized: [100, 784]
        images = images.to(device)
        labels = labels.to(device)
        
        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (i+1) % 100 == 0:
            print (f'Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{n_total_steps}], Loss: {loss.item():.4f}')



# Test the model
# In test phase, we don't need to compute gradients (for memory efficiency)
with torch.no_grad():
    n_correct = 0
    n_samples = 0
    for images, labels in test_loader:
        images = images.to(device)
        labels = labels.to(device)
        outputs = model(images)
        # max returns (value ,index)
        _, predicted = torch.max(outputs.data, 1)
        n_samples += labels.size(0)
        n_correct += (predicted == labels).sum().item()

    acc = 100.0 * n_correct / n_samples
    print(f'Accuracy of the network on the test images: {acc} %')