import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.title('Visualizing Theme Park Data')
url = 'https://github.com/justinross102/ThemeParkWaitTimes_EDA/raw/main/wait_times.csv'
df = pd.read_csv(url)


st.subheader("Comparing Attraction Counts Across Parks")
st.write("Use this interactive plot to compare the number of attractions across multiple parks. Select as many parks as you would like!")

# dropdown for selecting categories
selected_parks = st.multiselect("Select Multiple Parks", df['park'].unique())
filtered_df = df[df['park'].isin(selected_parks)].drop_duplicates(subset='attraction')
park_attraction_counts = filtered_df.groupby('park')['attraction'].count().reset_index()

fig = px.bar(park_attraction_counts, title = 'Number of Attractions in Selected Parks', x = 'park', y = 'attraction', color = 'park')
fig.update_layout(xaxis = dict(tickangle=45))
st.plotly_chart(fig)

st.divider()

st.subheader("Attraction Counts in Theme Park Lands")
st.write("""Each theme park usually has a variety of smaller lands within the larger park.
         Each land houses any number of rides and other attractions. Select a theme park below
         and see how many attractions are located in each land!""")

selected_park = st.selectbox('Select a Park', df['park'].unique())

selected_park_df = df[df['park'] == selected_park].drop_duplicates(subset='attraction')

# Create a DataFrame with counts for each 'land'
land_counts = selected_park_df['land'].value_counts().reset_index()
land_counts.columns = ['Land', 'Count']

# Use the new DataFrame in px.bar
fig = px.bar(land_counts, x='Land', y='Count', title='Number of Attractions in Each Land', color='Land')

# Use use_container_width=True for better layout in Streamlit
st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Highest and Lowest Wait Times")
st.write("The tables below display the attractions with the top five highest and lowest wait times. Select a day and a park, and then use the slider to choose which time of day!")

# Dropdown for selecting the day
selected_day = st.selectbox("Select a Day", df['day'].unique(), key="day_selector")

# Filter the DataFrame based on the selected day
filtered_df = df[df['day'] == selected_day]

# Dropdown for selecting the park
selected_park = st.selectbox("Select a Park", filtered_df['park'].unique(), key="park_selector")

# Select Slider for choosing the wait time column
wait_time_column = st.select_slider(
    "Select a Time of Day",
    options=['M', 'A', 'E'],
    key="wait_time_selector",
    format_func=lambda x: 'Morning' if x == 'M' else ('Afternoon' if x == 'A' else 'Evening')
)

# Use the appropriate is_open column based on the selected time
is_open_column = f'is_open_{wait_time_column}'

# Filter the DataFrame based on the selected park and only include open rides
filtered_df_by_park_open = filtered_df[(filtered_df['park'] == selected_park) & (filtered_df[is_open_column] == 1)]

# Find the top 5 attractions with the highest wait times for the selected park
top_attractions = filtered_df_by_park_open.nlargest(5, f'wait_time_{wait_time_column}')[['attraction', f'wait_time_{wait_time_column}']].reset_index(drop=True)

# Customize the column names for display
column_names = {'attraction': 'Attraction', f'wait_time_{wait_time_column}': 'Wait Time'}
top_attractions = top_attractions.rename(columns=column_names)

# Find the top 5 attractions with the smallest wait times for the selected park
top_attractions_smallest = filtered_df_by_park_open.nsmallest(5, f'wait_time_{wait_time_column}')[['attraction', f'wait_time_{wait_time_column}']].reset_index(drop=True)

# Customize the column names for display
column_names_mapping = {'attraction': 'Attraction', f'wait_time_{wait_time_column}': 'Wait Time'}
top_attractions_smallest = top_attractions_smallest.rename(columns=column_names_mapping)

data_container = st.container()

with data_container:
    table, plot = st.columns(2)
    with table:
        st.markdown("###### Top 5 Attractions with Highest Wait Times")
        st.dataframe(top_attractions)
    with plot:
        st.markdown("###### Top 5 Attractions with Lowest Wait Times")
        st.dataframe(top_attractions_smallest)

st.divider()
