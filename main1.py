import streamlit as st
import random

def rock_paper_scissors_game():
    st.title("가위바위보 게임 ✊✋✌️")
    st.write("가위, 바위, 보 중 하나를 선택하세요!")

    # 세션 상태 초기화 (게임이 처음 시작되거나 리셋될 때)
    if "player_score" not in st.session_state:
        st.session_state.player_score = 0
        st.session_state.computer_score = 0
        st.session_state.message = "게임을 시작해볼까요?"
        st.session_state.last_choices = {"player": "없음", "computer": "없음"}

    choices = ["가위", "바위", "보"]

    # 사용자 선택 버튼
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✊ 바위"):
            player_choice = "바위"
        else:
            player_choice = None
    with col2:
        if st.button("✋ 보"):
            player_choice = "보"
        else:
            if player_choice is None: # 다른 버튼이 눌리지 않았을 때만 None 유지
                player_choice = None
    with col3:
        if st.button("✌️ 가위"):
            player_choice = "가위"
        else:
            if player_choice is None: # 다른 버튼이 눌리지 않았을 때만 None 유지
                player_choice = None

    if player_choice:
        computer_choice = random.choice(choices)

        st.session_state.last_choices["player"] = player_choice
        st.session_state.last_choices["computer"] = computer_choice

        # 승패 판정 로직
        if player_choice == computer_choice:
            st.session_state.message = f"당신: {player_choice}, 컴퓨터: {computer_choice} - 비겼습니다! 🤝"
        elif (player_choice == "바위" and computer_choice == "가위") or \
             (player_choice == "가위" and computer_choice == "보") or \
             (player_choice == "보" and computer_choice == "바위"):
            st.session_state.message = f"당신: {player_choice}, 컴퓨터: {computer_choice} - 당신이 이겼습니다! 🎉"
            st.session_state.player_score += 1
        else:
            st.session_state.message = f"당신: {player_choice}, 컴퓨터: {computer_choice} - 컴퓨터가 이겼습니다! 😥"
            st.session_state.computer_score += 1

    st.write("---")
    st.subheader("결과")
    st.write(st.session_state.message)
    st.write(f"당신의 선택: **{st.session_state.last_choices['player']}**")
    st.write(f"컴퓨터의 선택: **{st.session_state.last_choices['computer']}**")

    st.subheader("점수")
    st.metric(label="당신", value=st.session_state.player_score)
    st.metric(label="컴퓨터", value=st.session_state.computer_score)

    st.write("---")
    if st.button("점수 초기화"):
        st.session_state.player_score = 0
        st.session_state.computer_score = 0
        st.session_state.message = "게임을 다시 시작합니다!"
        st.session_state.last_choices = {"player": "없음", "computer": "없음"}
        st.experimental_rerun() # 앱을 새로고침하여 상태 초기화

if __name__ == "__main__":
    rock_paper_scissors_game()
