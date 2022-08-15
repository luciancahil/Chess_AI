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




games = open("Engine Training\\Data\\InputGames.pgn", "r")

gameLines = games.readlines()


print(gameLines[0])