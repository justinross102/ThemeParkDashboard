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

#name_df = df[df['name'] == selected_name]
#if name_df.empty:
#    st.write('Name not found')
#else:
#    fig = px.line(name_df, x='year', y='n', color='sex',
#                  color_discrete_sequence=px.colors.qualitative.Set2)
#    st.plotly_chart(fig)

# remember, each attraction is listed twice. Once for Friday and again for Saturday
# as a result, we need to remove duplicates to get an accurate count of each park's attractions



# sns.countplot(x='park', data=parks_no_duplicates)

# # rotate x-axis tick labels for better readability
# plt.xticks(rotation=45)

# plt.title('Number of Attractions')
# plt.xlabel('Theme Park')
# plt.xticks(ha='right')  # adjust alignment for better readability
# plt.ylabel('Number of Attractions')
# plt.show()
