from PIL import Image
import numpy as np
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QBuffer
import io

class ImageData:
    def __init__(self):
        self.image = None
        self.width = 0
        self.height = 0
        self.channel = 0
    
    def toImage( self , img ):
        # Image.size = ( width , height , channel )
        res = None
        if type( img ) is Image.Image:
            res = img
        elif type( img ) is str:
            res = Image.open( img ).copy()
        elif type( img ) is QImage:
            buffer = QBuffer()
            buffer.open( QBuffer.ReadWrite )
            img.save( buffer , "PNG" )
            res = Image.open( io.BytesIO( buffer.data() ) )
        elif type( img ) is np.ndarray:
            res = Image.fromarray( img )
        
        return res
    
    def toNdarray( self , img ):
        # Ndarray.shape = ( height , width , channel )
        res = None
        if type( img ) is Image.Image:
            res = np.array( img )
        elif type( img ) is str:
            res = np.array( Image.open( img ) )
        elif type( img ) is QImage:
            buffer = QBuffer()
            buffer.open( QBuffer.ReadWrite )
            img.save( buffer , "PNG" )
            res = np.array( Image.open( io.BytesIO( buffer.data() ) ) )
        elif type( img ) is np.ndarray:
            res = img
        
        if len( res.shape ) == 3 and res.shape[ 2 ] == 4:
            res = res[ : , : , : 3 ]
        return res
    
    def toQImage( self , img ):
        res = None
        if type( img ) is Image.Image:
            imgByteArr = io.BytesIO()
            img.save( imgByteArr , "PNG" )
            res = QImage.fromData( imgByteArr.getvalue() , img.format )
        elif type( img ) is str:
            res = QImage( img )
        elif type( img ) is QImage:
            res = img
        elif type( img ) is np.ndarray:
            img = Image.fromarray( img )
            imgByteArr = io.BytesIO()
            img.save( imgByteArr , "PNG" )
            res = QImage.fromData( imgByteArr.getvalue() , img.format )
        
        return res
