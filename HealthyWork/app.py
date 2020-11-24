import os
import random

from PyQt5.QtCore import QTimer, QUrl, QDir
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication, QWidget

from HealthyWork.config import Config
from HealthyWork.mask import Mask
from HealthyWork.utils import is_song


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.rest_time = int(Config.TIME_REST * 60 * 1000)
        self.work_time = int(Config.TIME_WORK * 60 * 1000)
        self.masks = []
        primary_screen = QApplication.primaryScreen()

        for screen in QApplication.screens():
            if screen is primary_screen:
                self.masks.append(Mask(self, screen, primary=True))
            else:
                self.masks.append(Mask(self, screen, primary=False))

    def start(self):
        self.player = QMediaPlayer(self)
        self.rest_time = int(Config.TIME_REST * 60 * 1000)
        self.timer_work = QTimer()
        self.timer_rest = QTimer()
        self.timer_count = QTimer()
        self.timer_work.timeout.connect(self.start_rest)

        for mask in self.masks:
            self.timer_rest.timeout.connect(mask.show_button)
            self.timer_count.timeout.connect(mask.count_down)

        self.timer_work.start(self.work_time)

    def start_rest(self):
        self.play_music()
        for mask in self.masks:
            mask.show_background_picture()

        self.timer_work.stop()
        self.timer_rest.start(self.rest_time)
        self.timer_count.start(1000)

    def start_work(self):
        for mask in self.masks:
            if mask.primary:
                mask.button.hide()
            mask.hide()

        self.timer_work.start(self.work_time)
        self.rest_time = int(Config.TIME_REST * 60 * 1000)
        self.player.stop()

    def play_music(self):
        if not Config.PLAY_MUSIC:
            return

        if not os.path.exists(Config.DIR_MUSIC):
            return

        if os.path.isdir(Config.DIR_MUSIC):
            if not os.listdir(Config.DIR_MUSIC):
                return

            songs = [os.path.join(Config.DIR_MUSIC, song) for song in os.listdir(Config.DIR_MUSIC) if
                     is_song(os.path.join(Config.DIR_MUSIC, song))]
            if not songs:
                return

            song = random.choice(songs)
        else:
            if not is_song(Config.DIR_MUSIC):
                return

            song = Config.DIR_MUSIC

        try:
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(QDir.absolutePath(QDir(song)))))
        # noinspection PyBroadException
        except Exception as e:
            print(e)

        self.player.play()
