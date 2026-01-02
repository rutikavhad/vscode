import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

st.set_page_config(page_title="WAF Dashboard", layout="wide", page_icon="🛡️")

# --- Firewall Control Logic ---
STATUS_FILE = "firewall_status.txt"

def get_status():
    if not os.path.exists(STATUS_FILE): return "ON"
    with open(STATUS_FILE, "r") as f: return f.read().strip()

def toggle_status(status):
    with open(STATUS_FILE, "w") as f: f.write(status)

# --- Sidebar ---
st.sidebar.title("🛡️ Settings")
current_status = get_status()
btn_label = "🔴 Turn OFF Firewall" if current_status == "ON" else "🟢 Turn ON Firewall"

if st.sidebar.button(btn_label):
    toggle_status("OFF" if current_status == "ON" else "ON")
    st.rerun()

st.sidebar.markdown(f"**Current Status:** `{current_status}`")
st.sidebar.divider()
st.sidebar.info("This dashboard monitors traffic and controls the MITMProxy WAF engine.")

# --- Main Dashboard ---
st.title("Web Protector Analytics")

if os.path.exists("traffic_events.csv"):
    df = pd.read_csv("traffic_events.csv")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    attacks_df = df[df['attack_type'] != "NORMAL"]

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Requests", len(df))
    m2.metric("Attacks Blocked", len(attacks_df))
    m3.metric("Unique Attacker IPs", attacks_df['client_ip'].nunique() if not attacks_df.empty else 0)
    m4.metric("DDoS Events", len(df[df['attack_type'] == "DDOS"]))

    # Charts
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Attack Type Breakdown")
        if not attacks_df.empty:
            fig = px.pie(attacks_df, names='attack_type', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No attacks detected yet.")

    with col2:
        st.subheader("Threat Timeline (Hourly)")
        if not attacks_df.empty:
            timeline = attacks_df.set_index('timestamp').resample('H').count()
            st.line_chart(timeline['attack_type'])
        else:
            st.write("Timeline will appear once attacks are logged.")

    # Data Table
    st.subheader("Recent Traffic Logs")
    st.dataframe(df.sort_values(by='timestamp', ascending=False).head(50), use_container_width=True)
else:
    st.warning("Waiting for data... Please start MITMProxy and browse some sites.")