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
"""
with st.sidebar:
    with st.echo():
        st.write("This code will be printed to the sidebar.")

    with st.spinner("Loading..."):
        time.sleep(5)
    st.success("Done!")
#df = pd.DataFrame(np.random.randn(50, 20), columns=('col %d' % i for i in range(20)))
#df.to_csv('data/try1.csv', index=False)
df = pd.read_csv('data/try1.csv')
st.dataframe(df)
#pd.read_csv(r'\\MCC-DFS01\Mcc.Tdm.Marking\PROD\2023-January\09 PAS\streamlit_data/try1.csv')
"""