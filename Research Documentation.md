# Research Documentation



## Data Gathering

To train our Convolutional Neural Network, we many games. The MINST dataset for hand drawn digits uses 60 000 data examples for 10 possible outputs, and thus, to keep that ratio of examples to possible outcomes, we need 1 380 000 chess positions.

The average chess game lasts 40 moves. Since each "move" involves both players making a "ply", and thus 2 distinct positions, the average chess game represents 80 positions. As such, we will require about 17 250 games. Now, we may end up with many repeats, but that is a problem that can hopefully be fixed by playing each game out to mate using chess engines, and adding those positions to the dataset.

To gather a large amount of chess games, we used the [ficsgames database](https://www.ficsgames.org/download.html). To start off, we downloaded all games from January 2022 played in standard time controls, where average player rating was above 2000.

After decompiling, we have pgns in the following format:

<pre>
[Event "FICS rated standard game"]
[Site "FICS freechess.org"]
[FICSGamesDBGameNo "510278046"]
[White "blore"]
[Black "Slek"]
[WhiteElo "2015"]
[BlackElo "2079"]
[WhiteRD "0.0"]
[BlackRD "0.0"]
[TimeControl "900+0"]
[Date "2022.01.31"]
[Time "23:21:00"]
[WhiteClock "0:15:00.000"]
[BlackClock "0:15:00.000"]
[ECO "B06"]
[PlyCount "108"]
[Result "1/2-1/2"]

1. e4 g6 2. h4 d6 3. h5 gxh5 4. Qxh5 Nf6 5. Qe2 Nc6 6. c3 e5 7. Nf3 Bg4 8. d3 d5 9. Nbd2 Qd6 10. exd5 Qxd5 11. Ne4 Be7 12. Nxf6+ Bxf6 13. Qe4 Bxf3 14. gxf3 O-O-O 15. Qf5+ Qe6 16. Bh3 Qxf5 17. Bxf5+ Kb8 18. Be3 Ne7 19. Be4 Bg7 20. O-O-O f5 21. Bg5 fxe4 22. Bxe7 Rxd3 23. Rxd3 exd3 24. Kd2 Kc8 25. Kxd3 Kd7 26. Bc5 Ke6 27. Ke4 b6 28. Be3 h5 29. Bg5 c6 30. Rg1 Bf6 31. f4 exf4 32. Bxf4 h4 33. Rg6 Rh5 34. f3 h3 35. Bh2 Rg5 36. Rxg5 Bxg5 37. f4 Bh4 38. b3 Be1 39. c4 Kf6 40. f5 Bc3 41. Bb8 a6 42. Bc7 b5 43. cxb5 cxb5 44. a4 bxa4 45. bxa4 Kg5 46. Kf3 Kxf5 47. Bb6 Be5 48. Bd8 h2 49. Kg2 Ke4 50. Kh1 Kd5 51. Be7 Kc4 52. Bf8 a5 53. Bh6 Kb3 54. Be3 Kxa4 {Game drawn by mutual agreement} 1/2-1/2

[Event "FICS rated standard game"]
[Site "FICS freechess.org"]
[FICSGamesDBGameNo "510277839"]
[White "kamenozrout"]
[Black "Indrayoga"]
[WhiteElo "2173"]
[BlackElo "1960"]
[WhiteRD "0.0"]
[BlackRD "0.0"]
[WhiteIsComp "Yes"]
[TimeControl "900+0"]
[Date "2022.01.31"]
[Time "22:34:00"]
[WhiteClock "0:15:00.000"]
[BlackClock "0:15:00.000"]
[ECO "C48"]
[PlyCount "74"]
[Result "0-1"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 Nf6 4. Nc3 Nd4 5. Ba4 c6 6. O-O a5 7. Nxd4 exd4 8. e5 dxc3 9. exf6 d5 10. dxc3 b5 11. Re1+ Be6 12. fxg7 Bxg7 13. Qg4 O-O 14. Rxe6 fxe6 15. Qxe6+ Kh8 16. Qxc6 bxa4 17. Qxa4 Qb6 18. Be3 Qxb2 19. Rd1 Qxc3 20. Qb3 d4 21. Qxc3 dxc3 22. Kf1 Rfd8 23. Rxd8+ Rxd8 24. Ke2 Rb8 25. Kd3 Rb2 26. a3 Ra2 27. Bc5 Kg8 28. f4 a4 29. Bb4 Ra1 30. f5 Rd1+ 31. Kc4 Rd2 32. g4 Rxc2 33. h3 Rb2 34. Be7 c2 35. Bg5 Rb1 36. h4 c1=Q+ 37. Bxc1 Rxc1+ {White resigns} 0-1
</pre>

Unfortunately, we don't know how many games we have, and won't until we clean this data. 


## Data Cleaning

All Data Parsing is done in Java, and all code related to data parsing can be found in the folder "Data Cleaning".

Cleaning this data ended up being very fast and efficient. Simply ignore all lines that don't begin with the character '1', and then ignore everything in that line after the character '{'. 

As it turns out, there were 2 223 games, or just over 10 % of what we need. Thus, we will download more games, and clean their data as well.

We started with removing the rating requirement, and downloading all standard chess games. As it turns out, this dataset had more than twice as large as we needed, so we hardcoded a lines limit. Now, we have 17 250 games, and can now add to this data in order to create a dataset that a neural network can use. 

## Data Conversion

The goal of this section is to assign various positions a "rating", in a format I can easily feed into a neural network.

This was done by playing games, and then, ply by ply, giving stockfish 15 0.01 seconds to assign each position in the game an evaluation between 0 and 229 inclusive.

There are 3 types of evaluation: forced mate for black, forced mate for white, and no forced mate detected.

An output n such that n is between 0 and 14 inclusive means that the netork believes black to have a forced mate in n moves.

An evaluation n such that n is between 15 and 214 inclusive means that the network cannot find a mate. Instead, it then gives an evalutation. To find the evaluation in terms of Stockfish eval, use the formula (n - 215) / 10. This means that an engine cannot give an evaluation higher than +9.9 or below -9.9, and only gives evaluations with precision of 0.1.

Finally, for evaluations n such that n is between 215 and 229 inclusive, the network believes it has found a forced mate for white in 229 - n moves. That means if it outputs 229 exactly, it believes white to have checkmated black.

Another thing we did in order to ensure that the network has enough experience with forcing mate is to play out games that had an eval either greater than 500 centipawns or less than -500 cenitpawns.

Then, we will convert the data into one that makes it easier for a neural network to process, without taking up too much memory.

To begin, we have data like this:

<pre>
1. d4 d6 2. d5 c5 3. c4 Nf6 4. Nc3 g6 5. e4 Bg7 6. f4 O-O 7. Nf3 e6 8. e5 dxe5 9. fxe5 Nfd7 10. dxe6 fxe6 11. Ng5 Nxe5 12. Qxd8 Rxd8 13. Nge4 b6 14. Nb5 Na6 15. Bg5 Rf8 16. Nbd6 Nc6 17. Nxc8 Raxc8 18. O-O-O Nd4 19. g3 Nb4 20. Bh3 Nxa2+ 21. Kb1 Nb4 22. Bd2 Nbc6 23. Ng5 Rce8 24. Bc3 h6 25. Bxd4 Nxd4 26. Rxd4 Bxd4 27. Nxe6 Rxe6 28. Bxe6+ Kg7 29. g4 Rf2 30. h4 Rxb2+ 31. Kc1 Rg2 32. h5 gxh5 33. gxh5 Rg1+ 34. Rxg1+ Bxg1 35. Kc2 Kf6 36. Bd5 Ke5 37. Kb3 b5 38. Bf3 a6 39. cxb5 axb5 40. Be2 b4 41. Kc4 Ke4 42. Bd1 Bd4 43. Kb3 Kd3 44. Bc2+ Kd2 45. Bg6 Kc1 46. Ka2 c4 47. Bf7 b3+ 48. Ka3 b2 49. Bxc4 b1=Q 50. Ba2 Bc5+ 
1. d4 c5 2. c3 Na6 3. e3 b6 4. Bd3 Nf6 5. Nd2 Bb7 6. Ngf3 Rc8 7. O-O h5 8. Ne5 e6 9. f4 Bd6 10. Rf3 Bxf3 11. Qxf3 Bxe5 12. fxe5 c4 13. Bc2 Ng4 14. h3 Nh6 15. e4 h4 16. Nf1 O-O 17. Bxh6 gxh6 18. Qg4+ Qg5 19. Nh2 Rc7 20. Nf3 Qxg4 21. hxg4 Rb8 22. Nxh4 Kg7 23. a3 f6 24. exf6+ Kxf6 25. e5+ Kg7 26. Nf3 Rf8 27. g5 hxg5 28. Nxg5 Rc6 29. Be4 Rc7 30. Rf1 Rxf1+ 31. Kxf1 Rc8 32. g4 Rd8 33. Kg2 Re8 34. Kg3 Rh8 35. Nh3 Rf8 36. Nf4 Nc7 37. d5 exd5 38. Bxd5 Rxf4 39. Kxf4 Nxd5+ 40. Ke4 Ne7 41. Kd4 b5 42. Kc5 a6 43. Kd6 Nc6 44. Kxd7 Nxe5+ 45. Kd6 Nxg4 46. Kc6 Ne5+ 47. Kb6 Nf3 48. Kxa6 Kf6 49. Kxb5 Nd2 50. Kb4 Ke6 51. a4 Kd5 52. a5 Ne4 53. Kb5 Nc5 54. a6 Nd3 55. a7 Nxb2 56. a8=Q+ Ke6 57. Qc6+ Ke5 58. Qc5+ Ke6 59. Qe3+ Kd5 60. Qd2+ Nd3 61. Ka4 Ke4 62. Ka3 Kf3 63. Ka2 Nf4 64. Qd4 Ng6 65. Qxc4 Nf4 66. Ka3 Ne2 67. Ka4 Nf4 68. Ka5 Nh5 69. Ka6 Nf4 70. Ka7 Ng2 71. Qc8 Ke3 72. c4 Nf4 73. c5 Nd5 74. c6 Kd3 75. c7 Kd2 76. Qd7 Ke3 77. c8=Q Ke4 78. Qe6+ 
1. e4 e5 2. Nf3 Nc6 3. Bc4 d6 4. h3 Be7 5. Nc3 Nf6 6. d3 O-O 7. a3 a6 8. O-O Nd4 9. b4 Nxf3+ 10. Qxf3 b6 11. Qg3 Kh8 12. f4 exf4 13. Bxf4 Be6 14. Nd5 Nxd5 15. exd5 Bd7 16. Rae1 Bf6 17. Re2 Re8 18. Rfe1 Rxe2 19. Rxe2 b5 20. Bb3 a5 21. c4 axb4 22. axb4 Ra3 23. Bc2 bxc4 24. Bc1 Rc3 25. Bb2 cxd3 26. Bxd3 Rb3 27. Bxf6 gxf6 28. Re3 Rxb4 29. Qe1 Rb8 30. Qh4 f5 31. Qd4+ f6 32. Rf3 Qe7 33. Re3 Qf7 34. Rf3 Qe7 35. Kh2 Qe5+ 36. Qxe5 fxe5 37. Bxf5 Bxf5 38. Rxf5 Kg7 39. Rf1 Rb5 40. Rd1 Kf6 41. g4 Ke7 42. Kg3 Rc5 43. Kh4 c6 44. dxc6 Rxc6 45. Kg5 Ke6 46. Kh6 Rc7 47. h4 d5 48. g5 d4 49. h5 Kd5 50. g6 hxg6 51. hxg6 e4 52. g7 Rxg7 53. Kxg7 e3 54. Kf6 Ke4 55. Ke6 e2 56. Re1 d3 57. Kd6 Ke3 58. Kc5 d2 59. Rh1 d1=Q 60. Rh3+ Kf4 61. Rh4+ Kg3 
</pre>

And we will convert it into a format like so:

<pre>
d4;216:d6;220:d5;214:c5;222:c4;223:Nf6;223:Nc3;224:g6;225:e4;224:Bg7;225:f4;221:O-O;224:Nf3;221:e6;219:e5;209:dxe5;213:fxe5;214:Nfd7;219:dxe6;209:fxe6;211:Ng5;196:Nxe5;191:Qxd8;192:Rxd8;190:Nge4;191:b6;194:Nb5;191:Na6;206:Bg5;205:Rf8;203:Nbd6;202:Nc6;210:Nxc8;198:Raxc8;201:O-O-O;203:Nd4;205:g3;204:Nb4;204:Bh3;200:Nxa2+;209:Kb1;210:Nb4;212:Bd2;188:Nbc6;191:Ng5;182:Rce8;191:Bc3;180:h6;183:Bxd4;171:Nxd4;170:Rxd4;140:Bxd4;136:Nxe6;141:Rxe6;175:Bxe6+;175:Kg7;180:g4;166:Rf2;163:h4;176:Rxb2+;178:Kc1;176:Rg2;179:h5;180:gxh5;180:gxh5;181:Rg1+;210:Rxg1+;209:Bxg1;208:Kc2;212:Kf6;213:Bd5;212:Ke5;215:Kb3;212:b5;212:Bf3;212:a6;215:cxb5;215:axb5;215:Be2;215:b4;215:Kc4;215:Ke4;215:Bd1;214:Bd4;215:Kb3;214:Kd3;215:Bc2+;215:Kd2;215:Bg6;215:Kc1;215:Ka2;128:c4;152:Bf7;15:b3+;15:Ka3;15:b2;15:Bxc4;15:b1=Q;15:Ba2;2:Bc5+;1:Ka4;1:Qb4#;0:
d4;218:c5;225:c3;218:Na6;229:e3;222:b6;226:Bd3;223:Nf6;224:Nd2;219:Bb7;221:Ngf3;219:Rc8;222:O-O;220:h5;233:Ne5;225:e6;227:f4;221:Bd6;232:Rf3;216:Bxf3;216:Qxf3;205:Bxe5;259:fxe5;265:c4;267:Bc2;245:Ng4;256:h3;249:Nh6;259:e4;236:h4;252:Nf1;234:O-O;261:Bxh6;228:gxh6;231:Qg4+;209:Qg5;211:Nh2;208:Rc7;224:Nf3;203:Qxg4;200:hxg4;200:Rb8;212:Nxh4;207:Kg7;208:a3;211:f6;216:exf6+;226:Kxf6;218:e5+;222:Kg7;222:Nf3;218:Rf8;219:g5;215:hxg5;221:Nxg5;224:Rc6;229:Be4;224:Rc7;231:Rf1;202:Rxf1+;205:Kxf1;205:Rc8;205:g4;203:Rd8;207:Kg2;210:Re8;211:Kg3;209:Rh8;216:Nh3;215:Rf8;216:Nf4;215:Nc7;223:d5;193:exd5;192:Bxd5;180:Rxf4;173:Kxf4;171:Nxd5+;174:Ke4;166:Ne7;186:Kd4;188:b5;198:Kc5;200:a6;224:Kd6;216:Nc6;243:Kxd7;218:Nxe5+;217:Kd6;144:Nxg4;215:Kc6;215:Ne5+;215:Kb6;215:Nf3;222:Kxa6;218:Kf6;216:Kxb5;215:Nd2;215:Kb4;215:Ke6;215:a4;215:Kd5;215:a5;213:Ne4;222:Kb5;222:Nc5;217:a6;218:Nd3;310:a7;214:Nxb2;214:a8=Q+;214:Ke6;214:Qc6+;306:Ke5;304:Qc5+;214:Ke6;214:Qe3+;214:Kd5;214:Qd2+;214:Nd3;214:Ka4;301:Ke4;314:Ka3;296:Kf3;306:Ka2;302:Nf4;311:Qd4;314:Ng6;313:Qxc4;214:Nf4;214:Ka3;214:Ne2;214:Ka4;313:Nf4;214:Ka5;214:Nh5;214:Ka6;214:Nf4;214:Ka7;314:Ng2;214:Qc8;214:Ke3;214:c4;214:Nf4;214:c5;214:Nd5;214:c6;214:Kd3;214:c7;214:Kd2;214:Qd7;221:Ke3;224:c8=Q;214:Ke4;226:Qe6+;226:Kd3;226:Qf5+;226:Kd4;226:Qcc2;226:Nc3;226:Qcd3#;229:

</pre>

Where each line is a game, each ply is paired with its label. Ply-label pairs are seperated by colons, and plys are seperated from their labels by semicolons.

Consider the following data: <pre>d4;216:d6;220:</pre> This means that the first ply of a game was d4, and the label for the reulting position is 216. Black's first move was d6, and that position has a label of 220. 

Because of the strict time constraints, the exact same position may have slightly different evaluations. This is not necessarily a dealbreaker, but it could potentially cause issues in the training stage.

The network's structure was run with 64 neurons in the input layer, one for each square, 2 hidden layers with 200 neurons each, and 230 neurons in the output layer. A ReLU was run before each hidden layer, and no activation fuction was taken for the output layer.

After running the program for 5 epochs, it was able to achieve an accuracy of 16.2%. Quite lower than hoped, but perhaps still capable of playing decent chess.