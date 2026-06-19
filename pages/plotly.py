import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.title("🌍 글로벌 시가총액 Top10 주식 대시보드")

stocks = {
    "NVIDIA": "NVDA",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Alphabet": "GOOGL",
    "Amazon": "AMZN"
}

fig = go.Figure()

for company, ticker in stocks.items():

    df = yf.download(
        ticker,
        period="1y",
        auto_adjust=True,
        progress=False
    )

    if not df.empty:

        # numpy 배열로 강제 변환
        close = df["Close"].values.flatten()

        # 날짜
        dates = df.index

        # 100 기준 정규화
        close = close / close[0] * 100

        fig.add_trace(
            go.Scatter(
                x=dates,
                y=close,
                mode="lines",
                name=company
            )
        )

fig.update_layout(
    title="최근 1년 주가 변화",
    xaxis_title="날짜",
    yaxis_title="주가(100 기준)",
    template="plotly_white",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)
