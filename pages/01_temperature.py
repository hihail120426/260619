import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(page_title="서울 날씨 빅데이터 대시보드", layout="wide", page_icon="🌤️")

st.title("🌤️ 서울 기상 관측 빅데이터 종합 대시보드 (1907~현재)")
st.markdown("과거부터 현재까지의 서울 기온 데이터를 활용해 역대급 기후 기록을 찾아보고, 나의 생일 기온 변화 추이도 함께 탐구해 봅시다!")

# 2. 데이터 불러오기 및 전처리 함수
@st.cache_data
def load_data():
    try:
        # 데이터셋 읽기
        df = pd.read_csv("ta_20260619190504.csv")
        
        # 컬럼명 공백 제거
        df.columns = df.columns.str.strip()
        
        # '날짜' 컬럼 내부의 공백 및 탭 문자(\t) 제거 후 datetime 변환
        df['날짜'] = df['날짜'].astype(str).str.replace(r'\s+', '', regex=True)
        df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
        
        # 기온 데이터 수치형 변환
        for col in ['평균기온(℃)', '최저기온(℃)', '최고기온(℃)']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 필수 데이터가 누락된 행 제거
        df = df.dropna(subset=['날짜', '평균기온(℃)', '최저기온(℃)', '최고기온(℃)'])
        
        # 생일 검색을 위한 연도, 월, 일 파생 컬럼 추가
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
    
    # 역대 최고/최저 기온 정보 추출
    max_temp_row = data.loc[data['최고기온(℃)'].idxmax()]
    min_temp_row = data.loc[data['최저기온(℃)'].idxmin()]
    
    # 2개의 열로 나누어 Metric 대시보드 배치
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
        high_threshold = st.slider("이상 고온 탐색: 최고 기온이 몇 도 이상이었던 날을 찾을까요?", 
                                   min_value=20.0, max_value=42.0, value=35.0, step=0.5)
    with col_input2:
        low_threshold = st.slider("한파 탐색: 최저 기온이 몇 도 이하였던 날을 찾을까요?", 
                                  min_value=-30.0, max_value=10.0, value=-15.0, step=0.5)

    # 데이터 필터링 및 정렬
    filtered_data = data[(data['최고기온(℃)'] >= high_threshold) & (data['최저기온(℃)'] <= low_threshold)]
    display_df = filtered_data.copy().sort_values(by='날짜', ascending=False)
    display_df['날짜'] = display_df['날짜'].dt.strftime('%Y-%m-%d')
    
    # 필요한 컬럼만 추출하여 깔끔하게 표기
    cols_to_show = ['날짜', '평균기온(℃)', '최저기온(℃)', '최고기온(℃)']
    
    st.write(f"🔎 조건 검색 결과: 총 **{len(display_df)}건**이 검색되었습니다.")
    if len(display_df) > 0:
        st.dataframe(display_df[cols_to_show], use_container_width=True, hide_index=True)
        
        # 다운로드 버튼 (UTF-8-SIG 적용으로 엑셀 깨짐 방지)
        csv_buffer = display_df[cols_to_show].to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 조건 검색 결과 CSV 다운로드",
            data=csv_buffer,
            file_name="seoul_weather_filtered.csv",
            mime="text/csv"
        )
    else:
        st.info("조건에 맞는 날짜가 없습니다. 슬라이더 범위를 조절해 보세요.")

    # 구분선
    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    # ==========================================
    # PART 2: 내 생일 기온 검색 기능 (추가된 기능)
    # ==========================================
    st.header("2. 나의 '생일 기온' 추적기")
    st.write("선생님과 학생들이 각자의 생일을 입력하여 과거부터 오늘날까지 내 생일날 기온이 어떻게 변했는지 확인해 보세요.")
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        month_list = sorted(data['월'].unique())
        selected_month = st.selectbox("📅 태어난 월을 선택하세요", month_list, index=4) # 기본값: 5월
    with col_b2:
        # 선택한 월에 존재하는 일자만 리스트업
        day_list = sorted(data[data['월'] == selected_month]['일'].unique())
        selected_day = st.selectbox("📅 태어난 일을 선택하세요", day_list, index=4) # 기본값: 5일

    # 생일 데이터 필터링
    birthday_data = data[(data['월'] == selected_month) & (data['일'] == selected_day)].sort_values(by='연도')

    if len(birthday_data) > 0:
        # 역대 생일 중 최고/최저 기온 날짜 찾기
        b_hottest = birthday_data.loc[birthday_data['최고기온(℃)'].idxmax()]
        b_coldest = birthday_data.loc[birthday_data['최저기온(℃)'].idxmin()]
        
        st.markdown(f"##### ✨ 역대 {selected_month}월 {selected_day}일 중 날씨 극값")
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.warning(f"☀️ **역대 가장 더웠던 내 생일:** {int(b_hottest['연도'])}년 (최고 기온: {b_hottest['최고기온(℃)']} ℃)")
        with col_res2:
            st.info(f"❄️ **역대 가장 추웠던 내 생일:** {int(b_coldest['연도'])}년 (최저 기온: {b_coldest['최저기온(℃)']} ℃)")
            
        # 연도별 기온 변화 선그래프 시각화
        st.markdown(f"##### 📈 {selected_month}월 {selected_day}일의 연도별 기온 변화 추이")
        chart_data = birthday_data.set_index('연도')[['평균기온(℃)', '최저기온(℃)', '최고기온(℃)']]
        st.line_chart(chart_data)
        
        # 학생 탐구용 생각노트 기능
        st.markdown("##### 📝 탐구 활동: 나만의 데이터 분석 노트")
        student_opinion = st.text_area(
            label="그래프를 통해 내 생일 기온이 시간에 따라 전반적으로 오르고 있나요, 내리고 있나요? 기후 변화와 관련해 느낀 점을 기록해 보세요.",
            placeholder="여기에 생각한 내용을 적어보세요..."
        )
        if st.button("내용 제출 및 저장"):
            if student_opinion.strip():
                st.success("✅ 제출 완료! 작성한 내용이 화면에 임시 기록되었습니다. (새로고침 시 초기화)")
            else:
                st.warning("내용을 입력한 뒤 버튼을 눌러주세요.")
    else:
        st.error("선택하신 날짜의 기상 데이터가 존재하지 않습니다.")

else:
    st.error("데이터 파일을 불러올 수 없습니다. 경로와 파일명을 다시 한번 확인해 주세요.")
