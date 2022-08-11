# Chess_AI
A machine learning project to create an AI that can play chess competently. This was done by training an evaluation on stockfish 14 evaluations, then applying its evaluation abilities to a min/max algorithim to find the best move in a given position.


## Network Structure


### Input Layer
There are 64 squares on a chessboard, and the input layer will have 64 neurons.

There are 6 distinct piece types: King, Queen, Rook, Knight, Bishop, and Pawn. Since all pieces are 1 of 2 colors, there are 12 piece types. As such, all neurons will take one of the following 12 values:

<pre>
 1 / 12     White Pawn
 2 / 12     Black Pawn
 3 / 12     White Knight
 4 / 12     Black Knight
 5 / 12     White Bishop
 6 / 12     Black Bishop
 7 / 12     White Rook
 8 / 12     Black Rook
 9 / 12     White Queen
10 / 12     Black Queen
11 / 12     White King
12 / 12     Black King
</pre>

### Hidden Layers

Somewhat arbitrarily, it was chosen that this project will have 2 hidden layers, each with 200 neurons.


### Output Layer

The output layer will have 230 neurons explained below.

The outputs are meant to classify the position as a single integer output. Ideally, we want to keep a simple relationship, that the larger a number is, the better the position is for white. In the extremes, an output of 0 would mean that black has checkmated white.

There are 3 types of evaluation: forced mate for black, forced mate for white, and no forced mate detected.

An output n such that n is between 0 and 14 inclusive means that the netork believes black to have a forced mate in n moves.

An evaluation n such that n is between 15 and 214 inclusive means that the network cannot find a mate. Instead, it then gives an evalutation. To find the evaluation in terms of Stockfish eval, use the formula (n - 215) / 10. This means that an engine cannot give an evaluation higher than +9.9 or below -9.9, and only gives evaluations with precision of 0.1.

Finally, for evaluations n such that n is between 215 and 229 inclusive, the network believes it has found a forced mate for white in 229 - n moves. That means if it outputs 229 exactly, it believes white to have checkmated black.

### Rejected Ideas

It was considered to have 32 input layers, one for each piece, and have their values correspond to the square that piece occupies, and 0 if it is not on the board.

However, this runs into two problems. First, the same board position could be represented more than one way. Second, if a pawn were to promote, it would be difficult to convey which piece it had become.