import streamlit as st
import random
from datetime import date

st.set_page_config(
    page_title="💕 연애운 사주 카페 🔮",
    page_icon="🌸",
    layout="centered"
)

# 배경 꾸미기
st.markdown("""
<style>
.stApp{
    background: linear-gradient(to bottom,#FFE4EC,#FFF5E4);
}

h1,h2,h3{
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

st.title("💕🔮 연애운 사주 카페 🌸✨")
st.markdown("### 🌷 오늘의 연애운을 확인해보세요! 💖")

st.write("---")

birthday = st.date_input(
    "🎂 생년월일을 선택해주세요!",
    value=date(2008,1,1)
)

gender = st.selectbox(
    "💌 성별",
    ["👧 여자", "👦 남자", "🌈 기타"]
)

if st.button("🔮 연애운 보기 💕"):

    st.balloons()

    # 생년월일 숫자로 랜덤 시드 생성
    seed_num = int(birthday.strftime("%Y%m%d"))
    random.seed(seed_num)

    score = random.randint(60, 100)

    colors = [
        "💗 핑크",
        "💙 하늘색",
        "💜 보라색",
        "💚 초록색",
        "🧡 주황색",
        "❤️ 빨간색"
    ]

    lucky_numbers = list(range(1, 10))

    lovers = [
        "😊 다정한 사람",
        "😆 유머 감각이 좋은 사람",
        "🧠 똑똑한 사람",
        "🎨 감성적인 사람",
        "💪 든든한 사람",
        "🌷 배려심 많은 사람"
    ]

    advice = [
        "💖 상대방의 이야기를 잘 들어주는 것이 중요해요!",
        "🌸 진심 어린 표현이 좋은 인연을 불러와요!",
        "✨ 자신감을 가지면 더욱 매력적이에요!",
        "🍀 좋은 인연은 천천히 찾아와요!",
        "💕 웃는 모습이 큰 행운을 가져다줄 거예요!"
    ]

    st.success("🌷 사주 풀이가 완료되었어요! ✨")

    st.subheader("💕 연애운 점수")
    st.metric("오늘의 연애운", f"{score}점")

    st.subheader("🌹 이상형 스타일")
    st.info(random.choice(lovers))

    st.subheader("💌 연애 조언")
    st.success(random.choice(advice))

    st.subheader("✨ 행운의 색")
    st.write(random.choice(colors))

    st.subheader("🍀 행운의 숫자")
    st.write(random.choice(lucky_numbers))

    if score >= 90:
        st.markdown("""
        # 💖💖💖

        🌈 최고의 연애운!

        🥰 설레는 일이 생길지도 몰라요!

        🌸✨💕🍀
        """)
    elif score >= 75:
        st.markdown("""
        # 🌷🌷🌷

        😊 좋은 인연이 찾아올 수 있어요!

        💕✨🌸
        """)
    else:
        st.markdown("""
        # 🍀🌷

        💖 조급해하지 말고 자신을 사랑해보세요!

        ✨ 좋은 인연은 천천히 찾아온답니다!
        """)

st.write("---")
st.caption("🌸💕 연애운 사주 카페 🔮")
