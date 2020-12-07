#!/usr/bin/python
import sys
from random import randrange

from PySide2 import QtGui, QtCore
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QApplication, QFrame


class GameWidget(QWidget):
    def __init__(self, human=True):
        super(GameWidget, self).__init__()
        self.highScore: int = 0
        self.human = human
        self.initUI()

        self.lastKeyPress = Qt.Key_Right
        self.isPaused = False
        self.isOver = False
        self.foodx, self.foody = 0, 0

    def initUI(self):
        self.width = 300
        self.height = 300
        self.tileWidth = self.width / 25.0
        self.tileHeight = self.height / 25.0
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle("snaqe")
        self.setStyleSheet("QWidget { background: #A9F5D0 }")
        self.newGame()
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.scoreBoard(qp)
        self.placeFood(qp)
        self.drawSnake(qp)
        self.scoreText(event, qp)
        if self.isOver:
            self.gameOver(event, qp)
        qp.end()

    def keyPressEvent(self, e):
        if not self.isPaused:
            # print "inflection point: ", self.x, " ", self.y
            if (
                e.key() == Qt.Key_Up
                and self.lastKeyPress != Qt.Key_Up
                and self.lastKeyPress != Qt.Key_Down
            ):
                self.direction(Qt.Key_Up)
                self.lastKeyPress = Qt.Key_Up
            elif (
                e.key() == Qt.Key_Down
                and self.lastKeyPress != Qt.Key_Down
                and self.lastKeyPress != Qt.Key_Up
            ):
                self.direction(Qt.Key_Down)
                self.lastKeyPress = Qt.Key_Down
            elif (
                e.key() == Qt.Key_Left
                and self.lastKeyPress != Qt.Key_Left
                and self.lastKeyPress != Qt.Key_Right
            ):
                self.direction(Qt.Key_Left)
                self.lastKeyPress = Qt.Key_Left
            elif (
                e.key() == Qt.Key_Right
                and self.lastKeyPress != Qt.Key_Right
                and self.lastKeyPress != Qt.Key_Left
            ):
                self.direction(Qt.Key_Right)
                self.lastKeyPress = Qt.Key_Right
            elif e.key() == Qt.Key_P:
                self.pause()

        elif e.key() == Qt.Key_P:
            self.start()
        elif e.key() == Qt.Key_Space:
            self.newGame()
        elif e.key() == Qt.Key_Escape:
            self.close()

    # noinspection PyAttributeOutsideInit
    def newGame(self):
        self.score = 0
        self.x = self.tileWidth
        self.y = self.tileHeight * 3
        self.timer = QtCore.QBasicTimer()
        self.snakeArray = [
            [self.x, self.y],
            [self.x - self.tileWidth, self.y],
            [self.x - self.tileHeight, self.y],
        ]
        self.foodx = 0
        self.foody = 0

        self.isPaused = False
        self.isOver = False
        self.FoodPlaced = False
        if self.human:
            self.speed = 100
        else:
            self.speed = 1
        self.start()

    # noinspection PyAttributeOutsideInit
    def pause(self):
        self.isPaused = True
        self.timer.stop()
        self.update()

    def start(self):
        self.isPaused = False
        self.timer.start(self.speed, self)
        self.update()

    def direction(self, dir):
        if dir == Qt.Key_Down and self.checkStatus(self.x, self.y + self.tileHeight):
            self.y += self.tileHeight
            self.repaint()
            self.snakeArray.insert(0, [self.x, self.y])
        elif dir == Qt.Key_Up and self.checkStatus(self.x, self.y - self.tileHeight):
            self.y -= self.tileHeight
            self.repaint()
            self.snakeArray.insert(0, [self.x, self.y])
        elif dir == Qt.Key_Right and self.checkStatus(self.x + self.tileWidth, self.y):
            self.x += self.tileWidth
            self.repaint()
            self.snakeArray.insert(0, [self.x, self.y])
        elif dir == Qt.Key_Left and self.checkStatus(self.x - self.tileWidth, self.y):
            self.x -= self.tileWidth
            self.repaint()
            self.snakeArray.insert(0, [self.x, self.y])

    def scoreBoard(self, qp):
        qp.setPen(QtCore.Qt.NoPen)
        qp.setBrush(QtGui.QColor(25, 80, 0, 160))
        qp.drawRect(0, 0, 300, 24)

    def scoreText(self, event, qp):
        qp.setPen(QtGui.QColor(255, 255, 255))
        qp.setFont(QtGui.QFont("Decorative", 10))
        qp.drawText(8, 17, "SCORE: " + str(self.score))
        qp.drawText(170, 17, "HIGHSCORE: " + str(self.highScore))

    def gameOver(self, event, qp):
        self.highScore = max(self.highScore, self.score)
        qp.setPen(QtGui.QColor(0, 34, 3))
        qp.setFont(QtGui.QFont("Decorative", 10))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, "GAME OVER")
        qp.setFont(QtGui.QFont("Decorative", 8))
        qp.drawText(80, 170, "press space to play again")

    def checkStatus(self, x, y):
        if (
            y > self.height - self.tileHeight
            or x > self.width - self.tileWidth
            or x < 0
            or y < 2 * self.tileHeight
        ):
            self.pause()
            self.isPaused = True
            self.isOver = True
            return False
        elif self.snakeArray[0] in self.snakeArray[1 : len(self.snakeArray)]:
            self.pause()
            self.isPaused = True
            self.isOver = True
            return False
        elif self.y == self.foody and self.x == self.foodx:
            self.FoodPlaced = False
            self.score += 1
            return True
        elif self.score >= 573:
            print("Victory")

        self.snakeArray.pop()

        return True

    def placeFood(self, qp):
        if not self.FoodPlaced:
            self.foodx = randrange(24) * self.tileWidth
            self.foody = randrange(2, 24) * self.tileHeight
            if not [self.foodx, self.foody] in self.snakeArray:
                self.FoodPlaced = True
        qp.setBrush(QtGui.QColor(80, 180, 0, 160))
        qp.drawRoundedRect(
            self.foodx, self.foody, self.tileWidth, self.tileHeight, 6, 6
        )

    # draws each component of the snake
    def drawSnake(self, qp):
        qp.setPen(QtCore.Qt.NoPen)
        qp.setBrush(QtGui.QColor(0, 0, 0, 255))
        qp.drawRect(
            self.snakeArray[0][0],
            self.snakeArray[0][1],
            self.tileWidth,
            self.tileHeight,
        )
        qp.setBrush(QtGui.QColor(255, 80, 0, 255))
        for i in self.snakeArray[1::]:
            qp.drawRect(i[0], i[1], self.tileWidth, self.tileHeight)

    # game thread
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.direction(self.lastKeyPress)
            self.repaint()
        else:
            QFrame.timerEvent(self, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = GameWidget()
    sys.exit(app.exec_())
