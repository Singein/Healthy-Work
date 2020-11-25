# HealthyWork
生活不止有屏幕上的代码,还有诗和远方. 
这是一款基于Python语言和PyQt图形化框架编写的桌面应用，用来提醒正在电脑前工作的人们注意休息，以保障身体健康。

## Features
- 防颈椎病
- 防腰间盘突出
- 防痔疮
- 防心脏病
- 自定义壁纸
- 自定义时间
- 本地音乐播放
- 全屏显示，窗口置顶
- 界面简约（编不下去了）
- 你值得拥有

![截图](https://github.com/1zlab/HealthyWork/blob/master/screenshots/Screenshot.png)
![截图](https://github.com/1zlab/HealthyWork/blob/master/screenshots/Screenshot_2.png)
## Dependence
- python3
- PyQt5


## Install
```sh
pip install healthywork
```

## How to use
```sh
runhw
```
## Custom

初次运行会在用户目录下的.config文件夹中创建healthywork.json文件，存储程序基本的配置，你可以自行修改一下的所有选项：


```json
{
    "message": "喝杯水休息一下吧",
    "timeWork": 25,
    "timeRest": 5,
    "wallpaperDir": "./wallpapers",
    "musicDir": "./music",
    "playMusic": true
}
```

- message：提醒的文字
- timeWork: 工作时间间隔，单位分钟，默认25分钟
- timeRest: 休息时间间隔，单位分钟，默认5分钟
- wallpaperDir: 存放壁纸的目录，默认为用户主目录下的Pictures
- musicDir: 存放音频的目录，默认为用户主目录下的Music目录
- playMusic: 休息时是否播放音乐。默认播放。
