import streamlit as st
import yfinance as yf
import cufflinks as cf
import pandas as pd

# import requests, redis
import config, json
from iex import IEXStock
from helpers import format_number
import datetime

symbol = st.sidebar.text_input("Symbol", value="MSFT")

stock = IEXStock(config.IEX_TOKEN, symbol)

screen = st.sidebar.selectbox(
    "View", ("Overview", "Fundamentals", "News", "Top Gainers"), index=1
)

st.title(screen)

if screen == "Overview":

    st.markdown(
        """
    # Stock Price App
    Shown are the stock price data for query companies!
    """
    )
    st.write("---")

    start_date = st.sidebar.date_input("Start date", datetime.date(2021, 1, 1))
    end_date = st.sidebar.date_input("End date", datetime.date(2022, 1, 29))

    tickerData = yf.Ticker(symbol)  # Get ticker data
    tickerDf = tickerData.history(
        period="1d", start=start_date, end=end_date
    )  # get the historical prices for this ticker

    company = stock.get_company_info()

    col1, col2 = st.columns([1, 4])

    with col1:
        string_logo = "<img src=%s>" % tickerData.info["logo_url"]
        st.markdown(string_logo, unsafe_allow_html=True)

    with col2:
        st.subheader(company["companyName"])
        st.write(company["industry"])
        st.subheader("CEO")
        st.write(company["CEO"])
    st.subheader("Description")
    string_summary = tickerData.info["longBusinessSummary"]
    st.info(string_summary)

    # Ticker data
    st.header("**Ticker data**")
    st.write(tickerDf)

    # Bollinger bands
    st.header("**Bollinger Bands**")
    qf = cf.QuantFig(tickerDf, title="First Quant Figure", legend="top", name="GS")
    qf.add_bollinger_bands()
    fig = qf.iplot(asFigure=True)
    st.plotly_chart(fig)


if screen == "News":
    from datetime import datetime, timedelta

    news = stock.get_company_news()

    for article in news:
        st.subheader(article["headline"])
        # dt = datetime.utcfromtimestamp(article["datetime"] / 1000).isoformat()
        dt = article["datetime"]
        st.write(f"Posted by {article['source']} at {dt}")
        st.write(article["url"])
        st.write(article["summary"])
        st.image(article["image"])


if screen == "Fundamentals":
    st.header("Stats")

    stats = stock.get_stats()

    st.write(stats)

    st.header("Dividends")

    dividends = stock.get_dividends()

    for dividend in dividends:
        st.write("Dates: " + dividend["paymentDate"])
        st.write("Amount: " + str(dividend["amount"]))

if screen == "Top Gainers":

    st.subheader("List of Gainers")

    list_gainers = stock.get_list_gainers()

    for gainers in list_gainers:
        st.subheader(gainers["companyName"])
        st.write(gainers)
