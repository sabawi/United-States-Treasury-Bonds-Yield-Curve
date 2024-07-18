#!/usr/bin/env python
# coding: utf-8

# ### Download and Plot the Latest US Treasury Bonds Yield Curve
import pandas as pd
import datetime
import yfinance as yf
import numpy as np


last_five_years = [str(int(datetime.date.today().year) - i) for i in range(0, 6)]
this_year = last_five_years[0]

import time

yield_curves = pd.DataFrame()
yield_curves_diff = pd.DataFrame()

for i in range(len(last_five_years)):
    ustd_url = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/"+last_five_years[i]+"/all?type=daily_treasury_yield_curve&field_tdr_date_value="+last_five_years[i]+"&page&_format=csv"
    yield_curve_df = pd.read_csv(ustd_url)
    if('4 Mo' in yield_curve_df.columns):
        yield_curve_df = yield_curve_df.drop('4 Mo',axis=1)
    if i == 0: # Save this year data
        yield_curve_y0_df = yield_curve_df
        
    yc_1 = yield_curve_df.copy(deep=True)
    yc_1['Date'] = pd.to_datetime(yc_1['Date'])
    yc_1 = yc_1.set_index('Date')
    
    for j in range(1,len(yc_1.columns)): 
        yc_1.iloc[1:,j] = pd.to_numeric(yc_1.iloc[1:,j],errors='coerce') 
        
    yield_curves = pd.concat([yield_curves,yc_1])
    # yield_curves = y.groupby(level=0)
    
    yc_1_diff = round(yc_1.pct_change(periods=1)*100,3)
    yc_1_diff.dropna()
    
    yield_curves_diff = pd.concat([yield_curves_diff,yc_1_diff])
    # yield_curves_diff = yd.groupby()
    
    # print(yield_curves)
    print(".", end='')
    time.sleep(2)
    

ax = yield_curves.plot(figsize=(20,12),grid=True,xlabel='Dates',ylabel='Yields (%)',
                  title='US T Bonds Yields for Each Maturity',fontsize=12)
xtick = pd.date_range( start=yield_curves.index.min( ), end=yield_curves.index.max( ), freq='ME' )
ax.set_xticks( xtick, minor=True )
ax.grid('on', which='minor', axis='x' )

print('\n\n')
print('US Treasury Bonds Interest Rates:')
print(yield_curves.iloc[:8,4:])