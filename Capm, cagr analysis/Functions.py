import plotly.express as px 
import numpy as np 


# function to plot interactive plotly chart
def interactive_plot(df):
    fig = px.line()
    for i in df.columns[1:]:
        fig.add_scatter(x = df['Date'] , y = df[i] , name =i)
    fig.update_layout(width = 450 , margin = dict(l=20 , r=20 , t=50 , b = 20) , legend = dict(orientation ='h' , yanchor = 'bottom' , y = 1.02, xanchor = 'right' , x =1 ))
    return fig


# function to normalize the prices based on the intial prices

# Why do we normalize- so that we can compare different stocks irrepective of their starting price
def normalize(df):
    df1 = df.copy()
    for i in df.columns[1:]:
        df1[i] = df[i] /df[i][0]

    return df1


# Function to calculate daily returns
def daily_return(df):
    df1 = df.copy()   
    for i in df.columns[1: ]:
        for j in range(1, len(df)):
            df1[i][j] =  ((df[i][j] - df[i][j-1]) /df[i][j-1] )*100
        df1[i][0] = 0

    

    return df1

# Function to calculate Beta 

def calculate_beta(stocks_daily_return , stock):
   
    b,a = np.polyfit(stocks_daily_return['^NSEI'] , stocks_daily_return[stock], 1)

    return b,a



#Function to calculate multiplyiong factor.
def multiplying_factor(bonus_issued_dict, ticker ):
    mul =1
    if ticker in bonus_issued_dict.keys():
        dict_bonus = bonus_issued_dict[ticker]

        for key,value in dict_bonus.items():
            num1, num2 = map(int, key.split(':'))
            mul = mul * ((num1+num2)/num1)**value

    return mul
    