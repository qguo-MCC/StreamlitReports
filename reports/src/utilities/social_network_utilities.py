import pandas as pd
import networkx as nx
from sqlalchemy.engine.base import Engine
from typing import List
def get_topn(df: pd.DataFrame, n=10):
    top10 = df.iloc[:n].copy().round(3).transpose()
    top10.columns = range(1, n+1)
    return top10
def calculate_centrality(centrality_func, centrality_name: str, G: nx.classes.digraph.DiGraph, n=10) ->pd.DataFrame:
    centralities = nx.in_degree_centrality(G)
    centralities = pd.Series(centralities)
    centralities.index = list(G.nodes)
    centralities = centralities.reset_index().rename(columns={'index': 'user', 0: centrality_name})
    centralities['cluster'] = centralities['user'].apply(lambda e: G.nodes[e]['cluster'])
    centralities.sort_values(centrality_name, ascending=False, inplace=True)
    topn = get_topn(centralities, n)
    return topn

def get_leader_tweets(leader: str, queries: List[int], engine: Engine) -> List[str]:
    tweets = pd.read_sql(f'SELECT text, user FROM tweets WHERE query_number in {str(tuple(queries)).replace(",)", ")")}', engine)\
        .rename(columns={'user': 'user_id'})
    user_id = pd.read_sql(f'SELECT user_id, username FROM authors', engine).iloc[0]['user_id']
    tweets_about_leader = tweets.loc[tweets['text'].str.contains(leader), 'text'].to_list()
    leader_tweets = tweets.loc[tweets['user_id']==user_id, 'text'].to_list()
    leader_tweets = pd.Series(leader_tweets+tweets_about_leader).unique().tolist()
    return leader_tweets