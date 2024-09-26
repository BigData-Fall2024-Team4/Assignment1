import streamlit as st
from utils.database import get_data_from_db, update_attempt
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
        # Check if a file is associated with the selected case
        if selected_case['file_name']:
            # Show that the file is being accessed
            st.info("Accessing file...")

            # Fetch the file content
            file_content = get_file_content(selected_case['file_name'])

            # Check for errors in file content
            if "Error" in file_content:
                st.session_state.file_error = file_content  # Save the error in session state
                st.session_state.openai_response = None  # Reset the OpenAI response if there's an error
            else:
                st.session_state.file_error = None  # Clear any previous errors
                st.session_state.openai_response = get_openai_response(st.session_state.selected_question, file_content)
        else:
            # No file attached, so just get the OpenAI response
            st.session_state.file_error = None
            st.session_state.openai_response = get_openai_response(st.session_state.selected_question)

        st.rerun()

    st.subheader("OpenAI Response:")

    # Display any file error below the OpenAI Response title
    if 'file_error' in st.session_state and st.session_state.file_error:
        st.error(st.session_state.file_error)

        # If the error is "File format not supported", show the "Back to Question" button
        if "File format not supported" in st.session_state.file_error:
            if st.button("Back to Question"):
                st.session_state.current_page = "Question Selection"
                st.session_state.pop('file_error', None)  # Clear the error message
                st.session_state.pop('openai_response', None)  # Reset OpenAI response
                st.rerun()

    elif 'openai_response' in st.session_state and st.session_state.openai_response:
        st.write(st.session_state.openai_response)

        # Add the correctness prompt
        expected_answer = selected_case['final_answer'].lower()
        openai_response = st.session_state.openai_response.lower()
        is_correct = expected_answer in openai_response or openai_response in expected_answer

        if is_correct:
            st.success("The answer might be correct.")
        else:
            st.warning("The answer might be wrong.")


        col1, col2 = st.columns(2)
        with col1:
            if st.button("Correct Answer"):
                update_attempt(st.session_state.selected_question, "yes", 1)
                st.session_state.current_page = "Question Selection"
                st.session_state.pop('openai_response', None)
                st.rerun()
        with col2:
            if st.button("Wrong Answer (Provide steps)"):
                update_attempt(st.session_state.selected_question, "no", 1)
                st.session_state.current_page = "Edit Steps"
                st.rerun()
    else:
        st.info("Click 'Get OpenAI Response' to generate a new response.")

    if st.session_state.current_page != "Answer Comparison":
        st.session_state.pop('openai_response', None)

if __name__ == "__main__":
    main()