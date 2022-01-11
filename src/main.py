from tqdm import tqdm

from tictactoe import TicTacToe, Player, MinMaxPlayer, RandomPlayer


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
    player1 = MinMaxPlayer()
    player2 = RandomPlayer()
    game = TicTacToe(show_board=True)

    experiment(game, player1, player2, 100)
