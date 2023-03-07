import streamlit as st
st.title('First Report')
st.text('Experiment 1.')
st.text('Experiment 2.')
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)