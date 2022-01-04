from tqdm import tqdm

from tictactoe import *
from tictactoe.players import to_csv


def experiment(
    game: TicTacToe,
    player1: Player,
    player2: Player,
    n_games: int,
    is_tqdm: bool=True
) -> None:

    record: list[int] = []
    games = range(n_games)
    if is_tqdm:
        games = tqdm(games)

    for _ in games:
        record.append(game(player1, player2))

    print(record.count(1) / len(record))
    print(record.count(0) / len(record))
    print(record.count(-1) / len(record))


if __name__ == '__main__':
    player1 = MinMaxPlayer(boost=False)
    player2 = MinMaxPlayer(ab=False, boost=False)
    game = TicTacToe(show_board=False)

    experiment(game, player1, player2, 10)
    experiment(game, player2, player1, 10)

    to_csv([player1, player2], path='players.csv')
