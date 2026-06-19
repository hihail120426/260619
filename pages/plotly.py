import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="글로벌 시가총액 Top10 주식 대시보드",
    layout="wide"
)

st.title("🌍 글로벌 시가총액 Top10 주식 대시보드")
st.write("최근 1년간 주가 변화를 비교합니다.")

# 글로벌 시가총액 Top10 기업
stocks = {
    "NVIDIA": "NVDA",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Alphabet": "GOOGL",
    "Amazon": "AMZN",
    "Broadcom": "AVGO",
    "TSMC": "TSM",
    "Saudi Aramco": "2222.SR",
    "Meta": "META",
    "Tesla": "TSLA"
}

selected = st.multiselect(
    "기업 선택",
    list(stocks.keys()),
    default=list(stocks.keys())[:5]
)

normalize = st.checkbox("100 기준으로 수익률 비교", value=True)

if selected:
    fig = go.Figure()

    for company in selected:
        ticker = stocks[company]

        try:
            df = yf.download(
                ticker,
                period="1y",
                auto_adjust=True,
                progress=False
            )

            if len(df) > 0:

                price = df["Close"]

                if normalize:
                    price = price / price.iloc[0] * 100

                fig.add_trace(
                    go.Scatter(
                        x=price.index,
                        y=price,
                        mode="lines",
                        name=company
                    )
                )

        except:
            pass

    y_title = "주가 (100 기준)" if normalize else "주가"

    fig.update_layout(
        title="최근 1년 주가 변화",
        xaxis_title="날짜",
        yaxis_title=y_title,
        hovermode="x unified",
        height=700
    )

    st.plotly_chart(fig, use_container_width=True)
