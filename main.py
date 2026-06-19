import streamlit as st
import random
from datetime import date

st.set_page_config(
    page_title="💕🔮 연애운 사주 카페",
    page_icon="🌸",
    layout="centered"
)

st.markdown("""
<style>
.stApp{
background:linear-gradient(to bottom,#FFE4EC,#FFF5F5,#FFF8E7);
}
h1,h2,h3{
text-align:center;
}
</style>
""",unsafe_allow_html=True)

st.title("💕🔮 연애운 사주 카페 🌸")
st.markdown("### ✨ 오늘의 운세를 확인해보세요 ✨")

birthday = st.date_input(
    "🎂 생년월일을 선택해주세요",
    value=date(2008,1,1)
)

if st.button("🔮 운세 보기 💖"):

    st.balloons()

    seed_num = int(birthday.strftime("%Y%m%d"))
    random.seed(seed_num)

    score = random.randint(60,100)

    animals = [
        "🐭 쥐띠","🐮 소띠","🐯 호랑이띠","🐰 토끼띠",
        "🐲 용띠","🐍 뱀띠","🐴 말띠","🐑 양띠",
        "🐵 원숭이띠","🐔 닭띠","🐶 개띠","🐷 돼지띠"
    ]

    lovers = [
        "😊 다정한 사람",
        "🎨 감성적인 사람",
        "💖 배려심 많은 사람",
        "😆 유머 감각이 좋은 사람",
        "🌷 따뜻한 사람"
    ]

    partner = [
        "💪 든든하게 곁을 지켜주는 사람",
        "📚 공부를 열심히 하는 사람",
        "🎵 취미가 비슷한 사람",
        "🐶 동물을 좋아하는 사람",
        "✈️ 여행을 좋아하는 사람"
    ]

    colors = ["💗 핑크","💙 하늘색","💜 보라색","💚 초록색","❤️ 빨강"]
    foods = ["🍰 케이크","🍓 딸기","🍕 피자","🍜 라면","🍫 초콜릿"]
    items = ["🎀 리본","📚 책","🎧 이어폰","🧸 인형","🍀 네잎클로버"]

    year = birthday.year
    my_tti = animals[(year-4)%12]

    st.success("🌸 운세 결과가 나왔어요!")

    st.subheader("💕 연애운")
    st.metric("연애운 점수",f"{score}점")

    st.subheader("🌹 이상형 스타일")
    st.info(random.choice(lovers))

    st.subheader("🐰 띠")
    st.info(my_tti)

    st.subheader("💖 띠별 궁합")
    st.success(random.choice([
        "최고의 궁합이에요! 💕",
        "좋은 인연이 될 수 있어요 🌸",
        "서로 배려하면 더욱 좋아져요 ✨"
    ]))

    st.subheader("🥰 미래 연애 상대 특징")
    st.info(random.choice(partner))

    st.subheader("📚 학업운")
    st.success(random.choice([
        "📖 꾸준함이 좋은 결과를 가져와요!",
        "✏️ 복습이 행운을 가져와요!",
        "🌟 집중력이 높아질 수 있어요!"
    ]))

    st.subheader("🌞 오늘의 운세")
    st.write(random.choice([
        "🍀 좋은 일이 생길 수 있어요!",
        "😊 웃음이 행운을 불러와요!",
        "🌸 즐거운 하루가 될 수 있어요!"
    ]))

    st.subheader("📅 이번 주 운세")
    st.write(random.choice([
        "🌈 새로운 기회가 찾아올 수 있어요!",
        "💖 사람들과의 관계가 좋아질 수 있어요!",
        "⭐ 행복한 일이 기다리고 있어요!"
    ]))

    st.subheader("🌙 이번 달 운세")
    st.write(random.choice([
        "✨ 행운이 가득한 달이에요!",
        "🎉 좋은 추억을 만들 수 있어요!",
        "🌷 새로운 시작에 좋은 시기예요!"
    ]))

    st.subheader("💍 결혼운")
    st.success(random.choice([
        "💕 좋은 인연을 만날 가능성이 있어요!",
        "🌸 서로를 아껴주는 관계가 중요해요!",
        "💖 행복한 미래가 기다리고 있어요!"
    ]))

    st.subheader("💰 금전운")
    st.info(random.choice([
        "💰 계획적인 소비가 좋아요!",
        "🍀 작은 행운이 찾아올 수 있어요!",
        "✨ 절약이 행운을 가져와요!"
    ]))

    st.subheader("🏥 건강운")
    st.success(random.choice([
        "🚶 산책이 좋은 기운을 가져와요!",
        "💧 물을 충분히 마셔보세요!",
        "😴 충분한 휴식이 중요해요!"
    ]))

    st.subheader("🧑‍🤝‍🧑 친구운")
    st.info(random.choice([
        "🌸 친구들과 즐거운 일이 생길 수 있어요!",
        "💖 주변 사람들의 도움을 받을 수 있어요!",
        "😊 좋은 인연이 찾아올 수 있어요!"
    ]))

    st.subheader("🎓 대학 합격운")
    st.success(random.choice([
        "📚 꾸준한 노력이 빛을 발할 수 있어요!",
        "🌟 자신감을 가져보세요!",
        "🍀 좋은 결과가 기다리고 있을 수 있어요!"
    ]))

    st.subheader("🎨 행운의 색")
    st.write(random.choice(colors))

    st.subheader("🍰 행운의 음식")
    st.write(random.choice(foods))

    st.subheader("🎁 행운의 아이템")
    st.write(random.choice(items))

    st.subheader("🎲 행운의 숫자")
    st.write(random.randint(1,99))

    stars = "⭐" * random.randint(3,5)

    st.subheader("✨ 종합 운세")
    st.metric("행운 별점", stars)

    st.markdown("""
# 🌸🐰💖✨

💕 오늘도 행복한 하루 보내세요 💕

🌷🍀🎀🩷🌸✨🐰
""")
