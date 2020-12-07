import sys

from PySide2.QtWidgets import QApplication

from snaqe.game_widget import GameWidget
from snaqe.qbot import QBot


def main():
    app = QApplication(sys.argv)
    gameWidget = GameWidget()
    qbot = QBot(gameWidget)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
