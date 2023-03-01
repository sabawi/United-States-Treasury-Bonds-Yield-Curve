#!/usr/bin/env python
# coding: utf-8

# ### Download and Plot the Latest US Treasury Bonds Yield Curve

# In[66]:


import pandas as pd
import plotly.express as px
import datetime
import matplotlib.pyplot as plt


# In[3]:


this_year = str(datetime.date.today().year)


# In[4]:


ustd_url = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/"+this_year+"/all?type=daily_treasury_yield_curve&field_tdr_date_value="+this_year+"&page&_format=csv"
yield_curve_df = pd.read_csv(ustd_url)


# In[69]:


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
yc_1[['2 Yr','10 Yr']].plot(figsize=(10,6),grid=True,
                            lw=2,xlabel='Date',ylabel='% Yield',
                            title="Yields (%) Comparison")
yc_1_diff[['2 Yr','10 Yr']].plot(figsize=(10,6),grid=True,
                                 lw=2,xlabel='Date',ylabel='Changes (%) in Yields',
                                 title="Changes (%) in Yields")

plt.show()


# ### Re-Formating and Cleaning the Data into a DataFrame

# In[72]:


yield_curve_df2 = yield_curve_df.reset_index()
yield_curve_df2 = yield_curve_df2.T
yield_curve_df2 = yield_curve_df2.reset_index()

yield_curve_df2 = yield_curve_df2.drop([0])
yield_curve_df2.iloc[0,0] = 'Maturity'
cols = [str(x) for x in yield_curve_df2.iloc[0,:]]


# In[73]:


yield_curve_df2.columns = cols
yield_curve_df2 = yield_curve_df2.iloc[1:,:].copy()
yield_curve_df2.reset_index(inplace=True)
yield_curve_df2.drop(['index'],axis=1,inplace=True)
yield_curve_df2 = yield_curve_df2.set_index('Maturity')
yield_curve_df2


# In[74]:


fig = px.line(yield_curve_df2,markers=True)

fig.update_layout(
    width=1200,
    height=800,
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


# In[79]:


yield_curve_df2.plot(figsize=(20,10),title="US Treasury Bonds Yield Curve",ylabel='% Yield',
                     xlabel='Bond Maturities',grid=True)


# In[ ]:




