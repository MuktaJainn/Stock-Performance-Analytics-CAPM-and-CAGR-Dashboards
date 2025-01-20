import streamlit as st 
import pandas as pd 
import pandas_datareader.data as web
import yfinance as yf 
import datetime
import Functions as cFun
import numpy as np
import matplotlib.pyplot as plt 

#Relative imports not supported in streamlit
# from ..cal_cagr import multiplying_factor

st.set_page_config(page_title= "CAGR" , page_icon= "chart_with_upwards_trend", layout ="wide" )

st.title("17-Year Compound Annual Growth Rate (CAGR)")

col1, col2 = st.columns([1,1])

with col1:
        stocks_list = st.multiselect("Choose 4 stocks" , ('RELIANCE.NS', 'LT.NS', 'SBIN.NS', 'HINDUNILVR.NS', 'ITC.NS', 'BAJAJ-AUTO.NS', 
        'ASIANPAINT.NS', 'M&M.NS', 'WIPRO.NS', 'INFY.NS'), ['LT.NS' , 'SBIN.NS' , 'M&M.NS' , 'INFY.NS'])
            

year = 17
            


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


eg_df = pd.concat([stock_data.head(1), stock_data.tail(1)])

eg_df.reset_index(drop=True, inplace=True)



# Right now, manually checking it and filling it, will automate this.
bonus_issued_dict = { 'RELIANCE.NS' : {'1:1': 3  }, 
                     'LT.NS' :{'1:2': 2 , '1:1' :1},
                     'ITC.NS' :{'1:1' : 1 , "1:2" :1}, 
                     'BAJAJ-AUTO.NS' : { '1:1':1 },
                     'M&M.NS' : {'1:1' :1}, 
                     'WIPRO.NS' :{ '1:1' : 2 , '2:3' : 1 , '1:3' :1},   #2:3'
                     'INFY.NS' : {'1:1' :3} }


# mul =1
# dict_bonus = bonus_issued_dict['WIPRO.NS']
# for key,value in dict_bonus.items():
#         num1, num2 = map(int, key.split(':'))
#         mul = mul * ((num1+num2)/num1)**value

# print(mul)


# cagr_df = pd.DataFrame()

def multiplying_factor(bonus_issued_dict, ticker ):
    mul =1
    if ticker in bonus_issued_dict.keys():
        dict_bonus = bonus_issued_dict[ticker]

        for key,value in dict_bonus.items():
            num1, num2 = map(int, key.split(':'))
            mul = mul * ((num1+num2)/num1)**value

    return mul

dict ={}

for i in eg_df.columns[1:]:
        mul = multiplying_factor(bonus_issued_dict, i )
        dict[i] = (((eg_df.loc[1, i]*mul/eg_df.loc[0,i]) **(1/year)) -1) *100

# st.dataframe(cagr_df, use_container_width= True )


        
cagr_df = pd.DataFrame(columns=["Stock" , "CAGR_Return_%"])


cagr_df["Stock"] = dict.keys()
cagr_df["CAGR_Return_%"] = [round(i,2) for i in dict.values()]


col1, col2 = st.columns([2,1])

with col1:
       st.markdown("### Start Price and End Price")
       st.dataframe(eg_df, use_container_width=True)

col1, col2 = st.columns([1,1])

with col1:
    st.markdown("### CAGR Return Rates")
    st.dataframe(cagr_df, use_container_width= True )





# for i in stock_data.columns[1:]:
#         stock_data[i][end]