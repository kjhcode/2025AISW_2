import streamlit as st
import random

def quiz_game():
    st.title("간단 퀴즈 게임 🧠")
    st.write("아래 질문에 대한 정답을 선택하세요!")

    # 퀴즈 질문과 정답, 선택지 정의
    # 퀴즈를 더 추가하고 싶으면 이 리스트에 딕셔너리 형태로 추가하세요!
    quiz_data = [
        {
            "question": "대한민국의 수도는 어디일까요?",
            "options": ["부산", "서울", "대구", "인천"],
            "answer": "서울"
        },
        {
            "question": "다음 중 파이썬(Python)의 창시자는 누구일까요?",
            "options": ["제임스 고슬링", "귀도 반 로섬", "빌 게이츠", "스티브 잡스"],
            "answer": "귀도 반 로섬"
        },
        {
            "question": "지구상에서 가장 큰 바다는 어디일까요?",
            "options": ["대서양", "인도양", "북극해", "태평양"],
            "answer": "태평양"
        },
        {
            "question": "사과가 떨어지는 것을 보고 만유인력의 법칙을 발견한 사람은 누구일까요?",
            "options": ["알베르트 아인슈타인", "아이작 뉴턴", "갈릴레오 갈릴레이", "니콜라 테슬라"],
            "answer": "아이작 뉴턴"
        }
    ]

    # 세션 상태 초기화
    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0
        st.session_state.score = 0
        st.session_state.game_over = False
        st.session_state.feedback_message = ""
        st.session_state.quiz_order = list(range(len(quiz_data)))
        random.shuffle(st.session_state.quiz_order) # 질문 순서 무작위화

    # 게임이 종료된 경우
    if st.session_state.game_over:
        st.success(f"퀴즈가 종료되었습니다! 당신의 점수는 {st.session_state.score}점입니다. 🎉")
        if st.button("다시 시작"):
            st.session_state.current_question_index = 0
            st.session_state.score = 0
            st.session_state.game_over = False
            st.session_state.feedback_message = ""
            random.shuffle(st.session_state.quiz_order)
            st.experimental_rerun() # 앱 새로고침
        return

    # 현재 질문 가져오기
    current_q_index_in_order = st.session_state.quiz_order[st.session_state.current_question_index]
    question = quiz_data[current_q_index_in_order]

    st.subheader(f"문제 {st.session_state.current_question_index + 1}. {question['question']}")

    # 사용자가 선택한 답을 저장할 변수
    selected_option = st.radio("정답을 선택하세요:", question["options"], key=f"q_{current_q_index_in_order}")

    submit_button = st.button("정답 제출")

    if submit_button:
        # 정답 확인
        if selected_option == question["answer"]:
            st.session_state.score += 1
            st.session_state.feedback_message = "정답입니다! ✅"
        else:
            st.session_state.feedback_message = f"오답입니다. ❌ 정답은 '{question['answer']}'였습니다."

        st.write(st.session_state.feedback_message)
        st.write(f"현재 점수: {st.session_state.score}점")

        # 다음 질문으로 넘어가기 (또는 게임 종료)
        st.session_state.current_question_index += 1
        if st.session_state.current_question_index >= len(quiz_data):
            st.session_state.game_over = True
        st.button("다음 문제" if not st.session_state.game_over else "결과 확인") # 다음 문제 버튼 클릭 시 새로고침
        st.experimental_rerun() # 상태 업데이트 후 화면 새로고침

    st.write("---")
    st.write(f"현재 점수: {st.session_state.score}점")

if __name__ == "__main__":
    quiz_game()
