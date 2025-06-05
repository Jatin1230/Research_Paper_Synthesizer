# agents/plot_agent.py

import re
import plotly.graph_objects as go
import streamlit as st

import re

def extract_metrics(text):
    # Match something like: Paper A: Accuracy: 91.2%, F1: 87.6%
    pattern = r"(Paper\s[A-Z\d]+).*?(?:Accuracy|F1).*?(\d{2,3}(?:\.\d+)?)%?"
    matches = re.findall(pattern, text, re.IGNORECASE)

    if not matches:
        print("No matches found in summary:", text)

    return [{"title": title.strip(), "accuracy": float(score)} for title, score in matches]

def plot_metrics(metrics):
    titles = [m["title"] for m in metrics]
    accuracies = [m["accuracy"] for m in metrics]

    fig = go.Figure(data=[
        go.Bar(x=titles, y=accuracies, marker_color="royalblue")
    ])
    fig.update_layout(
        title="📊 Accuracy Comparison Across Papers",
        xaxis_title="Paper",
        yaxis_title="Accuracy (%)",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
