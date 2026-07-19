import streamlit as st

st.set_page_config(
    page_title="로봇 배터리 UI",
    page_icon="🤖",
    layout="wide"
)

# 배터리 초기값
if "soc" not in st.session_state:
    st.session_state.soc = 86

st.title("🤖 스마트 로봇청소기 배터리 관리")

st.write(
    "사용자의 청소 패턴을 기반으로 "
    "필요한 배터리 SOC를 예측하는 UI입니다."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("현재 SOC", f"{st.session_state.soc}%")

with col2:
    st.metric("배터리 온도", "32℃")

with col3:
    st.metric("배터리 건강도", "95%")

st.progress(st.session_state.soc / 100)

if st.session_state.soc <= 20:
    st.error("배가 너무 고파요! 충전이 필요해요.")
else:
    st.success("배가 든든해요! 청소를 준비할게요.")

left, center, right = st.columns([1, 2, 1])

with left:
    if st.button("청소 시작", use_container_width=True):
        st.session_state.soc = max(
            0,
            st.session_state.soc - 15
        )
        st.rerun()

with center:
    st.markdown(
        """
        <div style="
            background-color:#FFF1D6;
            border-radius:24px;
            padding:50px;
            text-align:center;
            font-size:100px;
        ">
            🤖
        </div>
        """,
        unsafe_allow_html=True
    )

with right:
    if st.button("충전하기", use_container_width=True):
        st.session_state.soc = min(
            100,
            st.session_state.soc + 15
        )
        st.rerun()

st.write("")

if st.button("초기화"):
    st.session_state.soc = 86
    st.rerun()
