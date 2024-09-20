# import streamlit as st
# from utils.database import get_data_from_db
# from utils.openai_helper import get_openai_response
# from utils.file_helper import get_file_content

# def main():
#     st.title("Answer Comparison")

#     # Check if a question has been selected, if not, warn the user
#     if 'selected_question' not in st.session_state:
#         st.warning("Please select a question first.")
#         return

#     # Fetch data from the database
#     data = get_data_from_db()
#     question_dict = {item['question']: item for item in data}
#     selected_case = question_dict[st.session_state.selected_question]

#     # Display the selected question
#     st.subheader("Question:")
#     st.write(st.session_state.selected_question)

#     # Display the expected answer
#     st.subheader("Expected Answer:")
#     st.write(selected_case['final_answer'])

#     # Get OpenAI response only if not already available in session state
#     if 'openai_response' not in st.session_state:
#         file_content = get_file_content(selected_case['file_name'])
#         st.session_state.openai_response = get_openai_response(st.session_state.selected_question, file_content)

#     # Display the OpenAI response
#     st.subheader("OpenAI Response:")
#     st.write(st.session_state.openai_response)

#     # Display buttons for Correct and Wrong, disable if not applicable
#     col1, col2 = st.columns(2)
#     with col1:
#         correct_button = st.button(
#             "Correct", 
#             disabled=(st.session_state.openai_response.lower() != selected_case['final_answer'].lower())
#         )
#     with col2:
#         wrong_button = st.button(
#             "Wrong", 
#             disabled=(st.session_state.openai_response.lower() == selected_case['final_answer'].lower())
#         )

#     # Handle button actions and change the current page state
#     if correct_button:
#         st.session_state.current_page = "Question Selection"
#     elif wrong_button:
#         st.session_state.current_page = "Edit Steps"

#     # Manage page navigation without rerun
#     if 'current_page' in st.session_state:
#         if st.session_state.current_page == "Question Selection":
#             st.write("Returning to question selection. Please refresh the app or proceed.")
#         elif st.session_state.current_page == "Edit Steps":
#             st.write("Navigating to Edit Steps page. Please refresh the app or proceed.")

# if __name__ == "__main__":
#     main()

# *************************************************************************************
# import streamlit as st
# from utils.database import get_data_from_db
# from utils.openai_helper import get_openai_response
# from utils.file_helper import get_file_content

# def main():
#     st.title("Answer Comparison")

#     # Check if a question has been selected, if not, warn the user
#     if 'selected_question' not in st.session_state:
#         st.warning("Please select a question first.")
#         return

#     # Fetch data from the database
#     data = get_data_from_db()
#     question_dict = {item['question']: item for item in data}
#     selected_case = question_dict[st.session_state.selected_question]

#     # Display the selected question
#     st.subheader("Question:")
#     st.write(st.session_state.selected_question)

#     # Display the expected answer
#     st.subheader("Expected Answer:")
#     st.write(selected_case['final_answer'])

#     # Get OpenAI response only if not already available in session state
#     if 'openai_response' not in st.session_state:
#         file_content = get_file_content(selected_case['file_name'])
#         st.session_state.openai_response = get_openai_response(st.session_state.selected_question, file_content)

#     # Display the OpenAI response, handle None case
#     st.subheader("OpenAI Response:")
#     openai_response = st.session_state.get('openai_response', None)

#     if openai_response:
#         st.write(openai_response)

#         # Display buttons for Correct and Wrong, disabled if not applicable
#         col1, col2 = st.columns(2)
#         with col1:
#             correct_button = st.button(
#                 "Correct", 
#                 disabled=(openai_response.lower() != selected_case['final_answer'].lower())
#             )
#         with col2:
#             wrong_button = st.button(
#                 "Wrong", 
#                 disabled=(openai_response.lower() == selected_case['final_answer'].lower())
#             )

#         # Handle button actions and change the current page state
#         if correct_button:
#             st.session_state.current_page = "Question Selection"
#         elif wrong_button:
#             st.session_state.current_page = "Edit Steps"

#     else:
#         st.error("OpenAI response is not available. Please check the process.")

# if __name__ == "__main__":
#     main()

import streamlit as st
from utils.database import get_data_from_db
from utils.openai_helper import get_openai_response
from utils.file_helper import get_file_content

def main():
    st.title("Answer Comparison")

    # Check if a question has been selected, if not, warn the user
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

    # Display the expected answer
    st.subheader("Expected Answer:")
    st.write(selected_case['final_answer'])

    # Button to get new OpenAI response
    if st.button("Get OpenAI Response"):
        file_content = get_file_content(selected_case['file_name'])
        st.session_state.openai_response = get_openai_response(st.session_state.selected_question, file_content)

    # Display the OpenAI response, handle None case
    st.subheader("OpenAI Response:")
    openai_response = st.session_state.get('openai_response', None)

    if openai_response:
        st.write(openai_response)

        # Display buttons for Correct and Wrong, disabled if not applicable
        col1, col2 = st.columns(2)
        with col1:
            correct_button = st.button(
                "Correct", 
                disabled=(openai_response.lower() != selected_case['final_answer'].lower())
            )
        with col2:
            wrong_button = st.button(
                "Wrong", 
                disabled=(openai_response.lower() == selected_case['final_answer'].lower())
            )

        # Handle button actions and change the current page state
        if correct_button:
            st.session_state.current_page = "Question Selection"
            # Clear the OpenAI response when returning to question selection
            st.session_state.pop('openai_response', None)
        elif wrong_button:
            st.session_state.current_page = "Edit Steps"
    else:
        st.info("Click 'Get OpenAI Response' to generate a new response.")

    # Clear OpenAI response when navigating away from this page
    if st.session_state.current_page != "Answer Comparison":
        st.session_state.pop('openai_response', None)

if __name__ == "__main__":
    main()