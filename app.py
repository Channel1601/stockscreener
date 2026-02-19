import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

st.set_page_config(layout="wide")

st.markdown("<p style='text-align:center; font-weight: 500; font-size:60px;'>HB: Stock Screener</p>", unsafe_allow_html=True)
st.text("")
st.text("")

def load_tickers():
    return pd.read_csv("sp500.csv")

sp500 = load_tickers()
sp500["Label"] = sp500["Symbol"] + " ( " + sp500["Shortname"] + ")"

st.write("---")
col1, col2, col3 = st.columns(3)
with col1:
    selected_label = st.selectbox("S&P 500 Listings:", sp500["Label"], width=700)
    name = selected_label.split(" (")[0]
with col2:
    startd = st.date_input("Start Date: ", datetime.date(2020, 1, 1), width=500)
with col3:
    endd = st.date_input("End Date: ", value=None, width=500, max_value="today")

data = yf.download([name], start=startd, end=endd)
df = pd.DataFrame(data["Close"])

st.header(name.upper() + " (Closing Price)")
st.line_chart(df, x_label="Date", y_label="Price (USD)")

st.write("---")
ticker = yf.Ticker(name)
st.header("Filter")


col1, col2, col3, col4 = st.columns(4)
with col1: 
    pe_filter = st.selectbox("Price per Earnings:", ("Any", "Low (<15)", "Profitable (>0)", "High (>50)"))

with col2:
    eps_filter = st.selectbox("Earnings Per Share:", ("Any", "Postive (>0)", "Negative (<0)", "Low Positive (0-10)", "Very High (>25)"))

with col3:
    evs_filter = st.selectbox("EV/Sales:", ("Any", "Negative (<0)", "Low (<1)", "Postive (>0)", "High (>10)"))

with col4:
    roe_filter = st.selectbox("Return on Equity:", ("Any", "Postive (>0)", "Negative (<0)", "Very Postive (>30%)", "Very Negative (<-15%)"))

col1, col2, col3, col4 = st.columns(4)
with col1: 
    cr_filter = st.selectbox("Current Ratio:", ("Any", "Low (<1)", "High (>1)", "Very High (>3)"))

with col2:
    dte_filter = st.selectbox("Debt/Equity:", ("Any", "High (>50)", "Low (<10)", "Under 100 (<100)"))

with col3:
    beta_filter = st.selectbox("Beta:", ("Any", "Negative (<0)", "Low (<1)", "Postive (>0)", "High (>1)"))

with col4:
    divy_filter = st.selectbox("Dividend Yield:", ("Any", "None (0)", "Positive (>0)", "High (>5)", "Very High (>10)"))

col1, col2, col3, col4 = st.columns(4)
with col1: 
    rev_filter = st.selectbox("Revenue Growth:", ("Any", "Postive (>0)", "Negative (<0)", "Low Positive (0-0.10)", "Very High (>0.25)"))

with col2:
    ebit_filter = st.selectbox("EV/EBITDA:", ("Any", "Negative (<0)", "Low (<15)", "Postive (>0)", "High (>50)"))

with col3:
    prof_filter = st.selectbox("Profit Margin:", ("Any", "Negative (<0)", "Very Negative(<-20)", "Postive (>0)", "High (>20)"))

with col4:
    gross_filter = st.selectbox("Gross Margin:", ("Any", "Negative (<0)", "Very Negative(<-20)", "Postive (>0)", "High (>50)"))

st.write("")
sptable = pd.read_csv("sp500_fundamentals.csv")
filtered = sptable.copy()

if pe_filter == "Low (<15)":
    filtered = filtered[filtered["P/E"] < 15]
elif pe_filter == "High (>50)":
    filtered = filtered[filtered["P/E"] > 50]
elif pe_filter == "Profitable (>0)":
    filtered = filtered[filtered["P/E"] > 0]

if eps_filter == "Postive (>0)":
    filtered = filtered[filtered["EPS"] > 0]
elif eps_filter == "Negative (<0)":
    filtered = filtered[filtered["EPS"] < 0]
elif eps_filter == "Low Positive (0-10)":
    filtered = filtered[(filtered["EPS"] > 0) & (filtered["EPS"] < 10)]
elif eps_filter == "Very High (>25)":
    filtered = filtered[filtered["EPS"] > 25]

if evs_filter == "Postive (>0)":
    filtered = filtered[filtered["EV/Sales"] > 0]
elif evs_filter == "Negative (<0)":
    filtered = filtered[filtered["EV/Sales"] < 0]
elif evs_filter == "Low (<1)":
    filtered = filtered[filtered["EV/Sales"] < 1]
elif evs_filter == "High (>10)":
    filtered = filtered[filtered["EV/Sales"] > 10]

if roe_filter == "Postive (>0)":
    filtered = filtered[filtered["ROE"] > 0]
elif roe_filter == "Negative (<0)":
    filtered = filtered[filtered["ROE"] < 0]
elif roe_filter == "very Positive (>30%)":
    filtered = filtered[filtered["ROE"] > 0.30]
elif roe_filter == "Very Negative (<-15%)":
    filtered = filtered[filtered["ROE"] < -0.15]

if cr_filter == "Low (<1)":
    filtered = filtered[filtered["Current Ratio"] < 1]
elif cr_filter == "High (>1)":
    filtered = filtered[filtered["Current Ratio"] > 1]
elif cr_filter == "very High (>3)":
    filtered = filtered[filtered["Current Ratio"] > 3]

if dte_filter == "Low (<10)":
    filtered = filtered[filtered["Debt/Equity"] < 10]
elif dte_filter == "High (>50)":
    filtered = filtered[filtered["Debt/Equity"] > 50]
elif dte_filter == "Under 1 (<100)":
    filtered = filtered[filtered["Debt/Equity"] < 100]

if beta_filter == "Postive (>0)":
    filtered = filtered[filtered["Beta"] > 0]
elif beta_filter == "Negative (<0)":
    filtered = filtered[filtered["Beta"] < 0]
elif beta_filter == "Low (<1)":
    filtered = filtered[filtered["Beta"] < 1]
elif beta_filter == "High (>1)":
    filtered = filtered[filtered["Beta"] > 1]

if divy_filter == "Postive (>0)":
    filtered = filtered[filtered["Dividend Yield"] > 0]
elif divy_filter == "None (0)":
    filtered = filtered[filtered["Dividend Yield"] == 0]
elif divy_filter == "Very High (>10)":
    filtered = filtered[filtered["Dividend Yield"] > 10]
elif divy_filter == "High (>5)":
    filtered = filtered[filtered["Dividend Yield"] > 5]

if rev_filter == "Postive (>0)":
    filtered = filtered[filtered["Revenue Growth"] > 0]
elif rev_filter == "Negative (<0)":
    filtered = filtered[filtered["Revenue Growth"] < 0]
elif rev_filter == "Low Positive (0-0.10)":
    filtered = filtered[(filtered["Revenue Growth"] > 0) & (filtered["Revenue Growth"] < .10)]
elif rev_filter == "Very High (>0.25)":
    filtered = filtered[filtered["Revenue Growth"] > .25]

if ebit_filter == "Postive (>0)":
    filtered = filtered[filtered["EV/EBITDA"] > 0]
elif ebit_filter == "Negative (<0)":
    filtered = filtered[filtered["EV/EBITDA"] < 0]
elif ebit_filter == "Low (<15)":
    filtered = filtered[filtered["EV/EBITDA"] < 15]
elif ebit_filter == "High (>10)":
    filtered = filtered[filtered["EV/EBITDA"] > 50]

if prof_filter == "Postive (>0)":
    filtered = filtered[filtered["Profit Margin"] > 0]
elif prof_filter == "Negative (<0)":
    filtered = filtered[filtered["Profit Margin"] < 0]
elif prof_filter == "Very Negative (<-20)":
    filtered = filtered[filtered["Profit Margin"] < -20]
elif prof_filter == "High (>20)":
    filtered = filtered[filtered["Profit Margin"] > 20]

if gross_filter == "Postive (>0)":
    filtered = filtered[filtered["Gross Margin"] > 0]
elif gross_filter == "Negative (<0)":
    filtered = filtered[filtered["Gross Margin"] < 0]
elif gross_filter == "Very Negative (<-20)":
    filtered = filtered[filtered["Gross Margin"] < -20]
elif gross_filter == "High (>50)":
    filtered = filtered[filtered["Gross Margin"] > 50]

st.dataframe(filtered, hide_index=True)