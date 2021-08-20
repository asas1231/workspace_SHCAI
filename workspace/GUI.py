from PyQt5.QtWidgets import (QWidget, QGridLayout, QLineEdit, QLabel,
    QHBoxLayout, QVBoxLayout, QPushButton, QApplication, QCheckBox,
    QMessageBox, QSizePolicy, QListWidget, QStackedWidget, QFrame,
    QAbstractScrollArea, QPlainTextEdit)
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PIL import ImageGrab , ImageQt
import io
import sys
import os
# import pyautogui
import random
import time
import requests
import json
import configparser
# import cv2
import queue
import win32api, win32con

import re
import urllib
from bs4 import BeautifulSoup as bs
# from pyquery import PyQuery as pq

import workspace.ImageData as ImgD
import screen_recording.screen_recording

"""
TODO
1. 存圖路徑，寫入 profile\workspace.ini
2. 透過剪貼簿溝通
"""

class ImageboxItemWidget( QWidget ):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QImage()
    
    @pyqtSlot( QImage )
    def image_data_slot(self, image_data):
        if 0 != image_data.width():
            self.image = image_data
            # if self.image.size() != self.size():
                # self.setFixedSize(self.image.size())
        
        self.update()
    
    def paintEvent(self, event):
        if ( not self.image.isNull() ) and ( 0 < self.image.width() ):
            painter = QPainter(self)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            painter.drawImage(self.rect(), self.image)
            # painter.drawImage(0, 0, self.image)


class Main_Widget(QWidget):
    imageScreenshotUpdated = pyqtSignal( QImage )
    def __init__(self):
        super( Main_Widget , self ).__init__()
        self.Load_ini()
        self.initUI()
        self.initParameters()
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '訊息', "是否確定關閉程式？", QMessageBox.Yes, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.Save_ini()
            event.accept()
        else:
            event.ignore()
    
    def initUI( self ):
        self.setGeometry( self.GUI_rect[ 0 ] , self.GUI_rect[ 1 ] , self.GUI_rect[ 2 ] , self.GUI_rect[ 3 ] )
        self.setWindowTitle( self.window_title )
        
        self.UI_list = QListWidget()
        sp = QSizePolicy()
        sp.setHorizontalPolicy( QSizePolicy.Maximum )
        sp.setHorizontalStretch( 0 )
        sp.setVerticalPolicy( QSizePolicy.Expanding )
        sp.setVerticalStretch( 1 )
        self.UI_list.setSizePolicy( sp )
        self.UI_list.setSizeAdjustPolicy( QAbstractScrollArea.AdjustToContents )
        self.UI_list.setFocusPolicy( Qt.NoFocus )
        self.UI_stack = QStackedWidget( self )
        
        self.initUI_dev()
        self.initUI_screenRecording()
        self.initUI_tabooNovel()
        # self.initUI_ADB()
        # self.initUI_farm()
        
        HBox = QHBoxLayout()
        HBox.addWidget( self.UI_list )
        HBox.addWidget( self.UI_stack )
        self.setLayout( HBox )
        
        self.show()
    
    def initUI_dev( self ):
        grid = QGridLayout()
        self.screenshotButton = QPushButton( "採草藥數學" , self )
        self.screenshotButton.setToolTip( "截取採集問題圖片" )
        if self.dev_shortcut_key_screenshot != "None":
            self.screenshotButton.setShortcut( self.dev_shortcut_key_screenshot )
        self.screenshotButton.setFocusPolicy( Qt.NoFocus )
        grid.addWidget( self.screenshotButton , *( 0 , 0 ) )
        self.ADBscreenshotButton = QPushButton( "ADB 截圖" , self )
        self.ADBscreenshotButton.setToolTip( "ADB 截圖" )
        if self.dev_shortcut_key_ADBscreenshot != "None":
            self.ADBscreenshotButton.setShortcut( self.dev_shortcut_key_ADBscreenshot )
        self.ADBscreenshotButton.setFocusPolicy( Qt.NoFocus )
        grid.addWidget( self.ADBscreenshotButton , *( 0 , 1 ) )
        self.dev_ADB_test_Button = QPushButton( "ADB 測試開發功能" )
        self.dev_ADB_test_Button.setFocusPolicy( Qt.NoFocus )
        grid.addWidget( self.dev_ADB_test_Button , *( 0 , 2 ) )
        self.LINE_LineEdit = QLineEdit()
        grid.addWidget( self.LINE_LineEdit , *( 1 , 0 ) )
        self.LINE_messageButton = QPushButton( "發送訊息" , self )
        if self.dev_shortcut_key_LINE_send != "None":
            self.LINE_messageButton.setShortcut( self.dev_shortcut_key_LINE_send )
        self.LINE_messageButton.setFocusPolicy( Qt.NoFocus )
        grid.addWidget( self.LINE_messageButton , *( 1 , 1 ) )
        self.devCheckGameStatusButton = QPushButton( "檢查RO狀態" , self )
        if self.dev_shortcut_key_CheckGameStatus != "None":
            self.devCheckGameStatusButton.setShortcut( self.dev_shortcut_key_CheckGameStatus )
        self.devCheckGameStatusButton.setFocusPolicy( Qt.NoFocus )
        grid.addWidget( self.devCheckGameStatusButton , *( 1 , 2 ) )
        self.label_formula = QLabel( "" )
        self.imagebox_item_widget = ImageboxItemWidget( self )
        
        grid.setColumnStretch( 0 , 1 )
        grid.setColumnStretch( 1 , 1 )
        sp = QSizePolicy()
        sp.setHorizontalPolicy( QSizePolicy.Expanding )
        sp.setHorizontalStretch( 1 )
        sp.setVerticalPolicy( QSizePolicy.Expanding )
        sp.setVerticalStretch( 1 )
        self.imagebox_item_widget.setSizePolicy( sp )
        layout = QVBoxLayout()
        layout.addLayout( grid )
        layout.addWidget( self.label_formula )
        layout.addWidget( self.imagebox_item_widget )
        
        stack = QWidget()
        stack.setLayout( layout )
        index = self.UI_stack.addWidget( stack )
        self.UI_list.insertItem( index , '開發功能' )
    
    def initUI_ADB( self ):
        grid = QGridLayout()
        self.ADB_formula_Button = QPushButton( "採草藥數學" , self )
        self.ADB_formula_Button.setToolTip( "截取採集問題圖片" )
        grid.addWidget( self.ADB_formula_Button , *( 0 , 0 ) )
        self.ADB_screenshotButton = QPushButton( "截圖" , self )
        self.ADB_screenshotButton.setToolTip( "截圖" )
        grid.addWidget( self.ADB_screenshotButton , *( 0 , 1 ) )
        self.ADB_address_Edit = QLineEdit( self.ADB_address )
        grid.addWidget( self.ADB_address_Edit , *( 1 , 0 ) )
        self.ADB_connect_Button = QPushButton( "連線" , self )
        grid.addWidget( self.ADB_connect_Button , *( 1 , 1 ) )
        self.ADB_formula_label = QLabel( "" )
        self.ADB_imagebox_item_widget = ImageboxItemWidget( self )
        
        grid.setColumnStretch( 0 , 1 )
        grid.setColumnStretch( 1 , 1 )
        sp = QSizePolicy()
        sp.setHorizontalPolicy( QSizePolicy.Expanding )
        sp.setHorizontalStretch( 1 )
        sp.setVerticalPolicy( QSizePolicy.Expanding )
        sp.setVerticalStretch( 1 )
        self.ADB_imagebox_item_widget.setSizePolicy( sp )
        layout = QVBoxLayout()
        layout.addLayout( grid )
        layout.addWidget( self.ADB_formula_label )
        layout.addWidget( self.ADB_imagebox_item_widget )
        
        stack = QWidget()
        stack.setLayout( layout )
        index = self.UI_stack.addWidget( stack )
        self.UI_list.insertItem( index , 'ADB' )
    
    def initUI_farm( self ):
        grid = QGridLayout()
        self.farm_wheat_Button = QPushButton( "啟動種小麥" , self )
        grid.addWidget( self.farm_wheat_Button , *( 0 , 0 ) )
        self.farm_sell_Button = QPushButton( "販賣小麥" , self )
        grid.addWidget( self.farm_sell_Button , *( 0 , 1 ) )
        self.farm_order_Button = QPushButton( "傳真訂單-藍單" , self )
        grid.addWidget( self.farm_order_Button , *( 0 , 2 ) )
        self.farm_wheat_1_Edit = QLineEdit( "" )
        grid.addWidget( self.farm_wheat_1_Edit , *( 1 , 0 ) )
        self.farm_wheat_2_Edit = QLineEdit( "150" )
        grid.addWidget( self.farm_wheat_2_Edit , *( 1 , 1 ) )
        self.farm_time_label = QLabel( "" )
        
        grid.setColumnStretch( 0 , 1 )
        grid.setColumnStretch( 1 , 1 )
        layout = QVBoxLayout()
        layout.addLayout( grid )
        layout.addWidget( self.farm_time_label )
        
        stack = QWidget()
        stack.setLayout( layout )
        index = self.UI_stack.addWidget( stack )
        self.UI_list.insertItem( index , '熊大農場' )
    
    def initUI_screenRecording( self ):
        grid = QGridLayout()
        self.screenRecording_recording_Button = QPushButton( "錄影開關" , self )
        grid.addWidget( self.screenRecording_recording_Button , *( 0 , 0 ) )
        self.screenRecording_prevent_lock_desktop_CheckBox = QCheckBox( '防止登出' , self )
        grid.addWidget( self.screenRecording_prevent_lock_desktop_CheckBox , *( 0 , 2 ) )
        self.screenRecording_screenshot_Button = QPushButton( '擷取圖片' , self )
        grid.addWidget( self.screenRecording_screenshot_Button , *( 1 , 0 ) )
        self.screenRecording_info_label = QLabel( "" )
        self.screenRecording_imagebox_item_widget = ImageboxItemWidget( self )
        
        grid.setColumnStretch( 0 , 1 )
        grid.setColumnStretch( 1 , 1 )
        sp = QSizePolicy()
        sp.setHorizontalPolicy( QSizePolicy.Expanding )
        sp.setHorizontalStretch( 1 )
        sp.setVerticalPolicy( QSizePolicy.Expanding )
        sp.setVerticalStretch( 1 )
        self.screenRecording_imagebox_item_widget.setSizePolicy( sp )
        layout = QVBoxLayout()
        layout.addLayout( grid )
        layout.addWidget( self.screenRecording_info_label )
        layout.addWidget( self.screenRecording_imagebox_item_widget )
        
        stack = QWidget()
        stack.setLayout( layout )
        index = self.UI_stack.addWidget( stack )
        self.UI_list.insertItem( index , '螢幕錄影' )
    
    def initUI_tabooNovel( self ):
        # TODO multi-website
        grid = QGridLayout()
        self.tabooNovel_url_Edit = QLineEdit( "" )
        grid.addWidget( self.tabooNovel_url_Edit , *( 0 , 0 ) )
        self.tabooNovel_download_Button = QPushButton( "下載" , self )
        grid.addWidget( self.tabooNovel_download_Button , *( 0 , 1 ) )
        
        self.tabooNovel_ = QLabel( "" )
        # TODO
        # https://www.cnblogs.com/yinsedeyinse/p/10841987.html, 訊息框行號
        sp = QSizePolicy()
        sp.setHorizontalPolicy( QSizePolicy.Expanding )
        sp.setHorizontalStretch( 1 )
        sp.setVerticalPolicy( QSizePolicy.Expanding )
        sp.setVerticalStretch( 1 )
        self.tabooNovel_infomation_PTE = QPlainTextEdit()
        self.tabooNovel_infomation_PTE.setReadOnly( True )
        self.tabooNovel_infomation_PTE.setLineWrapMode( QPlainTextEdit.NoWrap )
        self.tabooNovel_infomation_PTE.setSizePolicy( sp )
        
        # self.screenRecording_imagebox_item_widget = ImageboxItemWidget( self )
        # grid.setColumnStretch( 0 , 1 )
        # grid.setColumnStretch( 1 , 1 )
        # sp = QSizePolicy()
        # sp.setHorizontalPolicy( QSizePolicy.Expanding )
        # sp.setHorizontalStretch( 1 )
        # sp.setVerticalPolicy( QSizePolicy.Expanding )
        # sp.setVerticalStretch( 1 )
        # self.screenRecording_imagebox_item_widget.setSizePolicy( sp )
        layout = QVBoxLayout()
        layout.addLayout( grid )
        layout.addWidget( self.tabooNovel_infomation_PTE )
        # layout.addWidget( self.screenRecording_imagebox_item_widget )
        
        stack = QWidget()
        stack.setLayout( layout )
        index = self.UI_stack.addWidget( stack )
        self.UI_list.insertItem( index , '禁忌' )
    
    def initParameters( self ):
        self.UI_list.currentRowChanged.connect( self.UI_list_display )
        
        # self.adb_exe = ADB.ADB_control( self.ADB_address_Edit.text() )
        # self.adb_exe.start()
        
        self.initParameters_dev()
        self.initParameters_screenRecording()
        self.initParameters_tabooNovel()
        # self.initParameters_ADB()
        # self.initParameters_farm()
    
    def initParameters_dev( self ):
        # self.screenshot_id = 0
        self.screenshot_filename_format = '採集問題_{:04d}.png'
        # self.ADB_screenshot_id = 0
        self.ADB_screenshot_filename_format = 'ADB_{:04d}.png'
        
        self.devCheckGameStatusButton.clicked.connect( self.dev_check_game_status )
        self.screenshotButton.clicked.connect( self.get_screenshot )
        self.ADBscreenshotButton.clicked.connect( self.get_ADB_screenshot )
        self.dev_ADB_test_Button.clicked.connect( self.dev_ADB_test )
        self.LINE_LineEdit.returnPressed.connect( self.send_LINE_message_slot )
        self.LINE_messageButton.clicked.connect( self.send_LINE_message_slot )
        
        image_data_slot = self.imagebox_item_widget.image_data_slot
        self.imageScreenshotUpdated.connect( image_data_slot )
        
        # self.ocr = RO_OCR()
        
        self._invoked_screenshot = False
        self._invoked_ADB_screenshot = False
    
    def initParameters_ADB( self ):
        # image_data_slot = self.ADB_imagebox_item_widget.image_data_slot
        # self.adb_exe.imageFullScreenUpdated.connect( image_data_slot )
        # self.adb_exe.imageFullScreenUpdated.connect( self._process_get_ADB_screenshot )
        self.ADB_screenshotButton.clicked.connect( self.get_ADB_screenshot )
        self.ADB_connect_Button.clicked.connect( self.ADB_connect )
    
    def initParameters_farm( self ):
        self.farm_exe = FARM.FARM( self.ocr , self.adb_exe , self.send_LINE_message , self.imageScreenshotUpdated )
        self.farm_exe.info_signal.connect( self.farm_info )
        self.farm_wheat_Button.clicked.connect( self.farm_wheat_switch )
        self.farm_order_Button.clicked.connect( self.farm_order_switch )
        # self.farm_sell_Button.clicked.connect( self.ADB_connect )
    
    def initParameters_screenRecording( self ):
        self.screenRecording_recording_mode = False
        self.screenRecording_exe = screen_recording.screen_recording.screenRecording_control( save_path = self.screenRecording_save_path )
        self.screenRecording_exe.start()
        self.screenRecording_recording_Button.clicked.connect( self.screenRecording_recording_switch )
        self.screenRecording_prevent_lock_desktop_CheckBox.clicked.connect( self.screenRecording_prevent_lock_desktop_switch )
        self.screenRecording_screenshot_Button.clicked.connect( self.screenRecording_screenshot )
    
    def initParameters_tabooNovel( self ):
        self.tabooNovel_save_path = "taboo\\novel\\result"
        self.tabooNovel_download_Button.clicked.connect( self.tabooNovel_download_fun )
        self.tabooNovel_downloader = TabooNovelDownload( self.tabooNovel_save_path , self.tabooNovel_info )
    
    def UI_list_display( self , UI_index ):
        self.UI_stack.setCurrentIndex( UI_index )
    
    def Load_ini( self ):
        # config file
        self.config = configparser.ConfigParser()
        cfgpath = os.path.join( 'profile' , 'workspace.ini' )
        self.config.read( cfgpath , encoding = 'utf-8' )
        
        # GUI
        if not 'GUI' in self.config.sections():
            self.config[ 'GUI' ] = {}
        self.GUI_rect = [ int( s ) for s in self.config[ 'GUI' ].get( 'GUI_rectangle' , '1200 , 450 , 310 , 180' ).split( ',' ) ]
        self.window_title = self.config[ 'GUI' ].get( 'window_title' , 'RO' )
        # LINE
        if not 'LINE' in self.config.sections():
            self.config[ 'LINE' ] = {}
        self.LINE_token = "Bearer " + self.config[ 'LINE' ].get( 'token' , '' )
        self.LINE_send_to = self.config[ 'LINE' ].get( 'to' , '' )
        # dev
        if not 'GUI_dev' in self.config.sections():
            self.config[ 'GUI_dev' ] = {}
        self.screenshot_do = int( self.config[ 'GUI_dev' ].get( 'screenshot_save' , '0' ) )
        self.screenshot_id = int( self.config[ 'GUI_dev' ].get( 'screenshot_id' , '0' ) )
        self.dev_shortcut_key_screenshot = self.config[ 'GUI_dev' ].get( 'shortcut_screenshot' , 's' )
        self.dev_shortcut_key_ADBscreenshot = self.config[ 'GUI_dev' ].get( 'shortcut_ADB_screenshot' , 'd' )
        self.dev_shortcut_key_LINE_send = self.config[ 'GUI_dev' ].get( 'shortcut_LINE_send' , 'a' )
        self.dev_shortcut_key_CheckGameStatus = self.config[ 'GUI_dev' ].get( 'shortcut_CheckGameStatus' , 'f' )
        self.dev_screenshot_path = self.config[ 'GUI_dev' ].get( 'screenshot_path' , 'data' )
        # ADB
        if not 'GUI_ADB' in self.config.sections():
            self.config[ 'GUI_ADB' ] = {}
        self.ADB_screenshot_do = int( self.config[ 'GUI_ADB' ].get( 'screenshot_save' , '1' ) )
        self.ADB_screenshot_id = int( self.config[ 'GUI_ADB' ].get( 'screenshot_id' , '0' ) )
        self.ADB_address = self.config[ 'GUI_ADB' ].get( 'ADB_address' , '127.0.0.1:62001' )
        self.ADB_screenshot_path = self.config[ 'GUI_ADB' ].get( 'screenshot_path' , 'data' )
        
        # screenRecording
        if not 'screenRecording' in self.config.sections():
            self.config[ 'screenRecording' ] = {}
        self.screenRecording_save_path = self.config[ 'screenRecording' ].get( 'save_path' , 'test' )
        
    
    def Save_ini( self ):
        # GUI
        self.GUI_rect = self.geometry()
        self.GUI_rect = [ self.GUI_rect.x() , self.GUI_rect.y() , self.GUI_rect.width () , self.GUI_rect.height () ]
        self.config[ 'GUI' ][ 'GUI_rectangle'   ] = " , ".join( [ str( i ) for i in self.GUI_rect ] )
        self.config[ 'GUI' ][ 'window_title'    ] = self.window_title
        # dev
        self.config[ 'GUI_dev' ][ 'screenshot_save'         ] = str( self.screenshot_do )
        self.config[ 'GUI_dev' ][ 'screenshot_id'           ] = str( self.screenshot_id )
        self.config[ 'GUI_dev' ][ 'shortcut_screenshot'     ] = self.dev_shortcut_key_screenshot
        self.config[ 'GUI_dev' ][ 'shortcut_ADB_screenshot' ] = self.dev_shortcut_key_ADBscreenshot
        self.config[ 'GUI_dev' ][ 'shortcut_LINE_send'      ] = self.dev_shortcut_key_LINE_send
        self.config[ 'GUI_dev' ][ 'shortcut_CheckGameStatus'] = self.dev_shortcut_key_CheckGameStatus
        # ADB
        self.config[ 'GUI_ADB' ][ 'screenshot_save' ] = str( self.ADB_screenshot_do )
        self.config[ 'GUI_ADB' ][ 'screenshot_id'   ] = str( self.ADB_screenshot_id )
        # self.config[ 'GUI_ADB' ][ 'ADB_address'     ] = self.ADB_address_Edit.text()
        
        # screenRecording
        self.config[ 'screenRecording' ][ 'save_path' ] = self.screenRecording_save_path
        
        # config file
        cfgpath = os.path.join( 'profile' , 'workspace.ini' )
        with open( cfgpath , 'w' , encoding = 'utf-8' ) as configfile:
            self.config.write( configfile )
    
    def dev_ADB_test( self ):
        self.label_formula.setText( "目前此按鈕無功能" )
        x , y = win32api.GetCursorPos()
        print( 'mouse position: (%4d, %4d)' % ( x , y ) )
        x += 20
        y -= 10
        win32api.SetCursorPos( ( x , y ) )
    
    def farm_wheat_switch( self ):
        self.farm_exe.wheat_switch()
        self.farm_exe.wheat_num1 = int( self.farm_wheat_1_Edit.text() )
        self.farm_exe.wheat_num2 = int( self.farm_wheat_2_Edit.text() )
        self.farm_exe.button_plant_wheat = not self.farm_exe.button_plant_wheat
        if not self.farm_exe.alive():
            self.farm_exe.start()
    
    def farm_order_switch( self ):
        self.farm_exe.button_order = not self.farm_exe.button_order
        self.farm_exe.info_signal.emit( "傳真訂單-藍單 " + str( self.farm_exe.button_order ) )
        if not self.farm_exe.alive():
            self.farm_exe.start()
    
    def screenRecording_recording_switch( self ):
        self.screenRecording_recording_mode = not self.screenRecording_recording_mode
        # print( 'GUI recording mode: ' , self.screenRecording_recording_mode )
        # print( 'Alive: ' , self.screenRecording_exe.alive() )
        self.screenRecording_exe.set_screenshot_save_mode( self.screenRecording_recording_mode )
        if self.screenRecording_recording_mode:
            self.screenRecording_info_label.setText( '正在錄影' )
        else:
            self.screenRecording_info_label.setText( '停止錄影' )
        # self.farm_exe.info_signal.emit( "傳真訂單-藍單 " + str( self.farm_exe.button_order ) )
        if not self.screenRecording_exe.alive():
            self.screenRecording_exe.start()
        
        
    
    def dev_check_game_status( self ):
        # TODO: adb_socket.py -> adb_client.py
        # self.adb_exe.shell_signal.emit( "check_app_status,com.play.rogt/com.Ro.Ro.UnityPlayerActivity" )
        pass
        
    
    def send_LINE_message_slot( self ):
        message = self.LINE_LineEdit.text()
        self.send_LINE_message( message.strip() )
        self.LINE_LineEdit.setText( '' )
        # 恢復 Tab, 跳出後, 在取消 Tab
        self.screenshotButton.setFocusPolicy( Qt.TabFocus )
        self.focusNextChild()
        self.screenshotButton.setFocusPolicy( Qt.NoFocus )
    
    def send_LINE_message( self , message ):
        if len( message ) > 0 and len( self.LINE_token ) > 0 and len( self.LINE_send_to ) > 0:
            pushUrl = 'https://api.line.me/v2/bot/message/push'
            headers = { 
                "Authorization" : self.LINE_token ,
                "Content-Type"  : "application/json" 
            }
            upload_data = ( {
                "to"        : self.LINE_send_to ,
                "messages"  : [ { 
                    "type": "text",
                    "text": message
                } ] 
            } )
            r = requests.post( pushUrl , data = json.dumps( upload_data ) , headers = headers )
            
            if r.status_code == 200:
                self.label_formula.setText( "成功發送訊息" )
            else:
                self.label_formula.setText( "發送失敗" )
    
    def get_screenshot_filename( self ):
        while True:
            filename = os.path.join( self.dev_screenshot_path , self.screenshot_filename_format.format( self.screenshot_id ) )
            self.screenshot_id += 1
            if not os.path.isfile( filename ):
                return filename
    
    def get_ADB_screenshot_filename( self ):
        while True:
            filename = os.path.join( self.ADB_screenshot_path , self.ADB_screenshot_filename_format.format( self.ADB_screenshot_id ) )
            self.ADB_screenshot_id += 1
            if not os.path.isfile( filename ):
                return filename
    
    def get_ADB_screenshot( self ):
        if not self._invoked_ADB_screenshot:
            self._invoked_ADB_screenshot = True
            QMetaObject.invokeMethod( self , '_process_ADB_screenshot' , Qt.QueuedConnection )
            print('invoked: _process_ADB_screenshot')
        else:
            print('received: waiting...')
    
    @pyqtSlot()
    def _process_ADB_screenshot( self ):
        t1 = time.time()
        # QueuedConnection, DirectConnection
        # QMetaObject.invokeMethod( self.adb_exe, '_process_image', Qt.QueuedConnection )
        # TODO: adb_socket.py -> adb_client.py
        # self.adb_exe.get_image_signal.emit()
        # self.adb_exe.cmd( 'screenshot' , '' )
        img = self.adb_exe.get_screenshot()
        print( 'ADB_screenshot time: %.1f (ms)' % ( ( time.time() - t1 ) * 1000 ) )
        self._process_get_ADB_screenshot( img )
    
    
    def _process_get_ADB_screenshot( self , img ):
        print( 'self.UI_list.currentRow(): ' , self.UI_list.currentRow() )
        if self.UI_list.currentRow() == -1:
            self.imageScreenshotUpdated.emit( img )
        
        self.ADB_imagebox_item_widget.image_data_slot( img )
        
        if self.ADB_screenshot_do:
            img.save( self.get_ADB_screenshot_filename() )
        
        self._invoked_ADB_screenshot = False
    
    def get_screenshot( self ):
        if not self._invoked_screenshot:
            self._invoked_screenshot = True
            QMetaObject.invokeMethod( self , '_process_screenshot' , Qt.QueuedConnection )
            print('invoked: _process_screenshot')
        else:
            print('received: waiting...')
    
    @pyqtSlot()
    def _process_screenshot( self ):
        tries = 3 # 最多重複擷取三次
        while tries > 0:
            t1 = time.time()
            img = ImageGrab.grab( bbox = ( 402 , 233 , 838 , 525 ) )
            if self.screenshot_do:
                img.save( self.get_screenshot_filename() )
            imgByteArr = io.BytesIO()
            img.save( imgByteArr , format = 'PNG' )
            qimg = QImage.fromData( imgByteArr.getvalue() , "PNG" )
            # qimg = QImage( ImageQt.ImageQt( img ) )  ==>  Bug not fix
            self.imageScreenshotUpdated.emit( qimg )
            formula , answer = self.ocr.get_OCR_result( qimg )
            print( formula , answer )
            if answer:
                self.label_formula.setText( formula + " = " + str( answer ) )
                self.create_click_answer_work( answer )
                return # 成功處理算式，離開
            else:
                self.label_formula.setText( formula + ( '. 花費 %.3f 秒' % ( time.time() - t1 ) ) )
            tries -= 1
        
        self._process_screenshot_end()
    
    def _process_screenshot_end( self ):
        self._invoked_screenshot = False
    
    def create_click_answer_work( self , answer ):
        self.backend_click_answer = BackendThread_click_answer( str( answer ) + "v" )
        self.backend_click_answer.endSignal.connect( self._process_screenshot_end )
        self.backend_click_answer.start()
    
    def ADB_connect( self ):
        # TODO: adb_socket.py -> adb_client.py
        # self.adb_exe.set_device_name_signal.emit( self.ADB_address_Edit.text() )
        self.adb_exe.set_device_name( self.ADB_address_Edit.text() )
    
    @pyqtSlot( str )
    def farm_info( self , info ):
        self.farm_time_label.setText( info )
    
    def screenRecording_prevent_lock_desktop_switch( self ):
        if self.screenRecording_prevent_lock_desktop_CheckBox.isChecked():
            self.screenRecording_exe.set_prevent_pause_mode( True )
        else:
            self.screenRecording_exe.set_prevent_pause_mode( False )
        
        if not self.screenRecording_exe.alive():
            self.screenRecording_exe.start()
    
    def screenRecording_screenshot( self ):
        self.screenRecording_exe.get_screenshot()
        if not self.screenRecording_exe.alive():
            self.screenRecording_exe.start()
    
    def tabooNovel_info( self , _s ):
        self.tabooNovel_infomation_PTE.appendPlainText( "%s %s" % ( time.strftime( "[%Y-%m-%d %H:%M:%S]" , time.localtime() ) , _s ) )
    
    def tabooNovel_download_fun( self ):
        if self.tabooNovel_downloader.isAlive() == False:
            self.tabooNovel_downloader.setUrl( self.tabooNovel_url_Edit.text() )
            self.tabooNovel_downloader.start()
        else:
            self.tabooNovel_info( "Already processing..." )


class BackendThread_click_answer( QThread ):
    endSignal = pyqtSignal()
    def __init__( self , answer , parent = None ):
        QThread.__init__( self , parent )
        self.answer = answer

    def run( self ):
        # X: 792, 856, 921, 985
        # Y: 393, 459, 524
        kp = { "1" : [ 792 , 393 ] , "2" : [ 856 , 393 ] , "3" : [ 921 , 393 ] ,
               "4" : [ 792 , 459 ] , "5" : [ 856 , 459 ] , "6" : [ 921 , 459 ] , "0" : [ 985 , 459 ] ,
               "7" : [ 792 , 524 ] , "8" : [ 856 , 524 ] , "9" : [ 921 , 524 ] , "v" : [ 985 , 524 ] }
        # 回答問題
        pyautogui.click( x = random.randint( 575 , 680 ) , y = random.randint( 375 , 395 ) , duration = random.randint( 1 , 5 ) / 10 ) # Y: 369~404
        # answer
        for a in self.answer:
            pos = kp[ a ]
            pyautogui.click( x = pos[ 0 ] + random.randint( -15 , 15 ) , y = pos[ 1 ] + random.randint( -15 , 15 ) , duration = random.randint( 1 , 5 ) / 10 )
        
        # 確定
        pyautogui.click( x = random.randint( 575 , 680 ) , y = random.randint( 465 , 490 ) , duration = random.randint( 1 , 10 ) / 10 ) # Y: 458~498
        
        # 手掌 ( 761 , 290 )
        pyautogui.click( x = random.randint( 758 , 764 ) , y = random.randint( 287 , 293 ) , duration = random.randint( 1 , 5 ) / 10 ) # Y: 458~498
        
        self.endSignal.emit()

class TabooNovelDownload( QThread ):
    def __init__( self , tabooNovel_save_path , info , parent = None ):
        QThread.__init__( self , parent )
        self.info = info
        self.tabooNovel_save_path = tabooNovel_save_path
        self.isWork = False
    
    def tabooNovel_session_get( self , url ):
        # if proxies[ 0 ] == {} :
            # time.sleep( max( 0 , timestamp + random.randint( 1 , 5 ) - time.time() ) )
        # else:
            # time.sleep( max( 0 , timestamp + random.randint( 1 , 2 ) - time.time() ) )
        time.sleep( max( 0 , self.tabooNovel_timestamp + random.randint( 3 , 7 ) - time.time() ) )
        while True:
            # headers[ 'User-Agent' ] = ua.random
            # headers[ 'User-Agent' ] = ua.google
            # IP = get_proxy()
            # proxies = { 'http' : 'http://' + IP , 'https' : 'http://' + IP }
            proxies = {}
            try:
                r = self.tabooNovel_session.get( url , headers = self.tabooNovel_headers , proxies = proxies , timeout = 2 )
                status_code = r.status_code
            except:
                status_code = -1
            if status_code == 401:
                sleep_time = 10 + random.randint( 0 , 10 )
                self.info( 'Sleep %d secs. status_code: %d' % ( sleep_time , status_code ) )
                time.sleep( sleep_time )
                # proxy_add_time( IP , 10 + random.randint( 0 , 10 ) )
            elif status_code == 200:
                break
            elif status_code in self.tabooNovel_block_connect :
                # proxy_add_time( IP , 3600 )
                sleep_time = 120 + random.randint( 0 , 60 )
                self.info( 'Sleep %d secs. status_code: %d' % ( sleep_time , status_code ) )
                time.sleep( sleep_time )
            else:
                sleep_time = 300 + random.randint( 0 , 60 )
                self.info( 'Sleep %d secs. other status_code: %d' % ( sleep_time , status_code ) )
                time.sleep( sleep_time )
                # proxy_add_time( IP , 30 + random.randint( 0 , 10 ) )
                # print( 'status code: ' , status_code )
                pass
        self.tabooNovel_timestamp = time.time()
        return r
    
    def isAlive( self ):
        return self.isWork == True
    
    def setUrl( self , url ):
        self.tabooNovel_url = url
    
    def run( self ):
        self.isWork = True
        # self.tabooNovel_save_path
        self.tabooNovel_block_connect = [ 429 , 403 , 404 , 407 ]
        self.tabooNovel_session = requests.Session()
        self.tabooNovel_timestamp = time.time() - 1000
        
        self.tabooNovel_headers = {}
        fp = open( "profile\\tabooNovel_header.txt" , "r" , encoding = "utf-8" )
        for line in fp.readlines():
            [ d1 , d2 ] = line.split( '\n' )[ 0 ].split( ': ' )
            self.tabooNovel_headers[ d1 ] = d2

        fp.close()
        self.info( "Success to load header." )
        
        response_menu = self.tabooNovel_session_get( self.tabooNovel_url )
        soup = bs( response_menu.text , 'html.parser' )
        
        # Get file name
        tag_span_list = soup.select( '.top span' )
        file_name = tag_span_list[ 1 ].decode_contents() + "_" + tag_span_list[ 0 ].decode_contents()
        self.info( 'File name: %s' % file_name )
        
        novel_chapter_list = []
        for tag_a in soup.select('div.list a'):
            novel_chapter_list.append( [ urllib.parse.urljoin( self.tabooNovel_url , tag_a.get( "href" ) ) , tag_a.decode_contents() ] )
        
        content = [ '' ] * len( novel_chapter_list )
        
        with open( os.path.join( self.tabooNovel_save_path , file_name + ".txt" ) , "w" , encoding = "utf-8" ) as fp:
            res = ""
            fp_c = 0
            for index in range( len( novel_chapter_list ) ):
                url = novel_chapter_list[ index ][ 0 ]
                response_content = self.tabooNovel_session_get( url )
                soup = bs( response_content.text , 'html.parser' )
                # title
                self.info( soup.select( 'h1' )[ 0 ].decode_contents() )
                res = ( "Chaper %5d\n\n" % ( index + 1 ) ) + soup.select( 'h1' )[ 0 ].decode_contents() + '\n\n'
                # content
                ss = str( soup.select( '#content' )[ 0 ].decode_contents() ).strip()
                ss_len = len( ss ) + 1
                while ss.find( '&' ) != -1 and len( ss ) < ss_len:
                    ss_len = len( ss )
                    ss = html.unescape( ss ).strip()
                
                ss = re.sub( r'<[/]{0,1}[a-zA-Z]{0,}?>' , r'\n' , ss )
                ss = re.sub( r'<!--.{0,7}-->' , r'\n' , ss )
                res += ss
                fw_len = fp.write( res + "\n\n" )
                
                # Refresh headers 'Referer'
                self.tabooNovel_headers[ 'Referer' ] = url
                fp_c += 1
                if fp_c >= 10:
                    fp.flush()
                    fp_c = 0
        
        # blank
        self.info( "Process file blank..." )
        fp = open( os.path.join( self.tabooNovel_save_path , file_name + ".txt" ) , "r" , encoding = "utf-8" )
        lines = fp.readlines()
        fp.close()

        fp = open( os.path.join( self.tabooNovel_save_path , file_name + ".txt" ) , "w" , encoding = "utf-8" )
        for line in lines:
            ss = line.strip()
            if len( ss ) > 0:
                fw_len = fp.write( ss + "\n\n" )

        fp.close()
        self.info( "Finish to download. %s" % file_name )
        self.isWork = False
         
if __name__ == "__main__":
    app = QApplication( sys.argv )
    ex = Main_Widget()
    sys.exit( app.exec_() )

