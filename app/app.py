import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data
@st.cache
def load_data():
    # Replace with the path to your cleaned data
    return pd.read_csv('../data/benin-malanville_cleaned.csv', parse_dates=['Timestamp'], index_col='Timestamp')

df = load_data()

# Streamlit application
st.title("Solar Radiation and Weather Data Dashboard")

# Sidebar for filters
st.sidebar.header("Filters")
date_range = st.sidebar.date_input("Date Range", [df.index.min(), df.index.max()])
selected_columns = st.sidebar.multiselect("Select Columns", df.columns, default=df.columns)

# Filter data based on selections
filtered_df = df.loc[date_range[0]:date_range[1], selected_columns]

# Plot histograms
st.subheader("Histograms")
fig, ax = plt.subplots(figsize=(10, 6))
for col in filtered_df.columns:
    ax.hist(filtered_df[col].dropna(), bins=30, alpha=0.5, label=col)
ax.set_title('Histograms of Selected Columns')
ax.set_xlabel('Value')
ax.set_ylabel('Frequency')
ax.legend(loc='upper right')
st.pyplot(fig)

# Plot correlation matrix
st.subheader("Correlation Matrix")
corr = filtered_df.corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
ax.set_title('Correlation Matrix')
st.pyplot(fig)

# Plot time series
st.subheader("Time Series")
selected_ts_columns = st.sidebar.multiselect("Select Time Series Columns", df.columns, default=['GHI', 'DNI', 'DHI'])
fig, ax = plt.subplots(figsize=(10, 6))
for col in selected_ts_columns:
    ax.plot(filtered_df.index, filtered_df[col], label=col)
ax.set_title('Time Series of Selected Columns')
ax.set_xlabel('Date')
ax.set_ylabel('Value')
ax.legend(loc='upper left')
st.pyplot(fig)

# Add more visualizations and interactivity as needed
