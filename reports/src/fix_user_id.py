from sqlalchemy import create_engine
from pathlib import Path
import pandas as pd
import numpy as np
engine = create_engine("sqlite:///data\\data.db")
root = Path('data')
users_db = pd.read_sql_table('authors', engine)
users_df = pd.read_csv(root.joinpath('users.csv'))
original_users = users_db['username'].unique().tolist()
users_df['user_id'] = users_df.apply(lambda row: users_db.loc[users_db['username']==row['username'], 'user_id'].values[0] if row['username'] in original_users else str(int(row['user_id'])), axis=1)
users_df.to_csv(root.joinpath('users.csv'), index=False)

user_description = pd.read_csv('data/user_descriptions.csv')
user_description['user_id'] = user_description.apply(lambda row: users_db.loc[users_db['username']==row['username'], 'user_id'].values[0] if row['username'] in original_users else str(int(row['user_id'])) if pd.isnull(row['user_id'])==False else None, axis=1)
user_description.to_csv('data/user_descriptions.csv', index=False)