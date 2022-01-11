# tictactoe
The tictactoe game and its players.

## Environment
- Python 3.9

## Example
```Python
from tictactoe import TicTacToe, MinMaxPlayer, RandomPlayer

tictactoe = TicTacToe()
player1 = MinMaxPlayer(name='MinMax')
player2 = RandomPlayer(name='Random')

tictactoe(player1, player2)
```
