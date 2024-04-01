from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal
from queue import Queue
from multiprocessing import Process
from threading import Thread
import tkinter as tk
from time import sleep
from Olimp import futball, bascet, tennis, fb, ft, bt, fbt
from Pinacle import pin_futball
from threading import Thread
from multiprocessing import Process, Queue
from match import obrbotka
import pandas as pd

class Worker(QThread):
    data_ready = pyqtSignal(object)

    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        while True:
            if not self.queue.empty():
                df = self.queue.get()
                self.data_ready.emit(df)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Бот")
        self.setGeometry(0, 0, 500, 400)

        self.label_itog = QLabel("Ожидание данных...")
        self.label1 = QLabel("Выберите тип игры: \n f - футбол \n t - тенис \n b - баскетбол \n ft - футбол и теннис \n fb - футбол и баскетбол \n bt - баскетбол и теннис \n fbt - футбол, баскетбол, тенис ")
        self.entry = QLineEdit()
        self.label8 = QLabel("Введите % максимальной прибыльно ставки")
        self.entry1 = QLineEdit()
        self.button = QPushButton("Начать", clicked=self.counter)

        layout = QVBoxLayout()
        layout.addWidget(self.label_itog)
        layout.addWidget(self.label1)
        layout.addWidget(self.entry)
        layout.addWidget(self.label8)
        layout.addWidget(self.entry1)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.travel = Queue()
        self.queue = Queue()

        self.worker = Worker(self.queue)
        self.worker.data_ready.connect(self.update_gui)
        self.worker.start()

    def counter(self):
        vibor = str(self.entry.text())
        prochent = float(self.entry1.text())

        if vibor == "f":
            t1 = Thread(target=futball, args=(self.travel,))
            t1.start()
            t7 = Process(target=obrbotka, args=(self.travel, prochent, self.queue,))
            t7.start()
            t8 = Process(target=pin_futball, args=(self.travel,))
            t8.start()
        elif vibor == "t":
            t1 = Thread(target=tennis, args=(self.travel,))
            t1.start()
            t7 = Process(target=obrbotka, args=(self.travel, prochent, self.queue,))
            t7.start()
        elif vibor == "b":
            t1 = Thread(target=bascet, args=(self.travel,))
            t1.start()
            t7 = Process(target=obrbotka, args=(self.travel, prochent, self.queue,))
            t7.start()
        elif vibor == "ft":
            t1 = Thread(target=ft, args=(self.travel,))
            t1.start()
            t7 = Process(target=obrbotka, args=(self.travel, prochent, self.queue,))
            t7.start()
        elif vibor == "fb":
            t1 = Thread(target=fb, args=(self.travel,))
            t1.start()
            t7 = Process(target=obrbotka, args=(self.travel, prochent, self.queue,))
            t7.start()
        elif vibor == "bt":
            t1 = Thread(target=bt, args=(self.travel,))
            t1.start()
            t7 = Process(target=obrbotka, args=(self.travel, prochent, self.queue,))
            t7.start()
        elif vibor == "fbt":
            t1 = Thread(target=fbt, args=(self.travel,))
            t1.start()
            t7 = Process(target=obrbotka, args=(self.travel, prochent, self.queue,))
            t7.start()

    def update_gui(self, df):
        self.label_itog.setText(str(df))

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
