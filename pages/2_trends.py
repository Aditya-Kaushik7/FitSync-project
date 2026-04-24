import streamlit as st
from modules.processor import process_data
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(layout="wide", page_title="Trends and Insights")

# Initialize session state for theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# Extract CSS based on theme
def get_css(theme):
    if theme == 'dark':
        return """
        <style>
            body, .stApp { background-color: #0e153a !important; color: #ffffff; }
        </style>
        """
    else:
        return """
        <style>
            body, .stApp { background-color: #f4f6fb !important; color: #1a1a2e; }
        </style>
        """

st.markdown(get_css(st.session_state.theme), unsafe_allow_html=True)

# Theme toggle
def toggle_theme():
    st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'

_, col = st.columns([9, 1])
with col:
    st.button("Toggle Theme", on_click=toggle_theme)

# Title
st.title("Trends and Insights")

# Sidebar filter
st.sidebar.header("Filter")
time_range = st.sidebar.selectbox(
    "Select Time Range",
    ["Last 7 Days", "Last 30 Days", "All time"],
    index=2
)

# ---------------------------
# 🔥 LOAD + FIX DATA
# ---------------------------
df = process_data()

# ✅ Ensure date column is datetime
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Remove invalid dates
df = df.dropna(subset=['date'])

# Sort by date
df = df.sort_values('date')

# ---------------------------
# FILTER DATA
# ---------------------------
if time_range == "Last 7 Days":
    df = df[df['date'] >= df['date'].max() - pd.Timedelta(days=7)]
elif time_range == "Last 30 Days":
    df = df[df['date'] >= df['date'].max() - pd.Timedelta(days=30)]

# ---------------------------
# SUMMARY STATS
# ---------------------------
numeric_cols = ['Recovery_Score', 'Sleep_hours', 'steps', 'Calories_burned']

# Ensure numeric
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

summary_stats = df[numeric_cols].agg(['mean', 'min', 'max'])

st.write("### Summary Statistics")
st.dataframe(summary_stats)

# ---------------------------
# 📈 MONTHLY TREND (FIXED)
# ---------------------------
monthly_avg_recovery = (
    df.resample('M', on='date')[numeric_cols]
    .mean(numeric_only=True)
    .reset_index()
)

avg_recovery_fig = px.line(
    monthly_avg_recovery,
    x='date',
    y='Recovery_Score',
    title='Monthly Average Recovery Score'
)

st.plotly_chart(avg_recovery_fig, use_container_width=True)

# ---------------------------
# 📊 HISTOGRAMS
# ---------------------------
st.write("### Histogram Distributions")

st.plotly_chart(px.histogram(df, x='steps', title='Steps Distribution'), use_container_width=True)
st.plotly_chart(px.histogram(df, x='Calories_burned', title='Calories Burned Distribution'), use_container_width=True)
st.plotly_chart(px.histogram(df, x='Recovery_Score', title='Recovery Score Distribution'), use_container_width=True)
st.plotly_chart(px.histogram(df, x='Sleep_hours', title='Sleep Hours Distribution'), use_container_width=True)