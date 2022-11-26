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
        self.font = QtGui.QFont()
        self.font.setFamily('CeraPro-Bold')  # сам шрифт
        self.font.setPointSize(14)  # размер шрифта
        self.video_saving_path = QFileDialog.getExistingDirectory(self, 'Укажите папку сохранения видео ряда: ')

        # поле ввода
        self.input = QLineEdit('', self)
        self.input.move(10, 10)
        self.input.setFixedSize(QSize(380, 50))
        self.input.setFont(self.font)

        # кнопки
        self.play = self.add_button("СКАЧАТЬ ВИДЕО", 380, 50, 10, 60)
        self.exit = self.add_button("ВЫЙТИ", 380, 50, 10, 110)

        # события на кнопки
        self.play.clicked.connect(self.go_to_play)
        self.exit.clicked.connect(self.go_to_exit)
        self.show()

    def add_button(self, text: str, size_x: int, size_y: int, pos_x: int, pos_y: int):
        button = QPushButton(f"{text}", self)
        button.setFixedSize(QSize(size_x, size_y))
        button.move(pos_x, pos_y)
        button.setFont(self.font)
        button.setStyleSheet("background-color : #FFA07A")
        return button

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

    def go_to_exit(self):
        self.close()


class Vubor(QtWidgets.QDialog):
    def __init__(self, streams):
        super().__init__()

        self.setWindowTitle("Выбор")
        self.setFixedSize(QSize(400, 300))
        self.label = QLabel("", self)
        self.font = QtGui.QFont()
        self.font.setFamily('CeraPro-Bold')  # сам шрифт
        self.font.setPointSize(14)  # размер шрифта

        self.history = QTextEdit('', self)
        self.history.setFixedSize(QSize(380, 150))
        self.history.move(10, 10)
        self.history.setFont(self.font)

        # поле ввода
        self.input = QLineEdit('', self)
        self.input.move(10, 160)
        self.input.setFixedSize(QSize(380, 50))
        self.input.setFont(self.font)

        self.enter = self.add_button("ВВОД (iTag)", 380, 50, 10, 220)
        self.enter.clicked.connect(self.clk)
        self.streams = streams

        for i in range(len(streams)):
            self.history.insertPlainText(f"{streams[i]}\n")

        self.show()

    def add_button(self, text: str, size_x: int, size_y: int, pos_x: int, pos_y: int):
        button = QPushButton(f"{text}", self)
        button.setFixedSize(QSize(size_x, size_y))
        button.move(pos_x, pos_y)
        button.setFont(self.font)
        button.setStyleSheet("background-color : #FFA07A")
        return button

    def clk(self):
        file = open('tag.py', 'w')
        file.write(f"N = {self.input.text()}\n")
        file.close()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
