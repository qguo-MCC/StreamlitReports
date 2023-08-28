import networkx as nx
import streamlit as st
from pathlib import Path
from src.utilities.social_network_utilities import (
    calculate_centrality,
    get_leader_tweets_csv,
)
import langchain
from src.utilities.save_load_python_object import load_obj
import pandas as pd
import os
import re
st.set_page_config(layout="wide")
root = Path("data")

st.title("All tweets summary")

clusters = [
    "all",
    "advocacy",
    "assessment",
    "burnout",
    "CBME",
    "clinical_reasoning",
    "collaboration",
    "communication",
    "covid",
    "cultural",
    "data_informed_med",
    "equity",
    "indigenous",
    "leadership",
    "learning",
    "medical_expertise",
    "patient",
    "planetary_health",
    "procedural",
    "professionalism",
    "psychology",
    "research",
    "safety",
    "teaching",
    "technology",
    "telehealth",
    "wellness",
]

cluster_option = st.sidebar.selectbox("select cluster", tuple(clusters))
faiss_db_path = root.joinpath('all_tweets_embedding').__str__()
db = load_obj('data/faiss_db_obj_class.FAISS')
if cluster_option == "all":
    tweets = pd.read_csv(root.joinpath(r"tweets_classified_cleaned.csv"))
    st.write(
        'The all tweet analysis started with all 26357 tweets downnloaded. Duplicate tweets were removed. Then, ChatGPT (gpt-3.5 turbo) is used to classify each tweets into categories, including a category called "unrelated to medical competency". Unrelated tweets were then dropped. The resulting dataset contains 13078 tweets. Finally, each cluster of tweets was summarized with GPT4 to extract cluster themes.'
    )
    st.subheader("cluster count")
    st.dataframe(
        tweets.iloc[:, 6:]
        .sum()
        .reset_index()
        .rename(columns={"index": "cluster name", 0: "count"})
        .sort_values('count', ascending= False),
        hide_index=True,
    )
    st.subheader("Search tweets related to any topic")
    query = st.text_input('query')
    n_tweets = st.slider("how many tweets do you want?", 1, 20, 3)
    query_method = st.selectbox("search method", ('max diversity', 'highly related'))
    search_clusters = [
        'all',
        'advocacy',
        'assessment',
        'burnout',
        'CBME',
        'clinical_reasoning',
        'collaboration',
        'communication',
        'covid',
        'cultural',
        'data_informed_med',
        'equity',
        'indigenous',
        'leadership',
        'learning',
        'medical_expertise',
        'patient',
        'planetary_health',
        'procedural',
        'professionalism',
        'psychology',
        'research',
        'safety',
        'teaching',
        'technology',
        'telehealth',
        'wellness'
    ]
    search_cluster = st.selectbox("search cluster", tuple(search_clusters))
    #st.button('Search')

    if st.button('Search'):
        if query_method == 'highly related':
            if search_cluster != "all":
                results = db.similarity_search_with_score(query, k=n_tweets, filter={search_cluster: True})
            else:
                results = db.similarity_search_with_score(query, k=n_tweets)

            for i, t in enumerate(results):
                tid = re.search('id: (\d+)\nctext', t[0].page_content).group(1)
                hyperlink = f"https://twitter.com/anyuser/status/{tid}"
                st.write(f"<b>Tweet {i+1}</b>: (asimilarity score={t[1]}) {t[0].page_content.split('ctext:')[1]} [link]({hyperlink})", unsafe_allow_html=True)
        else:
            if search_cluster != "all":
                results = db.max_marginal_relevance_search(query, k=n_tweets, filter={search_cluster: True})
            else:
                results = db.max_marginal_relevance_search(query, k=n_tweets)
            for i, t in enumerate(results):
                tid = re.search('id: (\d+)\nctext', t.page_content).group(1)
                hyperlink = f"https://twitter.com/anyuser/status/{tid}"
                st.write(f"<b>Tweet {i+1}</b>: {t.page_content.split('ctext:')[1]} [link]({hyperlink})", unsafe_allow_html=True)

    st.subheader("Ask any question about the database to ChatGPT chatbot")
    question = st.text_input("question")
    qa = load_obj("data/dbchatbot.openai")
    tab1, tab2, tab3 = st.tabs(["answer", "queries", "history"])
    if st.button('Ask'):
        answer = qa({"question": question})
        tab1.write(f"Answer: {answer['answer']}")
        tab2.write(f"To be added later")
        tab3.dataframe(pd.DataFrame([[type(message), message.content] for message in answer['chat_history']]))

else:
    summary = pd.read_excel(
        root.joinpath("theme_examples.xlsx"),
        sheet_name=cluster_option,
        engine="openpyxl",
    )
    summary[["theme", "summary"]] = summary["themes"].str.split(": ", expand=True)
    st.subheader(f'Cluster: {cluster_option}')
    tweets = pd.read_csv(root.joinpath(r"tweets_classified_cleaned.csv"))
    tweets = tweets.loc[tweets[cluster_option]==True]
    st.write(f'there are {tweets.shape[0]} tweets in this cluster.')

    for idx, row in summary.iterrows():
        st.subheader(row['theme'])
        st.write(row['summary'])
        exp = row['mmr_examples'].split('|')
        st.write(f"<b>example 1</b>: {exp[0]}", unsafe_allow_html=True)
        st.write(f"<b>example 2</b>: {exp[1]}", unsafe_allow_html=True)


