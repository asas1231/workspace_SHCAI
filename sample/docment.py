#
enumerate( list )
>> 枚舉 list, ( 0 , list[ 0 ] ), ( 1 , list[ 1 ] ), ..., ( n - 1 , list[ n - 1 ] )
#redis
https://www.cnblogs.com/xuchunlin/p/7097255.html
import redis
redis.zrangebyscore( REDIS_KEY , 11 , 25 )
>> 返回有序集合(11<=value<=25)。有序集成员按分数值递增(从小到大)次序排列。

#list
a = [ 'a' , 1 ]
b = [ 'b' , 2 ]
c = a + b
>> c = [ 'a' , 1 , 'b' , 2 ]
reversed( c )
>> [ 2 , 'b' , 1 , 'a' ]

#dict
https://medium.com/ccclub/ccclub-python-for-beginners-tutorial-533b8d8d96f3
a.update(b)
>> 把 b 加入 a
writer = a.pop('writer')
>> 把 'writer' 從 a 移除
del dict_name[ 'key' ]
removed_value = dict_name.pop( 'key' )

for key in dict:
    print(key)
for key, value in dict.items():
    print(key, value)

#re
https://zh.wikipedia.org/zh-tw/%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F
key = 'new book - qwyd - 5'
bookId_p = re.compile(' ([\d]+)$')
bookId = int( bookId_p.findall( key )[ 0 ] )

s4 = re.sub( s1 = r'' , s2 = r'' , s3 = '' )
>> 回傳 s4, 將 s3 以 s1 為條件搜索, 把符合目標替換成 s2

#ffmpeg
ffmpeg -i concat:"2020-11-17.mkv|2020-11-18.mkv" -c copy "..\video\2020-11.mkv"
>> 合併影片

#ftplib
https://docs.python.org/3/library/ftplib.html

#PIL
https://ithelp.ithome.com.tw/m/articles/10230274
image = Image.open( "ponzo.jpg" )
image.save( "out.jpg" )

#os
with open( self._recent_filename , "a" , encoding = "utf-8" ) as fp:
    fwl = fp.write( self._all_info_str )
    fp.flush()
>> 追加檔案內容
os.system( cmd )
os.path.split( 'FTP.ini' )
>> ( 'PATH' , 'FILE NAME' )
os.path.isfile( 'path\\file' )
>> 檔案是否存在
size = os.path.getsize(path)
>> 檔案大小 size (bytes)
os.path.isdir( 'path\\dir' )
>> 路徑是否存在
os.path.join()
>> 添加路徑
https://yangsijie666.github.io/2018/06/11/%E9%80%9A%E8%BF%87os.statvfs%E8%AE%A1%E7%AE%97%E6%9F%90%E7%9B%AE%E5%BD%95%E7%9A%84%E4%BD%BF%E7%94%A8%E7%8E%87%E7%AD%89/
os.statvfs
>> Unix 系統可用, 資料夾空間訊息, 類似 df
os.listdir( dirpath )
>> 列出指定路徑的檔案、資料夾清單
#sys
argc = len( sys.argv )

#platform
platform.node()
>> 電腦名稱 ex: 'PC3'
platform.system()
>> 作業系統 ex: 'Windows'

#configparser
https://docs.python.org/zh-tw/3.6/library/configparser.html
config = configparser.ConfigParser()

#queue
https://docs.python.org/3.6/library/queue.html
import queue
queue.Queue( maxsize = 0 )
>> 先進先出佇列。可選參數 maxsize 來設定隊列長度。如果 maxsize 小於等於 0 就表示隊列長度無限。
queue.LifoQueue( maxsize = 0 )
>> 先進後出堆疊。可選參數 maxsize 來設定隊列長度。如果 maxsize 小於等於 0 就表示隊列長度無限。
queue.PriorityQueue( maxsize = 0 )
>> 優先級對列。可選參數 maxsize 來設定隊列長度。如果 maxsize 小於等於 0 就表示隊列長度無限。

Queue.put( item [ , block = True [ , timeout = None ] ] )
>> 放置 item 進入 Queue()。block 為 True，會等待有空間可以放置才會執行；block 為 False，則立即判定是否能放置，不能放置會報錯。在 block 為 True，timeout 為正數，則會等待最多 timeout 秒，否則會報錯。
Queue.get( [ block = True [ , timeout = None ] ] )
>> 從隊頭刪除並返回一個項目。block 為 True，會等待有項目才會執行取出；block 為 False，則立即判定是否能取出項目，不能取出會報錯。在 block 為 True，timeout 為正數，則會等待最多 timeout 秒，否則會報錯。

Queue.qsize()
>> 返回 Queue() 大概的大小，不能保證 Queue() 裡的項目數量以及剩餘空間，不能保證 get() 及 put() 是否會阻塞。
Queue.empty()
>> 如果 Queue() 為空，則返回 True，否則返回 False。不能保證 get() 及 put() 是否會阻塞。
Queue.full()
>> 如果 Queue() 已滿，則返回 True，否則返回 False。不能保證 get() 及 put() 是否會阻塞。
Queue.put_nowait( item )
>> 相當於 Queue.put( item , False )
Queue.get_nowait()
>> 相當於 Queue.get( False )
Queue.task_done()
>> 表示先前 Queue() 的任務已完成，由 Queue() 使用者線程使用。使用者線程為使用 get() 取得項目的線程。
Queue.join()
>> 一直阻塞直到 Queue() 裡的項目都被取出或是處理。

#Qt
QPlainTextEdit: https://doc.qt.io/qt-5/qplaintextedit.html

#BeautifulSoup
from bs4 import BeautifulSoup as bs
soup = bs( HTML , 'html.parser' )

title = soup.find( "meta",  property = "og:title" )
title["content"]
url = soup.find( "meta" ,  property = "og:url" )
url["content"]

soup = BeautifulSoup( webpage )
for tag in soup.find_all( "meta" ):
    if tag.get( "property" , None ) == "og:title":
        print( tag.get( "content" , None ) )
    elif tag.get( "property" , None ) == "og:url":
        print( tag.get( "content" , None ) )

img_tag = soup.find_all( "img" , class_ = "FFVAD" )

tag.parent
>> 父節點
for parent in link.parents: 
    if parent is None:
        print( parent ) 
    else: 
        print( parent.name )
輸出: p -> body -> html -> [document] -> None

tag.next_sibling(下一個); tag.previous_sibling(前一個)
>>兄弟節點

#urllib
import urllib
import requests
url = 'http://www.quanwenyuedu.io/n/jiandaoduzun/xiaoshuo.html'
result = urllib.parse.urlparse( url )
result = ParseResult(scheme='http', netloc='www.quanwenyuedu.io', path='/n/jiandaoduzun/xiaoshuo.html', params='', query='', fragment='')

#json
with open( fileName , 'r' , encoding = 'utf-8' ) as fp:
    data = json.loads( fp.read() )

with open( fileName , 'w' , encoding = 'utf-8' ) as fp:
    json.dump( data , fp , separators = ( ',', ':' ) )

#Excel operate
...