#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


#import libraries 
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
plt.style.use('ggplot')
import matplotlib.dates as mdates
from matplotlib.ticker import ScalarFormatter


# In[3]:


#read datasets: GlassNode Data

#BTC Datasets
ADR = pd.read_csv('new-addresses-btc-24h.csv')
BTC = pd.read_csv('price-btc-24h.csv')
Mcap = pd.read_csv('market-cap-btc-24h.csv')
Rcap = pd.read_csv('realized-cap-btc-24h.csv')
CoinDes = pd.read_csv('coin-days-destroyed-cdd-btc-24h.csv')
Whales = pd.read_csv('addresses-with-balance-≥-1-k-btc-24h.csv')

#ETH Datasets
BTC_price = pd.read_csv('price-btc-24h.csv')
ETH = pd.read_csv('price-eth-24h.csv')
ETH_ADR = pd.read_csv('new-addresses-eth-24h.csv')
ETH_Mcap = pd.read_csv('market-cap-eth-24h.csv')
ETH_Rcap = pd.read_csv('realized-cap-eth-24h.csv')
ETH_CoinDes = pd.read_csv('coin-days-destroyed-cdd-eth-24h.csv')
ETH_Whales = pd.read_csv('addresses-with-balance-≥-10-k-eth-24h.csv')


# In[4]:


#create BTC Dataset 

#Merge BTC data into one DF
BTC = pd.merge(BTC, ADR, on = 'timestamp', how = 'inner')
BTC = pd.merge(BTC, Mcap, on = 'timestamp', how = 'inner')
BTC = pd.merge(BTC, Rcap, on = 'timestamp', how = 'inner')
BTC = pd.merge(BTC, CoinDes, on = 'timestamp', how = 'inner')
BTC = BTC = pd.merge(BTC, Whales, on = 'timestamp', how = 'inner')

#rename columns
BTC.columns=['Date', 'BTC Close', 'New ADR','MCAP', 'RCAP', 'Coin Days Destroyed', 'Whales']

#add daily returns, and fwd (30,60,90) day return columns

#daily returns
BTC['BTC % COD']= round(BTC[['BTC Close']].pct_change(1)*100,2)

#forward returns 
BTC['BTC Fwd 30D % Ret'] = round((BTC['BTC Close'].shift(-30) / BTC['BTC Close'] - 1).fillna(0)*100,2)
BTC['BTC Fwd 60D % Ret'] = round((BTC['BTC Close'].shift(-60) / BTC['BTC Close'] - 1).fillna(0)*100,2)
BTC['BTC Fwd 90D % Ret'] = round((BTC['BTC Close'].shift(-90) / BTC['BTC Close'] - 1).fillna(0)*100,2)
BTC['BTC Fwd 180D % Ret'] = round((BTC['BTC Close'].shift(-180) / BTC['BTC Close'] - 1).fillna(0)*100,2)

#add column of 90 day rolling sum of coin days destroyed 
BTC['CD 90 Roll'] = BTC['Coin Days Destroyed'].rolling(90).sum().fillna(0)

#add MVRV column
BTC['MVRV'] = BTC['MCAP'] / BTC['RCAP']

#add 30-day rolling sum column of new addresses created on network
BTC['ADR 30 day roll sum'] = BTC['New ADR'].rolling(30).sum().fillna(0)

#Format date column to only include Y/M/D values 
BTC['Date'] = BTC['Date'].str[:+10]

#convert date column
BTC['Date'] = pd.to_datetime(BTC['Date'])


# In[5]:


#add 90 day rolling sum coin days destroyed (ETH)
ETH_CoinDes['ETH CD 90 Roll'] = ETH_CoinDes['value'].rolling(90).sum().fillna(0)

#merge datasets
ETH = pd.merge(ETH, BTC_price, on = 'timestamp', how = 'inner')
ETH = pd.merge(ETH, ETH_ADR, on = 'timestamp', how = 'inner')
ETH = pd.merge(ETH, ETH_Mcap, on = 'timestamp', how = 'inner')
ETH = pd.merge(ETH, ETH_Rcap, on = 'timestamp', how = 'inner')
ETH = pd.merge(ETH, ETH_CoinDes, on = 'timestamp', how = 'inner')
ETH = pd.merge(ETH, ETH_Whales, on = 'timestamp', how = 'inner')

#Rename Columns
ETH.columns=['Date', 'ETH Close', 'BTC Close', 'New ADR','MCAP', 'RCAP', 'ETH Coin Days Destroyed','ETH CD 90 Roll', 'Whales']

#add MVRV column
ETH['MVRV'] = ETH['MCAP'] / ETH['RCAP']

#Format date column to only include Y/M/D values 
ETH['Date'] = ETH['Date'].str[:+10]

#daily returns
ETH['BTC % COD']= round(ETH[['BTC Close']].pct_change(1)*100,2)

#forward returns 
ETH['ETH Fwd 30D % Ret'] = round((ETH['ETH Close'].shift(-30) / ETH['ETH Close'] - 1).fillna(0)*100,2)
ETH['ETH Fwd 60D % Ret'] = round((ETH['ETH Close'].shift(-60) / ETH['ETH Close'] - 1).fillna(0)*100,2)
ETH['ETH Fwd 90D % Ret'] = round((ETH['ETH Close'].shift(-90) / ETH['ETH Close'] - 1).fillna(0)*100,2)

#calculate rolling 30 day correlation 
ETH['BTC/ETH 30d Corr'] = ETH['ETH Close'].rolling(30).corr(ETH['BTC Close'])

#add column of ETH/BTC cross
ETH['ETH/BTC'] = ETH['ETH Close'] / ETH['BTC Close']

#add 30-day rolling sum column of new addresses created 
ETH['ADR 30 day roll sum'] = ETH['New ADR'].rolling(30).sum().fillna(0)

#convert date column
ETH['Date'] = pd.to_datetime(ETH['Date'])


# In[57]:


#BTC Price Chart 
fig, ax1 = plt.subplots()
ax1.plot(BTC['Date'],BTC['BTC Close'], color ='blue')
ax1.set_title('BTC: USD Price')
ax1.set_ylabel('USD')
ax1.set_xlabel('Year')
ax1.grid(True)
plt.yscale('log',base=2) 
ax1.get_yaxis().set_major_formatter(ScalarFormatter())
                           
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator(interval = 24))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

ax.vlines(x=['2013-12-10'], ymin=0, ymax=1100, color='r', label='test lines')
ax.vlines(x=['2021-04-10'], ymin=0, ymax=65000, color='r', label='test lines')
ax.vlines(x=['2017-12-12'], ymin=0, ymax=18000, color='r', label='test lines')

plt.show()


# In[54]:


#ETH Price Chart 
fig, ax1 = plt.subplots()
ax1.plot(ETH['Date'],ETH['ETH Close'], color ='blue')
ax1.set_title('ETH: USD Price')
ax1.set_ylabel('USD')
ax1.set_xlabel('Year')
ax1.grid(True)
plt.yscale('log',base=2) 
ax1.get_yaxis().set_major_formatter(ScalarFormatter())

ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator(interval = 12))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

ax.vlines(x=['2018-01-10'], ymin=0, ymax=1000, color='r', label='test lines')
ax.vlines(x=['2021-05-12'], ymin=0, ymax=4300, color='r', label='test lines')

plt.show()


# In[128]:


#2021 charts
#BTC Price Chart 
fig, ax1 = plt.subplots()
ax1.plot(BTC['Date'][3821:],BTC['BTC Close'][3821:], color ='blue')
ax1.set_title('BTC: USD Price')
ax1.set_ylabel('USD')
ax1.set_xlabel('Year')
ax1.grid(True)
plt.yscale('log',base=2) 
ax1.get_yaxis().set_major_formatter(ScalarFormatter())
ax1.set_ylim([0,80000])
ax1.set_yticks([29000,33000,39000,44000,50000,59000,67000])
                           
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator(interval = 2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%y'))

ax.vlines(x=['2021-02-08'], ymin=0, ymax=44000, color='r', label='test lines')
ax.vlines(x=['2021-04-14'], ymin=0, ymax=63000, color='r', label='test lines')
ax.vlines(x=['2021-05-12'], ymin=0, ymax=50000, color='r', label='test lines')


plt.show()


#ETH Price Chart 
fig, ax1 = plt.subplots()
ax1.plot(ETH['Date'][1972:],ETH['ETH Close'][1972:], color ='blue')
ax1.set_title('ETH: USD Price')
ax1.set_ylabel('USD')
ax1.set_xlabel('Year')
ax1.grid(True)
plt.yscale('log',base=2) 
ax1.get_yaxis().set_major_formatter(ScalarFormatter())
ax1.set_ylim([0,5000])
ax1.set_yticks([750, 900,1100,1400,1800,2300,2900,3600, 4500])

ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator(interval = 2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%y'))


plt.show()


# In[8]:


#ETH BTC correlation graph 

fig, ax1 = plt.subplots()
ax1.plot(ETH['Date'][1910:2274],ETH['BTC/ETH 30d Corr'][1910:2274], color ='blue')
ax1.set_title('ETH/BTC: 1y 30D Rolling Correlation')
ax1.set_ylabel('Correlation')
ax1.set_xlabel('Date')
ax1.grid(True)

ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator(interval = 2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%y'))

plt.show()


# In[9]:


#ETH/BTC chart 

fig, ax1 = plt.subplots()
ax1.plot(ETH['Date'],ETH['ETH/BTC'], color ='blue')
ax1.set_title('ETH/BTC')
ax1.set_ylabel('Cross')
ax1.set_xlabel('Year')
ax1.grid(True)

ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator(interval = 12))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.show()


# In[10]:


#BTC/MVRV chart
fig, ax1 = plt.subplots()
ax1.plot(BTC['Date'],BTC['BTC Close'], color ='blue')
ax1.set_title('BTC: MVRV')
ax1.set_ylabel('USD', color='blue')
ax1.set_xlabel('Year')
ax1.grid(True)
plt.yscale('log',base=2)
ax1.get_yaxis().set_major_formatter(ScalarFormatter())

ax2 = ax1.twinx()
ax2.plot(BTC['Date'],BTC['MVRV'], color = 'green')
ax2.set_ylabel('MVRV', color='green')

ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator(interval = 24))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.show()


# In[23]:


#BTC MVRV plot, since 1/01/13
M = BTC[899:].loc[(BTC['MVRV'] > 0)]
sns.jointplot(M['MVRV'], M['BTC Fwd 90D % Ret'])


# In[17]:


#BTC MVRV density plot vs. 90 day fwd. return, 110 days

N = BTC[899:].loc[(BTC['MVRV'] >= 3.5)]
sns.kdeplot(N['BTC Fwd 90D % Ret'], shade = True, label = 'Fwd. Ret. for MVRV > 3.5 since 2013')
plt.legend()
plt.show()
N['BTC Fwd 90D % Ret'].mean(), N['BTC Fwd 90D % Ret'].median()


# In[12]:


#ETH MVRV chart 
fig, ax1 = plt.subplots()
ax1.plot(ETH['Date'],ETH['ETH Close'], color ='blue')
ax1.set_title('ETH: MVRV')
ax1.set_ylabel('USD', color='blue')
ax1.set_xlabel('Year')
ax1.grid(True)
plt.yscale('log',base=2) 
ax1.get_yaxis().set_major_formatter(ScalarFormatter())

ax2 = ax1.twinx()
ax2.plot(ETH['Date'],ETH['MVRV'], color = 'green')
ax2.set_ylabel('MVRV', color='green')

ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator(interval = 12))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.show()


# In[27]:


#ETH MVRV 90 day return plot, since 01/01/17
c = ETH[512:].loc[(ETH['MVRV'] >= 0)]
sns.jointplot(c['MVRV'], c['ETH Fwd 90D % Ret'])


# In[29]:


#ETH density plot, since '17, MVRV>4
d = ETH[512:].loc[(ETH['MVRV'] > 3.5)]
sns.kdeplot(d['ETH Fwd 90D % Ret'], shade = True, label = 'MVRV > 3.5 since 2017')
plt.legend()
plt.show()
d['ETH Fwd 90D % Ret'].mean(), d['ETH Fwd 90D % Ret'].median()


# In[22]:


#BTC Price & CDD 90d roll um

fig, bx1 = plt.subplots()
bx1.plot(BTC['Date'],BTC['BTC Close'], color ='blue')
bx1.set_title('BTC: Coin Days Destroyed (90d Roll Sum)')
bx1.set_ylabel('USD', color='blue')
bx1.grid(True)
plt.yscale('log',base=2) 
bx1.get_yaxis().set_major_formatter(ScalarFormatter())

bx2 = bx1.twinx()
bx2.plot(BTC['Date'],BTC['CD 90 Roll'], color = 'green')
bx2.set_ylabel('CDD (1 bio)', color='green')

bx = plt.gca()
bx.xaxis.set_major_locator(mdates.MonthLocator(interval = 24))
bx.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.show()


# In[23]:


#BTC Price CDD chart, 2016-2019

BTC[2360:3300]

fig, bx1 = plt.subplots()
bx1.plot(BTC[2360:3300]['Date'],BTC[2360:3300]['BTC Close'], color ='blue')
bx1.set_title('BTC: Coin Days Destroyed (90d Roll Sum)')
bx1.set_ylabel('USD', color='blue')
bx1.set_xlabel('Date')
bx1.grid(True)
plt.yscale('log',base=2) 
bx1.get_yaxis().set_major_formatter(ScalarFormatter())

bx2 = bx1.twinx()
bx2.plot(BTC[2360:3300]['Date'],BTC[2360:3300]['CD 90 Roll'], color = 'green')
bx2.set_ylabel('CDD (1 bio)', color='green')

bx = plt.gca()
bx.xaxis.set_major_locator(mdates.MonthLocator(interval = 5))
bx.xaxis.set_major_formatter(mdates.DateFormatter('%m-%y'))

plt.show()


# In[32]:


#BTC fwd. ret. for CDD > 1.5 bio

dd = BTC.loc[(BTC['CD 90 Roll'] > 1.5e9) ]
sns.kdeplot(dd['BTC Fwd 90D % Ret'], shade = True, label = 'Fwd Ret. for 90D CDD > 1.5 bio')
plt.legend()
plt.show()
dd['BTC Fwd 90D % Ret'].mean(), dd['BTC Fwd 90D % Ret'].median()


# In[27]:


#ETH CDD plot

fig, bx1 = plt.subplots()
bx1.plot(ETH['Date'],ETH['ETH Close'], color ='blue')
bx1.set_title('ETH: Coin Days Destroyed (90d Roll Sum)')
bx1.set_ylabel('USD', color='blue')
bx1.grid(True)
plt.yscale('log',base=2) 
bx1.get_yaxis().set_major_formatter(ScalarFormatter())

bx2 = bx1.twinx()
bx2.plot(ETH['Date'],ETH['ETH CD 90 Roll'], color = 'green')
bx2.set_ylabel('CDD 10 bio)', color='green')

bx = plt.gca()
bx.xaxis.set_major_locator(mdates.MonthLocator(interval = 12))
bx.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.show()


# In[33]:


#ETH CDD 90 day fwd return plot, CDD > 10 bio
e = ETH[512:].loc[(ETH['ETH CD 90 Roll'] > 1e10)]
sns.jointplot(e['ETH CD 90 Roll'], e['ETH Fwd 90D % Ret'])
plt.legend()
plt.show()


# In[23]:


#BTC 30 day roll sum new addresses vs price

fig, bx1 = plt.subplots()
bx1.plot(BTC['Date'],BTC['BTC Close'], color ='blue')
bx1.set_title('BTC: Daily New Addresses (30d Roll Sum)')
bx1.set_ylabel('USD', color='blue')
bx1.grid(True)
plt.yscale('log',base=2) 
bx1.get_yaxis().set_major_formatter(ScalarFormatter())

bx2 = bx1.twinx()
bx2.plot(BTC['Date'],BTC['ADR 30 day roll sum'], color = 'green')
bx2.set_ylabel('Roll Sum New ADR 10 mio', color='green')

bx = plt.gca()
bx.xaxis.set_major_locator(mdates.MonthLocator(interval = 24))
bx.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.show()


# In[25]:


#ETH 30 day roll sum new addresses vs price

fig, bx1 = plt.subplots()
bx1.plot(ETH['Date'],ETH['ETH Close'], color ='blue')
bx1.set_title('ETH: Daily New Addresses (30d Roll Sum)')
bx1.set_ylabel('USD', color='blue')
bx1.grid(True)
plt.yscale('log',base=2) 
bx1.get_yaxis().set_major_formatter(ScalarFormatter())

bx2 = bx1.twinx()
bx2.plot(ETH['Date'],ETH['ADR 30 day roll sum'], color = 'green')
bx2.set_ylabel('Roll Sum New ADR: 1 mio', color='green')

bx = plt.gca()
bx.xaxis.set_major_locator(mdates.MonthLocator(interval = 12))
bx.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.show()


# In[33]:


#BTC 30 day roll sum > 15 mio vs fwd return

gg = BTC.loc[(BTC['ADR 30 day roll sum']> 1.5e7) ]
sns.kdeplot(gg['BTC Fwd 90D % Ret'], shade = True, label = 'ADR 30d roll sum > 15mio')
plt.legend()
plt.show()
gg['BTC Fwd 90D % Ret'].median()


# In[35]:


#ETH 30 day roll sum > 5 mio vs fwd return
hh = ETH.loc[(ETH['ADR 30 day roll sum'] > 5e6) ]
sns.kdeplot(hh['ETH Fwd 90D % Ret'], shade = True, label = 'ADR 30d roll sum > 5 mio')
plt.legend()
plt.show()
hh['ETH Fwd 90D % Ret'].mean()


# In[56]:


#BTC price vs whales

fig, bx1 = plt.subplots()
bx1.plot(BTC['Date'],BTC['BTC Close'], color ='blue')
bx1.set_title('BTC: Whales')
bx1.set_ylabel('USD', color='blue')
bx1.grid(True)
plt.yscale('log',base=2) 
bx1.get_yaxis().set_major_formatter(ScalarFormatter())

bx2 = bx1.twinx()
bx2.plot(BTC['Date'],BTC['Whales'], color = 'green')
bx2.set_ylabel('Number of Whales', color='green')

bx = plt.gca()
bx.xaxis.set_major_locator(mdates.MonthLocator(interval = 24))
bx.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.show()


# In[57]:


#ETH price vs whales

fig, bx1 = plt.subplots()
bx1.plot(ETH['Date'],ETH['ETH Close'], color ='blue')
bx1.set_title('ETH: Whales')
bx1.set_ylabel('USD', color='blue')
bx1.grid(True)
plt.yscale('log',base=2) 
bx1.get_yaxis().set_major_formatter(ScalarFormatter())

bx2 = bx1.twinx()
bx2.plot(ETH['Date'],ETH['Whales'], color = 'green')
bx2.set_ylabel('Number of Whales', color='green')

bx = plt.gca()
bx.xaxis.set_major_locator(mdates.MonthLocator(interval = 24))
bx.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.show()


# In[54]:


az = BTC.corr()
print(az)

