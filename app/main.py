# app/main.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- Page Configuration ---
st.set_page_config(
    page_title="Solar Farm Analysis Dashboard",
    page_icon="☀️",
    layout="wide"
)

# --- Title and Introduction ---
st.title("☀️ MoonLight Energy Solutions: Solar Farm Analysis")
st.write("""
This dashboard provides a comparative analysis of solar farm data from **Benin, Sierra Leone, and Togo**.
Use the options in the sidebar to explore the data and insights.
""")

# --- Data Loading ---
# This function caches the data so it doesn't have to reload every time.
@st.cache_data
def load_data():
    """Loads and combines the solar data for all countries."""
    try:
        benin_df = pd.read_csv('data/benin-solar-farm.csv')
        sierra_leone_df = pd.read_csv('data/sierraleone-solar-farm.csv')
        togo_df = pd.read_csv('data/togo-solar-farm.csv')

        benin_df['Country'] = 'Benin'
        sierra_leone_df['Country'] = 'Sierra Leone'
        togo_df['Country'] = 'Togo'

        combined_df = pd.concat([benin_df, sierra_leone_df, togo_df], ignore_index=True)
        return combined_df
    except FileNotFoundError:
        st.error("Error: The data files were not found. Please make sure `benin-solar-farm.csv`, `sierraleone-solar-farm.csv`, and `togo-solar-farm.csv` are in the `data/` directory.")
        return pd.DataFrame() # Return an empty dataframe on error

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("Dashboard Filters")
selected_countries = st.sidebar.multiselect(
    "Select Countries to Compare:",
    options=df['Country'].unique(),
    default=df['Country'].unique()
)

# Filter the dataframe based on selection
if not selected_countries:
    st.warning("Please select at least one country.")
    filtered_df = pd.DataFrame() # Empty dataframe if nothing is selected
else:
    filtered_df = df[df['Country'].isin(selected_countries)]


# --- Main Dashboard Content ---

# Only display content if data is available and countries are selected
if not filtered_df.empty:
    st.header("Comparative Analysis")

    # --- Metric Comparison Section ---
    st.subheader("Solar Irradiance Comparison")

    col1, col2 = st.columns(2)

    with col1:
        st.write("#### Global Horizontal Irradiance (GHI)")
        fig, ax = plt.subplots()
        sns.boxplot(x='Country', y='GHI', data=filtered_df, ax=ax)
        st.pyplot(fig)

    with col2:
        st.write("#### Direct Normal Irradiance (DNI)")
        fig, ax = plt.subplots()
        sns.boxplot(x='Country', y='DNI', data=filtered_df, ax=ax)
        st.pyplot(fig)

    # --- Summary Table ---
    st.subheader("Summary Statistics")
    st.write("Key metrics (mean, median, standard deviation) for GHI, DNI, and DHI.")
    summary_stats = filtered_df.groupby('Country')[['GHI', 'DNI', 'DHI']].agg(['mean', 'median', 'std'])
    st.dataframe(summary_stats)

    # --- Bar Chart Ranking ---
    st.subheader("Country Ranking by Average GHI")
    avg_ghi = filtered_df.groupby('Country')['GHI'].mean().sort_values(ascending=False)
    fig, ax = plt.subplots()
    sns.barplot(x=avg_ghi.index, y=avg_ghi.values, ax=ax)
    ax.set_ylabel("Average GHI (W/m²)")
    ax.set_xlabel("Country")
    st.pyplot(fig)

else:
    st.info("No data to display based on current selection.")

# --- Footer ---
st.markdown("---")
st.write("Project for 10 Academy | Week 1 Challenge")