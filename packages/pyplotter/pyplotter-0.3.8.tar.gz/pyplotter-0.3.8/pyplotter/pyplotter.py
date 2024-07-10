from PyQt5 import QtWidgets, QtGui
import sys
import os

from .sources.config import initConfig, loadConfigCurrent
# Init config file, to be done first
initConfig()
config = loadConfigCurrent()
from .ui.mainWindow import MainApp



# Get the folder path for pictures
PICTURESPATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ui/pictures/')

def main():

    app = QtWidgets.QApplication(sys.argv)
    app_icon = QtGui.QIcon()
    app_icon.addFile(PICTURESPATH+'icon.png')
    app.setWindowIcon(app_icon)

    if config['style']!='white':

        import qdarkstyle

        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    main_app = MainApp(app)
    main_app.show()
    app.exec_()


if __name__=='__main__':
    main()
