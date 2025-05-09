from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QSpinBox, QCheckBox, QPushButton, QFileDialog, QMessageBox
)

from HealthyWork.config import Config


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("HealthyWork 设置")
        self.setMinimumWidth(400)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 工作时间设置
        work_time_layout = QHBoxLayout()
        work_time_layout.addWidget(QLabel("工作时间 (分钟):"))
        self.work_time_spinbox = QSpinBox()
        self.work_time_spinbox.setRange(1, 120)
        self.work_time_spinbox.setValue(int(Config.TIME_WORK))
        work_time_layout.addWidget(self.work_time_spinbox)
        layout.addLayout(work_time_layout)
        
        # 休息时间设置
        rest_time_layout = QHBoxLayout()
        rest_time_layout.addWidget(QLabel("休息时间 (分钟):"))
        self.rest_time_spinbox = QSpinBox()
        self.rest_time_spinbox.setRange(1, 30)
        self.rest_time_spinbox.setValue(int(Config.TIME_REST))
        rest_time_layout.addWidget(self.rest_time_spinbox)
        layout.addLayout(rest_time_layout)
        
        # 提示消息设置
        message_layout = QHBoxLayout()
        message_layout.addWidget(QLabel("提示消息:"))
        self.message_edit = QLineEdit()
        self.message_edit.setText(Config.MESSAGE)
        message_layout.addWidget(self.message_edit)
        layout.addLayout(message_layout)
        
        # 壁纸目录设置
        wallpaper_layout = QHBoxLayout()
        wallpaper_layout.addWidget(QLabel("壁纸目录:"))
        self.wallpaper_edit = QLineEdit()
        self.wallpaper_edit.setText(Config.DIR_WALLPAPER)
        wallpaper_layout.addWidget(self.wallpaper_edit)
        self.browse_wallpaper_btn = QPushButton("浏览...")
        self.browse_wallpaper_btn.clicked.connect(self.browse_wallpaper_dir)
        wallpaper_layout.addWidget(self.browse_wallpaper_btn)
        layout.addLayout(wallpaper_layout)
        
        # 音乐目录设置
        music_layout = QHBoxLayout()
        music_layout.addWidget(QLabel("音乐目录:"))
        self.music_edit = QLineEdit()
        self.music_edit.setText(Config.DIR_MUSIC)
        music_layout.addWidget(self.music_edit)
        self.browse_music_btn = QPushButton("浏览...")
        self.browse_music_btn.clicked.connect(self.browse_music_dir)
        music_layout.addWidget(self.browse_music_btn)
        layout.addLayout(music_layout)
        
        # 播放音乐设置
        music_check_layout = QHBoxLayout()
        self.play_music_checkbox = QCheckBox("休息时播放音乐")
        self.play_music_checkbox.setChecked(Config.PLAY_MUSIC)
        music_check_layout.addWidget(self.play_music_checkbox)
        music_check_layout.addStretch()
        layout.addLayout(music_check_layout)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("保存设置")
        self.save_btn.clicked.connect(self.save_settings)
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.close)
        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def browse_wallpaper_dir(self):
        directory = QFileDialog.getExistingDirectory(
            self, "选择壁纸目录", self.wallpaper_edit.text()
        )
        if directory:
            self.wallpaper_edit.setText(directory)
    
    def browse_music_dir(self):
        directory = QFileDialog.getExistingDirectory(
            self, "选择音乐目录", self.music_edit.text()
        )
        if directory:
            self.music_edit.setText(directory)
    
    def save_settings(self):
        # 更新配置
        Config.profile.update_profile({
            "workTime": self.work_time_spinbox.value(),
            "restTime": self.rest_time_spinbox.value(),
            "message": self.message_edit.text(),
            "wallpaper": self.wallpaper_edit.text(),
            "music": self.music_edit.text(),
            "playMusic": self.play_music_checkbox.isChecked()
        })
        
        # 应用新配置
        self.parent.work_time = int(Config.TIME_WORK * 60 * 1000)
        self.parent.rest_time = int(Config.TIME_REST * 60 * 1000)
        
        # 显示保存成功消息
        QMessageBox.information(
            self, "设置保存成功", 
            "设置已成功保存，将在下个工作周期生效。"
        )
        
        # 关闭设置窗口
        self.hide()