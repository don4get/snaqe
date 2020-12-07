# -*- coding: utf-8 -*-
from PySide2.QtCore import Qt, QEvent, QCoreApplication, QTimer, QObject
from PySide2.QtGui import QKeyEvent

KEYS = [Qt.Key_Up, Qt.Key_Right, Qt.Key_Down, Qt.Key_Left]

DIR2KEYS = {"U": Qt.Key_Up, "R": Qt.Key_Right, "D": Qt.Key_Down, "L": Qt.Key_Left}


class QBot(QObject):
    def __init__(self, gameWidget, parent=None):
        super().__init__(parent)
        self.gameWidget = gameWidget
        self.count = 0
        self.timer = QTimer(self)
        self.timer.setInterval(100)

        self.timer.timeout.connect(self.turnClockwise)
        self.timer.start()

    def turnClockwise(self):
        self.sendkeys(KEYS[self.count])
        self.timer.start()
        self.count = (self.count + 1) % len(KEYS)

    def changeDirection(self, direction):
        self.sendkeys(DIR2KEYS[direction])

    def sendkeys(self, char, modifier=Qt.NoModifier):
        event = QKeyEvent(QEvent.KeyPress, char, modifier)
        QCoreApplication.postEvent(self.gameWidget, event)
