# Research Documentation



## Data Gathering

To train our Convolutional Neural Network, we many games. The MINST dataset for hand drawn digits uses 60 000 data examples for 10 possible outputs, and thus, to keep that ratio of examples to possible outcomes, we need 230 000 chess positions.

The average chess game lasts 40 moves. Since each "move" involves both players making a "ply", and thus 2 distinct positions, the average chess game represents 80 positions. As such, we will require about 2 900 games. Now, we may end up with many repeats, but that is a problem that can hopefully be fixed by playing each game out to mate using chess engines, and adding those positions to the dataset.

To gather a large amount of chess games, we used the [ficsgames database](https://www.ficsgames.org/download.html). To start off, we downloaded all games from January 2022 played in standard time controls, where average player rating was above 2000.

