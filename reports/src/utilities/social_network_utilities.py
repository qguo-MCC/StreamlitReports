import pandas as pd
import networkx as nx
from sqlalchemy.engine.base import Engine
from typing import List
def get_topn(df: pd.DataFrame, n=10):
    top10 = df.iloc[:n].copy().round(3)

    return top10
def calculate_centrality(centrality_func, centrality_name: str, G: nx.classes.digraph.DiGraph, user_info: pd.DataFrame, n=10) ->pd.DataFrame:
    centralities = centrality_func(G)
    centralities = pd.Series(centralities)
    centralities.index = list(G.nodes)
    centralities = centralities.reset_index().rename(columns={'index': 'user', 0: centrality_name})
    centralities['cluster'] = centralities['user'].apply(lambda e: G.nodes[e]['cluster'])
    centralities.sort_values(centrality_name, ascending=False, inplace=True)
    topn = get_topn(centralities, n)
    topn['Role'] = topn['user'].apply(lambda e: user_info.loc[user_info['username']==e, 'class'].values[0].split(", ")[0])
    topn = topn.transpose()
    topn.columns = range(1, n+1)
    return topn

def get_leader_tweets(leader: str, queries: List[int], engine) -> List[str]:
    tweets = engine.query(f'SELECT text, user FROM tweets WHERE query_number in {str(tuple(queries)).replace(",)", ")")}')\
        .rename(columns={'user': 'user_id'})
    user_id = engine.query(f'SELECT user_id, username FROM authors').iloc[0]['user_id']
    tweets_about_leader = tweets.loc[tweets['text'].str.contains(leader), 'text'].to_list()
    leader_tweets = tweets.loc[tweets['user_id']==user_id, 'text'].to_list()
    leader_tweets = pd.Series(leader_tweets+tweets_about_leader).unique().tolist()
    return leader_tweets

def get_leader_tweets_csv(leader: str, tweets: pd.DataFrame, user_id: int) -> List[str]:
    tweets_about_leader = tweets.loc[tweets['text'].str.contains(leader), 'text'].to_list()
    leader_tweets = tweets.loc[tweets['user_id']==user_id, 'text'].to_list()
    leader_tweets = pd.Series(leader_tweets+tweets_about_leader).unique().tolist()
    return leader_tweets