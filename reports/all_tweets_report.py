import networkx as nx
import streamlit as st
from pathlib import Path
from src.utilities.save_load_python_object import load_obj
from src.utilities.social_network_utilities import (
    calculate_centrality,
    get_leader_tweets_csv,
)
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import pandas as pd
import os

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
embeddings = OpenAIEmbeddings()
db = FAISS.load_local(faiss_db_path, embeddings)
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

    #st.button('Search')
    if st.button('Search'):
        results = db.max_marginal_relevance_search(query, k=3)
        for i, t in enumerate(results):
            st.write(f"<b>Example {i+1}</b>: {t.page_content.split('ctext:')[1]}", unsafe_allow_html=True)



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


