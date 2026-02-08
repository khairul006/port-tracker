import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Port Tracker", layout="wide", page_icon="🛡️")

def run_query(query):
    with sqlite3.connect("ports.db") as conn:
        return pd.read_sql_query(query, conn)
    
# Title and Auto-Refresh Info
st.title("🛡️ Network Port Monitor")
st.caption(f"Last UI Update: {datetime.now().strftime('%H:%M:%S')}")

# --- SECTION 1: SYSTEM OVERVIEW ---
st.subheader("System Overview")
live_query = """
SELECT port, status, is_authorized, timestamp 
FROM port_logs 
WHERE id IN (SELECT MAX(id) FROM port_logs GROUP BY port) 
AND status = 'Open'
"""
live_df = run_query(live_query)
    
# Display Metrics in columns
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Active Open Ports", len(live_df))
with col2:
    # Check if any unauthorized ports are open
    unauth_count = len(live_df[live_df['is_authorized'] == 0])
    st.metric("Security Alerts", unauth_count, delta_color="inverse", delta=f"{unauth_count} Unauthorized" if unauth_count > 0 else "All Clear")
with col3:
    st.metric("Database Entries", len(run_query("SELECT id FROM port_logs")))

st.divider()

# --- SECTION 2: LIVE PORTS WITH VISUALS ---
st.subheader("🟢 Live Open Ports")
if not live_df.empty:
    # Adding a 'Status' emoji for a better look
    live_df['indicator'] = live_df['is_authorized'].apply(lambda x: "✅ Authorized" if x == 1 else "🚨 WARNING")
    st.table(live_df[['port', 'indicator', 'timestamp']])
else:
    st.info("No open ports detected. Your network is locked down.")

# --- SECTION 3: RECENT ACTIVITY (HISTORY) ---
st.subheader("📜 Recent Activity Log")

# Get the data (make sure to include scripts_output in your SQL query)
history_df = run_query("SELECT timestamp, port, status, product, scripts_output FROM port_logs ORDER BY id DESC LIMIT 10")

# 1. Show the summary table first
st.dataframe(history_df[['timestamp', 'port', 'status', 'product']], use_container_width=True)

# 2. Loop through the rows to create the detail expanders
st.write("#### Detailed Audit Reports")
for index, row in history_df.iterrows():
    # Only show expander if there is actually Nmap data to show
    if row['scripts_output'] and row['scripts_output'] != "None":
        with st.expander(f"🔍 Audit Details: Port {row['port']} ({row['timestamp']})"):
            st.json(row['scripts_output'])
    else:
        # Optional: show a small note if no audit data exists for that log
        pass

# Sidebar for controls
with st.sidebar:
    st.header("Settings")
    if st.button('🔄 Manual Refresh'):
        st.rerun()
    
    st.write("---")
    st.write("Current Database: `ports.db` (SQLite)")

# Auto-refresh button
if st.button('Refresh Data'):
    st.rerun()