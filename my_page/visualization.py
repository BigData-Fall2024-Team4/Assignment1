import streamlit as st
import pandas as pd
import plotly.express as px
from utils.database import get_data_from_db

def visualization_page():
    st.title("Answer Visualization")

    data = get_data_from_db()
    
    # Count correct and incorrect answers
    correct_count = sum(1 for item in data if item.get('correct_answer', False))
    incorrect_count = len(data) - correct_count

    # Create a DataFrame for the pie chart
    df = pd.DataFrame({
        'Status': ['Correct', 'Incorrect'],
        'Count': [correct_count, incorrect_count]
    })

    # Create the pie chart
    fig = px.pie(df, values='Count', names='Status', title='Correct vs Incorrect Answers')
    
    # Display the chart
    st.plotly_chart(fig)

    # Display a table with question details
    st.subheader("Question Details")
    question_data = [
        {
            "Question": item['question'],
            "Status": "Correct" if item.get('correct_answer', False) else "Incorrect"
        }
        for item in data
    ]
    st.table(pd.DataFrame(question_data))

if __name__ == "__main__":
    visualization_page()
