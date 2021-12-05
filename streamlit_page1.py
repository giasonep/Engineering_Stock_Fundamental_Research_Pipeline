# import packages
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import yfinance as yf
import datetime

from sqlalchemy import create_engine
from my_functions import color_text, color_background, text_size, font_weight
from datetime import datetime, timedelta

def app():
    # ignore any pyplot warnings
    st.set_option('deprecation.showPyplotGlobalUse', False)

    # set the page background color
    page_bg_img = '''<style> div {background-color: #4d7554;}</style>'''
    st.markdown(page_bg_img, unsafe_allow_html=True)
    # prints page header
    st.markdown("<p style='text-align:center;color:black;font-size:100px;font-family:Helvetica;'><b>Powerful</b> Stock Fundamentals</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:black;font-size:30px;font-family:Helvetica;'><b>Research</p>", unsafe_allow_html=True)
    # column structure for page
    col1, col2, col3 = st.columns(3)

    # create sql engines
    engineStocks = create_engine("sqlite:///stocks.db")

    # read in the databases into pandas
    df = pd.read_sql('''SELECT * FROM "stocks_table"''', engineStocks)
    df_descriptive_columns = ['Filing_Date', 'Q_End', 'Name', 'Industry', 'Exchange', 'Market_Cap']
    df_momentum_columns = ['T1', 'T2','RT1', 'RT2','Q1_3', 'Q1_2', 'Q1_1', 'Q1','Q2_3', 'Q2_2', 'Q2_1', 'Q2', \
                    'QS_3', 'QS_2', 'QS_1', 'S', 'R1_3', 'R1_2', 'R1_1', 'R1', 'R2_3', 'R2_2', 'R2_1', 'R2', \
                    'RS_3', 'RS_2', 'RS_1', 'RS', 'BO1','BO2', 'BOS', 'Total']

    # create a list of every stock in df
    every_stock = df.Ticker.unique().tolist()

    # take in user ticker input for analysis
    ticker = col2.text_input(' ')
    ticker = ticker.upper()
    # assign ticker for yfinance retrieval
    tickerData = yf.Ticker(ticker)

    # if stock is in df, then perform analysis, else ask for a valid input from user
    if ticker in every_stock:

        # get a list of all of the company's filing dates
        filing_mask = df[df['Ticker'] == ticker]
        filing_date_list = filing_mask.Filing_Date.unique().tolist()

        # time
        today = datetime.today()
        end_date = datetime.today()
        retro_range = today - timedelta(days=180)
        filing_date = pd.to_datetime(today)

        # variable place holders 
        per_change = 0
        stale_text = ''
        missing_text = ''
        per_text = ''

        # provide a slectbox that handles datetime exceptions
        filing_date = col2.selectbox("Choose an earnings report to analyze:",(filing_date_list))

        # filter the filing date for missing data
        if filing_date == '-':
            filing_date = today
            str_date = filing_date
        else:
            str_date = filing_date
            filing_date = datetime.strptime(filing_date, '%Y-%m-%d')
            day_diff = int((today-filing_date).days)

        # determines if filing date is the current period or past period
        # returns desired date ranges for yfinance charting 
        try: 
            if day_diff < 92:
                today = today
                retro_range = retro_range
            else: 
                today = filing_date
                percentDFstart = tickerData.history(start=today - timedelta(days=3), end=today + timedelta(days=1))
                retro_range = today - timedelta(days=122)
                end_date = today + timedelta(days=92)
                today = today + timedelta(days=92)
                percentDFend = tickerData.history(start=today - timedelta(days=1), end=today + timedelta(days=3))
                today = today + timedelta(days=15)
                start = percentDFstart.Close[-1]
                end = percentDFend.Close[-1]
                per_change = round(((end-start)/abs(start))*100,1)
                stale_text = "***Be aware, you are <u>NOT</u> viewing the most recent quarter's earnings report.***"
                per_text = f"<b>${ticker} saw a ~ <u>{per_change}</u>% change in the three month period following the release of its {str_date} earnings report.</b>"
        except: 
            today = filing_date
            retro_range = today - timedelta(days=180)
            missing_text = f'${ticker} is missing fundamental and/or price data for the period selected.'

        # prints that the data being viewed is not the current quarter's or most recent data
        st.markdown(f"<p style='text-align:center;color:#ff6347 ;font-size:25px;font-family:Helvetica;'>{stale_text}</p>", unsafe_allow_html=True)
        # prints if the stock is missing data
        st.markdown(f"<p style='text-align:center;color:#ff6347 ;font-size:50px;font-family:Helvetica;'>{missing_text}</p>", unsafe_allow_html=True)

        # momentum table
        df_desc = df[(df['Ticker'] == ticker) & (df['Filing_Date'] == str_date)]
        df_desc = df_desc[df_descriptive_columns].head(1)
        df_mom = df[(df['Ticker'] == ticker) & (df['Filing_Date'] == str_date)]
        df_mom = df_mom[df_momentum_columns].head(1)
        # display the momentum table
        st.table(df_desc)
        st.table(df_mom.style.applymap(color_text).applymap(color_background).applymap(text_size).applymap(font_weight))

        # provide a section with definition and symbol legend
        with st.expander("Definitions & Legends"):
            st.write('''
                EPS: “Earnings per share,” refers to company’s revenue divided by the total amount of outstanding shares of its common stock. This figure can be interpreted as an indicator of a company’s profitability

                Sales: Total income generated by a company

                Profit Margin: Revenue less the cost of doing business, hence profit

                GAAP EPS: “Generally Accepted Accounting Principles,” refers to a common set of accounting principles that public companies in the United States must adhere to. 

                non-GAAP EPS: Refers to accounting practices that exclude certain figures which could cause high interpretation volatility and provides for a clearer picture of the company’s overall performance.

                    Symbol legend:

                        ‘ - ‘ = less than 0% ( < 0 )

                        ‘ . ‘ = between 0 and 18% ( 0 <= 17.5 )

                        ‘ ~ ‘ =  between 18 and 40% ( 18 <= 40 )

                        ‘ ^ ‘ =  between 40 and 100% ( 40 <= 100 )

                        ‘ ! ‘ = greater than 100% ( 100 < )

                        ‘ T ‘ = Tenet met

                        ‘ M ‘ = Quarter momentum met for a particular metric

                        ‘ D ‘ = Quarter deceleration in momentum met for a particular metric

                        ‘ BO ‘ = Breakout met

                T1 = ‘Tenet One’ (T): expresses if a company is showing year over year quarterly increases for non-GAAP earnings per share, sales, and profit margin for 3 or more consecutive quarters

                T2 = ‘Tenet Two’ (T): expresses if a company is showing year over year quarterly increases for GAAP earnings per share, sales, and profit margin for 3 or more consecutive quarters

                RT1 = ‘Rolling Tenet One’ (T): expresses if a company is showing year over year quarterly increases for non-GAAP earnings per share, sales, and profit margin for 3 or more consecutive quarters on a two-quarter rolling basis

                RT2 = ‘Rolling Tenet Two’ (T): expresses if a company is showing year over year quarterly increases for GAAP earnings per share, sales, and profit margin for 3 or more consecutive quarters on a two-quarter rolling basis

                Q1_1 - 3 = non-GAAP earnings per share year over year percent change: 1 = current quarter, 2 = last quarter, 3 = two quarter’s ago

                Q2_1 - 3 = GAAP earnings per share year over year percent change: 1 = current quarter, 2 = last quarter, 3 = two quarter’s ago

                QS_1 - 3 = Sales year over year percent change: 1 = current quarter, 2 = last quarter, 3 = two quarter’s ago

                Q1, Q2, S = Quarterly year over year metric has increased for 3 or more consecutive quarters  (non-GAAP eps, GAAP eps, sales)

                R1_1 - 3 = non-GAAP earnings per share year over year percent change on a two-quarter rolling basis: 1 = current quarter, 2 = last quarter, 3 = two quarter’s ago

                R2_1 - 3 = GAAP earnings per share year over year percent change on a two-quarter rolling basis: 1 = current quarter, 2 = last quarter, 3 = two quarter’s ago

                RS_1 - 3 = Sales year over year percent change on a two-quarter rolling basis: 1 = current quarter, 2 = last quarter, 3 = two quarter’s ago

                R1, R2, RS = Quarterly year over year metric has increased for 3 or more consecutive quarters on a two quarter rolling basis (non-GAAP eps, GAAP eps, sales)

                BO1 = "Breakout non-GAAP" (BO): determines if non-GAAP earnings per share are performing 75 percent or better than each of the three preceding years (determined using a trailing twelve-month period, ‘TTM’)

                BO2 = "Breakout GAAP" (BO): determines if GAAP earnings per share are performing 75 or better than each of the three preceding years (determined using a trailing twelve-month period, ‘TTM’)

                BOS = "Breakout Sales" (BO): determines if sales are performing 75 percent or better than each of the three preceding years (determined using a trailing twelve-month period, ‘TTM’)

                Total: a proprietary score that weighs each of the preceding columns to give an overall picture of a company’s health based on general level fundamentals
            ''')
        
        # if not most recent report, prints out 3 month % price change after report was filed
        st.markdown(f"<p style='text-align:center;color:black;font-size:25px;font-family:Helvetica;'>{per_text}</p>", unsafe_allow_html=True)

        ## add charts of EPS/Sales: reg and non rolling
        # create columns
        
        # get dataframe to plot % change over time for EPS and Revenue
        df_plot = df[df['Ticker'] == ticker]
        df_plot = df_plot[df_plot['Filing_Date'] != '-']
        df_plot['Filing_Date'] = pd.to_datetime(df_plot['Filing_Date'])
        df_plot = df_plot[df_plot['Filing_Date'] <= filing_date].head(12)

        sub1, sub2, sub3 = st.columns(3)

        fig = px.line(df_plot, x='Filing_Date', y="QNG_EPS")
        fig.update_layout(title='Non-Gaap EPS Yr over Yr % Change', title_x=0.5, title_y=0.91, xaxis_title='Filing Report Date', yaxis_title='% Change')
        sub1.plotly_chart(fig, use_container_width=True, layout='centered')

        fig = px.line(df_plot, x='Filing_Date', y="QG_EPS")
        fig.update_layout(title='Gaap EPS Yr over Yr % Change', title_x=0.5, title_y=0.91, xaxis_title='Filing Report Date', yaxis_title='% Change')
        sub2.plotly_chart(fig, use_container_width=True, layout='centered')

        fig = px.line(df_plot, x='Filing_Date', y="QRev")
        fig.update_layout(title='Gaap Revenue Yr over Yr % Change', title_x=0.5, title_y=0.91, xaxis_title='Filing Report Date', yaxis_title='% Change')
        sub3.plotly_chart(fig, use_container_width=True, layout='centered')

        fig = px.line(df_plot, x='Filing_Date', y="QRNG_EPS")
        fig.update_layout(title='Non-Gaap 2 Quarter Rolling EPS Yr over Yr % Change', title_x=0.5, title_y=0.91, xaxis_title='Filing Report Date', yaxis_title='% Change')
        sub1.plotly_chart(fig, use_container_width=True, layout='centered')

        fig = px.line(df_plot, x='Filing_Date', y="QRG_EPS")
        fig.update_layout(title='Gaap 2 Quarter Rolling EPS Yr over Yr % Change', title_x=0.5, title_y=0.91, xaxis_title='Filing Report Date', yaxis_title='% Change')
        sub2.plotly_chart(fig, use_container_width=True, layout='centered')

        fig = px.line(df_plot, x='Filing_Date', y="QR_Rev")
        fig.update_layout(title='Revenue 2 Quarter Rolling EPS Yr over Yr % Change', title_x=0.5, title_y=0.91, xaxis_title='Filing Report Date', yaxis_title='% Change')
        sub3.plotly_chart(fig, use_container_width=True, layout='centered')   

        # build price chart 
        try: 
            tickerDf = tickerData.history(period='1d', start=retro_range, end=today)
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=tickerDf.index, open=tickerDf['Open'], high=tickerDf['High'], low=tickerDf['Low'], close=tickerDf['Close'], name='market data'))
            fig.update_layout(title = '$' + ticker + ' Daily Stock Candlestick Chart.', yaxis_title = f'${ticker}  Price (USD)', width=1250, height=750)
            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label='1mo', step="month", stepmode="backward"),
                        dict(step="all")
                    ])
                )
            )
        except: fig = go.Figure()
        # display price chart
        st.plotly_chart(fig, use_container_width=True, layout='centered')

    else: col2.markdown(f"<p style='text-align:center;color:black;font-size:40px;font-family:Helvetica;'>Please enter a valid ticker</p>", unsafe_allow_html=True)