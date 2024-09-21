from streamlit_option_menu import option_menu
import importlib
import streamlit as st

# Set page configuration
st.set_page_config(page_title="Dataset Application", layout="wide")

# Function to dynamically load a page
def load_page(page_name):
    try:
        module = importlib.import_module(f"my_page.{page_name}")
        module.main()
    except ImportError:
        st.error(f"Error: Could not load the page '{page_name}'. Please check if the file exists and is properly formatted.")

def main():
    # Define and store the current page in session state to manage navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Question Selection"  # Default page
    if 'selected_question' not in st.session_state:
        st.session_state.selected_question = None

    # Sidebar with navigation menu
    with st.sidebar:
        selected = option_menu(
            menu_title="Navigation",
            options=["Question Selection", "Answer Comparison", "Edit Steps", "Final Result"],
            default_index=["Question Selection", "Answer Comparison", "Edit Steps", "Final Result"].index(st.session_state.current_page),
        )

    # Update the current page in session state based on user selection
    if selected != st.session_state.current_page:
        st.session_state.current_page = selected
        st.rerun()  # Use st.rerun() instead of st.experimental_rerun()

    # Load the appropriate page based on selection
    page_mapping = {
        "Question Selection": "page1",
        "Answer Comparison": "page2",
        "Edit Steps": "page3",
        "Final Result": "page4"
    }

    if st.session_state.current_page in page_mapping:
        load_page(page_mapping[st.session_state.current_page])
    else:
        st.error("Invalid page selection.")

if __name__ == "__main__":
    main()