import streamlit as st
import random
import time

st.set_page_config(page_title="数字炸damn游戏", page_icon=" ", layout="centered")

st.markdown("""
<style>
    .stApp {
        background-color: #ffffff;
    }
    .title-decoration {
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        color: #333;
    }
    .output-box {
        width: 150px;
        height: 113px;
        margin: 0 auto 2rem auto;
        background-color: #e6f3ff;
        border: 2px solid #000000;
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
        color: #000000;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .input-container {
        width: 100%;
        display: flex;
        justify-content: center;
        margin-top: 1rem;
    }
    .stNumberInput > div {
        border: 2px solid #000000 !important;
        border-radius: 5px !important;
        background-color: #ffffff !important;
    }
    .stButton > button {
        background-color: #f0f0f0;
        border: 1px solid #aaa;
        border-radius: 5px;
        margin-left: 10px;
    }
</style>
""", unsafe_allow_html=True)

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(0, 100)
    st.session_state.low = 0
    st.session_state.high = 100
    st.session_state.mode = None
    st.session_state.max_attempts = float('inf')
    st.session_state.attempts_left = float('inf')
    st.session_state.game_over = False
    st.session_state.message = ""
    st.session_state.won = False
    st.session_state.attempts_input = ""
    st.session_state.step = "setup"

st.markdown('<div class="title-decoration">数字炸damn游戏</div>', unsafe_allow_html=True)

if st.session_state.step == "setup":
    mode = st.radio("模式：", ["猜对胜利", "猜对失败"], index=None, horizontal=True)
    if mode:
        st.session_state.mode = 1 if mode == "猜对胜利" else 2

    attempts = st.text_input("尝试次数（不填为无限次数）", value=st.session_state.attempts_input)
    st.session_state.attempts_input = attempts

    if st.button("开始新游戏"):
        if st.session_state.mode is None:
            st.warning("请先选择模式")
        else:
            if attempts.strip() == "":
                st.session_state.max_attempts = float('inf')
            else:
                try:
                    st.session_state.max_attempts = int(attempts)
                    if st.session_state.max_attempts <= 0:
                        st.error("次数必须大于0")
                        st.stop()
                except:
                    st.error("请输入有效数字")
                    st.stop()
            st.session_state.attempts_left = st.session_state.max_attempts
            st.session_state.secret = random.randint(0, 100)
            st.session_state.low = 0
            st.session_state.high = 100
            st.session_state.game_over = False
            st.session_state.message = f"范围：0～100"
            st.session_state.step = "playing"
            st.rerun()

elif st.session_state.step == "playing":
    st.markdown(f'<div class="output-box">{st.session_state.message}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1,1])
    with col1:
        guess = st.number_input("", min_value=0, max_value=100, step=1, label_visibility="collapsed", key="guess_input")
    with col2:
        if st.button("猜测"):
            if guess < st.session_state.low or guess > st.session_state.high:
                st.session_state.message = f"数字必须在 {st.session_state.low}～{st.session_state.high} 之间"
            else:
                if st.session_state.attempts_left != float('inf'):
                    st.session_state.attempts_left -= 1

                if guess == st.session_state.secret:
                    st.session_state.game_over = True
                    if st.session_state.mode == 1:
                        st.session_state.message = f"对了！炸弹是 {st.session_state.secret}\n你赢了！"
                    else:
                        st.session_state.message = f"炸了！炸弹是 {st.session_state.secret}\n你输了！"
                elif guess > st.session_state.secret:
                    st.session_state.high = guess
                    st.session_state.message = f"damn在：{st.session_state.low}～{st.session_state.high}之间"
                else:
                    st.session_state.low = guess
                    st.session_state.message = f"damn在：{st.session_state.low}～{st.session_state.high}之间"

                if not st.session_state.game_over and st.session_state.attempts_left == 0 and st.session_state.max_attempts != float('inf'):
                    st.session_state.game_over = True
                    st.session_state.message = f"游戏结束！damn是 {st.session_state.secret}"

                if st.session_state.game_over:
                    st.session_state.step = "ended"
            st.rerun()

elif st.session_state.step == "ended":
    st.markdown(f'<div class="output-box">{st.session_state.message}</div>', unsafe_allow_html=True)

    if st.button("再来一局"):
        for key in ["secret", "low", "high", "mode", "max_attempts", "attempts_left", "game_over", "message", "won", "attempts_input", "step"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()