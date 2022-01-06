import copy
import random
import pandas as pd
from typing import Optional, cast
from time import time
from abc import ABC, abstractmethod

from .grid import Grid


class Player(ABC):
    '''
    tic-tac-toeのプレイヤーを表す抽象クラス.
    '''
    def __init__(self, name: Optional[None]=None) -> None:
        self.name = name
        self.records: dict[int, list[float]] = {i: [] for i in range(10)}
    
    def __str__(self) -> str:
        if self.name:
            return self.name
        else:
            return 'Player'

    @abstractmethod
    def choice(self, grid: Grid, mark: str) -> int:
        '''
        現在の盤面から１箇所マークを場所を選ぶメソッド.
        
        Parameters
        ----------
        grid: Grid
            現在の盤面
        
        mark: str
            追加するマーク
        
        Returns
        -------
        idx: int
            マークをする場所.
        '''
        ...
    
    def place(self, grid: Grid, mark: str) -> None:
        n_blanks = grid.n_blanks
        tic: float = time()
        idx: int = self.choice(grid, mark)
        grid.place(mark, idx)
        self.records[n_blanks].append(time() - tic)
    

def to_csv(players: list[Player], path: str) -> None:
    means: list[list[Optional[float]]] = []
    for i in range(1, 10):
        row: list[Optional[float]] = []
        for player in players:
            if len(player.records[i]) == 0:
                row.append(None)
            else:
                _sum: float = 0.
                for v in player.records[i]:
                    _sum += v
                ave: float = _sum / len(player.records)
                row.append(ave)
        means.append(row)
    
    df: pd.DataFrame = pd.DataFrame(
        means,
        index=range(1, 10),
        columns=[player.name for player in players]
    )
    df.to_csv(path)


class RandomPlayer(Player):
    '''
    ランダムにマークをするtic-tac-toeのプレイヤー
    '''
    def __init__(self, name: Optional[None]=None) -> None:
        if name is None:
            name = 'RandomPlayer'
        super(RandomPlayer, self).__init__(name)
    
    def choice(self, grid: Grid, mark: str) -> int:
        '''
        現在の盤面から１箇所マークを場所を選ぶメソッド.
        マークをする場所は, 現在の盤面のうち空欄のマスからランダムに選択する.
        
        Parameters
        ----------
        grid: Grid
            現在の盤面
        
        mark: str
            追加するマーク

        Returns
        -------
        random_idx: int
            マークをする場所.
        '''
        random_idx: int =  random.choice(grid.blanks)
        return random_idx


class HumanPlayer(Player):
    '''
    ユーザーの入力に従ってマークをするtic-tac-toeのプレイヤー
    '''
    def __init__(self, name: Optional[None]=None) -> None:
        if name is None:
            name = 'HumanPlayer'
        super(HumanPlayer, self).__init__(name)
    
    def choice(self, grid: Grid, mark: str) -> int:
        '''
        現在の盤面から１箇所マークを場所を選ぶメソッド.
        マークする箇所はユーザーの入力により決定する.
        
        Parameters
        ----------
        grid: Grid
            現在の盤面
        
        mark: str
            追加するマーク

        Returns
        -------
        idx: int
            マークをする場所.
        '''
        while True:
            s = input(f'Player {mark}: ')
            idx: int = int(s)
            if idx in grid.blanks:
                return idx
            else:
                print(f'Invalid input: {s}.')


class MinMaxPlayer(Player):
    '''
    Mini-Max探索によりマークするを決定するtic-tac-toeのプレイヤー

    Attributes
    ----------
    ab: bool=True
        alpha値, beta値による枝刈りを行うかどうかを表す.
    
    show_score: bool=False
        探索を行った後にスコアを表示するかどうかを表す.
    
    boost: bool=True
        Trueならば盤面が空のとき, 探索を行わない.
    '''
    def __init__(
        self,
        name: Optional[None]=None,
        ab: bool=True,
        show_score: bool=False,
        boost: bool=True
    ) -> None:

        if name is None:
            name = 'MiniMaxPlayer'
        self.ab = ab
        self.show_score = show_score
        self.boost = boost
        super(MinMaxPlayer, self).__init__(name)
    
    def choice(self, grid: Grid, mark: str) -> int:
        '''
        現在の盤面から１箇所マークを場所を選ぶメソッド.
        マークする箇所はMini-Max探索により決定する.
        
        Parameters
        ----------
        grid: Grid
            現在の盤面
        
        mark: str
            追加するマーク

        Returns
        -------
        best_idx: int
            マークをする場所.
        '''

        if self.boost and grid.is_empty:
            return random.choice(grid.blanks)

        marks: tuple[str, str] = grid.marks
        best_indices: Optional[list[int]] = None
        best_score: Optional[int] = None

        for idx in grid.blanks:
            g = copy.deepcopy(grid)
            g.place(mark, idx)
            score: Optional[int] = None
            if self.ab:
                score = self._min_value(g, -1, 1) if mark == marks[0] else self._max_value(g, -1, 1)
            else:
                score = self._min_value(g) if mark == marks[0] else self._max_value(g)
            
            if self.show_score:
                print(f'idx = {idx}, score = {score}')

            if best_indices is None:
                best_indices = [idx]
                best_score = score
            elif (mark == marks[0] and score >= cast(int, best_score)) or \
                        (mark == marks[1] and score <= cast(int, best_score)):
                if score == best_score:
                    best_indices.append(idx)
                else:
                    best_indices = [idx]
                best_score = score

        best_idx: int = random.choice(cast(list[int], best_indices))
        return best_idx


    def _max_value(self, grid: Grid, alpha: int=0, beta: int=0) -> int:
        '''
        Mini-Max探索のための再帰関数
        '''
        marks: tuple[str, str] = grid.marks
        if grid.judge(marks[0]):
            return 1
        if grid.judge(marks[1]):
            return -1
        if len(grid.blanks) == 0:
            return 0
        
        v: int = -1
        for idx in grid.blanks:
            g = copy.deepcopy(grid)
            g.place(marks[0], idx)
            if self.ab:
                v = max(v, self._min_value(g, alpha, beta))
                if v >= beta:
                    return v
                if v > alpha:
                    alpha = v
            else:
                v = max(v, self._min_value(g))
        return v

    def _min_value(self, grid: Grid, alpha: int=0, beta: int=0) -> int:
        '''
        Mini-Max探索のための再帰関数
        '''
        marks: tuple[str, str] = grid.marks
        if grid.judge(marks[0]):
            return 1
        if grid.judge(marks[1]):
            return -1
        if len(grid.blanks) == 0:
            return 0
        
        v: int = 1
        for idx in grid.blanks:
            g = copy.deepcopy(grid)
            g.place(marks[1], idx)
            if self.ab:
                v = min(v, self._max_value(g, alpha, beta))
                if v <= alpha:
                    return v
                if v < beta:
                    beta = v
            else:
                v = min(v, self._max_value(g))
        return v
