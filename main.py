# import streamlit as st
# import mysql.connector
# from openai import OpenAI
# import os
# from dotenv import load_dotenv
# import pandas as pd
# import json
# import docx
# import PyPDF2
# from PIL import Image
# import io
# import pptx
# from azure.storage.blob import BlobServiceClient
# import logging

# # Load environment variables from .env file
# load_dotenv()

# # Set up OpenAI API key
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # Set up Azure Blob Storage connection
# blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_CONNECTION_STRING"))
# container_client = blob_service_client.get_container_client(os.getenv("AZURE_CONTAINER_NAME"))

# # Function to get questions, answers, steps, and file names from MySQL
# def get_data_from_db():
#     try:
#         connection = mysql.connector.connect(
#             host=os.getenv("MYSQL_HOST"),
#             user=os.getenv("MYSQL_USER"),
#             passwd=os.getenv("MYSQL_PASSWORD"),
#             database=os.getenv("MYSQL_DATABASE"),
#             auth_plugin='mysql_native_password'
#         )
#         cursor = connection.cursor(dictionary=True)
#         cursor.execute("SELECT question, final_answer, steps, file_name FROM validation_cases")
#         results = cursor.fetchall()
#         cursor.close()
#         connection.close()
#         return results
#     except mysql.connector.Error as err:
#         st.error(f"Error connecting to MySQL: {err}")
#         return []

# def get_file_content(file_name):
#     try:
#         logging.info(f"Attempting to retrieve file: {file_name} from Azure Blob Storage")
#         blob_client = container_client.get_blob_client(file_name)
#         file_content = blob_client.download_blob().readall()
#         file_extension = os.path.splitext(file_name)[1].lower()
        
#         logging.info(f"Successfully retrieved file: {file_name}")

#         if file_extension in ['.xlsx', '.csv']:
#             df = pd.read_excel(io.BytesIO(file_content)) if file_extension == '.xlsx' else pd.read_csv(io.StringIO(file_content.decode()))
#             return df.to_string()
        
#         elif file_extension == '.pdb':
#             return file_content.decode()
        
#         elif file_extension == '.json':
#             return json.dumps(json.loads(file_content), indent=2)
        
#         elif file_extension in ['.png', '.jpg']:
#             image = Image.open(io.BytesIO(file_content))
#             return f"Image dimensions: {image.size}"
        
#         elif file_extension == '.docx':
#             doc = docx.Document(io.BytesIO(file_content))
#             return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
#         elif file_extension == '.zip':
#             with zipfile.ZipFile(io.BytesIO(file_content)) as zip_ref:
#                 return "\n".join(zip_ref.namelist())
        
#         elif file_extension == '.mp3':
#             return f"Audio file: {file_name}"
        
#         elif file_extension == '.txt':
#             return file_content.decode()
        
#         elif file_extension == '.pptx':
#             prs = pptx.Presentation(io.BytesIO(file_content))
#             text = []
#             for slide in prs.slides:
#                 for shape in slide.shapes:
#                     if hasattr(shape, 'text'):
#                         text.append(shape.text)
#             return "\n".join(text)
        
#         elif file_extension == '.pdf':
#             pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
#             text = []
#             for page in pdf_reader.pages:
#                 text.append(page.extract_text())
#             return "\n".join(text)
        
#         elif file_extension == '.py':
#             return file_content.decode()
        
#         else:
#             return f"Unsupported file type: {file_extension}"
    
#     except Exception as e:
#         st.error(f"Error reading file from Azure Blob Storage: {str(e)}")
#         return None

# def get_openai_response(prompt, file_content=None):
#     try:
#         messages = [
#             {"role": "system", "content": "You are a helpful assistant. Please provide your answer in one word or one number only."},
#             {"role": "user", "content": prompt + " Answer in one word or one number only."}
#         ]
        
#         if file_content:
#             messages.insert(1, {"role": "user", "content": f"Here's additional context from a file:\n\n{file_content}"})
        
#         logging.info("Sending request to OpenAI")
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=messages,
#             max_tokens=300,
#             n=1,
#             temperature=0.7
#         )
#         logging.info("Received response from OpenAI")
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         return f"Error: {str(e)}"

# def main():
#     st.title("Dataset Application - Assignment 1")

#     # Initialize session state
#     if 'initial_openai_response' not in st.session_state:
#         st.session_state.initial_openai_response = None
#     if 'edited_openai_response' not in st.session_state:
#         st.session_state.edited_openai_response = None
#     if 'edited_steps_submitted' not in st.session_state:
#         st.session_state.edited_steps_submitted = False
#     if 'file_content' not in st.session_state:
#         st.session_state.file_content = None

#     # Fetch data from the database
#     data = get_data_from_db()

#     if data:
#         # Create dictionaries mapping questions to their answers, steps, and file names
#         question_dict = {item['question']: item for item in data}
        
#         # Dropdown for selecting a question
#         selected_question = st.selectbox("Select a question:", list(question_dict.keys()))

#         if selected_question:
#             selected_case = question_dict[selected_question]
#             expected_answer = selected_case['final_answer']
#             steps = selected_case['steps']
#             file_name = selected_case['file_name']

#             st.subheader("Expected Answer:")
#             st.write(expected_answer)

#             # Check if file name exists and is not empty
#             if file_name and file_name.strip():
#                 st.info(f"File associated with this question: {file_name}")
#                 st.session_state.file_content = get_file_content(file_name)
#                 if st.session_state.file_content:
#                     st.success("File content loaded successfully")
#                     if len(st.session_state.file_content) > 1000:
#                         st.write(st.session_state.file_content[:1000] + "... (truncated)")
#                     else:
#                         st.write(st.session_state.file_content)
#                 else:
#                     st.warning("Failed to load file content")

#             # Submit button for initial OpenAI response
#             if st.button("Submit to OpenAI"):
#                 # Get initial response from OpenAI
#                 prompt = f"Question: {selected_question}\n\nPlease provide an answer based on the information given."
#                 st.session_state.initial_openai_response = get_openai_response(prompt, st.session_state.file_content)
#                 st.session_state.edited_steps_submitted = False
#                 st.session_state.edited_openai_response = None

#             # Display the initial OpenAI response
#             if st.session_state.initial_openai_response:
#                 st.subheader("Initial OpenAI Response:")
#                 st.write(st.session_state.initial_openai_response)

#                 # Compare initial answer
#                 if st.session_state.initial_openai_response.lower() == expected_answer.lower():
#                     st.success("OpenAI's initial answer matches the expected answer!")
#                 else:
#                     st.error("OpenAI's initial answer does not match the expected answer.")
                    
#                     # Show editable text box with steps
#                     edited_steps = st.text_area("Edit steps and submit to OpenAI:", value=steps, height=200)
                    
#                     # Button to submit edited steps
#                     if st.button("Submit Edited Steps to OpenAI"):
#                         new_prompt = f"Question: {selected_question}\n\nSteps to solve:\n{edited_steps}\n\nBased on these steps and any additional context provided, what is the answer?"
#                         st.session_state.edited_openai_response = get_openai_response(new_prompt, st.session_state.file_content)
#                         st.session_state.edited_steps_submitted = True
#                         st.rerun()

#             # Display new response after submitting edited steps
#             if st.session_state.edited_steps_submitted and st.session_state.edited_openai_response:
#                 st.subheader("New OpenAI Response (Based on Edited Steps):")
#                 st.write(st.session_state.edited_openai_response)

#                 # Compare new response with expected answer
#                 if st.session_state.edited_openai_response.lower() == expected_answer.lower():
#                     st.success("The new answer matches the expected answer!")
#                 else:
#                     st.error("The new answer still does not match the expected answer.")

#     else:
#         st.error("No data available. Please check your database connection.")

# if __name__ == "__main__":
#     main()



from streamlit_option_menu import option_menu
import importlib
import streamlit as st

# Set page configuration
st.set_page_config(page_title="Dataset Application", layout="wide")

# Function to dynamically load a page
def load_page(page_name):
    module = importlib.import_module(f"my_page.{page_name}")
    module.main()

def main():
    # Define and store the current page in session state to manage navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Question Selection"  # Default page

    # Sidebar with navigation menu
    with st.sidebar:
        selected = option_menu(
            menu_title="Navigation",
            options=["Question Selection", "Answer Comparison", "Edit Steps", "Final Result"],
            default_index=["Question Selection", "Answer Comparison", "Edit Steps", "Final Result"].index(st.session_state.current_page),
        )

    # Update the current page in session state based on user selection
    st.session_state.current_page = selected

    # Load the appropriate page based on selection
    if selected == "Question Selection":
        load_page("page1")
    elif selected == "Answer Comparison":
        load_page("page2")
    elif selected == "Edit Steps":
        load_page("page3")
    elif selected == "Final Result":
        load_page("page4")

if __name__ == "__main__":
    main()
