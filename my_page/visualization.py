import streamlit as st
import pandas as pd
import plotly.express as px
from utils.database import get_attempts_data

def main():
    st.title("Attempts Visualization")

    # Fetch attempts data
    attempts_data = get_attempts_data()
    df = pd.DataFrame(attempts_data)

    # Overall statistics
    st.subheader("Overall Statistics")
    total_attempts = len(df)
    correct_attempt_1 = df[df['attempt_1_answer'] == 'yes'].shape[0]
    correct_attempt_2 = df[(df['attempt_2_answer'] == 'yes')].shape[0]
    wrong_both_attempts = df[(df['attempt_1_answer'] == 'no') & (df['attempt_2_answer'] != 'no')].shape[0]
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Questions", total_attempts)
    col2.metric("Correct on 1st Attempt", correct_attempt_1)
    col3.metric("Correct on 2nd Attempt", correct_attempt_2)
    col4.metric("Wrong on Both Attempts", wrong_both_attempts)

    # Pie chart for attempt distribution
    pie_data = pd.DataFrame({
        'Category': ['Correct on 1st Attempt', 'Correct on 2nd Attempt', 'Wrong on Both Attempts'],
        'Count': [correct_attempt_1, correct_attempt_2, wrong_both_attempts]
    })

    fig_pie = px.pie(
        pie_data,
        names='Category',
        values='Count',
        title="Distribution of Attempts",
        color='Category',
        color_discrete_map={
            'Correct on 1st Attempt': 'green',
            'Correct on 2nd Attempt': 'yellow',
            'Wrong on Both Attempts': 'red'
        }
    )
    st.plotly_chart(fig_pie)

    # Detailed attempts table
    st.subheader("Detailed Attempts")
    st.dataframe(df)

if __name__ == "__main__":
    main()