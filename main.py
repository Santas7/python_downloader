
import math
import os
import sys

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QGridLayout, QLineEdit, \
    QVBoxLayout, QTextEdit, QProgressBar
from PyQt6 import QtGui, QtWidgets, QtCore
import datetime
from pytube import YouTube
import tag

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # параметры окна MainWindow
        self.setWindowTitle("AppDownloader")
        self.setFixedSize(QSize(400, 180))
        self.label = QLabel("", self)
        font = QtGui.QFont()
        font.setFamily('CeraPro-Bold')  # сам шрифт
        font.setPointSize(14)  # размер шрифта
        self.video_saving_path = QFileDialog.getExistingDirectory(self, 'Укажите папку сохранения видео ряда: ')

        # поле ввода
        self.input = QLineEdit('', self)
        self.input.move(10, 10)
        self.input.setFixedSize(QSize(380, 50))
        self.input.setFont(font)

        # кнопки
        self.play = QPushButton("СКАЧАТЬ ВИДЕО", self)
        self.play.setFixedSize(QSize(380, 50))
        self.play.move(10, 60)
        self.play.setFont(font)
        self.play.setStyleSheet("background-color : #FFA07A")

        self.exit = QPushButton("ВЫЙТИ", self)
        self.exit.setFixedSize(QSize(380, 50))
        self.exit.move(10, 110)
        self.exit.setFont(font)
        self.exit.setStyleSheet("background-color : #FFA07A")

        # события на кнопки
        self.play.clicked.connect(self.go_to_play)
        self.exit.clicked.connect(self.go_to_exit)
        self.show()

    def go_to_play(self):
        yt = YouTube(f'{self.input.text()}')  # ссылка на видео.
        # yt.stream показывает какое видео ты можешь скачать
        # (mp4(720) + audio или только mp4(1080) без звука).
        # Сейчас стоит фильтр по mp4.
        streams = yt.streams.filter(file_extension='mp4')
        new_window = Vubor(streams)
        new_window.exec()
        stream = yt.streams.get_by_itag(tag.N)
        stream.download(self.video_saving_path)
        self.close()

        #stream = yt.streams.get_by_itag(22)  # выбираем по тегу, в каком формате будем скачивать.
       # stream.download()  # загружаем видео.

    def go_to_exit(self):
        self.close()


class Vubor(QtWidgets.QDialog):
    def __init__(self, streams):
        super().__init__()

        self.setWindowTitle("Выбор")
        self.setFixedSize(QSize(400, 300))
        self.label = QLabel("", self)
        font = QtGui.QFont()
        font.setFamily('CeraPro-Bold')  # сам шрифт
        font.setPointSize(14)  # размер шрифта

        self.history = QTextEdit('', self)
        self.history.setFixedSize(QSize(380, 150))
        self.history.move(10, 10)
        self.history.setFont(font)

        # поле ввода
        self.input = QLineEdit('', self)
        self.input.move(10, 160)
        self.input.setFixedSize(QSize(380, 50))
        self.input.setFont(font)

        self.enter = QPushButton("ВВОД (iTag)", self)
        self.enter.setFixedSize(QSize(380, 50))
        self.enter.move(10, 220)
        self.enter.setFont(font)
        self.enter.setStyleSheet("background-color : #FFA07A")
        self.enter.clicked.connect(self.clk)
        self.streams = streams

        for i in range(len(streams)):
            self.history.insertPlainText(f"{streams[i]}\n")

        self.show()

    def clk(self):
        file = open('tag.py', 'w')
        file.write(f"N = {self.input.text()}\n")
        file.close()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    app.exec()