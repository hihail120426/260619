import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# 1. 페이지 기본 설정
st.set_page_config(page_title="서울 날씨 빅데이터 대시보드", layout="wide", page_icon="🌤️")

st.title("🌤️ 서울 기상 관측 빅데이터 종합 대시보드 (1907~현재)")
st.markdown("과거부터 현재까지의 서울 기온 데이터를 활용해 기후 기록을 찾고, 인공지능 알고리즘(선형 회귀)으로 미래 기온을 예측해 봅시다!")

# 2. 데이터 불러오기 및 전처리 함수
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("ta_20260619190504.csv")
        df.columns = df.columns.str.strip()
        df['날짜'] = df['날짜'].astype(str).str.replace(r'\s+', '', regex=True)
        df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
        
        for col in ['평균기온(℃)', '최저기온(℃)', '최고기온(℃)']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.dropna(subset=['날짜', '평균기온(℃)', '최저기온(℃)', '최고기온(℃)'])
        
        df['연도'] = df['날짜'].dt.year
        df['월'] = df['날짜'].dt.month
        df['일'] = df['날짜'].dt.day
        
        return df
    except Exception as e:
        st.error(f"데이터를 로드하는 중 오류가 발생했습니다: {e}")
        return None

data = load_data()

if data is not None:
    # ==========================================
    # PART 1: 역대급 기온 통계 & 조건 검색
    # ==========================================
    st.header("1. 역대 최고/최저 기온 기록 & 조건 검색")
    
    max_temp_row = data.loc[data['최고기온(℃)'].idxmax()]
    min_temp_row = data.loc[data['최저기온(℃)'].idxmin()]
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric(
            label="🔥 역대 최고 기온 기록", 
            value=f"{max_temp_row['최고기온(℃)']} ℃", 
            delta=f"기록일: {max_temp_row['날짜'].strftime('%Y년 %m월 %d일')}", 
            delta_color="inverse"
        )
    with col_m2:
        st.metric(
            label="❄️ 역대 최저 기온 기록", 
            value=f"{min_temp_row['최저기온(℃)']} ℃", 
            delta=f"기록일: {min_temp_row['날짜'].strftime('%Y년 %m월 %d일')}"
        )

    st.markdown("#### 🔍 기온 조건 검색 필터")
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        high_threshold = st.slider("이상 고온 탐색: 최고 기온이 몇 도 이상이었던 날을 찾을까요?", min_value=20.0, max_value=42.0, value=35.0, step=0.5)
    with col_input2:
        low_threshold = st.slider("한파 탐색: 최저 기온이 몇 도 이하였던 날을 찾을까요?", min_value=-30.0, max_value=10.0, value=-15.0, step=0.5)

    filtered_data = data[(data['최고기온(℃)'] >= high_threshold) & (data['최저기온(℃)'] <= low_threshold)]
    display_df = filtered_data.copy().sort_values(by='날짜', ascending=False)
    display_df['날짜'] = display_df['날짜'].dt.strftime('%Y-%m-%d')
    cols_to_show = ['날짜', '평균기온(℃)', '최저기온(℃)', '최고기온(℃)']
    
    st.write(f"🔎 조건 검색 결과: 총 **{len(display_df)}건**이 검색되었습니다.")
    if len(display_df) > 0:
        st.dataframe(display_df[cols_to_show], use_container_width=True, hide_index=True)
        csv_buffer = display_df[cols_to_show].to_csv(index=False).encode('utf-8-sig')
        st.download_button(label="📥 조건 검색 결과 CSV 다운로드", data=csv_buffer, file_name="seoul_weather_filtered.csv", mime="text/csv")
    else:
        st.info("조건에 맞는 날짜가 없습니다. 슬라이더 범위를 조절해 보세요.")

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    # ==========================================
    # PART 2: 내 생일 기온 검색 기능
    # ==========================================
    st.header("2. 나의 '생일 기온' 추적기")
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        month_list = sorted(data['월'].unique())
        selected_month = st.selectbox("📅 태어난 월을 선택하세요", month_list, index=4)
    with col_b2:
        day_list = sorted(data[data['월'] == selected_month]['일'].unique())
        selected_day = st.selectbox("📅 태어난 일을 선택하세요", day_list, index=4)

    birthday_data = data[(data['월'] == selected_month) & (data['일'] == selected_day)].sort_values(by='연도')

    if len(birthday_data) > 0:
        b_hottest = birthday_data.loc[birthday_data['최고기온(℃)'].idxmax()]
        b_coldest = birthday_data.loc[birthday_data['최저기온(℃)'].idxmin()]
        
        st.markdown(f"##### ✨ 역대 {selected_month}월 {selected_day}일 중 날씨 극값")
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.warning(f"☀️ **역대 가장 더웠던 내 생일:** {int(b_hottest['연도'])}년 (최고 기온: {b_hottest['최고기온(℃)']} ℃)")
        with col_res2:
            st.info(f"❄️ **역대 가장 추웠던 내 생일:** {int(b_coldest['연도'])}년 (최저 기온: {b_coldest['최저기온(℃)']} ℃)")
            
        st.markdown(f"##### 📈 {selected_month}월 {selected_day}일의 연도별 기온 변화 추이")
        chart_data = birthday_data.set_index('연도')[['평균기온(℃)', '최저기온(℃)', '최고기온(℃)']]
        st.line_chart(chart_data)
    else:
        st.error("선택하신 날짜의 기상 데이터가 존재하지 않습니다.")

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    # ==========================================
    # PART 3: 선형 회귀(Linear Regression) 미래 기온 예측 (신규 추가)
    # ==========================================
    st.header("3. 🤖 인공지능(선형 회귀) 모델 기반 미래 기온 예측 표")
    st.write("연도별 평균 기온의 추세를 수학적으로 분석하여 100년 뒤, 200년 뒤, 300년 뒤의 서울 날씨를 예측합니다.")

    # 연도별 평균 기온 데이터 추출
    yearly_summary = data.groupby('연도')['평균기온(℃)'].mean().reset_index()
    
    # 선형 회귀 모델 학습 (독립변수 X: 연도, 종속변수 y: 평균기온)
    X = yearly_summary[['연도']].values
    y = yearly_summary['평균기온(℃)'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    # 최근 연도 기준으로 100년, 200년, 300년 뒤 연도 계산
    current_year = int(yearly_summary['연도'].max())
    future_years = [current_year + 100, current_year + 200, current_year + 300]
    
    # 미래 기온 예측값 계산
    predictions = model.predict(np.array(future_years).reshape(-1, 1))
    
    # 기울기 계산 (1년당 평균 기온 상승폭)
    slope = model.coef_[0]

    # 결과 표 작성을 위한 데이터프레임 구축
    prediction_df = pd.DataFrame({
        "구분": ["100년 뒤 미래", "200년 뒤 미래", "300년 뒤 미래"],
        "예측 연도": [f"{y}년" for y in future_years],
        "예측 서울 평균 기온": [f"{pred:.2f} ℃" for pred in predictions]
    })
    
    # 대시보드 화면에 표 출력
    st.subheader(f"🔮 서울 연도별 평균 기온 예측 결과")
    st.table(prediction_df)
    
    # 과학적 원리 설명을 위한 안내 박스
    st.info(f"""
    💡 **교실 안 수학·정보 상식 (선생님 가이드):**
    * 이 분석 모델은 **선형 회귀(Linear Regression)** 알고리즘을 사용했습니다. 과거 데이터의 흐름을 가장 잘 대변하는 하나의 '직선 방정식'을 찾는 원리입니다.
    * 현재 데이터 분석 결과, 서울의 평균 기온은 매년 약 **{slope:.4f} ℃**씩 상승하는 추세를 보이고 있습니다.
    * 이에 따라 계산된 {future_years[0]}년, {future_years[1]}년, {future_years[2]}년의 예측치를 보며 기후 변화의 심각성에 대해 토론해 봅시다.
    """)
