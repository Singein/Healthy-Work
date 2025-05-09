import os
import random

from PyQt5.QtCore import QTimer, QUrl, QDir
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu, QAction, QMessageBox

from HealthyWork.config import Config
from HealthyWork.mask import Mask
from HealthyWork.settings import SettingsWindow
from HealthyWork.utils import is_song


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.rest_time = int(Config.TIME_REST * 60 * 1000)
        self.work_time = int(Config.TIME_WORK * 60 * 1000)
        self.masks = []
        self.init_ui()
        
    def init_ui(self):
        # 初始化遮罩窗口
        primary_screen = QApplication.primaryScreen()
        for screen in QApplication.screens():
            if screen is primary_screen:
                self.masks.append(Mask(self, screen, primary=True))
            else:
                self.masks.append(Mask(self, screen, primary=False))
        
        # 初始化系统托盘
        self.init_tray_icon()
        
        # 初始化计时器
        self.start()

    def init_tray_icon(self):
        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("app.ico"))  # 设置托盘图标
        self.tray_icon.setToolTip("HealthyWork - 保护你的健康")
        
        # 创建托盘菜单
        tray_menu = QMenu()
        
        # 添加打开设置动作
        self.settings_action = QAction("设置", self)
        self.settings_action.triggered.connect(self.open_settings)
        tray_menu.addAction(self.settings_action)
        
        # 添加退出动作
        self.quit_action = QAction("退出", self)
        self.quit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(self.quit_action)
        
        # 设置托盘菜单
        self.tray_icon.setContextMenu(tray_menu)
        
        # 连接点击事件
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        
        # 显示托盘图标
        self.tray_icon.show()

        self.settings_window = SettingsWindow(self)

    def on_tray_icon_activated(self, reason):
        # 点击托盘图标打开设置窗口
        if reason == QSystemTrayIcon.Trigger:
            self.open_settings()

    def open_settings(self):
        # 创建并显示设置窗口
        self.settings_window.show()

    def quit_application(self):
        # 确认退出
        reply = QMessageBox.question(
            self, '确认退出', '确定要退出 HealthyWork 吗？',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.tray_icon.hide()  # 隐藏托盘图标
            QApplication.quit()  # 退出应用

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
