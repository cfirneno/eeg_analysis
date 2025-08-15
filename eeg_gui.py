import streamlit as st
import pandas as pd
import os

st.title("EEG Data Loader and Analyzer")

# Upload CSV files
uploaded_files = st.file_uploader("Upload your CSV file(s)", accept_multiple_files=True, type=["csv"])

# Sample rate (adjust as necessary)
sample_rate = st.number_input("Sample rate (Hz)", value=512)

if uploaded_files:
    # For simplicity, process only the first file
    file = uploaded_files[0]
    df = pd.read_csv(file)

    st.write(f"Loaded: {file.name}")
    st.write("Preview:")
    st.write(df.head())

    # Detect if 'time' or 'Time' column exists
    if 'Time' in df.columns or 'time' in df.columns:
        st.write("Using existing 'Time' column.")
        if 'Time' in df.columns:
            time_col = 'Time'
        else:
            time_col = 'time'
    else:
        st.write("No 'Time' column found. Creating based on sample rate.")
        df['Time'] = df.index / sample_rate
        time_col = 'Time'

    # Show available channels
    channels = [col for col in df.columns if col != time_col]
    st.write("Available channels:")
    st.write(channels)

    # Select a channel to plot
    selected_channel = st.selectbox("Select channel to plot", channels)

    if st.button("Plot Signal"):
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.plot(df[time_col], df[selected_channel])
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        ax.set_title(f"Channel: {selected_channel}")
        st.pyplot(fig)
