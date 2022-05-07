import pandas as pd
import os
import datetime

def highlight_max(s, props=''):
    return np.where(s == np.nanmax(s.values), props, '')

today = datetime.date(2022, 4, 13)
past_date = datetime.date(1900, 1, 1) #Jan 1 1970
print ((today - past_date).days + 1)
fn_1 = os.path.join( 'sample' , 'Spreadsheet_job_0003.xlsx' )
fn_1_tabN = 'S1'
title_1_list = [ 'ID', 'Date', 'Job' ]
fn_2 = os.path.join( 'sample' , 'Spreadsheet_job_0003.xlsx' )
fn_2_tabN = 'S2'
title_2_list = [ 'ID' ]

df_2 = pd.read_excel( fn_2 , sheet_name = fn_2_tabN )
idx_2 = pd.IndexSlice
slice_ = idx_2[ idx_2[ : , 'B01' ] , idx_2[ : , datetime.datetime(2022, 4, 15, 0, 0) ]]
df_2.style.apply(highlight_max, props='color:blue;', axis=0, subset=slice_).set_properties(**{'background-color': '#ffff00'}, subset=slice_)

df_2.to_excel('excel_output.xlsx' , 'asas' )