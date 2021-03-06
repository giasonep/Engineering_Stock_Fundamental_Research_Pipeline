# import packages
import streamlit as st
import pandas as pd

from sqlalchemy import create_engine
from my_functions import color_text, color_background, text_size, font_weight

def app():
    # prints page header
    st.markdown("<p style='text-align:center;color:black;font-size:100px;font-family:Helvetica;'><b>Powerful</b> Stock Fundamentals</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:black;font-size:30px;font-family:Helvetica;'><b>Leaderboard</p>", unsafe_allow_html=True)

    # create sql engines
    engineLeaders = create_engine("sqlite:///leaders.db")

    # read in the databases into pandas
    df = pd.read_sql('''SELECT * FROM "leaders_table"''', engineLeaders)
    df_momentum_columns = ['Ticker', 'Filing_Date', 'T1', 'T2','RT1', 'RT2','Q1_3', 'Q1_2', 'Q1_1', 'Q1','Q2_3', 'Q2_2', 'Q2_1', 'Q2', \
                    'QS_3', 'QS_2', 'QS_1', 'S', 'R1_3', 'R1_2', 'R1_1', 'R1', 'R2_3', 'R2_2', 'R2_1', 'R2', \
                    'RS_3', 'RS_2', 'RS_1', 'RS', 'BO1','BO2', 'BOS', 'Total']

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


    # momentum table
    df_leader = df.sort_values(by='Total', ascending=False).reset_index()
    df_leader = df_leader[df_momentum_columns].head(250)
    # display the momentum table
    st.table(df_leader.style.applymap(color_text).applymap(color_background).applymap(text_size).applymap(font_weight))