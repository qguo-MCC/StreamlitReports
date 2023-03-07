import streamlit as st
import pandas as pd
import numpy as np
st.title('First Report')
st.text('Experiment 1.')
st.text('Experiment 2.')
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

df = pd.DataFrame(
   np.random.randn(50, 20),
   columns=('col %d' % i for i in range(20)))
st.dataframe(df)
#pd.read_csv(r'\\MCC-DFS01\Mcc.Tdm.Marking\PROD\2023-January\09 PAS\streamlit_data/try1.csv')