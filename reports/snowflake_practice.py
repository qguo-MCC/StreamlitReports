import snowflake.connector as sc
from snowflake.connector.pandas_tools import pd_writer
from snowflake.connector.pandas_tools import write_pandas
import os
import pandas as pd
conn = sc.connect(
    user='qguo',
    password='%1502Laixilaifu',
    account='hf58754.canada-central.azure',
    database = 'testdb_mg',
    schema = 'testschema_mg'
)

cur = conn.cursor()
conn.cursor().execute("CREATE WAREHOUSE IF NOT EXISTS tiny_warehouse_mg")
conn.cursor().execute("CREATE DATABASE IF NOT EXISTS testdb_mg")
conn.cursor().execute("USE DATABASE testdb_mg")
conn.cursor().execute("CREATE SCHEMA IF NOT EXISTS testschema_mg")

conn.cursor().execute("USE WAREHOUSE tiny_warehouse_mg")
conn.cursor().execute("USE DATABASE testdb_mg")
conn.cursor().execute("USE SCHEMA testdb_mg.testschema_mg")

conn.cursor().execute(
    "CREATE OR REPLACE TABLE "
    "truth_table(names string, gtw integer)")
conn.cursor().execute(
    "INSERT INTO truth_table(names, gtw) VALUES " +
    "    ('jn', 1), " +
    "    ('wt', 1)")
# Putting Data
conn.cursor().execute("PUT file://./data/truth.csv @%truth_table")
conn.cursor().execute("COPY INTO truth_table")
cur.execute('SELECT * FROM daily_14_total LIMIT 10')

q = cur.execute('SELECT * FROM testschema_mg.truth_table')
q.fetch_pandas_all()

#has to capitalize variables, table name
truth2 = pd.DataFrame({'NAMES':['rn', 'yz'], 'GTW': [1,1]})
success, nchunks, nrows, _ = write_pandas(conn=conn, df=truth2, table_name='TRUTH_TABLE')