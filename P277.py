# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 01:08:41 2023

@author: DSN RAJU
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import datetime
import streamlit as st
import model_building as m


with st.sidebar:
    st.markdown("# Reliance Industries Stock Forecast")
    user_input = st.multiselect('Please select the stock',['RELIANCE.NS'],['RELIANCE.NS'])

    # user_input = st.text_input('Enter Stock Name', "RELIANCE.NS")
    st.markdown("### Choose Date for your anaylsis")
    START = st.date_input("From",datetime.date(2000, 1, 1))
    END = st.date_input("To",datetime.date(2024, 8, 31))
    bt = st.button('Submit') 

#adding a button
if bt:

# Importing dataset------------------------------------------------------
    df = yf.download('RELIANCE.NS', start=START, end=END)
    plotdf, future_predicted_values =m.create_model(df)
    df.reset_index(inplace = True)
    st.title('Reliance Industries Stock Market Prediction')
    st.header("Data We collected from the source")
    st.write(df)

    reliance_1=df.drop(["Open", "High", "Low", "Adj Close"],axis=1).reset_index(drop=True)
    reliance_2=reliance_1.dropna().reset_index(drop=True)

    reliance=reliance_2.copy()
    reliance['Date']=pd.to_datetime(reliance['Date'],format='%Y-%m-%d')
    reliance=reliance.set_index('Date')
    st.title('EDA')
    st.write(reliance)


# ---------------------------Graphs--------------------------------------

    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.title('Visualizations')

    st.header("Graphs")
    plt.figure(figsize=(20,10))
    #Plot 1
    plt.subplot(2,2,1)
    plt.plot(reliance['Close'],color='green')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title('Close')
    #Plot 2
    plt.subplot(2,2,2)
    plt.plot(reliance['Volume'],color='red')
    plt.xlabel('Date')
    plt.ylabel('Shares Traded')
    plt.title('Volume')
    st.pyplot()
#------------------------box-plots---------------------------------

    # Creating box-plots
    st.header("Box Plots")

    plt.figure(figsize=(20,10))
    #Plot 1
    plt.subplot(2,2,1)
    plt.boxplot(reliance['Close'])
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title('Close')
    #Plot 2
    plt.subplot(2,2,2)
    plt.boxplot(reliance['Volume'])
    plt.xlabel('Date')
    plt.ylabel('Shares Traded')
    plt.title('Volume')
    st.pyplot()

#---------------------Histogram---------------------------------------

    st.header("Histogram")
    # Ploting Histogram
    plt.figure(figsize=(20,10))
    #Plot 1
    plt.subplot(2,2,1)
    plt.hist(reliance['Close'],bins=50, color='green')
    plt.xlabel("Close Price")
    plt.ylabel("Frequency")
    plt.title('Close')
    #Plot 2
    plt.subplot(2,2,2)
    plt.hist(reliance['Volume'],bins=50, color='red')
    plt.xlabel("Shares Traded")
    plt.ylabel("Frequency")
    plt.title('Volume')
    st.pyplot()


#-------------------------KDE Plots-----------------------------------------

    st.header("KDE Plots")
    # KDE-Plots
    plt.figure(figsize=(20,10))
    #Plot 1
    plt.subplot(2,2,1)
    sns.kdeplot(reliance['Close'], color='green')
    plt.title('Close')
    st.pyplot()


    st.header('Years vs Volume')
    st.line_chart(reliance['Volume'])


#-------------------Finding long-term and short-term trends---------------------

    st.title('Finding long-term and short-term trends')
    reliance_ma=reliance.copy()
    reliance_ma['365-day MA']=reliance['Close'].rolling(window=365).mean()
    reliance_ma['2100-day MA']=reliance['Close'].rolling(window=2100).mean()

    st.write(reliance_ma)


    st.subheader('Stock Price vs 365-day Moving Average')
    plt.plot(reliance_ma['Close'],label='Original data')
    plt.plot(reliance_ma['365-day MA'],label='365-MA')
    plt.legend()
    plt.title('Stock Price vs 365-day Moving Average')
    plt.xlabel('Date')
    plt.ylabel('Price')
    st.pyplot()


    st.subheader('Stock Price vs 2100-day Moving Average')
    plt.plot(reliance_ma['Close'],label='Original data')
    plt.plot(reliance_ma['2100-day MA'],label='2100-MA')
    plt.legend()
    plt.title('Stock Price vs 2100-day Moving Average')
    plt.xlabel('Date')
    plt.ylabel('Price')
    st.pyplot()

    df1 = pd.DataFrame(future_predicted_values)
    st.markdown("### Next 365 days forecast")
    df1.rename(columns={0: "Predicted Prices"}, inplace=True)
    st.write(df1)

    st.markdown("### Original vs predicted close price")
    fig= plt.figure(figsize=(20,10))
    sns.lineplot(data=plotdf)
    st.pyplot(fig)
    
    
else:
    #displayed when the button is unclicked
    st.write('Please click on the submit button to get the EDA ans Prediction') 