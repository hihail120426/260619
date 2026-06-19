import streamlit as st
import random

st.set_page_config(
    page_title="🌈 MBTI 진로 탐험소",
    page_icon="🐰",
    layout="centered"
)

# 배경 꾸미기
st.markdown("""
<style>
.stApp{
background: linear-gradient(to bottom,#FFF0F5,#E6F7FF);
}

h1,h2,h3{
text-align:center;
}

div[data-testid="stMetric"]{
background-color:white;
padding:15px;
border-radius:20px;
}

</style>
""", unsafe_allow_html=True)

st.title("🌈✨ MBTI 진로 탐험소 ✨🌈")
st.markdown("## 🐰 나에게 어울리는 꿈은 무엇일까? 💖")
st.write("⭐ 미래의 나를 만나보자! ⭐")

career_data = {

"INTJ":{
"직업":["🧠 데이터 과학자","💻 개발자","🔬 연구원"],
"학과":"컴퓨터공학과",
"계열":"자연계열",
"이유":"논리적 사고와 분석 능력이 뛰어나요!",
"적성":5
},

"INTP":{
"직업":["💡 발명가","🔍 연구원","👨‍💻 프로그래머"],
"학과":"전자공학과",
"계열":"자연계열",
"이유":"호기심이 많고 새로운 것을 탐구하는 것을 좋아해요!",
"적성":5
},

"ENTJ":{
"직업":["👑 CEO","📈 경영 컨설턴트","⚖️ 변호사"],
"학과":"경영학과",
"계열":"인문계열",
"이유":"리더십과 추진력이 뛰어나요!",
"적성":5
},

"ENTP":{
"직업":["🚀 창업가","🎤 마케터","📺 콘텐츠 기획자"],
"학과":"광고홍보학과",
"계열":"인문계열",
"이유":"창의적인 아이디어가 풍부해요!",
"적성":5
},

"INFJ":{
"직업":["💖 상담사","✍️ 작가","🏫 교사"],
"학과":"심리학과",
"계열":"인문계열",
"이유":"다른 사람을 이해하고 돕는 능력이 뛰어나요!",
"적성":4
},

"INFP":{
"직업":["🎨 디자이너","🎵 음악가","📚 작가"],
"학과":"디자인학과",
"계열":"예체능계열",
"이유":"감수성과 창의성이 풍부해요!",
"적성":5
},

"ENFP":{
"직업":["🎬 크리에이터","🌍 여행작가","📺 방송인"],
"학과":"미디어학과",
"계열":"인문계열",
"이유":"열정적이고 사람들과 잘 어울려요!",
"적성":4
},

"ISTJ":{
"직업":["📊 회계사","🏛 공무원","⚖️ 법률 전문가"],
"학과":"행정학과",
"계열":"인문계열",
"이유":"성실하고 책임감이 강해요!",
"적성":5
},

"ISFP":{
"직업":["📸 사진작가","🎨 일러스트레이터","🎵 음악가"],
"학과":"예술학과",
"계열":"예체능계열",
"이유":"예술적 감각이 뛰어나요!",
"적성":4
},

"ESTP":{
"직업":["🏅 스포츠 선수","💼 영업 전문가","🚀 기업가"],
"학과":"체육학과",
"계열":"예체능계열",
"이유":"도전 정신이 강하고 활동적이에요!",
"적성":4
},

"ESFP":{
"직업":["🎤 연예인","🎭 배우","📺 유튜버"],
"학과":"연극영화과",
"계열":"예체능계열",
"이유":"밝고 에너지가 넘쳐요!",
"적성":5
}

}

# 없는 MBTI 자동 생성
all_mbti = [
"INTJ","INTP","ENTJ","ENTP",
"INFJ","INFP","ENFJ","ENFP",
"ISTJ","ISFJ","ESTJ","ESFJ",
"ISTP","ISFP","ESTP","ESFP"
]

sample = career_data["ENFP"]

for mbti in all_mbti:
    if mbti not in career_data:
        career_data[mbti] = sample

mbti = st.selectbox(
"💌 MBTI를 선택해 주세요!",
all_mbti
)

if st.button("🔮 진로 추천 받기 ✨"):

    st.balloons()

    data = career_data[mbti]

    st.success(f"🎉 {mbti} 유형 분석 완료!")

    st.subheader("🌟 추천 직업")

    for job in data["직업"]:
        st.write(job)

    st.subheader("📚 추천 학과")
    st.info(data["학과"])

    st.subheader("🏫 추천 계열")
    st.info(data["계열"])

    st.subheader("💡 추천 이유")
    st.success(data["이유"])

    st.subheader("🏆 적성 점수")

    stars = "⭐" * data["적성"]
    st.metric("적합도", stars)

    messages = [
        "🌱 작은 꿈이 큰 미래가 될 수 있어요!",
        "🚀 여러분의 가능성은 무한해요!",
        "🌈 자신만의 꿈을 찾아가 보세요!",
        "💖 오늘의 선택이 미래를 만들어요!",
        "✨ 무엇이든 도전해 보세요!"
    ]

    st.subheader("💌 응원 메시지")
    st.write(random.choice(messages))

    st.write("---")

    st.markdown("""
    # 🐰🌸✨

    ⭐⭐⭐⭐⭐

    💖 꿈꾸는 여러분을 응원합니다 💖

    🌈✨🩵🌷🐰🌸🎀⭐
    """)

st.write("---")
st.caption("🐰 MBTI 진로 탐험소 🌸")
