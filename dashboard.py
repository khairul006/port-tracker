import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Port Tracker Admin", layout="wide")

st.title("🛡️ Network Port Monitor")

# Function to pull data from the shared DB
def load_data():
    conn = sqlite3.connect("ports.db")
    df = pd.read_sql_query("SELECT * FROM port_logs ORDER BY timestamp DESC", conn)
    conn.close()
    return df

df = load_data()

# Show Summary Stats
col1, col2 = st.columns(2)
col1.metric("Total Events Logged", len(df))
if not df.empty:
    col2.metric("Latest Port Activity", f"Port {df.iloc[0]['port']}")

# Show Data Table
st.subheader("Recent Activity")
st.dataframe(df, use_container_width=True)

# Auto-refresh button
if st.button('Refresh Data'):
    st.rerun()