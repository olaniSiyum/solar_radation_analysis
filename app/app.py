import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data
@st.cache_data
def load_data():
    # Replace with the path to your cleaned data
    return pd.read_csv('../data/benin-malanville_cleaned.csv', index_col='Timestamp', parse_dates=True)

df = load_data()

# Convert columns to a list
columns_list = df.columns.tolist()

# Streamlit application
st.title("Solar Radiation Analysis Data Dashboard")

# Sidebar for filters
st.sidebar.header("Filters")

# Date range selection with default values set to the min and max dates in the dataset
start_date, end_date = st.sidebar.date_input("Select Date Range", [df.index.min().date(), df.index.max().date()])

# Ensure that the selected date range is valid
if start_date > end_date:
    st.error("Error: End date must fall after start date.")
else:
    selected_columns = st.sidebar.multiselect("Select Columns", columns_list, default=columns_list)

    # Filter data based on selections
    filtered_df = df.loc[start_date:end_date, selected_columns]

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
    if len(filtered_df.columns) > 1:  # Ensure there is more than one column for correlation
        corr = filtered_df.corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        ax.set_title('Correlation Matrix')
        st.pyplot(fig)
    else:
        st.write("Not enough columns to compute correlation matrix.")

    # Plot time series
    st.subheader("Time Series")
    selected_ts_columns = st.sidebar.multiselect(
        "Select Time Series Columns", 
        columns_list, 
        default=[col for col in ['GHI', 'DNI', 'DHI'] if col in columns_list]  # Ensure default columns exist in the dataset
    )
    
    if not selected_ts_columns:
        st.write("Please select at least one column to display the time series.")
    else:
        fig, ax = plt.subplots(figsize=(10, 6))
        for col in selected_ts_columns:
            if col in filtered_df.columns:  # Ensure the column exists in filtered data
                ax.plot(filtered_df.index, filtered_df[col], label=col)
        ax.set_title('Time Series of Selected Columns')
        ax.set_xlabel('Date')
        ax.set_ylabel('Value')
        ax.legend(loc='upper left')
        st.pyplot(fig)

    # Horizontal Box plot
    st.subheader("Box Plot")
    selected_box_columns = st.sidebar.multiselect("Select Columns for Box Plot", columns_list, default=columns_list)
    if selected_box_columns:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=filtered_df[selected_box_columns], ax=ax, orient='h')
        ax.set_title('Box Plot of Selected Columns')
        ax.set_xlabel('Value')
        ax.set_ylabel('Columns')
        st.pyplot(fig)
    # Wind Speed and Direction Scatter Plot
    st.subheader("Wind Speed vs. Direction Scatter Plot")
    if 'WD' in filtered_df.columns and 'WS' in filtered_df.columns:
        fig, ax = plt.subplots(figsize=(10, 6))
        scatter = ax.scatter(filtered_df['WD'], filtered_df['WS'], c=filtered_df['WS'], cmap='viridis', alpha=0.5)
        ax.set_title('Wind Speed vs. Wind Direction')
        ax.set_xlabel('Wind Direction (Degrees)')
        ax.set_ylabel('Wind Speed (m/s)')
        fig.colorbar(scatter, ax=ax, label='Wind Speed (m/s)')
        st.pyplot(fig)
    else:
        st.write("Wind Speed and Direction scatter plot requires 'WD' (Wind Direction) and 'WS' (Wind Speed) columns.")

    # Scatter plot
    st.subheader("Scatter Plot")
    x_axis = st.sidebar.selectbox("X-axis", columns_list)
    y_axis = st.sidebar.selectbox("Y-axis", columns_list)
    
    if x_axis and y_axis:
        fig, ax = plt.subplots(figsize=(10, 6))
        scatter = ax.scatter(filtered_df[x_axis], filtered_df[y_axis], alpha=0.5, c=filtered_df[x_axis], cmap='plasma')
        ax.set_title(f'Scatter Plot of {x_axis} vs. {y_axis}')
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        fig.colorbar(scatter, ax=ax, label=x_axis)
        st.pyplot(fig)