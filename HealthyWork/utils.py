import os


def is_img(uri: str):
    ext = os.path.splitext(uri)[-1].lower()
    if ext == '.jpg':
        return True
    elif ext == '.png':
        return True
    elif ext == '.jpeg':
        return True
    elif ext == '.bmp':
        return True
    else:
        return False


def is_song(uri: str):
    ext = os.path.splitext(uri)[-1].lower()
    if ext == '.mp3':
        return True
    elif ext == '.wav':
        return True
    else:
        return False
