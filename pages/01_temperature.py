import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(page_title="서울 역대급 날씨 대시보드", layout="wide", page_icon="☀️")

st.title("📊 서울 역대급 날씨 대시보드 (1907~현재)")
st.markdown("우리나라 기상 관측 이래 서울에서 가장 덥고 추웠던 날을 찾아보고, 조건에 맞는 날씨 데이터를 검색해 봅시다.")

# 2. 데이터 불러오기 및 전처리 함수
@st.cache_data
def load_data():
    # 데이터셋 읽기
    df = pd.read_csv("ta_20260619190504.csv")
    
    # 컬럼명 공백 제거 및 데이터 전처리
    df.columns = df.columns.str.strip()
    
    # '날짜' 컬럼 내부의 탭 문자(\t) 제거 후 datetime 변환
    df['날짜'] = df['날짜'].astype(str).str.replace(r'\s+', '', regex=True)
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    
    # 기온 데이터 수치형 변환 및 결측치 제거
    for col in ['평균기온(℃)', '최저기온(℃)', '최고기온(℃)']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df = df.dropna(subset=['날짜', '평균기온(℃)', '최저기온(℃)', '최고기온(℃)'])
    return df

try:
    data = load_data()

    # 3. 상단 주요 통계 (Metric) 표시
    st.subheader("📌 역대 최고/최저 기온 기록")
    
    # 역대 최고기온 정보 추출
    max_temp_row = data.loc[data['최고기온(℃)'].idxmax()]
    max_temp = max_temp_row['최고기온(℃)']
    max_temp_date = max_temp_row['날짜'].strftime('%Y년 %m월 %d일')
    
    # 역대 최저기온 정보 추출
    min_temp_row = data.loc[data['최저기온(℃)'].idxmin()]
    min_temp = min_temp_row['최저기온(℃)']
    min_temp_date = min_temp_row['날짜'].strftime('%Y년 %m월 %d일')
    
    # 2개의 열로 나누어 Metric 배치
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="🔥 역대 최고 기온", value=f"{max_temp} ℃", delta=f"기록일: {max_temp_date}", delta_color="inverse")
    with col2:
        st.metric(label="❄️ 역대 최저 기온", value=f"{min_temp} ℃", delta=f"기록일: {min_temp_date}")

    st.markdown("---")

    # 4. 조건 검색 테이블 (슬라이더 기능)
    st.subheader("🔍 내 맘대로 조건 검색 필터")
    st.write("슬라이더를 조절하여 극한의 기온을 기록한 날들을 필터링해 보세요.")
    
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        # 최고 기온 필터 슬라이더 (기본값 35도)
        high_threshold = st.slider("이상 기온 탐색: 최고 기온이 몇 도 이상이었던 날을 찾을까요?", 
                                   min_value=20.0, max_value=42.0, value=35.0, step=0.5)
        
    with col_input2:
        # 최저 기온 필터 슬라이더 (기본값 영하 15도)
        low_threshold = st.slider("한파 탐색: 최저 기온이 몇 도 이하였던 날을 찾을까요?", 
                                  min_value=-30.0, max_value=10.0, value=-15.0, step=0.5)

    # 데이터 필터링 실행
    filtered_data = data[
        (data['최고기온(℃)'] >= high_threshold) & 
        (data['최저기온(℃)'] <= low_threshold)
    ]
    
    # 날짜 정렬 후 가독성 있게 포맷 변경한 복사본 생성
    display_df = filtered_data.copy()
    display_df['날짜'] = display_df['날짜'].dt.strftime('%Y-%m-%d')
    display_df = display_df.sort_values(by='날짜', ascending=False)

    # 결과 출력
    st.write(f"🔎 검색 결과: 총 **{len(display_df)}건**이 검색되었습니다.")
    
    if len(display_df) > 0:
        st.dataframe(display_df, use_container_width=True)
        
        # 5. CSV 다운로드 버튼
        csv_buffer = display_df.to_csv(index=False).encode('utf-8-sig') # 엑셀 깨짐 방지 utf-8-sig
        st.download_button(
            label="📥 필터링된 결과 CSV 다운로드",
            data=csv_buffer,
            file_name=f"seoul_weather_filtered.csv",
            mime="text/csv"
        )
    else:
        st.info("조건에 맞는 날짜가 없습니다. 슬라이더 범위를 조절해 보세요!")

except FileNotFoundError:
    st.error("데이터 파일('ta_20260619190504.csv')을 찾을 수 없습니다. 파일명을 확인하고 저장소에 함께 업로드해 주세요.")
