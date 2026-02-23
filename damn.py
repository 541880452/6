import streamlit as st
import random
import time

st.set_page_config(page_title="damn游戏", page_icon=" ", layout="centered")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(145deg, #f9f9f9 0%, #ffffff 100%);
    }
    .title-decoration {
        text-align: center;
        font-size: 3rem;
        margin-bottom: 2rem;
        color: #2c3e50;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        font-weight: 600;
    }
    .output-box {
        width: 60%;
        height: 40vh;
        margin: 0 auto 3rem auto;
        background-color: #e6f3ff;
        border: 3px solid #2c3e50;
        border-radius: 20px;
        padding: 20px;
        font-size: 24px;
        color: #1e2b36;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
    }
    .input-wrapper {
        width: 60%;
        margin: 0 auto;
        height: 20vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .stNumberInput > div {
        border: 2px solid #2c3e50 !important;
        border-radius: 10px !important;
        background-color: #ffffff !important;
        font-size: 20px !important;
        padding: 8px !important;
    }
    .stButton > button {
        background-color: #f0f0f0;
        border: 2px solid #2c3e50;
        border-radius: 10px;
        font-size: 20px;
        padding: 10px 25px;
        transition: all 0.2s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton > button:hover {
        background-color: #e0e0e0;
        transform: translateY(-2px);
        box-shadow: 0 6px 10px rgba(0,0,0,0.15);
    }
    div[data-testid="stNumberInput"] label {
        display: none !important;
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

st.markdown('<div class="title-decoration">damn游戏</div>', unsafe_allow_html=True)

if st.session_state.step == "setup":
    mode = st.radio("选择模式：", ["猜对胜利", "猜对失败"], index=None, horizontal=True)
    if mode:
        st.session_state.mode = 1 if mode == "猜对胜利" else 2

    attempts = st.text_input("尝试次数（留空为无限次）", value=st.session_state.attempts_input)
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
            st.session_state.message = f"范围：0～100\n剩余次数：{'∞' if st.session_state.attempts_left == float('inf') else st.session_state.attempts_left}"
            st.session_state.step = "playing"
            st.rerun()

elif st.session_state.step == "playing":
    st.markdown(f'<div class="output-box">{st.session_state.message}</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1:
            guess = st.number_input("", min_value=0, max_value=100, step=1, label_visibility="collapsed", key="guess_input")
        with col2:
            if st.button("猜"):
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
                        st.session_state.message = f"大了\n范围：{st.session_state.low}～{st.session_state.high}"
                    else:
                        st.session_state.low = guess
                        st.session_state.message = f"小了\n范围：{st.session_state.low}～{st.session_state.high}"

                    if not st.session_state.game_over and st.session_state.attempts_left == 0 and st.session_state.max_attempts != float('inf'):
                        st.session_state.game_over = True
                        st.session_state.message = f"次数用完！炸弹是 {st.session_state.secret}"

                    if st.session_state.game_over:
                        st.session_state.step = "ended"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.step == "ended":
    st.markdown(f'<div class="output-box">{st.session_state.message}</div>', unsafe_allow_html=True)

    if st.button("再来一局"):
        for key in ["secret", "low", "high", "mode", "max_attempts", "attempts_left", "game_over", "message", "won", "attempts_input", "step"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()