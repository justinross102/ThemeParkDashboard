import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import plotly.express as px

st.title('Visualizing Theme Park Data')
url = 'https://github.com/justinross102/ThemeParkWaitTimes_EDA/raw/main/wait_times.csv'
df = pd.read_csv(url)

selected_park = st.selectbox('Select a Park', df['park'].unique())

selected_park_df = df[df['park'] == selected_park].drop_duplicates(subset='attraction')

# Create a DataFrame with counts for each 'land'
land_counts = selected_park_df['land'].value_counts().reset_index()
land_counts.columns = ['Land', 'Count']

# Use the new DataFrame in px.bar
fig = px.bar(land_counts, x='Land', y='Count', title='Number of Attractions in Each Land', color='Land')

# Use use_container_width=True for better layout in Streamlit
st.plotly_chart(fig, use_container_width=True)


# Dropdown for selecting categories
selected_parks = st.multiselect("Select Park(s)", df['park'].unique())

# Filter the DataFrame based on selected parks
filtered_df = df[df['park'].isin(selected_parks)].drop_duplicates(subset='attraction')

# Group by park and count attractions
park_attraction_counts = filtered_df.groupby('park')['attraction'].count()

# Create a bar graph
st.bar_chart(park_attraction_counts)
