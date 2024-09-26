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

    is_correct = expected_answer in openai_response or openai_response in expected_answer
    
    if is_correct:
        st.success("Note: The answer appears to be correct.")
    else:
        st.warning("Note: The answer might be incorrect.")

    st.write("Please verify and select whether the answer is correct or wrong:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Correct"):
            update_attempt(st.session_state.selected_question, "yes", 2)
            st.success("Updated as correct answer.")
            st.session_state.current_page = "Question Selection"
            st.rerun()
    
    with col2:
        if st.button("Wrong"):
            update_attempt(st.session_state.selected_question, "no", 2)
            st.error("Updated as wrong answer.")
            st.session_state.current_page = "Question Selection"
            st.rerun()

if __name__ == "__main__":
    main()