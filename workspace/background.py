import win32api
import win32gui
import win32con
from PIL import Image
import win32ui
from PyQt5.QtCore import QEventLoop , QTimer

class background:
    def __init__( self ):
        pass
    
    def get_children_hWnd( self , hWnd_parent = None ):
        hWndList = []
        if hWnd_parent is None:
            win32gui.EnumWindows( lambda hWnd , param : param.append( hWnd ) , hWndList )
        else:
            win32gui.EnumChildWindows( hWnd_parent , lambda hWnd , param: param.append( hWnd ) , hWndList )
        
        return hWndList
    
    def get_hWnd_attribute( self , hWnd = None ):
        if hWnd is None:
            hWndList = self.get_children_hWnd()
            return [ { 'title' : win32gui.GetWindowText( h ) , 'class' : win32gui.GetClassName( h ) , 'handle' : h } for h in hWndList ]
        elif type( hWnd ) is list:
            return [ { 'title' : win32gui.GetWindowText( h ) , 'class' : win32gui.GetClassName( h ) , 'handle' : h } for h in hWnd ]
        
        return { 'title' : win32gui.GetWindowText( hWnd ) , 'class' : win32gui.GetClassName( hWnd ) , 'handle' : hWnd }
    
    def search( self , className = None , titleName = None ):
        window_list = self.get_hWnd_attribute()
        if 0 == len( window_list ):
            return 0
        
        if ( className is None ) and ( titleName is None ):
            pass
        elif className is None:
            window_list = [ w for w in window_list if titleName in w[ 'title' ] ]
        elif titleName is None:
            window_list = [ w for w in window_list if className in w[ 'class' ] ]
        else:
            window_list = [ w for w in window_list if ( className in w[ 'class' ] ) and ( titleName in w[ 'title' ] ) ]
        
        if len( window_list ):
            return window_list[ 0 ][ 'handle' ]
        
        return 0
    
    def searchAll( self , className = None , titleName = None ):
        window_list = self.get_hWnd_attribute()
        if 0 == len( window_list ):
            return 0
        
        if ( className is None ) and ( titleName is None ):
            pass
        elif className is None:
            window_list = [ w for w in window_list if titleName in w[ 'title' ] ]
        elif titleName is None:
            window_list = [ w for w in window_list if className in w[ 'class' ] ]
        else:
            window_list = [ w for w in window_list if ( className in w[ 'class' ] ) and ( titleName in w[ 'title' ] ) ]
        
        if len( window_list ):
            return [ w[ 'handle' ] for w in window_list ]
        
        return 0
    
    def get_screen_size( self ):
        """
        # ????????????
        # return [ ???, ??? ]
        """
        # MoniterDev = win32api.EnumDisplayMonitors(None, None) # ?????????????????????
        return [ win32api.GetSystemMetrics( win32con.SM_CXSCREEN ) , win32api.GetSystemMetrics( win32con.SM_CYSCREEN ) ]
    
    def get_window_Rect( self , hWnd = 0 ):
        left , top , right , bot = win32gui.GetWindowRect( hWnd )
        return [ left , top , right , bot ]
    
    def window_capture( self , hWnd = 0 , bbox = None ):
        """
        hWnd = ??????????????????0???????????????????????????
        """
        # ????????????????????????????????????????????????DC???Divice Context???
        hWndDC = win32gui.GetWindowDC( hWnd )
        # ???????????????DC??????mfcDC
        mfcDC = win32ui.CreateDCFromHandle( hWndDC )
        # mfcDC??????????????????DC
        saveDC = mfcDC.CreateCompatibleDC()
        # ????????????
        screen_size = self.get_window_Rect( hWnd )
        if bbox is None:
            x = 0
            y = 0
            w = screen_size[ 2 ] - screen_size[ 0 ]
            h = screen_size[ 3 ] - screen_size[ 1 ]
        else:
            x = bbox[ 0 ]
            y = bbox[ 1 ]
            w = bbox[ 2 ] - bbox[ 0 ]
            h = bbox[ 3 ] - bbox[ 1 ]
        
        # ?????? bitmap ??????????????????
        dataBitMap = win32ui.CreateBitmap()
        # ???bitmap????????????
        dataBitMap.CreateCompatibleBitmap( mfcDC , w , h )
            
        # ??????saveDC?????????????????????saveBitmap???
        saveDC.SelectObject( dataBitMap )
        
        # ?????????????????????x, y???????????????w???h????????????, ????????? saveDC saveDC_img_pos( 0 , 0 )
        saveDC_img_pos = ( 0 , 0 )
        saveDC.BitBlt( saveDC_img_pos , ( w , h ) , mfcDC , ( x , y ) , win32con.SRCCOPY )
        # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0) 
        
        # dataBitMap.SaveBitmapFile( saveDC , filename ) # ??????
        bmpinfo = dataBitMap.GetInfo()
        bmpstr = dataBitMap.GetBitmapBits( True )
        img = Image.frombuffer(
            'RGB' ,
            ( bmpinfo[ 'bmWidth' ] , bmpinfo[ 'bmHeight' ] ) ,
            bmpstr , 'raw' , 'BGRX' , 0 , 1 )
        
        # ???????????????????????????????????????
        
        win32gui.DeleteObject( dataBitMap.GetHandle() )
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC( hWnd , hWndDC )
        return img
    
    def get_cursor_position( self ):
        return win32api.GetCursorPos()
    
    def mouse_move( self , x , y ):
        win32api.SetCursorPos( ( x , y ) )
    
    def delay( self , time_ms ):
        remaining_time_ms = time_ms
        while remaining_time_ms > 0:
            if remaining_time_ms >= 100:
                dt = 100
            else:
                dt = remaining_time_ms
            
            loop = QEventLoop()
            QTimer.singleShot( dt , loop.quit )
            loop.exec_()
            remaining_time_ms -= dt
    
    def click( self , hWnd = None , x = None , y = None , duration = 0 ):
        """
        duration: ???????????????????????? (ms)
        """
        if hWnd is None:
            return False
        if x is None:
            x = 0
        if y is None:
            y = 0
        
        # ?????????????????? ?????????????????????
        long_position = win32api.MAKELONG( x , y )
        # ??????????????????
        win32api.SendMessage( hWnd , win32con.WM_LBUTTONDOWN , win32con.MK_LBUTTON , long_position )
        self.delay( duration )
        # ??????????????????
        win32api.SendMessage( hWnd , win32con.WM_LBUTTONUP , win32con.MK_LBUTTON , long_position )
        
        return True

    

if __name__ == "__main__":
    app = QApplication( sys.argv )
    hwndL = list( set( background().searchAll( None , '???????????????' ) ) & set( background().searchAll( None , 'Facebook' ) ) )
    img = background().window_capture( hwndL[ 0 ] )
    
    imgbox = ImageboxWidget( title_name = "test" )
    imgbox.setImage( img )
    
    
    
    
    