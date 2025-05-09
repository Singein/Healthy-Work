# import os
# import random
#
# from PyQt5.QtCore import Qt, QDir
# from PyQt5.QtGui import QPixmap, QCloseEvent
# from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
#
# from HealthyWork.config import Config
# from HealthyWork.utils import is_img
#
#
# class Mask(QWidget):
#     def __init__(self, parent, screen, primary=False):
#         super().__init__()
#         self.parent = parent
#         self.primary = primary
#         self.setGeometry(screen.geometry())
#         self.init_ui()
#
#     def init_ui(self):
#         # TODO
#         # set a window icon
#         # self.setWindowIcon(QIcon('./icon.png'))
#         self.setAttribute(Qt.WA_TranslucentBackground)
#         self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
#         self.label_background = QLabel(self)
#
#         if not self.primary:
#             return
#
#         self.button = QPushButton(self)
#         self.button.setText('BACK TO WORK')
#         self.button.setStyleSheet(Config.BUTTON_STYLESHEET)
#         self.button.resize(self.button.sizeHint())
#         self.set_position(self.button, Label='Message')
#         self.button.clicked.connect(self.parent.start_work)
#         self.button.hide()
#         self.label_message = QLabel(self)
#         self.label_count = QLabel(self)
#         self.label_message.setText(Config.MESSAGE)
#         self.label_count.setText(" " * 16)
#         self.label_message.setStyleSheet(Config.LABEL_STYLESHEET)
#         self.label_count.setStyleSheet(Config.LABEL_STYLESHEET)
#         self.label_message.resize(self.label_message.sizeHint())
#         self.label_count.resize(self.label_count.sizeHint())
#         self.set_position(self.label_message, Label='Message')
#         self.set_position(self.label_count, Label='Count')
#
#     def set_position(self, label, **kwargs):
#
#         def position(widget):
#             # 计算label显示位置
#             window_size = QApplication.desktop().screenGeometry()
#             x = (window_size.width() - widget.width()) // 2
#             y = (window_size.height() - widget.height()) // 2
#             return x, y, widget.width(), widget.height()
#
#         pos = position(label)
#
#         if kwargs['Label'] == 'Message':
#             label.setGeometry(pos[0], pos[1], pos[2], pos[3])
#         else:
#             label.setGeometry(pos[0], pos[1] + 80, pos[2], pos[3])
#
#     def show_background_picture(self):
#         """
#         随机展示一张壁纸
#         :return:
#         """
#         self.showFullScreen()
#         window_size = QApplication.desktop().screenGeometry()
#         self.label_background.setGeometry(0, 0, window_size.width(), window_size.height())
#
#         if not os.path.exists(Config.DIR_WALLPAPER):
#             return
#
#         if os.path.isdir(Config.DIR_WALLPAPER):
#             if not os.listdir(Config.DIR_WALLPAPER):
#                 return
#
#             wallpapers = [os.path.join(Config.DIR_WALLPAPER, wallpaper) for wallpaper in
#                           os.listdir(Config.DIR_WALLPAPER)
#                           if is_img(os.path.join(Config.DIR_WALLPAPER, wallpaper))]
#
#             if not wallpapers:
#                 return
#
#             wallpaper = random.choice(wallpapers)
#
#         else:
#             if not is_img(Config.DIR_WALLPAPER):
#                 return
#             wallpaper = Config.DIR_WALLPAPER
#
#         try:
#             self.label_background.setPixmap(QPixmap(QDir.absolutePath(QDir(wallpaper)))
#                                             .scaled(window_size.width(), window_size.height()))
#         # noinspection PyBroadException
#         except Exception as e:
#             print(e)
#
#         if not self.primary:
#             return
#
#         self.label_message.show()
#         self.label_count.show()
#
#     def count_down(self):
#         if not self.primary:
#             return
#
#         def format_time(millisecond):
#             m, s = divmod(millisecond / 1000, 60)
#             h, m = divmod(m, 60)
#             return h, m, s
#
#         self.label_count.setText("%02d:%02d:%02d" % format_time(self.parent.rest_time - 1000))
#         self.parent.rest_time = self.parent.rest_time - 1000
#
#     def show_button(self):
#         if not self.primary:
#             return
#
#         self.parent.timer_rest.stop()
#         self.parent.timer_count.stop()
#         self.label_count.hide()
#         self.label_message.hide()
#         self.button.show()
#
#     def closeEvent(self, event: QCloseEvent):
#         # 忽略关闭事件，防止窗口被关闭
#         event.ignore()
#
#     def keyPressEvent(self, event):
#         # 忽略空格键事件，防止触发按钮
#         if event.key() == Qt.Key_Space:
#             event.ignore()
#         else:
#             super().keyPressEvent(event)

import os
import random
import sys
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint, QUrl
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QPainterPath, QFont, QCloseEvent
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGraphicsOpacityEffect

from HealthyWork.config import Config
from HealthyWork.utils import is_img


class Mask(QWidget):
    def __init__(self, parent, screen, primary=False):
        super().__init__()
        self.parent = parent
        self.primary = primary
        self.setGeometry(screen.geometry())

        # 粒子系统
        self.particles = []
        self.max_particles = 30
        self.init_particles()

        # 音频可视化数据
        self.audio_levels = []
        self.max_levels = 50

        # 动画效果
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setDuration(1000)
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setEasingCurve(QEasingCurve.InOutQuad)

        self.fade_out_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_out_animation.setDuration(1000)
        self.fade_out_animation.setStartValue(1.0)
        self.fade_out_animation.setEndValue(0.0)
        self.fade_out_animation.finished.connect(self.hide)

        # 按钮悬停动画
        self.button_effect = QGraphicsOpacityEffect()

        # 计时器
        self.particle_timer = QTimer()
        self.particle_timer.timeout.connect(self.update_particles)
        self.particle_timer.start(30)

        self.audio_timer = QTimer()
        self.audio_timer.timeout.connect(self.update_audio_visualization)
        self.audio_timer.start(100)

        self.init_ui()

    def init_ui(self):
        # 设置窗口属性
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)

        # 背景标签
        self.label_background = QLabel(self)
        self.label_background.setAlignment(Qt.AlignCenter)

        # 毛玻璃效果（半透明背景）
        self.blur_overlay = QLabel(self)
        self.blur_overlay.setGeometry(0, 0, self.width(), self.height())
        self.blur_overlay.setStyleSheet(f"background-color: rgba(255, 255, 255, 100);")

        if not self.primary:
            return

        # 消息标签
        self.label_message = QLabel(self)
        self.label_message.setText(Config.MESSAGE)
        self.label_message.setStyleSheet(Config.LABEL_STYLESHEET)
        self.label_message.setAlignment(Qt.AlignCenter)

        # 倒计时标签
        self.label_count = QLabel(self)
        self.label_count.setText(" " * 16)
        self.label_count.setStyleSheet(Config.LABEL_STYLESHEET)
        self.label_count.setAlignment(Qt.AlignCenter)

        # 返回工作按钮
        self.button = QPushButton(self)
        self.button.setText('BACK TO WORK')
        self.button.setStyleSheet("""
            QPushButton {
                background-color: rgba(182, 176, 171, 90);
                color: rgb(255, 0, 127);
                font: 30pt "WenQuanYi Micro Hei Mono";
                border-radius: 15px;
                padding: 10px 20px;
                transition: all 0.3s;
                border: 2px solid rgba(255, 255, 255, 50);
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 220);
                color: rgb(255, 50, 150);
                transform: scale(1.05);
                border: 2px solid rgba(255, 50, 150, 80);
                box-shadow: 0 0 20px rgba(255, 50, 150, 50);
            }
            QPushButton:pressed {
                transform: scale(0.95);
            }
        """)
        self.button.setGraphicsEffect(self.button_effect)
        self.button.clicked.connect(self.parent.start_work)
        self.button.hide()

        # 布局控件
        self.resize_widgets()

    def back_to_work(self):
        if self.primary:
            self.button.hide()
            self.label_message.hide()
            self.label_count.hide()

        self.hide()

    def resize_widgets(self):
        # 调整控件大小和位置
        window_size = self.geometry()

        # 背景和毛玻璃覆盖层
        self.label_background.setGeometry(0, 0, window_size.width(), window_size.height())
        self.blur_overlay.setGeometry(0, 0, window_size.width(), window_size.height())

        if not self.primary:
            return

        # 计算垂直居中位置
        center_y = window_size.height() // 2

        # 消息标签位置
        self.label_message.resize(self.label_message.sizeHint())
        message_y = center_y - 100
        self.label_message.move(
            (window_size.width() - self.label_message.width()) // 2,
            message_y
        )

        # 倒计时标签位置
        self.label_count.resize(self.label_count.sizeHint())
        count_y = center_y
        self.label_count.move(
            (window_size.width() - self.label_count.width()) // 2,
            count_y
        )

        # 按钮位置
        self.button.resize(self.button.sizeHint())
        button_y = center_y + 100
        self.button.move(
            (window_size.width() - self.button.width()) // 2,
            button_y
        )

    def resizeEvent(self, event):
        # 窗口大小改变时重新布局
        self.resize_widgets()
        super().resizeEvent(event)

    def init_particles(self):
        # 初始化粒子系统
        for _ in range(self.max_particles):
            x = random.randint(0, self.width())
            y = random.randint(0, self.height())
            speed_x = random.randint(-1, 1)
            speed_y = random.randint(-1, 1)
            size = random.randint(2, 5)
            alpha = random.randint(100, 200)
            self.particles.append({
                'pos': QPoint(x, y),
                'speed': QPoint(speed_x, speed_y),
                'size': size,
                'color': QColor(255, 255, 255, alpha)
            })

    def update_particles(self):
        # 更新粒子位置
        for particle in self.particles:
            particle['pos'] += particle['speed']

            # 边界检测
            if particle['pos'].x() < 0 or particle['pos'].x() > self.width():
                particle['speed'].setX(-particle['speed'].x())
            if particle['pos'].y() < 0 or particle['pos'].y() > self.height():
                particle['speed'].setY(-particle['speed'].y())

        self.update()  # 重绘窗口

    def update_audio_visualization(self):
        # 更新音频可视化数据
        if self.parent.player.state() == QMediaPlayer.PlayingState:
            level = random.uniform(0.1, 1.0)  # 模拟音频级别
        else:
            level = 0.0

        self.audio_levels.append(level)
        if len(self.audio_levels) > self.max_levels:
            self.audio_levels.pop(0)

        self.update()  # 重绘窗口

    def paintEvent(self, event):
        # 绘制粒子和音频可视化
        super().paintEvent(event)

        if not self.primary:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制粒子
        for particle in self.particles:
            painter.setPen(QPen(particle['color'], particle['size']))
            painter.drawPoint(particle['pos'])

        # 绘制音频波形
        if self.audio_levels:
            width = self.width()
            height = self.height()
            bar_width = width / self.max_levels
            max_bar_height = height * 0.1  # 波形高度占窗口的10%

            for i, level in enumerate(self.audio_levels):
                bar_height = level * max_bar_height
                x = i * bar_width
                y = height - bar_height - 20  # 底部留出20px边距

                # 渐变颜色
                hue = 280 - level * 100  # 从紫色到粉色
                color = QColor.fromHsv(int(hue), 255, 255, 180)

                # 绘制音频条
                path = QPainterPath()
                path.addRoundedRect(x, y, bar_width - 1, bar_height, 2, 2)
                painter.fillPath(path, color)

    def keyPressEvent(self, event):
        event.ignore()

    def closeEvent(self, event: QCloseEvent):
        # 忽略关闭事件，防止窗口被关闭
        event.ignore()

    def show_background_picture(self):
        """随机展示一张壁纸"""
        self.setWindowOpacity(0.0)
        self.showFullScreen()

        if not os.path.exists(Config.DIR_WALLPAPER):
            self.fade_in_animation.start()
            return

        if os.path.isdir(Config.DIR_WALLPAPER):
            if not os.listdir(Config.DIR_WALLPAPER):
                self.fade_in_animation.start()
                return

            wallpapers = [os.path.join(Config.DIR_WALLPAPER, wallpaper) for wallpaper in
                          os.listdir(Config.DIR_WALLPAPER)
                          if is_img(os.path.join(Config.DIR_WALLPAPER, wallpaper))]

            if not wallpapers:
                self.fade_in_animation.start()
                return

            wallpaper = random.choice(wallpapers)

        else:
            if not is_img(Config.DIR_WALLPAPER):
                self.fade_in_animation.start()
                return
            wallpaper = Config.DIR_WALLPAPER

        try:
            self.label_background.setPixmap(QPixmap(wallpaper).scaled(
                self.width(), self.height(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            ))
        except Exception as e:
            print(f"Error loading wallpaper: {e}")

        if not self.primary:
            self.fade_in_animation.start()
            return

        self.label_message.show()
        self.label_count.show()
        self.fade_in_animation.start()

    def count_down(self):
        """更新倒计时显示"""
        if not self.primary:
            return

        def format_time(millisecond):
            m, s = divmod(millisecond / 1000, 60)
            h, m = divmod(m, 60)
            return h, m, s

        self.label_count.setText("%02d:%02d:%02d" % format_time(self.parent.rest_time))
        self.parent.rest_time = self.parent.rest_time - 1000

    def show_button(self):
        """显示返回工作按钮"""
        if not self.primary:
            return

        self.parent.timer_rest.stop()
        self.parent.timer_count.stop()

        # 淡出消息和倒计时
        opacity_effect = QGraphicsOpacityEffect()
        self.label_message.setGraphicsEffect(opacity_effect)

        fade_out = QPropertyAnimation(opacity_effect, b"opacity")
        fade_out.setDuration(500)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.finished.connect(self.label_message.hide)
        fade_out.start()

        opacity_effect_count = QGraphicsOpacityEffect()
        self.label_count.setGraphicsEffect(opacity_effect_count)

        fade_out_count = QPropertyAnimation(opacity_effect_count, b"opacity")
        fade_out_count.setDuration(500)
        fade_out_count.setStartValue(1.0)
        fade_out_count.setEndValue(0.0)
        fade_out_count.finished.connect(self.label_count.hide)
        fade_out_count.start()

        self.label_message.hide()
        self.label_count.hide()

        # 淡入按钮
        self.button.setWindowOpacity(0.0)
        self.button.show()

        fade_in_button = QPropertyAnimation(self.button, b"windowOpacity")
        fade_in_button.setDuration(800)
        fade_in_button.setStartValue(0.0)
        fade_in_button.setEndValue(1.0)
        fade_in_button.start()
