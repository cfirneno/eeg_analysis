import streamlit as st
import pandas as pd
import os
import sys

st.set_page_config(layout="wide", page_title="EEG Loader (safe)")

st.title("EEG Data Loader — Safe Mode")

# Check for optional libraries (deferred)
_missing = []

def try_import(name, alias=None):
    try:
        module = __import__(name)
        if alias:
            globals()[alias] = module
        else:
            globals()[name] = module
        return True
    except Exception as e:
        _missing.append(name)
        return False

# Defer heavy imports until after UI loads
# We'll attempt to import when needed.

uploaded_files = st.file_uploader("Upload your CSV file(s)", accept_multiple_files=True, type=["csv"])
sample_rate = st.number_input("Sample rate (Hz)", value=512, min_value=1)

# Show which optional packages are available (attempt one quick check)
st.sidebar.header("Optional packages status")
# Quick check: see if basic optional libs are importable without raising the app
for pkg in ["plotly", "scipy", "matplotlib"]:
    try:
        __import__(pkg)
        st.sidebar.write(f"{pkg} — OK")
    except Exception:
        st.sidebar.write(f"{pkg} — missing")

if uploaded_files:
    file = uploaded_files[0]
    try:
        df = pd.read_csv(file)
    except Exception as e:
        st.error(f"Failed to read {file.name}: {e}")
        st.stop()

    st.write(f"Loaded: {file.name}")
    st.dataframe(df.head())

    # Determine time column
    if 'time' in df.columns:
        time_col = 'time'
    elif 'Time' in df.columns:
        time_col = 'Time
