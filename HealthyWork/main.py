import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QApplication

from HealthyWork.app import MainWindow


def run_app():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    QCoreApplication.setApplicationName("HealthyWork")
    QGuiApplication.setApplicationDisplayName("HealthyWork")

    hw = MainWindow()
    hw.start()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_app()
