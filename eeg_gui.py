import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(layout="wide", page_title="EEG Loader (safe)")

st.title("EEG Data Loader — Safe Mode")

# Helper: check optional packages without raising
def check_pkg(name):
    try:
        __import__(name)
        return True
    except Exception:
        return False

st.sidebar.header("Optional packages status")
pkgs = {"plotly": check_pkg("plotly"), "scipy": check_pkg("scipy"), "matplotlib": check_pkg("matplotlib")}
for k, ok in pkgs.items():
    st.sidebar.write(f"{k}: {'OK' if ok else 'missing'}")

# File upload + settings
uploaded_files = st.file_uploader("Upload your CSV file(s)", accept_multiple_files=True, type=["csv"])
sample_rate = st.number_input("Sample rate (Hz)", value=512, min_value=1)

if not uploaded_files:
    st.info("Upload one or more CSV files (or place them in SMNI_CMI_TEST folder if running locally).")
    st.stop()

# Use the first uploaded file for now (can be extended)
file = uploaded_files[0]
try:
    df = pd.read_csv(file)
except Exception as e:
    st.error(f"Failed to read {file.name}: {e}")
    st.stop()

st.write(f"Loaded: {file.name}")
st.dataframe(df.head())

# Determine time column (case-insensitive)
if 'time' in df.columns:
    time_col = 'time'
elif 'Time' in df.columns:
    time_col = 'Time'
else:
    st.warning("No time column found — creating 'Time' from index using sample_rate.")
    df['Time'] = df.index / float(sample_rate)
    time_col = 'Time'

# List available channels (exclude time)
channels = [c for c in df.columns if c != time_col]
st.write("Available channels:", channels)

# Channel selector
selected_channel = st.selectbox("Select channel to plot", channels)

# Button: Plot signal (Plotly preferred)
if st.button("Plot Signal"):
    if not check_pkg("plotly"):
        st.error("Plotly is not installed in the environment. Add 'plotly' to requirements.txt and redeploy, or run locally with pip install plotly.")
    else:
        import plotly.express as px
        try:
            fig = px.line(df, x=time_col, y=selected_channel, labels={time_col: "Time (s)", selected_channel: "Amplitude"}, title=f"Signal: {selected_channel}")
            fig.update_layout(legend=dict(orientation="h"))
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Failed to plot signal: {e}")

# Button: Compute and
