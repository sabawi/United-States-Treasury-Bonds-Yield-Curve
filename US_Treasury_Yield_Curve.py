#!/usr/bin/env python
# coding: utf-8

# ### Download and Plot the Latest US Treasury Bonds Yield Curve

# In[121]:


import pandas as pd
import plotly.express as px
import datetime
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np


# ### Helper Functions

# In[122]:


def find_crossings(series1, series2):
    # Find the crossings of Series 1 and Series 2
    crossing_series = pd.Series([0] * len(series1), index=series1.index)
    for i in range(1, len(series1)):
        if ((series1.iloc[i-1] < series2.iloc[i-1]) and (series1.iloc[i] >= series2.iloc[i])):
            crossing_series.iloc[i] = 1
        elif ((series1.iloc[i-1] >= series2.iloc[i-1]) and (series1.iloc[i] < series2.iloc[i])):
            crossing_series.iloc[i] = -1

    # print(series2)
    cross_up = []
    cross_down = []
    for i in series1.index: 
        if crossing_series.loc[i] == 1 : 
            cross_up.append(series1.loc[i])
            cross_down.append(np.nan)
        elif crossing_series.loc[i] == -1:
            cross_down.append(series1.loc[i])
            cross_up.append(np.nan)
        else:
            cross_down.append(np.nan)
            cross_up.append(np.nan)
        

    return crossing_series,cross_up,cross_down

def plot_crossing_series(series1,series2,crossed_up,crossed_down):
    ax = series1.plot(figsize=(15,6))
    ax.grid(True)
    series2.plot(ax=ax)
    
    # Plot the corressing up and down
    ax.plot(series1.index,crossed_up,marker='^',color='green', 
                markersize = 12, linewidth = 0, label = f'{series1.name} Crossed Up')
    ax.plot(series1.index,crossed_down,marker='v',color='red', 
                    markersize = 12, linewidth = 0, label = f'{series1.name} Crossed Down')
    ax.legend()
    ax.grid(which='both')


# In[123]:


last_five_years = [str(int(datetime.date.today().year) - i) for i in range(0, 6)]
this_year = last_five_years[0]


# ### Get Latest Bond Yield Data from US Dept. of Treasury

# In[129]:


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
    


# In[130]:


ax = yield_curves.plot(figsize=(20,12),grid=True,xlabel='Dates',ylabel='Yields (%)',
                  title='US T Bonds Yields for Each Maturity',fontsize=12)
xtick = pd.date_range( start=yield_curves.index.min( ), end=yield_curves.index.max( ), freq='M' )
ax.set_xticks( xtick, minor=True )
ax.grid('on', which='minor', axis='x' )


# ### Create Data Series

# In[131]:


# print('Yield Data:')
# # display(yield_curve_df)
# yc_1 = yield_curve_df.copy(deep=True)
# yc_1['Date'] = pd.to_datetime(yc_1['Date'])
# yc_1 = yc_1.set_index('Date')
# # print(yc_1.index)
# for i in range(1,len(yc_1.columns)): 
#     yc_1.iloc[1:,i] = pd.to_numeric(yc_1.iloc[1:,i],errors='coerce') 
# # yc_1.info()
# yc_1_diff = round(yc_1.pct_change(periods=1)*100,3)
# yc_1_diff.dropna()
yield_curves.iloc[:8,4:]


# ### Check Long-End vs. Short End Crossing

# In[132]:


crossing_series, crossed_up, crossed_down=find_crossings(yield_curves['2 Yr'],yield_curves['10 Yr'])

plot_crossing_series(series2=yield_curves['2 Yr'],series1=yield_curves['10 Yr'],
                     crossed_up=crossed_up,crossed_down=crossed_down)
plt.show()

crossing_series, crossed_up, crossed_down=find_crossings(yield_curves['10 Yr'],yield_curves['30 Yr'])

plot_crossing_series(series2=yield_curves['10 Yr'],series1=yield_curves['30 Yr'],
                     crossed_up=crossed_up,crossed_down=crossed_down)
plt.show()


crossing_series, crossed_up, crossed_down=find_crossings(yield_curves['2 Yr'],yield_curves['30 Yr'])

plot_crossing_series(series2=yield_curves['2 Yr'],series1=yield_curves['30 Yr'],
                     crossed_up=crossed_up,crossed_down=crossed_down)
plt.show()


# ### Check for other Anomalies in the Long-Short Curves Data

# In[133]:


# Plot all
yield_curves[['2 Yr','10 Yr']].plot(figsize=(18,6),grid=True,
                            lw=2,xlabel='Date',ylabel='% Yield',
                            title="T-Bonds Yields (%) Comparison")
yield_curves_diff[['2 Yr','10 Yr']].plot(figsize=(18,6),grid=True,
                                 lw=2,xlabel='Date',ylabel='Changes (%) in Yields',
                                 title="Changes (%) in T-Bonds Yields")

plt.show()


# ### T-Bonds Vs. S&P 500 

# In[134]:


fig, ax = plt.subplots(2,1,figsize=(18,12),sharex=True)
yield_curves[['5 Yr','10 Yr','30 Yr']].plot(ax=ax[0],grid=True,
                            lw=2,xlabel='Date',ylabel='% Yield',
                            title="T-Bonds Yields (%) Comparison")

start_date = yield_curves.index[-1].strftime("%Y-%m-%d")
df_sp500 = yf.Ticker('^GSPC').history(start=start_date,interval='1d')['Close']


df_sp500.plot(ax=ax[1],grid=True,
                            lw=2,xlabel='Date',ylabel='Price',
                            title="S&P 500 Closing Prices")
plt.show()


# In[140]:


corr_with_bond = yield_curves.tz_localize('America/New_York').corrwith(df_sp500)
# corr_with_bond.values
corr_with_bond_df = pd.DataFrame({'Maturities':corr_with_bond.index,'Correlations':corr_with_bond.values})
print("S&P 500 Correlation with Bond Yields :")
print(corr_with_bond_df)
corr_with_bond_df.plot.bar(x='Maturities',y='Correlations',figsize=(12,4),
                           title="S&P 500 Prices Correlation with T Bond Yields",ylabel="Corr with S&P 500",
                           xlabel='T Bonds by Maturity',grid=True)


# ### Re-Formating and Cleaning the Data into a DataFrame

# In[141]:


yield_curve_df2 = yield_curve_y0_df.reset_index()
yield_curve_df2 = yield_curve_df2.T
yield_curve_df2 = yield_curve_df2.reset_index()

yield_curve_df2 = yield_curve_df2.drop([0])
yield_curve_df2.iloc[0,0] = 'Maturity'
cols = [str(x) for x in yield_curve_df2.iloc[0,:]]


# In[142]:


yield_curve_df2.columns = cols
yield_curve_df2 = yield_curve_df2.iloc[1:,:].copy()
yield_curve_df2.reset_index(inplace=True)
yield_curve_df2.drop(['index'],axis=1,inplace=True)
yield_curve_df2 = yield_curve_df2.set_index('Maturity')
yield_curve_df2


# ### Plot the Most Recent Yield Curves

# In[143]:


longest_n_maturities = 8   # For ALL maturities set = len(yield_curve_df2)
last_n_days = 5            # For ALL days in the data set = -1
fig = px.line(yield_curve_df2.iloc[-longest_n_maturities:,:last_n_days],markers=True)

fig.update_layout(
    width=1200,
    height=600,
   title="US Treasury Bonds Yield Curve",
   xaxis_title='Bond Maturity',
   yaxis_title='Interest Rate %',
   legend_title="Curve Date",
   font=dict(
      family="Arial",
      size=20,
      color="blue"
   )
)
fig.show()


# In[144]:


yield_curve_df2.iloc[-8:,:5].plot(figsize=(20,10),title="US Treasury Bonds Yield Curve",ylabel='% Yield',
                     xlabel='Bond Maturities',grid=True)
plt.show()

