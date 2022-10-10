# %pip install mplfinance
# !pip install talib-binary
# %pip install yfinance
# %pip install --upgrade pandas
# %pip install --upgrade pandas-datareader

import pandas_datareader as web
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import talib as tb
import yfinance as yf
yf.pdr_override()

#Data
start = dt.datetime(2022,1,1)
end = dt.datetime.now()
Ethereum = web.get_data_yahoo('ETH-USD',start,end)

# view data
print(Ethereum)

#Functions for SMA and EMA
def SMA_short(data, period = 5, column = 'Close'):
  return data[column].rolling(window = period).mean()
def SMA_medium(data, period = 21, column = 'Close'):
  return data[column].rolling(window = period).mean()
def EMA_short(data, period = 5, column = 'Close'):
  return data[column].ewm(span = period, adjust = False).mean()
def EMA_medium(data, period = 21, column = 'Close'):
  return data[column].ewm(span = period, adjust = False).mean()

#Variables
SMA_sh= SMA_short(Ethereum, period = 5, column = 'Close')
SMA_med = SMA_medium(Ethereum, period = 21, column = 'Close')

EMA_sh= EMA_short(Ethereum, period = 5, column = 'Close')
EMA_med = EMA_medium(Ethereum, period = 21, column = 'Close')

#Relative Strength Index(RSI)
def RSI(data = Ethereum, period = 14, column = 'CLose'):
  delta = data[column].diff(1)
  delta = delta[1:]
  up = delta.copy()
  down = delta.copy()
  up[up>0] = 0
  down[down<0] = 0
  data['up'] = up
  data['down'] = down
  AVG_gain = SMA_short(data, period, column = 'up')
  AVG_loss = abs(SMA_short(data, period, column = 'down'))
  RS = AVG_gain/AVG_loss
  RSI = 100.0 - (100.0/(1.0+RS))
  data['RSI'] = RSI
  return data

#RSI_new
delta = Ethereum['Close'].diff(1)
delta = delta.dropna()
up = delta.copy()
down = delta.copy()
up[up>0] = 0
down[down<0] = 0
period =14
Avg_gain = abs(up.rolling(window=period).mean())
Avg_loss = abs(down.rolling(window=period).mean())
RS2 = Avg_gain/Avg_loss
RSI_new = 100.0 - (100.0/(1.0+RS2))

#Adding Data Frame

Ethereum['SMA_medium'] = SMA_medium(Ethereum)
Ethereum['EMA_medium'] = EMA_medium(Ethereum)
new_df = pd.DataFrame()
new_df['Close'] = Ethereum['Close']
new_df['RSI'] = RSI_new
new_df['MACD'] = MACD_new
new_df['Signal'] = Signal
new_df['EMA_s'] = EMA_sh
new_df['EMA_m'] = EMA_med
new_df['SMA_s'] = SMA_sh
new_df['SMA_m'] = SMA_med

#Plot style
plt.style.use('fivethirtyeight')

#Plots for Adjusted Close Price
plt.figure(figsize=(16,8))
Ethereum['Adj Close'].plot()
plt.ylabel('Adj Close')
plt.show()

#Plots for SMA short
column_list = ['SMA_s','Close']
new_df[column_list].plot(figsize=(16,8))
plt.show()
#Plots for SMA medium
column_list = ['SMA_m','Close']
new_df[column_list].plot(figsize=(16,8))
plt.show()

#Plots for EMA short
column_list = ['EMA_s','Close']
new_df[column_list].plot(figsize=(16,8))
plt.show()
#Plots for EMA medium
column_list = ['EMA_m','Close']
new_df[column_list].plot(figsize=(16,8))
plt.show()

#Plot for RSI
plt.figure(figsize=(16,8))
RSI_new.plot()
plt.axhline(30, linestyle = '--', alpha = 0.5, color = 'red')
plt.axhline(70, linestyle = '--', alpha = 0.5, color = 'red')
plt.show()
