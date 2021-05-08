# https://benhoff.net/face-detection-opencv-pyqt.html
import sys
from os import path
import time
import math

import cv2
import numpy as np

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui


class RecordVideo(QtCore.QObject):
    image_data = QtCore.pyqtSignal(np.ndarray)
    
    def __init__(self, camera_port=0, parent=None):
        super().__init__(parent)
        self.camera = cv2.VideoCapture( "http://192.168.24.114:8088/video" )
        
        self.timer = QtCore.QBasicTimer()
    
    def start_recording(self):
        self.timer.start(0, self)
    
    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            print( 'event.timerId() = %d, timer.timerId() = %d' % ( event.timerId() , self.timer.timerId() ) )
            return
        
        print( 'Read image. event.timerId() = %d.' % ( event.timerId() ) )
        read, data = self.camera.read()
        if read:
            self.image_data.emit(data)

class FaceDetectionWidget(QtWidgets.QWidget):
    def __init__(self, haar_cascade_filepath, parent=None):
        super().__init__(parent)
        self.classifier = cv2.CascadeClassifier(haar_cascade_filepath)
        self.image = QtGui.QImage()
        self._red = (0, 0, 255)
        self._width = 2
        self._min_size = (30, 30) # 1280x960, 4x3

    def detect_faces(self, image: np.ndarray):
        # haarclassifiers work better in black and white
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.equalizeHist(gray_image)

        faces = self.classifier.detectMultiScale(gray_image,
                                                 scaleFactor=1.3,
                                                 minNeighbors=4,
                                                 flags=cv2.CASCADE_SCALE_IMAGE,
                                                 minSize=self._min_size)

        return faces

    def image_data_slot(self, image_data):
        faces = self.detect_faces(image_data)
        for (x, y, w, h) in faces:
            cv2.rectangle(image_data,
                          (x, y),
                          (x+w, y+h),
                          self._red,
                          self._width)

        self.image = self.get_qimage(image_data)
        # self.image = self.get_qimage(image_data)
        if self.image.size() != self.size():
            self.setFixedSize(self.image.size())

        self.update()

    def get_qimage(self, image: np.ndarray):
        height, width, colors = image.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage

        image = QImage(image.data,
                       width,
                       height,
                       bytesPerLine,
                       QImage.Format_RGB888)

        image = image.rgbSwapped()
        image = image.scaledToHeight( 320 )
        return image

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()


class MainWidget(QtWidgets.QWidget):
    def __init__(self, haarcascade_filepath, parent=None):
        super().__init__(parent)
        fp = haarcascade_filepath
        self.face_detection_widget = FaceDetectionWidget(fp)

        # TODO: set video port
        self.record_video = RecordVideo()

        image_data_slot = self.face_detection_widget.image_data_slot
        self.record_video.image_data.connect(image_data_slot)

        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(self.face_detection_widget)
        self.run_button = QtWidgets.QPushButton('Start')
        layout.addWidget(self.run_button)

        self.run_button.clicked.connect(self.record_video.start_recording)
        self.setLayout(layout)
        
        # timer = QtCore.QBasicTimer()
        # timer.start( 0 , self.record_video )
        # print( 'Start timer. %d' % ( timer.timerId() ) )


def main(haar_cascade_filepath):
    app = QtWidgets.QApplication(sys.argv)

    main_window = QtWidgets.QMainWindow()
    main_widget = MainWidget(haar_cascade_filepath)
    main_window.setCentralWidget(main_widget)
    main_window.show()
    sys.exit(app.exec_())

class Qtimer01(QtWidgets.QWidget):
    finish = QtCore.pyqtSignal( int )
    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = QtCore.QBasicTimer()
    
    def start_timer( self ):
        print( 'start_timer' )
        # self.timer.start( 0 , self )
        self.times = 0
    
    def timerEvent(self, event):
        print( 'timerEvent' )
        if (event.timerId() != self.timer.timerId()):
            print( 'event.timerId() = %d, timer.timerId() = %d' % ( event.timerId() , self.timer.timerId() ) )
            return
        
        print( 'Qtimer01(). Sleep 1 secs. timerId() = %d.' % ( event.timerId() ) )
        QtCore.QThread.msleep( 1000 )
        self.times += 1
        if self.times > 11:
            self.finish.emit( 1 )

class Qtimer02(QtWidgets.QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def timerEvent(self, event):
        print( 'Read image. event. timerId() = %d.' % ( event.timerId() ) )
        print( 'Sleep 5 secs. timerId() = %d.' % ( event.timerId() ) )
        time.sleep( 5 )

class QThreadQtimer(QtCore.QObject): # QObject, QtCore.QThread
    finish = QtCore.pyqtSignal( int )
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
    
    def run( self ):
        print( 'QThreadQtimer run(). (thread: %r)' % QtCore.QThread.currentThread() )
        self.times = 0
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self.timerEvent)
        self._timer.start( 0 )
        print( 'Timer start.' , self._timer.isActive() , self._timer.timerId() )
    
    def timerEvent(self):
        print( 'timerEvent' )
        # if (event.timerId() != self._timer.timerId()):
            # print( 'event.timerId() = %d, timer.timerId() = %d' % ( event.timerId() , self._timer.timerId() ) )
            # return
        
        # print( 'Qtimer01(). Sleep 1 secs. timerId() = %d.' % ( event.timerId() ) )
        QtCore.QThread.msleep( 1000 )
        self.times += 1
        if self.times > 11:
            print( 'Emit finish signal.' )
            self.finish.emit( 1 )

class QtimerMainWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.thread = QtCore.QThread()
        self.work = QThreadQtimer()
        self.work.finish.connect(self.showResult)
        self.work.moveToThread(self.thread)
        self.thread.started.connect(self.work.run)
        
        layout = QtWidgets.QVBoxLayout()
        
        self.run_button = QtWidgets.QPushButton('Start')
        layout.addWidget(self.run_button)

        self.run_button.clicked.connect( self.start_work )
        
        self.while_button = QtWidgets.QPushButton('While')
        layout.addWidget(self.while_button)

        self.while_button.clicked.connect(self.start_run)
        self.setLayout(layout)
        # self.work.start()
    
    def start_work( self ):
        self.thread.start()
    
    def start_run( self ):
        self.whileCode()
        print( 'work.wait()' )
        self.whileCode()
    
    def whileCode( self ):
        print( 'Function whileCode' )
        times = 10
        while times > 0:
            print( 'Times: %d' % times )
            times -= 1
            QtCore.QThread.msleep( 1000 )
            # time.sleep( 1 )
    
    def showResult( self , val ):
        print( 'Work is finish. %d' % val )
        self.work.terminate()

def test_Qtimer():
    app = QtWidgets.QApplication(sys.argv)

    main_window = QtWidgets.QMainWindow()
    main_widget = QtimerMainWidget()
    main_window.setCentralWidget(main_widget)
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    test_Qtimer()
    # script_dir = path.dirname(path.realpath(__file__))
    # cascade_filepath = path.join(script_dir,
                                 # '..',
                                 # '..',
                                 # '..',
                                 # 'data',
                                 # 'haarcascade_frontalface_default.xml')
    # print( 'Cascade file path: ' , cascade_filepath )

    # cascade_filepath = path.abspath(cascade_filepath)
    # main(cascade_filepath)