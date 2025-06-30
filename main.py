import streamlit as st
import random

def guess_the_number_game():
    st.title("숫자 맞히기 게임 🎮")
    st.write("1부터 100 사이의 숫자를 맞춰보세요!")

    # 세션 상태에 정답이 없으면 새로운 정답 생성
    if "secret_number" not in st.session_state:
        st.session_state.secret_number = random.randint(1, 100)
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.session_state.message = ""

    # 게임이 종료되었으면 다시 시작 버튼 표시
    if st.session_state.game_over:
        st.success(f"축하합니다! {st.session_state.secret_number}을(를) {st.session_state.attempts}번 만에 맞히셨습니다!")
        if st.button("다시 시작"):
            st.session_state.secret_number = random.randint(1, 100)
            st.session_state.attempts = 0
            st.session_state.game_over = False
            st.session_state.message = ""
            st.experimental_rerun() # 앱을 새로고침하여 상태 초기화
        return

    # 사용자 입력 받기
    user_guess = st.number_input("숫자를 입력하세요:", min_value=1, max_value=100, value=50, step=1)
    submit_button = st.button("제출")

    if submit_button:
        st.session_state.attempts += 1
        if user_guess < st.session_state.secret_number:
            st.session_state.message = "UP! ⬆️ 더 큰 숫자입니다."
        elif user_guess > st.session_state.secret_number:
            st.session_state.message = "DOWN! ⬇️ 더 작은 숫자입니다."
        else:
            st.session_state.message = "정답입니다! 🎉"
            st.session_state.game_over = True

    st.write(st.session_state.message)
    st.write(f"시도 횟수: {st.session_state.attempts}번")

if __name__ == "__main__":
    guess_the_number_game()
