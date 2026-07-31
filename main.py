from config import GameConfig
from game import Game


def main() -> None:
    config = GameConfig()
    game = Game(config)
    game.run()


if __name__ == "__main__":
    main()