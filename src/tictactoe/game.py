from typing import Optional

from .grid import Grid
from .players import Player


class TicTacToe(object):
    '''
    tic-tac-toeのゲーム本体を表すクラス.

    Attributes
    ----------
    grid: Grid=None
        tic-tac-toeを行う盤面であるGridクラス.
        Noneであればゲーム開始時自動的に盤面が全て空欄のGridが与えられる.
    
    show_board: bool=True
        盤面が更新されるたびに, 盤面の内容を出力するかどうかを表す.
    
    refresh: bool=True
        ゲーム開始時に盤面を初期化するかどうかを表す.
    '''
    def __init__(self, grid: Grid=None, show_board: bool=True, refresh: bool=True) -> None:
        self.grid = grid
        self.show_board = show_board
        self.refresh = refresh

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
        grid: Optional[Grid] = self.grid
        if grid is None:
            grid = Grid()
        if self.refresh:
            grid.refresh()

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
