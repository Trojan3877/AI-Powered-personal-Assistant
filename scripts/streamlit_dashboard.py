import pandas as pd
import streamlit as st

df = pd.read_csv("logs/performance_metrics.csv")

st.title("🧠 AI Assistant Performance Dashboard")
st.dataframe(df)

st.subheader("📈 Latency Over Time")
df["latency (s)"] = df["latency"].str.replace("s", "").astype(float)
st.line_chart(df["latency (s)"])
