from typing import Optional
from copy import deepcopy

from .grid import Grid
from .players import Player


class TicTacToe(object):
    '''
    tic-tac-toeのゲーム本体を表すクラス.

    Attributes
    ----------
    grid: Grid=None
        tic-tac-toeの初期盤面を表すGridクラス.
        Noneであればゲーム開始時自動的に盤面が全て空欄のGridが与えられる.
    
    show_board: bool=True
        盤面が更新されるたびに, 盤面の内容を出力するかどうかを表す.
    '''
    def __init__(self, grid: Optional[Grid]=None, show_board: bool=True) -> None:
        if grid is None:
            grid = Grid()
        self.grid: Grid = grid
        self.show_board: bool = show_board

    def __call__(self, player1: Player, player2: Player) -> int:
        return self.tictactoe(player1, player2)

    def tictactoe(self, player1: Player, player2: Player) -> int:
        '''
        実際にtic-tac-toeのゲームを行うメソッド.

        Parameters
        ----------
        player1: Player
            先手のプレイヤー.
        
        player2: Player
            後手のプレイヤー
        
        Returns
        -------
        status: int
            ゲームがどのように終了したかを表す数値を返す.
            具体的には, 「先手勝ちならば1」, 「引き分けならば0」, 「後手勝ちならば-1」を返す.
        '''
        grid: Grid = deepcopy(self.grid)
        first: bool = True
        mark: str = grid.marks[0]
        player: Player = player1

        while True:
            player.place(grid, mark)

            if self.show_board:
                print(grid)
                print()

            if grid.judge(mark):
                return 1 if first else -1
            if len(grid.blanks) == 0:
                return 0

            first = not first
            mark = grid.marks[0] if first else grid.marks[1]
            player = player1 if first else player2
