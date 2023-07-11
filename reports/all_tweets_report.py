import networkx as nx
import streamlit as st
from pathlib import Path
from src.utilities.save_load_python_object import load_obj
from src.utilities.social_network_utilities import (
    calculate_centrality,
    get_leader_tweets_csv,
)
import pandas as pd

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
        .rename(columns={"index": "cluster name", 0: "count"}),
        hide_index=True,
    )
else:
    summary = pd.read_excel(
        root.joinpath("cluster_theme_summary.xlsx"),
        sheet_name=cluster_option,
        engine="openpyxl",
    )
    summary[["theme", "summary"]] = summary["themes"].str.split(": ", expand=True)
    st.dataframe(
        summary[["theme", "summary"]], use_container_width=True, hide_index=True
    )
