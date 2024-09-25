import streamlit as st
from utils.database import get_data_from_db, update_attempt
from utils.openai_helper import get_openai_response
from utils.file_helper import get_file_content

def main():
    st.title("Edit Steps")

    # Ensure a question has been selected
    if 'selected_question' not in st.session_state or st.session_state.selected_question is None:
        st.warning("Please select a question on the Question Selection page first.")
        return

    # Fetch data from the database
    data = get_data_from_db()
    question_dict = {item['question']: item for item in data}
    selected_case = question_dict[st.session_state.selected_question]

    # Display the selected question
    st.subheader("Question:")
    st.write(st.session_state.selected_question)

    # Allow the user to edit the steps
    edited_steps = st.text_area("Edit steps and submit to OpenAI:", value=selected_case['steps'], height=200)

    # Submit the edited steps to OpenAI
    if st.button("Submit Edited Steps"):
        file_content = get_file_content(selected_case['file_name'])
        new_prompt = f"Question: {st.session_state.selected_question}\n\nSteps to solve:\n{edited_steps}\n\nBased on these steps and any additional context provided, what is the answer?"
        st.session_state.new_openai_response = get_openai_response(new_prompt, file_content)
        st.session_state.current_page = "Final Result"
        st.rerun()

if __name__ == "__main__":
    main()