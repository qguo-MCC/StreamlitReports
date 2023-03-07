import streamlit as st
import pandas as pd
st.title('First Report')
st.text('Experiment 1.')
st.text('Experiment 2.')
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)
st.dataframe(pd.read_csv(r'\\MCC-DFS01\Mcc.Tdm.Marking\PROD\2023-January\09 PAS\streamlit_data/try1.csv'))