#!/usr/bin/env python
# coding: utf-8

# ### Download and Plot the Latest US Treasury Bonds Yield Curve

# In[1]:


import pandas as pd
import plotly.express as px
import datetime
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np


# ### Helper Functions

# In[14]:


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


# In[3]:


this_year = str(datetime.date.today().year)


# ### Get Latest Bond Yield Data from US Dept. of Treasury

# In[4]:


ustd_url = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/"+this_year+"/all?type=daily_treasury_yield_curve&field_tdr_date_value="+this_year+"&page&_format=csv"
yield_curve_df = pd.read_csv(ustd_url)


# ### Create Data Series

# In[5]:


print('Yield Data:')
# display(yield_curve_df)
yc_1 = yield_curve_df.copy(deep=True)
yc_1['Date'] = pd.to_datetime(yc_1['Date'])
yc_1 = yc_1.set_index('Date')
# print(yc_1.index)
for i in range(1,len(yc_1.columns)): 
    yc_1.iloc[1:,i] = pd.to_numeric(yc_1.iloc[1:,i],errors='coerce') 
# yc_1.info()
yc_1_diff = round(yc_1.pct_change(periods=1)*100,3)
yc_1_diff.dropna()
yc_1.iloc[:8,4:]


# ### Check Long-End vs. Short End Crossing

# In[15]:


crossing_series, crossed_up, crossed_down=find_crossings(yc_1['10 Yr'],yc_1['30 Yr'])

plot_crossing_series(series2=yc_1['10 Yr'],series1=yc_1['30 Yr'],
                     crossed_up=crossed_up,crossed_down=crossed_down)


# ### Check for other Anomalies in the Long-Short Curves Data

# In[23]:


# Plot all
yc_1[['2 Yr','10 Yr']].plot(figsize=(10,6),grid=True,
                            lw=2,xlabel='Date',ylabel='% Yield',
                            title="T-Bonds Yields (%) Comparison")
yc_1_diff[['2 Yr','10 Yr']].plot(figsize=(10,6),grid=True,
                                 lw=2,xlabel='Date',ylabel='Changes (%) in Yields',
                                 title="Changes (%) in T-Bonds Yields")

plt.show()


# ### T-Bonds Vs. S&P 500 

# In[24]:


fig, ax = plt.subplots(2,1,figsize=(10,6),sharex=True)
yc_1[['5 Yr','10 Yr','30 Yr']].plot(ax=ax[0],grid=True,
                            lw=2,xlabel='Date',ylabel='% Yield',
                            title="T-Bonds Yields (%) Comparison")

start_date = yc_1.index[-1].strftime("%Y-%m-%d")
df_sp500 = yf.Ticker('^GSPC').history(start=start_date,interval='1d')['Close']


df_sp500.plot(ax=ax[1],grid=True,
                            lw=2,xlabel='Date',ylabel='Price',
                            title="S&P 500 Closing Prices")
plt.show()


# ### Re-Formating and Cleaning the Data into a DataFrame

# In[26]:


yield_curve_df2 = yield_curve_df.reset_index()
yield_curve_df2 = yield_curve_df2.T
yield_curve_df2 = yield_curve_df2.reset_index()

yield_curve_df2 = yield_curve_df2.drop([0])
yield_curve_df2.iloc[0,0] = 'Maturity'
cols = [str(x) for x in yield_curve_df2.iloc[0,:]]


# In[27]:


yield_curve_df2.columns = cols
yield_curve_df2 = yield_curve_df2.iloc[1:,:].copy()
yield_curve_df2.reset_index(inplace=True)
yield_curve_df2.drop(['index'],axis=1,inplace=True)
yield_curve_df2 = yield_curve_df2.set_index('Maturity')
yield_curve_df2


# ### Plot the Most Recent Yield Curves

# In[28]:


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


# In[25]:


yield_curve_df2.iloc[-8:,:5].plot(figsize=(20,10),title="US Treasury Bonds Yield Curve",ylabel='% Yield',
                     xlabel='Bond Maturities',grid=True)
plt.show()

