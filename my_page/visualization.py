import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from utils.database import get_attempts_data

def main():
    st.title("Overall Statistics")

    # Fetch attempts data
    attempts_data = get_attempts_data()
    df = pd.DataFrame(attempts_data)


    # Overall statistics
    st.subheader("")
    total_attempts = len(df)
    correct_attempt_1 = df[df['attempt_1_answer'] == 'yes'].shape[0]
    correct_attempt_2 = df[(df['attempt_1_answer'] != 'yes') & (df['attempt_2_answer'] == 'yes')].shape[0]
    wrong_both_attempts = df[(df['attempt_1_answer'] == 'no') & (df['attempt_2_answer'] == 'no')].shape[0]
    unanswered_questions = df[(df['attempt_1_answer'].isin(['yes', 'no']) == False) & 
                              (df['attempt_2_answer'].isin(['yes', 'no']) == False)].shape[0]
    

    # col1, col2, col3, col4, col5 = st.columns(5)
    # col1.metric("Total Questions", total_attempts)
    # col2.metric("Correct on 1st Attempt", correct_attempt_1)
    # col3.metric("Correct on 2nd Attempt", correct_attempt_2)
    # col4.metric("Wrong on Both Attempts", wrong_both_attempts)
    # col5.metric("Unanswered Questions", unanswered_questions)


    # Define custom CSS for rectangular boxes with centered alignment
    st.markdown(
    """
    <style>
    .metric-box {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        border: 1px solid #e0e0e0;
        height: 100px;
    }
    .metric-number {
        font-size: 32px;
        font-weight: bold;
        color: #333;
    }
    .metric-label {
        font-size: 12px;
        font-weight: normal;
        color: #555;
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    # Define the metrics
    with col1:
        st.markdown(f'<div class="metric-box"><div class="metric-number">{total_attempts}</div><div class="metric-label">Total Questions</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-box"><div class="metric-number">{correct_attempt_1}</div><div class="metric-label">Correct on 1st Attempt</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-box"><div class="metric-number">{correct_attempt_2}</div><div class="metric-label">Correct on 2nd Attempt</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-box"><div class="metric-number">{wrong_both_attempts}</div><div class="metric-label">Wrong on Both Attempts</div></div>', unsafe_allow_html=True)
    with col5:
        st.markdown(f'<div class="metric-box"><div class="metric-number">{unanswered_questions}</div><div class="metric-label">Unanswered Questions</div></div>', unsafe_allow_html=True)
        




    # Donut chart for attempt distribution
    pie_data = pd.DataFrame({
        'Category': ['Correct on 1st Attempt', 'Correct on 2nd Attempt', 'Wrong on Both Attempts', 'Unanswered Questions'],
        'Count': [correct_attempt_1, correct_attempt_2, wrong_both_attempts, unanswered_questions],
        'Percentage': [correct_attempt_1/total_attempts*100, 
                       correct_attempt_2/total_attempts*100, 
                       wrong_both_attempts/total_attempts*100,
                       unanswered_questions/total_attempts*100]
    })

    colors = ['#216e35', '#f5ea53', '#f53333', '#808080']  # Green, Yellow, Red, Gray

    fig = go.Figure(data=[go.Pie(
        labels=pie_data['Category'],
        values=pie_data['Count'],
        hole=.4,
        marker_colors=colors,
        textposition='outside',
        textinfo='percent+label',
        hoverinfo='label+percent+value',
        textfont_size=12,
        insidetextorientation='radial'
    )])

    fig.update_layout(
        title_text="Distribution of Attempts",
        annotations=[dict(text='Total No. of Questions : 165', x=0.5, y=0.5, font_size=12, showarrow=False)],
        showlegend=False,
        width=800,
        height=600
    )

    st.plotly_chart(fig)

    # Detailed attempts table
    st.subheader("Detailed Attempts")
    
    st.dataframe(df)


if __name__ == "__main__":
    main()