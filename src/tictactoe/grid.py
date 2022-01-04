import os


class Grid(object):
    '''
    tic-tac-toeのための3x3の盤面を表すクラス.
    盤面の位置は0から8のただ1つの整数のインデックスで表現され,
    実際の盤面とインデックスとの対応は
        0|1|2
        3|4|5
        6|7|8
    とする.

    Attributes
    ----------
    marks: tuple[str, str]
        盤面に書き込むマークを表す長さ2のタプル.
        0番目の要素が先手, 1番目の要素が後手のマークを表す.
    '''
    def __init__(self, marks: tuple[str, str]=('o', 'x')) -> None:
        if '-' in marks:
            raise ValueError()
        if marks[0] == marks[1]:
            raise ValueError()
        if len(marks) != 2:
            raise ValueError()

        self.marks = marks

        self._state: list[str] = ['-' for _ in range(9)]
        self._win_patterns: list[tuple[int, int, int]] = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6)
        ]

    def __str__(self) -> str:
        s: str = ''
        for i in range(9):
            s += f'{self._state[i]}'
            if i % 3 == 2:
                if not i == 8:
                    s += os.linesep
            else:
                s += '|'
        return s
    
    @property
    def blanks(self) -> list[int]:
        '''
        盤面の中で互いのプレイヤーがマークをつけていないマスのインデックスのリストを返す.
        '''
        return [i for i, mark in enumerate(self._state) if mark == '-']
    
    @property
    def n_blanks(self) -> int:
        '''
        盤面の中で互いのプレイヤーがマークをつけていないマスの数を返す.
        '''
        return len(self.blanks)
 
    @property
    def is_empty(self) -> bool:
        '''
        盤面がすべて空欄ならばTrue, そうでなければFalseを返す.
        '''
        if len(self.blanks) == 9:
            return True    
        return False
    
    def refresh(self) -> None:
        '''
        盤面を全てリセットしすべて空欄にする.
        '''
        self._state = ['-' for _ in range(9)]

    def place(self, mark: str, idx: int) -> bool:
        '''
        盤面の指定した位置に, 指定したマークをするメソッド.
        盤面に正しくマークをしたらTrueを返す.
        すでにマークされている場所が指定されたなどの理由でマークが出来なければFalseを返す.

        Parameters
        ----------
        mark: str
            追加するマーク
        
        idx: int
            マークをする場所のインデックス
        '''
        if idx not in self.blanks:
            return False
        self._state[idx] = mark
        return True
    
    def judge(self, mark: str) -> bool:
        '''
        指定したマークが縦, 横, 斜めのいずれか3つに揃っているかどうかを判定する.

        Parameters
        ----------
        mark: str
            判定するマーク
        '''
        for pattern in self._win_patterns:
            if [self._state[pattern[i]] for i in range(3)].count(mark) == 3:
                return True
        return False
