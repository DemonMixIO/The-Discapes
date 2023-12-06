import random
import sys
from enum import Enum
import sqlite3

from PyQt5.QtCore import Qt, QUrl, QTimer, QRect
from PyQt5.QtGui import QTransform
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaContent
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from PyQt5.QtWidgets import QColorDialog

count = 0
array = []

step = 50  # Размер клетки
N_X = 11
N_Y = 11  # Размер сетки
bg_color = (255, 255, 255)
horizontal = False


class Type(Enum):
    PLAYER = 1
    ENEMY = 2
    FIRE = 3
    EXIT = 4


class GameMode(Enum):
    PLAY = 1
    SUSPENDED = 2
    WIN = 3
    LOSEENEMY = 4
    LOSEFIRE = 5


class Direction(Enum):
    LEFT = 1
    RIGHT = -1


gamemode = GameMode.SUSPENDED


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(320, 329))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(190, 10, N_X * step, N_Y * step))
        self.label.setObjectName("label")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 168, 300))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.settingsLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.settingsLayout.setContentsMargins(0, 0, 0, 0)
        self.settingsLayout.setObjectName("settingsLayout")
        self.stats = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.stats.setObjectName("stats")
        self.stats.setColumnCount(2)
        self.stats.setRowCount(2)
        self.settingsLayout.addWidget(self.stats)
        self.settingsText = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.settingsText.setFont(font)
        self.settingsText.setObjectName("settingsText")
        self.settingsLayout.addWidget(self.settingsText)
        self.enemyLayout = QtWidgets.QHBoxLayout()
        self.enemyLayout.setObjectName("enemyLayout")
        self.countEnemyText = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.countEnemyText.setFont(font)
        self.countEnemyText.setObjectName("countEnemyText")
        self.enemyLayout.addWidget(self.countEnemyText)
        self.countEnemy = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.countEnemy.setProperty("value", 1)
        self.countEnemy.setObjectName("countEnemy")
        self.enemyLayout.addWidget(self.countEnemy)
        self.settingsLayout.addLayout(self.enemyLayout)
        self.fireLayout = QtWidgets.QHBoxLayout()
        self.fireLayout.setObjectName("fireLayout")
        self.countFireText = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.countFireText.setFont(font)
        self.countFireText.setObjectName("countFireText")
        self.fireLayout.addWidget(self.countFireText)
        self.countFire = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.countFire.sizePolicy().hasHeightForWidth())
        self.countFire.setSizePolicy(sizePolicy)
        self.countFire.setProperty("value", 1)
        self.countFire.setObjectName("countFire")
        self.fireLayout.addWidget(self.countFire)
        self.settingsLayout.addLayout(self.fireLayout)
        self.selectBGButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.selectBGButton.setFont(font)
        self.selectBGButton.setObjectName("selectBGButton")
        self.settingsLayout.addWidget(self.selectBGButton)
        self.button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.button.setFont(font)
        self.button.setObjectName("button")
        self.settingsLayout.addWidget(self.button)
        self.soundTextLayout = QtWidgets.QHBoxLayout()
        self.soundTextLayout.setObjectName("soundTextLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.soundTextLayout.addItem(spacerItem)
        self.soundText = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.soundText.setFont(font)
        self.soundText.setObjectName("soundText")
        self.soundTextLayout.addWidget(self.soundText)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.soundTextLayout.addItem(spacerItem1)
        self.settingsLayout.addLayout(self.soundTextLayout)
        self.soundBtnLayout = QtWidgets.QHBoxLayout()
        self.soundBtnLayout.setObjectName("soundBtnLayout")
        self.playBtn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.playBtn.setFont(font)
        self.playBtn.setObjectName("playBtn")
        self.soundBtnLayout.addWidget(self.playBtn)
        self.pauseBtn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pauseBtn.setFont(font)
        self.pauseBtn.setObjectName("pauseBtn")
        self.soundBtnLayout.addWidget(self.pauseBtn)
        self.stopBtn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.stopBtn.setFont(font)
        self.stopBtn.setObjectName("stopBtn")
        self.soundBtnLayout.addWidget(self.stopBtn)
        self.settingsLayout.addLayout(self.soundBtnLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.settingsText.setText(_translate("MainWindow", "Настройки"))
        self.countEnemyText.setText(_translate("MainWindow", "Кол-во врагов"))
        self.countFireText.setText(_translate("MainWindow", "Кол-во ловушек"))
        self.selectBGButton.setText(_translate("MainWindow", "Выбрать цвет фона"))
        self.button.setText(_translate("MainWindow", "Новая игра"))
        self.soundText.setText(_translate("MainWindow", "Звук"))
        self.playBtn.setText(_translate("MainWindow", "Играть"))
        self.pauseBtn.setText(_translate("MainWindow", "Пауза"))
        self.stopBtn.setText(_translate("MainWindow", "Стоп"))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.playlist = QMediaPlaylist()

        self.count = 0
        self.bg_rgb = (255, 255, 255)
        self.can_move = True
        self.player = None
        self.ext = None
        self.fires = []
        self.enemies = []
        self.setupUi(self)
        self.bg_music = QtMultimedia.QMediaPlayer()
        self.secondsound = QtMultimedia.QMediaPlayer()
        self.final = QtMultimedia.QMediaPlayer()
        self.load_second_mp3('bind_not_found_music.mp3.mp3')
        self.load_mp3('in-game_music.mp3')
        self.is_play = True
        canvas = QtGui.QPixmap(N_X * step, N_Y * step)
        canvas.fill(Qt.white)
        self.label.setPixmap(canvas)
        self.setFixedSize(N_X * step + 200 if (N_X * step + 200) > 320 else 320,
                          N_Y * step + 30 if (N_Y * step + 30) > 329 else 329)
        self.button.clicked.connect(self.prepare_and_start)
        self.selectBGButton.clicked.connect(self.setbgcolor)
        self.playBtn.clicked.connect(self.play)
        self.pauseBtn.clicked.connect(self.pause)
        self.stopBtn.clicked.connect(self.stop)
        self.bg_music.play()
        self.prepare_and_start()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.dance)
        self.timer.start(1320)

    def dance(self):
        global horizontal
        horizontal = not horizontal
        self.update()

    def play_steps(self):
        self.steps = QtMultimedia.QMediaPlayer()
        media = QtCore.QUrl.fromLocalFile('step_music.mp3')
        content = QtMultimedia.QMediaContent(media)
        self.steps.setMedia(content)
        self.steps.play()
        self.label.setFocus()

    def play(self):
        self.bg_music.play()
        self.label.setFocus()

    def play_final_music(self, win):
        if win:
            media = QtCore.QUrl.fromLocalFile('win_music.mp3')
        else:
            media = QtCore.QUrl.fromLocalFile('lose_music.mp3')
        content = QtMultimedia.QMediaContent(media)
        self.final.setMedia(content)
        self.stop()
        self.final.play()

    def stop_final_music(self):
        self.final.stop()

    def play_2(self):
        self.secondsound.play()
        self.label.setFocus()

    def pause(self):
        self.bg_music.pause()
        self.label.setFocus()

    def stop(self):
        self.bg_music.stop()
        self.label.setFocus()

    def load_second_mp3(self, filename):
        media = QtCore.QUrl.fromLocalFile(filename)
        content = QtMultimedia.QMediaContent(media)
        self.secondsound.setMedia(content)

    def load_mp3(self, filename):
        url = QUrl.fromLocalFile(filename)
        self.playlist.addMedia(QMediaContent(url))
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
        self.bg_music.setPlaylist(self.playlist)

    def setbgcolor(self):
        global bg_color
        self.load_second_mp3('mouse_click.mp3')
        self.play_2()
        color = QColorDialog.getColor()
        if color.isValid():
            self.bg_rgb = bg_color = color.getRgb()[:3]
            self.label.setFocus()

    def stats_update(self):
        con = sqlite3.connect("player_stats.sqlite")
        cur = con.cursor()
        query = cur.execute(f"""select * from stats""").fetchall()
        self.stats.setRowCount(len(query))
        self.stats.setColumnCount(len(query[0]))
        self.stats.setItem(0, 0, QTableWidgetItem(query[0][0]))
        self.stats.setItem(0, 1, QTableWidgetItem(str(query[0][1])))
        self.stats.setItem(1, 0, QTableWidgetItem(query[1][0]))
        self.stats.setItem(1, 1, QTableWidgetItem(str(query[1][1])))
        self.stats.resizeColumnsToContents()
        con.commit()

    def prepare_and_start(self):
        global gamemode
        self.stop_final_music()
        self.setWindowTitle('The Discapes')
        self.label.setFocus()
        self.count = 0
        n_fires = self.countFire.value()
        n_enemies = self.countEnemy.value()
        array.clear()
        gamemode = GameMode.PLAY
        self.can_move = True
        self.stats_update()
        self.stop()
        self.load_mp3('in-game_music.mp3')
        self.play()

        x, y = (random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step)
        player_pos = (x, y)
        array.append(player_pos)
        self.player = GameObject(player_pos[0], player_pos[1], Type.PLAYER)

        x, y = (random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step)
        while (x, y) in array:
            x, y = (random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step)
        array.append((x, y))
        exit_pos = (x, y)
        self.ext = GameObject(exit_pos[0], exit_pos[1], Type.EXIT)

        self.fires = []
        for i in range(n_fires):
            x, y = (random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step)
            while (x, y) in array:
                x, y = (random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step)
            array.append((x, y))
            fire_pos = (x, y)
            fire = GameObject(fire_pos[0], fire_pos[1], Type.FIRE)

            self.fires.append(fire)

        self.enemies = []
        for i in range(n_enemies):
            x, y = (random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step)
            while (x, y) in array:
                x, y = (random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step)
            array.append((x, y))
            enemy_pos = (x, y)
            enemy = Enemy(enemy_pos[0], enemy_pos[1], Type.ENEMY)

            self.enemies.append(enemy)

        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self.label.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor(*self.bg_rgb))  # r, g, b
        painter.setPen(pen)
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(*self.bg_rgb))  # r, g, b
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        painter.setBrush(brush)
        painter.begin(self)
        painter.drawRect(0, 0, N_X * step, N_Y * step)

        self.player.draw(painter)
        self.ext.draw(painter)
        for fire in self.fires:
            fire.draw(painter)
        for enemy in self.enemies:
            enemy.draw(painter)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R:
            self.prepare_and_start()
        if event.key() == Qt.Key_Space:
            self.play() if self.is_play else self.pause()
            self.is_play = not self.is_play
        elif self.can_move:
            if event.key() == Qt.Key_P:
                bind = True
                self.count = 6
            elif event.key() == Qt.Key_Up:
                self.play_steps()
                bind = True
                self.player.move_wrap(mx=0, my=-step)
            elif event.key() == Qt.Key_Down:
                self.play_steps()
                bind = True
                self.player.move_wrap(mx=0, my=step)
            elif event.key() == Qt.Key_Left:
                self.play_steps()
                bind = True
                self.player.move_wrap(mx=-step, my=0)
            elif event.key() == Qt.Key_Right:
                self.play_steps()
                bind = True
                self.player.move_wrap(mx=step, my=0)
            else:
                self.load_second_mp3('bind_not_found_music.mp3')
                self.play_2()
                bind = False
            if bind:
                if self.count > 0:
                    self.count -= 1
                else:
                    for enemy in self.enemies:
                        direction = enemy.persuit(self.player)  # вызвать функцию перемещения у "врага"
                        enemy.move_wrap(*direction)  # произвести  перемещение
                self.update()
                self.check_move()
        else:
            self.load_second_mp3('bind_not_found_music.mp3')
            self.play_2()

    def check_move(self):
        global gamemode
        con = sqlite3.connect("player_stats.sqlite")
        cur = con.cursor()
        if self.player == self.ext:
            self.play_final_music(True)
            self.setWindowTitle('Победа!')
            self.query = cur.execute(f"""update stats set stats = stats + 1 where title = 'Кол-во побед'
            """).fetchall()
            gamemode = GameMode.WIN
            self.can_move = False
        else:
            changes = False
            for f in self.fires:
                if self.player == f:
                    self.play_final_music(False)
                    self.query = cur.execute(
                        f"""update stats set stats = stats + 1 where title = 'Кол-во поражений'""").fetchall()
                    gamemode = GameMode.LOSEFIRE
                    self.can_move = False
                    changes = True
                    break
            if not changes:
                for e in self.enemies:
                    if self.player == e:
                        self.play_final_music(False)
                        self.setWindowTitle("Поражение!")
                        self.query = cur.execute(f"""update stats set stats = stats + 1 where title =
                         'Кол-во поражений'""").fetchall()
                        gamemode = GameMode.LOSEENEMY
                        self.can_move = False
                        break
        con.commit()
        self.stats_update()


class GameObject:
    def __init__(self, x, y, type):
        self.desk = [[None for _ in range(N_X)] for _ in range(N_Y)]  # поле
        self.x = x
        self.y = y
        self.type = type

    def __repr__(self):
        return f'{self.type}, {self.x}, {self.y}'

    def placeObject(self):
        self.desk[self.x][self.y] = (self.x, self.y, self.type)

    def draw(self, painter):
        tmp = QtGui.QPixmap(self.path()).scaled(QtCore.QSize(step, step),
                                                aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                transformMode=QtCore.Qt.TransformationMode.FastTransformation)
        if gamemode != gamemode.PLAY:
            tmppen = QtGui.QPen()
            tmppen.setWidth(1)
            tmppen.setColor(QtGui.QColor(*bg_color))  # r, g, b
            painter.setPen(tmppen)
            tmpbrush = QtGui.QBrush()
            tmpbrush.setColor(QtGui.QColor(*bg_color))  # r, g, b
            tmpbrush.setStyle(Qt.BrushStyle.SolidPattern)
            painter.setBrush(tmpbrush)
            painter.drawRect(QRect(self.x, self.y, step, step))
        if horizontal:  # horizontal
            if self.type == Type.PLAYER:
                tmp = tmp.transformed(QTransform().scale(-1, 1))
            painter.drawPixmap(QRect(self.x, self.y, step, step), tmp, QRect(0, 0, step, step))
        else:  # vertical
            painter.drawPixmap(QRect(self.x, self.y, step, step), tmp, QRect(0, 0, step, step))

    def path(self):
        global gamemode
        if self.type == Type.PLAYER:
            return 'player.svg'
        elif self.type == Type.ENEMY:
            return 'enemy.svg'
        elif self.type == Type.FIRE:
            return 'trap_on.svg' if gamemode == GameMode.LOSEFIRE else 'trap_off.svg'
        elif self.type == Type.EXIT:
            return 'exit_open.svg' if gamemode == GameMode.PLAY else 'exit_closed.svg'

    def color(self):
        if self.type == Type.PLAYER:
            return 0, 255, 0  # green
        elif self.type == Type.ENEMY:
            return 255, 0, 0  # red
        elif self.type == Type.FIRE:
            return 255, 165, 0  # orange
        elif self.type == Type.EXIT:
            return 255, 255, 0  # yellow

    def move_wrap(self, mx, my):
        outofbounds = False

        self.x += mx
        self.y += my
        if self.x < 0:
            mx = step * N_X
            outofbounds = True
        if self.x > step * N_X - N_X:
            mx = -step * N_X
            outofbounds = True
        if self.y < 0:
            my = step * N_Y
            outofbounds = True
        if self.y > step * N_Y - N_Y:
            my = -(step * N_Y)
            outofbounds = True
        if outofbounds:
            self.x += mx
            self.y += my

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Enemy(GameObject):
    def __init__(self, x, y, type):
        super().__init__(x, y, type)
        self.direction = Direction.LEFT

    def persuit(self, player):
        x1, y1, x2, y2 = (self.x, self.y, player.x, player.y)
        if x1 >= x2:
            self.direction = Direction.LEFT
        else:
            self.direction = Direction.RIGHT
        if abs(x1 - x2) > abs(y1 - y2):
            if x1 >= x2:
                return -step, 0
            if x2 > x1:
                return step, 0
        else:
            if y1 >= y2:
                return 0, -step
            if y2 > y1:
                return 0, step

    def draw(self, painter):
        tmp = QtGui.QPixmap(self.path()).scaled(QtCore.QSize(step, step),
                                                aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                transformMode=QtCore.Qt.TransformationMode.FastTransformation)
        if gamemode != gamemode.PLAY:
            tmppen = QtGui.QPen()
            tmppen.setWidth(1)
            tmppen.setColor(QtGui.QColor(*bg_color))  # r, g, b
            painter.setPen(tmppen)
            tmpbrush = QtGui.QBrush()
            tmpbrush.setColor(QtGui.QColor(*bg_color))  # r, g, b
            tmpbrush.setStyle(Qt.BrushStyle.SolidPattern)
            painter.setBrush(tmpbrush)
            painter.drawRect(QRect(self.x, self.y, step, step))
        if horizontal:  # horizontal
            tmp = tmp.transformed(QTransform().scale(self.direction.value, 1))
            painter.drawPixmap(QRect(self.x, self.y, step, step), tmp, QRect(0, 0, step, step))

        else:  # vertical
            tmp = tmp.transformed(QTransform().scale(self.direction.value, 1))
            painter.drawPixmap(QRect(self.x, self.y, step, step), tmp, QRect(0, 0, step, step))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
