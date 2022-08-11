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

We started with removing the rating requirement, and downloading all standard chess games. As it turns out, this dataset had more than twice as large as we needed, so we hardcoded a lines limit. Now, we have 1750 games, and can now add to this data in order to create a dataset that a neural network can use. 