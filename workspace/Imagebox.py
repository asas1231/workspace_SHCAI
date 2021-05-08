import sys
import io
from PIL import ImageGrab, ImageQt, Image
from PyQt5.QtWidgets import (QWidget, QGridLayout, QLineEdit, QLabel, QHBoxLayout,
    QVBoxLayout, QPushButton, QApplication, QCheckBox, QMessageBox, QSizePolicy)
from PyQt5 import (QtWidgets, QtCore, QtGui)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np

class ImageboxItemWidget( QWidget ):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QImage()
        self.last_x = 0
        self.last_y = 0
        self.width = self.image.width()
        self.height = self.image.height()
    
    @pyqtSlot( QImage )
    def image_data_slot(self, image_data):
        if 0 != image_data.width():
            self.image = image_data
            self.width = self.image.width()
            self.height = self.image.height()
			# if self.image.size() != self.size():
				# self.setFixedSize(self.image.size())
        self.update()
    
    def paintEvent(self, event):
        if not self.image.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            painter.drawImage(self.rect(), self.image)

    def mouseMoveEvent( self , event ):
        if event.buttons() == Qt.LeftButton:
            x = event.x()
            y = event.y()
            _rect = self.rect()
            px = ( self.image.width()  * x ) // _rect.width()
            py = ( self.image.height() * y ) // _rect.height()
            if 0 <= px < self.width and 0 <= py < self.height:
                if self.last_x != px or self.last_y != py:
                    pixel = self.image.pixel( px , py )
                    print( 'click (x, y): (%d, %d). ColorRGB: (%d, %d, %d). Gray: %d' % ( px , py , qRed( pixel ) , qGreen( pixel ) , qBlue( pixel ) , qGray( pixel ) ) )
                    self.last_x = px
                    self.last_y = py
            
    def mousePressEvent(self, event):
        if 1 == event.button():
            x = event.x()
            y = event.y()
            _rect = self.rect()
            px = ( self.image.width()  * x ) // _rect.width()
            py = ( self.image.height() * y ) // _rect.height()
            if 0 <= px < self.width and 0 <= py < self.height:
                pixel = self.image.pixel( px , py )
                print( 'click (x, y): (%d, %d). ColorRGB: (%d, %d, %d). Gray: %d' % ( px , py , qRed( pixel ) , qGreen( pixel ) , qBlue( pixel ) , qGray( pixel ) ) )
                # print( 'click (x, y): (%d, %d).' % ( px , py ) )
                self.last_x = px
                self.last_y = py

class ImageboxWidget( QWidget ):
    imageScreenshotUpdated = pyqtSignal( QImage )
    def __init__(self, title_name = "", parent=None):
        super().__init__(parent)
        
        self.imagebox_item_widget = ImageboxItemWidget( self )
        self.imagebox_item_widget.setSizePolicy( QSizePolicy.Expanding , QSizePolicy.Expanding )
        image_data_slot = self.imagebox_item_widget.image_data_slot
        self.imageScreenshotUpdated.connect( image_data_slot )

        layout = QVBoxLayout()
        layout.addWidget( self.imagebox_item_widget )
        self.setLayout( layout )
        
        self.setWindowTitle( title_name )
        
        self.show()
    
    def setImage( self , img ):
        if type( img ) is Image.Image:
            imgByteArr = io.BytesIO()
            img.save( imgByteArr , format = 'PNG' )
            qimg = QImage.fromData( imgByteArr.getvalue() , "PNG" )
            self.imageScreenshotUpdated.emit( qimg )
        elif type( img ) is QImage:
            self.imageScreenshotUpdated.emit( img )
        elif type( img ) == np.ndarray:
            if len( img.shape ) == 2 :
                img2 = np.zeros( ( img.shape[ 0 ] , img.shape[ 1 ] , 3 ) , np.uint8 )
                img2[ : , : , 0 ] = img
                img2[ : , : , 1 ] = img
                img2[ : , : , 2 ] = img
                img = img2
            # img = np.transpose( img , ( 1 , 0 , 2 ) )
            img = Image.fromarray( img )
            self.setImage( img )


