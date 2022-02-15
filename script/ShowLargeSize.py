import os

dir_path = 'Z:'
folder_size = {} # Byte
folder_subfolder = {}

def SumSize( SumSize_path ):
    global folder_size , folder_subfolder
    folder_size[ SumSize_path ] = 0
    folder_subfolder[ SumSize_path ] = []
    for filenames in os.listdir( SumSize_path ):
        fullpath = os.path.join( SumSize_path , filenames )
        if os.path.isfile( fullpath ):
            folder_size[ SumSize_path ] += os.stat( fullpath ).st_size
        else:
            folder_subfolder[ SumSize_path ].append( filenames )
            SumSize( fullpath )
            folder_size[ SumSize_path ] += folder_size[ fullpath ]
    
    # print( SumSize_path , ':' , folder_size[ SumSize_path ] )

def OptimalSize( value ):
    # Byte -> B, KB, MB, GB, TB
    num = value
    if num < 1024:
        return '{:6.2f}  B'.format( num )
    num /= 1024
    if num < 1024:
        return '{:6.2f} KB'.format( num )
    num /= 1024
    if num < 1024:
        return '{:6.2f} MB'.format( num )
    num /= 1024
    if num < 1024:
        return '{:6.2f} GB'.format( num )
    num /= 1024
    if num < 1024:
        return '{:6.2f} TB'.format( num )
    return '{:6.2f}  B'.format( value )

def Show( dir_path , number , depth ):
    global folder_size , folder_subfolder
    ke = [ os.path.join( dir_path , x ) for x in folder_subfolder[ dir_path ] ]
    rank_sort_key = sorted( ke , key = lambda ke : folder_size[ ke ] , reverse = True )
    count = number
    rec = []
    print( '{}: {}'.format( OptimalSize( folder_size[ dir_path ] ) , dir_path ) )
    for i in rank_sort_key:
        rec.append( i )
        print( '    {}, {:6.2f}%: {}'.format( OptimalSize( folder_size[ i ] ) , 100.0 * folder_size[ i ] / folder_size[ dir_path ] , i ) )
        count -= 1
        if count < 1:
            break
    
    if depth > 1:
        for i in rec:
            print( "" )
            Show( i , number , depth - 1 )
        

folder_size = {} # Byte
folder_subfolder = {}
SumSize( dir_path )
Show( dir_path , 3 , 2 )
