import os
import random

from PyQt5.QtCore import Qt, QDir
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton

from HealthyWork.config import Config
from HealthyWork.utils import is_img


class Mask(QWidget):
    def __init__(self, parent, screen, primary=False):
        super().__init__()
        self.parent = parent
        self.primary = primary
        self.setGeometry(screen.geometry())
        self.init_ui()

    def init_ui(self):
        # TODO
        # set a window icon
        # self.setWindowIcon(QIcon('./icon.png'))
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.label_background = QLabel(self)

        if not self.primary:
            return

        self.button = QPushButton(self)
        self.button.setText('BACK TO WORK')
        self.button.setStyleSheet(Config.BUTTON_STYLESHEET)
        self.button.resize(self.button.sizeHint())
        self.set_position(self.button, Label='Message')
        self.button.clicked.connect(self.parent.start_work)
        self.button.hide()
        self.label_message = QLabel(self)
        self.label_count = QLabel(self)
        self.label_message.setText(Config.MESSAGE)
        self.label_count.setText(" " * 16)
        self.label_message.setStyleSheet(Config.LABEL_STYLESHEET)
        self.label_count.setStyleSheet(Config.LABEL_STYLESHEET)
        self.label_message.resize(self.label_message.sizeHint())
        self.label_count.resize(self.label_count.sizeHint())
        self.set_position(self.label_message, Label='Message')
        self.set_position(self.label_count, Label='Count')

    def set_position(self, label, **kwargs):

        def position(widget):
            # 计算label显示位置
            window_size = QApplication.desktop().screenGeometry()
            x = (window_size.width() - widget.width()) // 2
            y = (window_size.height() - widget.height()) // 2
            return x, y, widget.width(), widget.height()

        pos = position(label)

        if kwargs['Label'] == 'Message':
            label.setGeometry(pos[0], pos[1], pos[2], pos[3])
        else:
            label.setGeometry(pos[0], pos[1] + 80, pos[2], pos[3])

    def show_background_picture(self):
        """
        随机展示一张壁纸
        :return:
        """
        self.showFullScreen()
        window_size = QApplication.desktop().screenGeometry()
        self.label_background.setGeometry(0, 0, window_size.width(), window_size.height())

        if not os.path.exists(Config.DIR_WALLPAPER):
            return

        if os.path.isdir(Config.DIR_WALLPAPER):
            if not os.listdir(Config.DIR_WALLPAPER):
                return

            wallpapers = [os.path.join(Config.DIR_WALLPAPER, wallpaper) for wallpaper in
                          os.listdir(Config.DIR_WALLPAPER)
                          if is_img(os.path.join(Config.DIR_WALLPAPER, wallpaper))]

            if not wallpapers:
                return

            wallpaper = random.choice(wallpapers)

        else:
            if not is_img(Config.DIR_WALLPAPER):
                return
            wallpaper = Config.DIR_WALLPAPER

        try:
            self.label_background.setPixmap(QPixmap(QDir.absolutePath(QDir(wallpaper)))
                                            .scaled(window_size.width(), window_size.height()))
        # noinspection PyBroadException
        except Exception as e:
            print(e)

        if not self.primary:
            return

        self.label_message.show()
        self.label_count.show()

    def count_down(self):
        if not self.primary:
            return

        def format_time(millisecond):
            m, s = divmod(millisecond / 1000, 60)
            h, m = divmod(m, 60)
            return h, m, s

        self.label_count.setText("%02d:%02d:%02d" % format_time(self.parent.rest_time - 1000))
        self.parent.rest_time = self.parent.rest_time - 1000

    def show_button(self):
        if not self.primary:
            return

        self.parent.timer_rest.stop()
        self.parent.timer_count.stop()
        self.label_count.hide()
        self.label_message.hide()
        self.button.show()
