
import streamlit as st
from utils.database import get_data_from_db
from utils.openai_helper import get_openai_response
from utils.file_helper import get_file_content

def main():
    st.title("Answer Comparison")

    if 'selected_question' not in st.session_state or st.session_state.selected_question is None:
        st.warning("Please select a question on the Question Selection page first.")
        return

    data = get_data_from_db()
    question_dict = {item['question']: item for item in data}
    selected_case = question_dict[st.session_state.selected_question]

    st.subheader("Question:")
    st.write(st.session_state.selected_question)

    st.subheader("Expected Answer:")
    st.write(selected_case['final_answer'])

    if st.button("Get OpenAI Response"):
        file_content = get_file_content(selected_case['file_name'])
        st.session_state.openai_response = get_openai_response(st.session_state.selected_question, file_content)
        st.rerun()

    st.subheader("OpenAI Response:")
    openai_response = st.session_state.get('openai_response', None)

    if openai_response:
        st.write(openai_response)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Correct Answer"):
                st.session_state.current_page = "Question Selection"
                st.session_state.pop('openai_response', None)
                st.rerun()
        with col2:
            if st.button("Wrong Answer(Provide steps)"):
                st.session_state.current_page = "Edit Steps"
                st.rerun()
    else:
        st.info("Click 'Get OpenAI Response' to generate a new response.")

    if st.session_state.current_page != "Answer Comparison":
        st.session_state.pop('openai_response', None)

if __name__ == "__main__":
    main()