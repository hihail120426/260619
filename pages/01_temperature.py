import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(
    page_title="120년 서울 기후 변화 연구소",
    layout="wide"
)

st.title("🌍 120년 서울 기후 변화 연구소")

# 데이터 로드 함수 (들여쓰기 수정)
@st.cache_data
def load_data():
    df = pd.read_csv("ta_20260619190504.csv", encoding="utf-8")
    df["날짜"] = pd.to_datetime(df["날짜"])
    df["연도"] = df["날짜"].dt.year
    return df

df = load_data()

# 연도별 평균 계산 (들여쓰기 수정)
yearly = (
    df.groupby("연도")
    .agg(
        평균기온=("평균기온(℃)", "mean"),
        최고기온=("최고기온(℃)", "mean"),
        최저기온=("최저기온(℃)", "mean")
    )
    .reset_index()
)

# =========================
# 평균기온 변화
# =========================
st.header("📈 연도별 평균기온 변화")
fig = px.line(
    yearly,
    x="연도",
    y="평균기온",
    title="1907~2026 평균기온 변화"
)
st.plotly_chart(fig, use_container_width=True)

# =========================
# 기후변화 체감기
# =========================
st.header("🌡️ 기후변화 체감기")
start_temp = yearly.iloc[0]["평균기온"]
end_temp = yearly.iloc[-1]["평균기온"]

fig_indicator = go.Figure()
fig_indicator.add_trace(
    go.Indicator(
        mode="number+delta",
        value=end_temp,
        number={"suffix": "℃"},
        delta={
            "reference": start_temp,
            "relative": False
        },
        title={
            "text": f"1907년 대비 {yearly.iloc[-1]['연도']}년"
        }
    )
)
st.plotly_chart(fig_indicator, use_container_width=True)

delta = end_temp - start_temp
st.success(
    f"{yearly.iloc[0]['연도']}년 → {yearly.iloc[-1]['연도']}년 : "
    f"{delta:.2f}℃ 상승"
)

# =========================
# 미래 기온 예측
# =========================
st.header("🔮 미래 기온 예측")
x = yearly["연도"]
y = yearly["평균기온"]
coef = np.polyfit(x, y, 1)

predict_years = [2030, 2050, 2100]
predicted = []

# for문 내부 들여쓰기 수정
for year in predict_years:
    temp = coef[0] * year + coef[1]
    predicted.append(temp)

pred_df = pd.DataFrame({
    "연도": predict_years,
    "예측 평균기온(℃)": np.round(predicted, 2)
})
st.dataframe(pred_df)

future_x = np.arange(1907, 2101)
future_y = coef[0] * future_x + coef[1]

fig2 = go.Figure()
fig2.add_trace(
    go.Scatter(
        x=yearly["연도"],
        y=yearly["평균기온"],
        mode="lines",
        name="실제 기온"
    )
)
fig2.add_trace(
    go.Scatter(
        x=future_x,
        y=future_y,
        mode="lines",
        name="예측"
    )
)
fig2.update_layout(
    title="2100년까지 평균기온 예측"
)
st.plotly_chart(fig2, use_container_width=True)

# =========================
# 연도별 애니메이션
# =========================
st.header("🎬 연도별 기온 변화 애니메이션")
animation_df = yearly.copy()
fig3 = px.bar(
    animation_df,
    x="평균기온",
    y="연도",
    orientation="h",
    animation_frame="연도",
    range_x=[
        animation_df["평균기온"].min() - 1,
        animation_df["평균기온"].max() + 1
    ],
    title="연도별 평균기온 변화"
)
st.plotly_chart(fig3, use_container_width=True)
