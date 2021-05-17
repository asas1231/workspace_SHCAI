# -*- coding: UTF-8 -*-
import workspace.Imagebox  as ImgB
import workspace.ImageData as ImgD

from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from PIL import ImageGrab , Image , ImageOps
import math
import numpy as np
import io
import sys
import os
import queue
import time
import datetime
import random
import winsound
import win32api, win32con

# import cv2
# import skimage
# import skimage.measure

"""
#
# TODO: 各種影像資料轉換, 長寬翻轉問題
#
# com.linecorp.LGFARM/.AppActivity
#
"""
class screenVideo( QtCore.QObject ):
    image_data = QtCore.pyqtSignal( np.ndarray )
    
    def __init__( self , parent = None ):
        super().__init__( parent )
        
        self.timer = QtCore.QBasicTimer()
        self.imgData = ImgD.ImageData()
        self.isSave = False
        self.get_screenshot_count = 0
        self.get_screenshot_limit = 0
    
    def start_recording( self ):
        self.timer.start( 100 , self )
    
    def timerEvent( self , event ):
        if ( event.timerId() != self.timer.timerId() ):
            print( 'event.timerId() = %d, timer.timerId() = %d' % ( event.timerId() , self.timer.timerId() ) )
            return
        
        # print( 'Read image. event.timerId() = %d.' % ( event.timerId() ) )
        read , data = self.get_screenshot()
        if read:
            self.image_data.emit( data )
    
    def get_screenshot( self ):
        # print( self.get_screenshot_count , self.get_screenshot_limit )
        if self.get_screenshot_count < self.get_screenshot_limit:
            self.get_screenshot_count += 1
            img = ImageGrab.grab()
            return [ True , self.imgData.toNdarray( img ) ]
        
        # print( self.isSave )
        if not self.isSave:
            return [ False , False ]
        
        img = ImageGrab.grab()
        return [ self.isSave , self.imgData.toNdarray( img ) ]

class screenRecording( QThread ):
    info_signal = QtCore.pyqtSignal( str )
    def __init__( self , save_path = "test" , file_name_count = 0 , parent = None ):
        QThread.__init__( self , parent = parent )
        self.isWork = False
        self.q_img = queue.Queue()
        self.isSave = True
        self.file_name_count = file_name_count
        self.imgData = ImgD.ImageData()
        self.img_last = np.zeros( [ 100 , 100 , 3 ] , np.uint8 )
        self.save_path = save_path
        self.save_file_format = datetime.datetime.now().strftime( "%Y%m%d_%%05d.png" )
        if not os.path.isdir( self.save_path ):
            os.makedirs( self.save_path ) # create a directory recursively
    
    def quit( self ):
        self.isWork = False
    
    def alive( self ):
        return self.isWork == True
    
    def run( self ):
        self.isWork = True
        while self.alive():
            item = self.q_img.get()
            if item is None:
                break
            
            img_fileName = self.get_file_name()
            item.save( img_fileName )
            print( img_fileName )
            
        self.isWork = False
    
    def Little_Bee( self ):
        s = "12333233 23213333 12333233 23221111 "
        s = "5333422212345555533342221355333322222344333334555333422213551111 "
        s = "533-422-1234555-533-422-13553---2222234-3333345-533-422-13551--- "
        duration = 1000 // 4
        freq = [ 0 , 262, 294, 330, 349, 392, 440, 494 ]
        freq = [ 0 , 523, 587, 659, 698, 784, 880, 988 ]
        freq = [ 0 , 1046, 1175, 1318, 1397, 1568, 1760, 1976 ]

        freq = [ 0 , 523, 587, 659, 698, 784, 880, 988 ]
        i = 0
        while i < len( s ):
            if s[ i ] == " ":
                time.sleep( duration / 1000 )
                i += 1
            else:
                # print( i , ":" , s[ i ] )
                j = i + 1
                while s[ j ] == "-":
                    j += 1
                winsound.Beep( freq[ int( s[ i ] ) ] , duration * ( j - i ) )
                i = j
        
    def image_data_slot( self , image_data ):
        if self.compare_image( image_data ):
            return
        
        if self.isSave:
            self.q_img.put( self.imgData.toImage( image_data ) )
            self.img_last = image_data
    
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
        # image = image.scaledToHeight( 320 )
        return image
    
    def get_file_name( self ):
        while True:
            fn = os.path.join( self.save_path , self.save_file_format % self.file_name_count )
            if not os.path.isfile( fn ):
                break
            self.file_name_count += 1
        return fn
    
    def compare_image( self , img2 ):
        hash_h , hash_w = ( 10 , 19 )
        img1 = self.img_last
        Image_01 = Image.fromarray( img1 )
        Image_02 = Image.fromarray( img2 )
        Image_01 = Image_01.resize( size = ( hash_h , hash_w ) )
        Image_02 = Image_02.resize( size = ( hash_h , hash_w ) )
        Image_gray_01 = ImageOps.grayscale( Image_01 )
        Image_gray_02 = ImageOps.grayscale( Image_02 )
        img1 = self.imgData.toNdarray( Image_gray_01 )
        img2 = self.imgData.toNdarray( Image_gray_02 )
        img1 = img1[ 0 : hash_w , 0 : hash_h - 1 ] # 少掉畫面底部
        img2 = img2[ 0 : hash_w , 0 : hash_h - 1 ]
        img1_average = np.sum( img1 ) / ( hash_h * hash_w )
        img2_average = np.sum( img2 ) / ( hash_h * hash_w )
        hash_str_01 = ""
        hash_str_02 = ""
        # 均值
        for i in range( hash_h - 1 ):
            for j in range( hash_w ):
                if img1[ j , i ] > img1_average:
                    hash_str_01 = hash_str_01 + "1"
                else:
                    hash_str_01 = hash_str_01 + "0"
                if img2[ j , i ] > img2_average:
                    hash_str_02 = hash_str_02 + "1"
                else:
                    hash_str_02 = hash_str_02 + "0"
        
        # 差值
        for i in range( hash_h - 1 ):
            for j in range( hash_w ):
                if j + 1 < hash_w and img1[ j , i ] > img1[ j + 1 , i ]:
                    hash_str_01 = hash_str_01 + "1"
                else:
                    hash_str_01 = hash_str_01 + "0"
                if j + 1 < hash_w and img2[ j , i ] > img2[ j + 1 , i ]:
                    hash_str_02 = hash_str_02 + "1"
                else:
                    hash_str_02 = hash_str_02 + "0"
        
        # 比較
        return hash_str_01 == hash_str_02

class preventLockDesktop( QtCore.QObject ):
    def __init__( self , parent = None ):
        super().__init__( parent )
        
        self.timer = QtCore.QBasicTimer()
        # self.isWork = False
        self.isPause = False
        self.mx = 0
        self.my = 0
    
    def start_prevent( self ):
        self.timer.start( 300000 , self ) # 5 分鐘檢查一次, 15 分鐘無動作自動登出
    
    def timerEvent( self , event ):
        if ( event.timerId() != self.timer.timerId() ):
            print( 'event.timerId() = %d, timer.timerId() = %d' % ( event.timerId() , self.timer.timerId() ) )
            return
        
        if self.isPause:
            return
        
        x , y = win32api.GetCursorPos()
        if x == self.mx and y == self.my:
            win32api.SetCursorPos( ( x + 1 , y ) )
            win32api.SetCursorPos( ( x , y ) )
        
        self.mx = x
        self.my = y
        

class screenRecording_control( QThread ):
    def __init__( self , save_path = "" , parent = None ):
        QThread.__init__( self , parent = parent )
        self.q_cmd = queue.Queue()
        self.isWork = False
        
        self.screen_recording = screenRecording( save_path = save_path , file_name_count = 0 )
        self.screen_recording.start()
        self.screen_video = screenVideo()
        self.screen_video.image_data.connect( self.screen_recording.image_data_slot )
        self.screen_video.start_recording()
        self.prevent_lock_desktop = preventLockDesktop()
        self.prevent_lock_desktop.start_prevent()
    
    def alive( self ):
        return self.isWork == True
    
    def run( self ):
        self.isWork = True
        while self.alive():
            self.q_cmd.get()
        self.isWork = False
    
    def set_screenshot_save_mode( self , isSave ):
        print( isSave )
        self.screen_video.isSave     = isSave
        # self.screen_recording.isSave = True
    
    def set_prevent_pause_mode( self , value ):
        self.prevent_lock_desktop.isPause = not value
    
    def get_screenshot( self ):
        self.screen_video.get_screenshot_limit += 1

if __name__ == "__main__":
    img = QImage( os.path.join( "dev" , "熊大農場" , "ADB_0223.png" ) )
    pass