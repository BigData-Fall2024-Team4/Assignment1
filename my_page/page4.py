import streamlit as st
from utils.database import get_data_from_db

def main():
    st.title("Final Result")

    # Ensure the user has gone through previous steps
    if 'selected_question' not in st.session_state or 'new_openai_response' not in st.session_state:
        st.warning("Please go through the previous steps first.")
        return

    # Fetch data from the database
    data = get_data_from_db()
    question_dict = {item['question']: item for item in data}
    selected_case = question_dict[st.session_state.selected_question]

    # Display selected question
    st.subheader("Question:")
    st.write(st.session_state.selected_question)

    # Display expected answer
    st.subheader("Expected Answer:")
    st.write(selected_case['final_answer'])

    # Display new OpenAI response
    st.subheader("New OpenAI Response:")
    st.write(st.session_state.new_openai_response)

    # Handle the "Back to Question Selection" button without rerun
    if st.button("Back to Question Selection"):
        # Reset session state variables
        st.session_state.current_page = "Question Selection"
        st.session_state.selected_question = None
        st.session_state.openai_response = None
        st.session_state.new_openai_response = None

        # Instead of using st.experimental_rerun, just inform the user
        st.write("Navigating back to the question selection. Please refresh or continue as needed.")

if __name__ == "__main__":
    main()
