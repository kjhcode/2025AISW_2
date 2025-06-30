import streamlit as st
import random

st.set_page_config(layout="wide") # 페이지를 넓게 사용하도록 설정

st.title("🔫 팬더의 텍스트 FPS 시뮬레이션")
st.write("환영해, 팬더 용사! 지금부터 너의 임무를 시작한다!")

if 'game_state' not in st.session_state:
    st.session_state.game_state = 'start'
    st.session_state.score = 0
    st.session_state.ammo = 10

def start_game():
    st.session_state.game_state = 'playing'
    st.session_state.score = 0
    st.session_state.ammo = 10
    st.session_state.message = "전방에 적이 나타났다! 어떻게 할까?"

def shoot_enemy():
    if st.session_state.ammo > 0:
        st.session_state.ammo -= 1
        if random.random() < 0.7: # 70% 확률로 명중
            st.session_state.score += 1
            st.session_state.message = "명중! 적을 제압했다! 다음 적을 찾아보자."
        else:
            st.session_state.message = "아쉽게 빗나갔다! 탄약이 줄었어. 다음 적은 꼭 맞춰봐!"
    else:
        st.session_state.message = "탄약이 없어! 재장전이 필요하다!"
    st.session_state.game_state = 'playing'

def reload_ammo():
    st.session_state.ammo = 10
    st.session_state.message = "재장전 완료! 다시 싸울 준비가 되었다!"
    st.session_state.game_state = 'playing'

def run_away():
    st.session_state.message = "후퇴! 다음 기회를 노리자... 게임 종료!"
    st.session_state.game_state = 'end'

# 게임 상태에 따른 화면 구성
if st.session_state.game_state == 'start':
    st.write("미션을 시작하려면 아래 버튼을 눌러줘!")
    if st.button("미션 시작"):
        start_game()
        st.experimental_rerun() # 상태 변경 후 새로고침

elif st.session_state.game_state == 'playing':
    st.subheader("현재 상황")
    st.info(st.session_state.message)
    st.write(f"🎯 점수: {st.session_state.score}점")
    st.write(f"🔫 남은 탄약: {st.session_state.ammo}발")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("사격!", help="적에게 총을 쏜다."):
            shoot_enemy()
            st.experimental_rerun()
    with col2:
        if st.button("재장전", help="탄약을 보충한다."):
            reload_ammo()
            st.experimental_rerun()
    with col3:
        if st.button("후퇴", help="미션을 포기하고 도망간다."):
            run_away()
            st.experimental_rerun()

elif st.session_state.game_state == 'end':
    st.subheader("미션 종료!")
    st.warning(st.session_state.message)
    st.write(f"최종 점수: {st.session_state.score}점")
    if st.button("다시 시작하기"):
        start_game()
        st.experimental_rerun()

st.sidebar.markdown("---")
st.sidebar.header("게임 정보")
st.sidebar.write("이 게임은 Streamlit으로 만든 아주 간단한 텍스트 기반 시뮬레이션입니다.")
st.sidebar.write("실제 FPS 게임과는 다릅니다.")
