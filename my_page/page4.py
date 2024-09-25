import streamlit as st
from utils.database import get_data_from_db, update_attempt

def main():
    st.title("Final Result")

    if 'selected_question' not in st.session_state or 'new_openai_response' not in st.session_state or st.session_state.selected_question is None:
        st.warning("Please go through the previous steps first.")
        return

    data = get_data_from_db()
    question_dict = {item['question']: item for item in data}
    selected_case = question_dict[st.session_state.selected_question]

    st.subheader("Question:")
    st.write(st.session_state.selected_question)

    st.subheader("Expected Answer:")
    st.write(selected_case['final_answer'])

    st.subheader("New OpenAI Response:")
    st.write(st.session_state.new_openai_response)

    expected_answer = selected_case['final_answer'].lower()
    openai_response = st.session_state.new_openai_response.lower()

    if expected_answer in openai_response or openai_response in expected_answer:
        st.success("The answer matches or contains the expected answer!")
        if st.button("Correct Answer"):
            update_attempt(st.session_state.selected_question, "yes", 2)
            st.session_state.current_page = "Question Selection"
            st.rerun()
    else:
        st.error("The answer does not match or contain the expected answer.")
        if st.button("Wrong Answer"):
            update_attempt(st.session_state.selected_question, "no", 2)
            st.session_state.current_page = "Question Selection"
            st.rerun()

    if st.button("Back to Question"):
        st.session_state.current_page = "Question Selection"
        st.session_state.selected_question = None
        st.session_state.openai_response = None
        st.session_state.new_openai_response = None
        st.rerun()

if __name__ == "__main__":
    main()