#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

from OSProfile import OSProfile

DEFAULT_LABEL_STYLE = "color: rgb(255, 0, 127);font: 30pt \"WenQuanYi Micro Hei Mono\";"
DEFAULT_BUTTON_STYLE = "background-color: rgba(182, 176, 171, 90);color: rgb(255, 0, 127);font: 30pt \"WenQuanYi Micro Hei Mono\";"
DEFAULT_MESSAGE = "喝杯水休息一下吧"
DEFAULT_WORK_TIME = "25"
DEFAULT_REST_TIME = "5"
DEFAULT_WALLPAPER_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media", "wallpapers")
DEFAULT_MUSIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media", "music")

DEFAULT_CONFIG_OPTIONS = {
    'message': "喝杯水休息一下吧",
    'workTime': 25,
    'restTime': 5,
    'wallpaper': '',
    'music': '',
    'playMusic': False
}


class Config:
    profile = OSProfile(appname="HealthyWork", profile="settings.json", options=DEFAULT_CONFIG_OPTIONS)

    LABEL_STYLESHEET = profile.read_profile().get('label_stylesheet', DEFAULT_LABEL_STYLE)
    BUTTON_STYLESHEET = profile.read_profile().get('button_stylesheet', DEFAULT_BUTTON_STYLE)
    MESSAGE = profile.read_profile().get('message', DEFAULT_MESSAGE)
    TIME_WORK = profile.read_profile().get('workTime', DEFAULT_WORK_TIME)
    TIME_REST = profile.read_profile().get('restTime', DEFAULT_REST_TIME)
    DIR_WALLPAPER = profile.read_profile().get('wallpaper', DEFAULT_WALLPAPER_DIR)
    DIR_WALLPAPER = DIR_WALLPAPER if DIR_WALLPAPER else DEFAULT_WALLPAPER_DIR
    DIR_MUSIC = profile.read_profile().get('music', DEFAULT_MUSIC_DIR)
    DIR_MUSIC = DIR_MUSIC if DIR_MUSIC else DEFAULT_MUSIC_DIR
    PLAY_MUSIC = profile.read_profile().get('playMusic')
