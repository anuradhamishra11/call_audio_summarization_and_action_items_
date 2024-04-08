import streamlit as st
import pandas as pd

def display_summary_and_cost(file, cost_analysis):
    st.title("Markdown Viewer")
    with open(file, 'r') as markdown_file:
        markdown_content = markdown_file.read()
    st.markdown("""
    <style>
        /* Add your CSS styles here */
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 0;
            background-color: #f4f4f4;
        }
        .markdown-content {
            max-width: 800px;
            margin: 0 auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #007bff;
        }
        p {
            color: #333;
        }
        strong {
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)
    st.markdown(f'<div class="markdown-content">{markdown_content}</div>', unsafe_allow_html=True)

    data = [line.split(": ") for line in str(cost_analysis).strip().split("\n")]
    df = pd.DataFrame(data, columns=["Metric", "Value"])
    st.subheader("Cost Analysis")
    st.table(df)