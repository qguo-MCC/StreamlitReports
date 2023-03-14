import streamlit as st
import pandas as pd
import numpy as np
import time
import snowflake.connector
@st.cache_resource
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()
st.title('First Report')
st.text('Experiment 1.')
st.text('Experiment 2.')
cur = conn.cursor()
q = cur.execute('SELECT * FROM testschema_mg.truth_table')
df = q.fetch_pandas_all()
st.dataframe(df)

with st.sidebar:
    st.header("Truths")
    st.write("Truth 1: jn is a gtw.")
    st.write("Truth2: wt is a gtw.")

