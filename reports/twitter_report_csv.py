import networkx as nx
import streamlit as st
from pathlib import Path
from src.utilities.save_load_python_object import load_obj
from src.utilities.social_network_utilities import calculate_centrality, get_leader_tweets_csv
import pandas as pd
import community

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
    ('mention_retweet',))
G = load_obj(root.joinpath(f'{query_option}_{edge_type_option}_nx.graph'))
clusters = ['all'] + pd.Series([G.nodes[node]['cluster'] for node in G.nodes]).sort_values().astype(str).unique().tolist()
cluster_option = st.sidebar.selectbox(
    'select cluster',
    tuple(clusters))
fig = load_obj(root.joinpath(f'{query_option}_{edge_type_option}_plotly.fig'))

if cluster_option == 'all':
    st.plotly_chart(fig, use_container_width=True)
    var_names = ['Medical_professional', 'Advocate_Activist', 'Educator', 'Researcher', 'Job_Posting', 'organizations',
                 'Government', 'Miscellaneous']
    user_info = pd.read_csv('data/user_descriptions.csv')
    user_class = user_info[var_names] \
        .replace('None', None) \
        .dropna() \
        .astype(int)
    st.subheader('GPT4 summary of leader tweets')
    themes = pd.read_csv(f'data/{query_option}ThemeFinal.csv')
    themes.sort_values('cluster_size', ascending=False, inplace = True)
    themes.reset_index(inplace=True)
    for idx, row in themes.iterrows():
        examples = row['examples'].split('|| ')
        st.write(f'<h4>Theme {idx+1}: {row["text"]}</h4>', unsafe_allow_html=True)
        st.write(f'<b>Cluster size:</b> {row["cluster_size"]} tweets', unsafe_allow_html=True)
        st.write(f'<b>Summary:</b> {row["summary"]}', unsafe_allow_html=True)
        st.write(f'<b>Example 1:</b> {examples[0]}', unsafe_allow_html=True)
        st.write(f'<b>Example 2:</b> {examples[1]}', unsafe_allow_html=True)
    st.subheader('GPT3.5 User Classification')
    st.dataframe(user_class.sum().reset_index().transpose(), use_container_width=True, hide_index=True)
    st.subheader('Network density and modularity')
    partition = community.best_partition(G.to_undirected())
    modularity = community.modularity(partition, G.to_undirected())
    st.write("Density is a measure of how closely knit a social network is. In simpler terms, it's about how many friends or connections everyone has compared to how many they could possibly have.")
    st.write(f'The density of the network is {nx.density(G)}. There are {len(G.nodes)} nodes and {len(G.edges)} edges.')
    st.write(f"Social networks' modularity refers to the degree to which the network can be divided into distinct communities or groups without many connections between them.")
    st.write(f'The modularity of the network is {modularity}.')
    st.subheader('Leader social group distribution')
    leaders = pd.read_csv(f'data/{query_option}Influencers.csv')
    st.write(f'There are {leaders.shape[0]} influencers identified based on top 20 degree (indegree + outdegree) and top degree influencers of clusters with 5 or more users.')
    leader_stats = user_info.loc[user_info['username'].isin(leaders['Influencer'].to_list())].iloc[:,4:].sum().reset_index().rename(columns={'index': 'influencer', 0:'N'})
    leader_stats['Percentage'] = (leader_stats['N']*100/leaders.shape[0]).round(1).astype(str)+"%"
    st.dataframe(leader_stats, hide_index=True)
    st.write(f'Max leader degree: {leaders["Degree"].max()}, Min leader degree: {leaders["Degree"].min()}')
    st.dataframe(leaders.sort_values('Degree', ascending=False), hide_index=True)

    st.write('Note: some influencers have multiple social group labels, so the percentages of social groups do not add to 100%.')
    st.subheader('Top 10 leaders based on indegree centrality')
    st.write("A node's (or a person's) in-degree corresponds to the number of incoming connections they have.")
    st.dataframe(calculate_centrality(nx.in_degree_centrality, 'Indegree', G, user_info), use_container_width=True)
    st.subheader('Top 10 leaders based on outdegree centrality')
    st.write("""The "out-degree" of a node is the number of outgoing connections they have, or the number of people they are following.""")
    st.dataframe(calculate_centrality(nx.out_degree_centrality, 'Outdegree', G, user_info), use_container_width=True)
    st.subheader('Top 10 leaders based on eigen vector centrality')
    st.write("""Eigenvector Centrality is based on the idea that not all connections are created equal. If you're connected to someone who is highly connected, that should boost your own importance in the network. In other words, it's not just about how many people you're connected to, but also how important those people are.""")
    st.dataframe(calculate_centrality(nx.eigenvector_centrality, 'EigenVector', G, user_info), use_container_width=True)
    st.subheader('Top 10 leaders based on closeness centrality')
    st.write("""Closeness calculates how efficiently and directly one person can reach all the other individuals in the network. If you have high closeness centrality, it means you can quickly reach a large number of people, and you are considered important in terms of information flow or influence.""")
    st.dataframe(calculate_centrality(nx.closeness_centrality, 'Closeness', G, user_info), use_container_width=True)
    st.subheader('Top 10 leaders based on betweenness centrality')
    st.write("""Betweenness Centrality is a measure of how often a particular node (a person, in the case of a social network) serves as a bridge along the shortest path between two other nodes. In simpler words, it shows how much a person stands between others, acting as a connector or a go-between.""")
    st.dataframe(calculate_centrality(nx.betweenness_centrality, 'Betweenness', G, user_info), use_container_width=True)
else:
    for trace in fig.data:
        if trace['name'] != f'c{cluster_option}':
            trace.visible = 'legendonly'
    st.plotly_chart(fig, use_container_width=True)
    cmembers = [node for node in G.nodes if G.nodes[node]['cluster'] == int(cluster_option)]
    users = pd.read_csv('data/users.csv')
    users = users.loc[users['username'].isin(cmembers)]
    cids = users['user_id'].to_list()
    st.subheader('Cluster Title')
    st.write('To be implement later if needed.')
    st.subheader('Cluster Summary')
    st.write('To be implement later if needed.')
    st.subheader('GPT3.5 Cluster Member Classification')
    var_names = ['Medical_professional', 'Advocate_Activist', 'Educator', 'Researcher', 'Job_Posting', 'organizations',
                 'Government', 'Miscellaneous']
    user_class = pd.read_csv('data/user_descriptions.csv')
    user_class = user_class.loc[user_class['username'].isin(cmembers), var_names]\
        .replace('None', None) \
        .dropna() \
        .astype(int)
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
    user_id = users.loc[users['username']==leader, 'user_id'].values[0]
    tweets = pd.DataFrame({'Tweets': get_leader_tweets_csv(leader, tweets, user_id)})
    st.subheader(f'Tweets by or about {leader}')
    st.dataframe(tweets, use_container_width = True, hide_index=True, column_config=None)


