import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.title('Visualizing Theme Park Data')
url = 'https://github.com/justinross102/ThemeParkWaitTimes_EDA/raw/main/wait_times.csv'
df = pd.read_csv(url)

st.divider() # Comparing Attraction Counts Across Parks

st.subheader("Comparing Attraction Counts Across Parks")
st.write("Use this interactive plot to compare the number of attractions across multiple parks. Select as many parks as you would like!")

# dropdown for selecting categories
selected_parks = st.multiselect("Select Multiple Parks", df['park'].unique())
filtered_df = df[df['park'].isin(selected_parks)].drop_duplicates(subset='attraction')
park_attraction_counts = filtered_df.groupby('park')['attraction'].count().reset_index()

fig = px.bar(park_attraction_counts, title = 'Number of Attractions in Selected Parks', x = 'park', y = 'attraction', color = 'park')
fig.update_layout(xaxis = dict(tickangle=45))
st.plotly_chart(fig)

st.divider() # Attraction Counts in Theme Park Lands

st.subheader("Attraction Counts in Theme Park Lands")
st.write("""Each theme park usually has a variety of smaller lands within the larger park.
         Each land houses any number of rides and other attractions. Select a theme park below
         and see how many attractions are located in each land!""")

selected_park = st.selectbox('Select a Park', df['park'].unique())
selected_park_df = df[df['park'] == selected_park].drop_duplicates(subset='attraction')

# count attractions in each land
land_counts = selected_park_df['land'].value_counts().reset_index()
land_counts.columns = ['Land', 'Count']

# Use the new DataFrame in px.bar
fig = px.bar(land_counts, x='Land', y='Count', color='Land',
             title='Number of Attractions in Each Land')
st.plotly_chart(fig, use_container_width=True)

st.divider() # Highest and Lowest Wait Times

st.subheader("Highest and Lowest Wait Times")
st.write("""The tables below display the attractions with the top five highest and lowest wait times.
         Select a day and a park, and then use the slider to choose which time of day!""")

selected_day = st.selectbox("Select a Day", df['day'].unique(), key="day_selector")
filtered_df = df[df['day'] == selected_day]

selected_park = st.selectbox("Select a Park", filtered_df['park'].unique(), key="park_selector")

# slider to choose morning, afternoon, or evening
daytime = st.select_slider(
    "Select a Time of Day",
    options=['M', 'A', 'E'],
    key="wait_time_selector",
    format_func=lambda x: 'Morning' if x == 'M' else ('Afternoon' if x == 'A' else 'Evening'))


is_open_column = f'is_open_{daytime}'

filtered_data = filtered_df[(filtered_df['park'] == selected_park) & (filtered_df[is_open_column] == 1)]

# top 5 attractions with highest wait times
top_attractions = filtered_data.nlargest(5, f'wait_time_{daytime}')[['attraction', f'wait_time_{daytime}']].reset_index(drop=True)

# top 5 attractions with smallest wait times
bottom_attractions = filtered_data.nsmallest(5, f'wait_time_{daytime}')[['attraction', f'wait_time_{daytime}']].reset_index(drop=True)

# relabel
column_names = {'attraction': 'Attraction', f'wait_time_{daytime}': 'Wait Time'}
top_attractions = top_attractions.rename(columns=column_names)
bottom_attractions = bottom_attractions.rename(columns=column_names)

st.markdown("###### Top 5 Attractions with Highest Wait Times")
st.dataframe(top_attractions)

st.markdown("###### Top 5 Attractions with Lowest Wait Times")
st.dataframe(bottom_attractions)

st.divider() # Ride Closures

st.subheader("Ride Closures")
st.write("Select a park below and compare the number of Open and Closed Rides!")

selected_park = st.selectbox("Select a Park", df['park'].unique(), key="park_selector2")
selected_day = st.selectbox("Select a Day", df['day'].unique(), key="day_selector2")
selected_df = df[(df['park'] == selected_park) & (df['day'] == selected_day)]

# combine all is_open columns into a single column for graphing
melted_df = pd.melt(selected_df, id_vars=['attraction'], value_vars=['is_open_M', 'is_open_A', 'is_open_E'],
                    var_name='time_of_day', value_name='is_open')

# relabel
melted_df['is_open'] = melted_df['is_open'].apply(lambda x: 'Open' if x == 1 else 'Closed')

# count open and closed rides for each time of day
count_df = melted_df.groupby(['time_of_day', 'is_open']).size().reset_index(name='count')

fig = px.bar(count_df, x='time_of_day', y='count', color='is_open', barmode='group',
            labels={'count': 'Number of Attractions', 'time_of_day': 'Time of Day'},
            category_orders={'time_of_day': ['is_open_M', 'is_open_A', 'is_open_E']},
            color_discrete_map={'Open': 'green', 'Closed': 'red'},
            title=f'Ride Closures at {selected_park} on {selected_day}')

# change axis labels
fig.update_layout(
    xaxis=dict(tickmode='array', tickvals=[0, 1, 2], ticktext=['Morning', 'Afternoon', 'Evening']),
    legend=dict(title='Attraction Status', traceorder='reversed'))
st.plotly_chart(fig)

# find the closed rides for each time of day
closed_rides_morning = melted_df[(melted_df['is_open'] == 'Closed') & (melted_df['time_of_day'] == 'is_open_M')]['attraction'].unique()
closed_rides_afternoon = melted_df[(melted_df['is_open'] == 'Closed') & (melted_df['time_of_day'] == 'is_open_A')]['attraction'].unique()
closed_rides_evening = melted_df[(melted_df['is_open'] == 'Closed') & (melted_df['time_of_day'] == 'is_open_E')]['attraction'].unique()

# print the lists
st.markdown("###### Closed Attractions:")
st.write(f'Morning: {", ".join(closed_rides_morning)}')
st.write(f'Afternoon: {", ".join(closed_rides_afternoon)}')
st.write(f'Evening: {", ".join(closed_rides_evening)}')

st.divider() # Wait Time Distributions

st.subheader("Wait Time Distributions")
st.write("""Choose a park below to see how wait times vary throughout the day and compare them with the next day!
         Consider checking out the Violin Plot to see not only the range of values, but the distribution of the values over that range!""")

# filter data
parks_filtered = df[(df['wait_time_M'] != 0) & (df['wait_time_A'] != 0) & (df['wait_time_E'] != 0)]

selected_park = st.selectbox("Select a Park", parks_filtered['park'].unique(), key="park_selector3")
selected_df = parks_filtered[parks_filtered['park'] == selected_park]

# combine wait times for graphing
melted_df = pd.melt(selected_df, id_vars=['day'], value_vars=['wait_time_M', 'wait_time_A', 'wait_time_E'],
                    var_name='time_of_day', value_name='wait_time')

fig_box = px.box(melted_df, x='time_of_day', y='wait_time', color='day',
                labels={'wait_time': 'Wait Time (minutes)', 'time_of_day': 'Time of Day'},
                category_orders={'time_of_day': ['wait_time_M', 'wait_time_A', 'wait_time_E']},
                title=f'Wait Time Distribution at {selected_park}')

day_order = ['Friday', 'Saturday']

fig_violin = px.violin(melted_df, x="time_of_day", y="wait_time", color="day", box=True, points="all",
                       labels={'wait_time': 'Wait Time (minutes)', 'time_of_day': 'Time of Day'},
                       title=f'Wait Time Distribution at {selected_park}',
                       category_orders={'day': ['Friday', 'Saturday']},
                       violinmode='group')

# change axis values
fig_box.update_layout(xaxis=dict(tickmode='array', tickvals=[0, 1, 2], ticktext=['Morning', 'Afternoon', 'Evening']))
fig_violin.update_layout(xaxis=dict(tickmode='array', tickvals=[0, 1, 2], ticktext=['Morning', 'Afternoon', 'Evening']))

# put graphs in separate tabs
tab1, tab2 = st.tabs(["Box Plot", "Violin Plot"])

with tab1:
   st.plotly_chart(fig_box)

with tab2:
   st.plotly_chart(fig_violin)

st.divider()

st.write("""Thank you so much for visiting this dashboard. If you're interested in learning more about how I did
         this project, feel free to check out my [blog](https://justinross102.github.io/386-blog/fourth-post/)
         and GitHub [repository](https://github.com/justinross102/ThemeParkWaitTimes_EDA).""")