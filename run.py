import workspace.GUI as Main_GUI
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication( sys.argv )
    ex = Main_GUI.Main_Widget()
    sys.exit( app.exec_() )
