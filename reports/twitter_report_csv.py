import networkx as nx
import streamlit as st
from pathlib import Path
from src.utilities.save_load_python_object import load_obj
from src.utilities.social_network_utilities import calculate_centrality, get_leader_tweets_csv
import pandas as pd


st.set_page_config(layout="wide")

root = Path('data')
st.title('Twitter Social Network Analysis')
query_option = st.sidebar.selectbox(
    'select queries',
    ('CanMEDS', 'MedEd'))
if query_option == 'CanMEDS':
    queries = [1,2]
else:
    queries = [4]
edge_type_option = st.sidebar.selectbox(
    'select edge type',
    ('mention_retweet', 'retweet', 'mention'))
G = load_obj(root.joinpath(f'{query_option}_{edge_type_option}_nx.graph'))
clusters = ['all'] + pd.Series([G.nodes[node]['cluster'] for node in G.nodes]).sort_values().astype(str).unique().tolist()
cluster_option = st.sidebar.selectbox(
    'select cluster',
    tuple(clusters))
fig = load_obj(root.joinpath(f'{query_option}_{edge_type_option}_plotly.fig'))
var_names = ['Medical_professional', 'Advocate_Activist', 'Educator', 'Researcher', 'Job_Posting', 'organizations', 'Government', 'Miscellaneous']
user_class = pd.read_csv('data/user_descriptions.csv')[var_names] \
    .replace('None', None) \
    .dropna() \
    .astype(int)
if cluster_option == 'all':
    st.plotly_chart(fig, use_container_width=True)


    st.subheader('GPT4 summary of leader tweets')
    summary = pd.read_excel('data/GPT4summaries.xlsx', engine='openpyxl', sheet_name=f'{query_option}_{edge_type_option}')
    summary[['Theme', 'Summary']] = summary['Themes'].str.split(': ', expand = True)
    st.dataframe(summary[['Theme', 'Summary']], use_container_width=True, hide_index=True)
    st.subheader('User Classification')
    st.dataframe(user_class.sum().reset_index().transpose(), use_container_width=True, hide_index=True)
    st.subheader('Top 10 leaders based on indegree centrality')
    st.dataframe(calculate_centrality(nx.in_degree_centrality, 'Indegree', G), use_container_width=True)
    st.subheader('Top 10 leaders based on outdegree centrality')
    st.dataframe(calculate_centrality(nx.out_degree_centrality, 'Outdegree', G), use_container_width=True)
    st.subheader('Top 10 leaders based on eigen vector centrality')
    st.dataframe(calculate_centrality(nx.eigenvector_centrality, 'EigenVector', G), use_container_width=True)
    st.subheader('Top 10 leaders based on closeness centrality')
    st.dataframe(calculate_centrality(nx.closeness_centrality, 'Closeness', G), use_container_width=True)
    st.subheader('Top 10 leaders based on betweenness centrality')
    st.dataframe(calculate_centrality(nx.betweenness_centrality, 'Betweenness', G), use_container_width=True)
else:
    for trace in fig.data:
        if trace['name'] != f'c{cluster_option}':
            trace.visible = 'legendonly'
    st.plotly_chart(fig, use_container_width=True)
    cmembers = [node for node in G.nodes if G.nodes[node]['cluster'] == int(cluster_option)]

    users = pd.read_csv('data/users.csv')
    users = users.loc[users['username'].isin(cmembers)]
    cids = str(tuple(users['user_id'].to_list())).replace(",)", ")")
    st.subheader('Cluster Title')
    st.write('To be implement later if needed.')
    st.subheader('Cluster Summary')
    st.write('To be implement later if needed.')
    st.subheader('Cluster Member Classification')
    st.dataframe(user_class.sum().reset_index().transpose(), use_container_width=True, hide_index=True)
    centralities = nx.in_degree_centrality(G)
    centralities = pd.Series(centralities)
    centralities.index = list(G.nodes)
    centralities = centralities.loc[cmembers]
    centralities.sort_values(ascending=False, inplace=True)
    st.subheader('Cluster Leader')
    leader = centralities.index[0]
    st.write(leader)
    tweets = pd.read_csv('data/tweets.csv')
    tweets = tweets.loc[tweets['query_number'].isin(queries), ['text', 'user']].rename(columns={'user': 'user_id'})

    tweets = pd.DataFrame({'Tweets': get_leader_tweets_csv(leader, tweets, users.loc[users['username']==leader, 'user_id'].values[0])})
    st.subheader(f'Tweets by or about {leader}')
    st.dataframe(tweets, use_container_width = True, hide_index=True, column_config=None)


