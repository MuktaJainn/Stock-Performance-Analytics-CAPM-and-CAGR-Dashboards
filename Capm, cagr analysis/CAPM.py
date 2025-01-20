import streamlit as st 
import pandas as pd 
import pandas_datareader.data as web
import yfinance as yf 
import datetime
import Functions as cFun
import numpy as np

st.set_page_config(page_title= "CAPM" , page_icon= "chart_with_upwards_trend", layout ="wide" )

st.title("Capital Asset Pricing Model")

col1, col2 = st.columns([1,1])
try:
    with col1:
            stocks_list = st.multiselect("Choose 4 stocks" , ('RELIANCE.NS', 'LT.NS', 'SBIN.NS', 'HINDUNILVR.NS', 'ITC.NS', 'BAJAJ-AUTO.NS', 
            'ASIANPAINT.NS', 'M&M.NS', 'WIPRO.NS', 'INFY.NS'), ['LT.NS' , 'SBIN.NS' , 'M&M.NS' , 'INFY.NS'])
            
    with col2 :
            year = st.number_input("Number of years" , 1, 18)
            


    end = datetime.date.today() 

        
    start = datetime.date(end.year- year, end.month, end.day)


    nifty50 = yf.download(['^NSEI'], start, end)

    # print(nifty50.dtypes)

    nifty50 = nifty50.loc[: , "Close"]
    # print(nifty50.head())

    stock_data = pd.DataFrame()

    for stock in stocks_list:
            data = yf.download(stock, period = f'{year}y')
            stock_data[stock] = data['Close']  

    # print(stock_data.head())
    # print(nifty50.head())

    stock_data.reset_index(inplace=True)
    nifty50.reset_index(inplace=True)


    stock_data = pd.merge(stock_data , nifty50 , on="Date" , how= "inner")

    # print(stock_data.head())

    col1, col2 = st.columns([1,1])

    with col1:
            st.markdown('### Dataframe head')
            st.dataframe(stock_data.head() , use_container_width=True)

    with col2:
            st.markdown('### Dataframe Tail')
            st.dataframe(stock_data.tail(), use_container_width= True )

    col1, col2 = st.columns([1,1])

    with col1:
            st.markdown('### Price of all the Stocks')
            st.plotly_chart(cFun.interactive_plot(stock_data))

    with col2: 
            normalized_stock_df = cFun.normalize(stock_data)
            st.markdown("### Price of all the Stocks (After Normalizing)")
            st.plotly_chart(cFun.interactive_plot(normalized_stock_df))

    
#     col1,col2 = st.columns([1,1])
#     with col1:
#             st.dataframe(normalized_stock_df.head() , use_container_width=True)

#     with col2:
#           st.dataframe(normalized_stock_df.tail() , use_container_width=True)
          

    stocks_daily_return_df = cFun.daily_return(stock_data)

    alpha = {}

    beta = {}
    for i in stocks_list:

        b,a = cFun.calculate_beta(stocks_daily_return_df , i)
        alpha[i] = a
        beta[i] = b


    beta_df = pd.DataFrame(columns =["Stock" , "Beta Value"])

    beta_df["Stock"] = beta.keys()
    beta_df["Beta Value"] = [round(i,2) for i in beta.values()]

    # print(beta_df.head())

    col1, col2 = st.columns([1,1])

    with col1:
        st.markdown('### Calculated Beta Values')
        st.dataframe(beta_df, use_container_width=True)


    rf = 0
    
    rm = stocks_daily_return_df['^NSEI'].mean() * 252
        

    return_df = pd.DataFrame()
    stocks =[]
    return_value = []

    for stock, value in beta.items() :
        stocks.append(stock)
        return_value.append(round(rf + value*(rm-rf),2))

    return_df["Stock"] = stocks 
    return_df["Return Value"] = return_value


    with col2:
        st.markdown('### Calculated Return using CAPM')
        st.dataframe(return_df, use_container_width=True)

except:

    st.write("Please put valid input!")

# beta_manual = np.cov(stocks_daily_return_df["M&M.NS"], stocks_daily_return_df["^NSEI"])[0][1] / np.cov(stocks_daily_return_df["M&M.NS"], stocks_daily_return_df["^NSEI"])[1][1]
# print(beta_manual)

# print(stocks_daily_return_df['^NSEI'].mean())



        



