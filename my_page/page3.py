# import streamlit as st
# from utils.database import get_data_from_db
# from utils.openai_helper import get_openai_response
# from utils.file_helper import get_file_content

# def main():
#     st.title("Edit Steps")

#     if 'selected_question' not in st.session_state:
#         st.warning("Please select a question first.")
#         return

#     data = get_data_from_db()
#     question_dict = {item['question']: item for item in data}
#     selected_case = question_dict[st.session_state.selected_question]

#     st.subheader("Question:")
#     st.write(st.session_state.selected_question)

#     edited_steps = st.text_area("Edit steps and submit to OpenAI:", value=selected_case['steps'], height=200)

#     if st.button("Submit Edited Steps"):
#         file_content = get_file_content(selected_case['file_name'])
#         new_prompt = f"Question: {st.session_state.selected_question}\n\nSteps to solve:\n{edited_steps}\n\nBased on these steps and any additional context provided, what is the answer?"
#         st.session_state.new_openai_response = get_openai_response(new_prompt, file_content)
#         st.session_state.current_page = "Final Result"
#         st.experimental_rerun()
import streamlit as st
from utils.database import get_data_from_db
from utils.openai_helper import get_openai_response
from utils.file_helper import get_file_content

def main():
    st.title("Edit Steps")

    # Ensure a question has been selected
    if 'selected_question' not in st.session_state:
        st.warning("Please select a question first.")
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

        # Optionally use session state to control rerendering
        st.write("Steps submitted, see the final result on the next page.")

if __name__ == "__main__":
    main()
