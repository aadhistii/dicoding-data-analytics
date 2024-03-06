import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

sns.set(style='dark')


def df_count_user(df):
    user = ['casual', 'registered']
    count_casual = df['casual'].sum()
    count_registered = df['registered'].sum()
    count = [count_casual, count_registered]
    df_count = pd.DataFrame({'User': user, 'Count': count}).reset_index()
    return df_count


st.title("Dicoding Submission")

df = pd.read_csv("data/bike_data.csv")

df['date'] = pd.to_datetime(df['date'])
min_date = df["date"].min()
max_date = df["date"].max()

with st.sidebar:
    st.image("assets/icon-bike.svg")

    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

df_bf = df
df = df[(df['date'] >= str(start_date)) &
        (df['date'] <= str(end_date))]

df_count = df_count_user(df)

st.header('Bike Sharing Adhisti :sparkles:')

col1, col2, col3 = st.columns(3)

with col1:
    casual = df.casual.sum()
    st.metric('Total Casual User', value=casual)

with col2:
    registered = df.registered.sum()
    st.metric('Total Registered User', value=registered)

with col3:
    total = df['count'].sum()
    st.metric('Total User', value=total)

st.subheader('Question 1: Does the amount of bike sharing increase in 2012?')

fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(data=df_bf, x='year', y='count', hue='season', ax=ax)
ax.set(title='Bike Sharing Over Time')
st.pyplot(fig)

st.subheader('Question 2: Is there any correlation between each feature especially on count with other features?')

df_num = df.select_dtypes(include=['number'])
fig, ax = plt.subplots(figsize=(20, 12))
corr = df_num[df_num.columns[1:]].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, linewidths=1, annot=True, fmt=".2f", ax=ax)
st.pyplot(fig)

st.subheader('Question 3: When do people feel it is important to use bicycle?')

fig, ax = plt.subplots(figsize=(20, 5))
sns.pointplot(data=df, x='hour', y='count', hue='weekday', ax=ax)
ax.set(title='Bikes Sharing Everyday')
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(20, 5))
sns.barplot(data=df, x='month', y='count', hue='weather', ax=ax)
ax.set(title='Bike Sharing Based From Weather and Month')
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(20, 5))
sns.barplot(data=df, x='workingday', y='count', hue='month', ax=ax)
ax.set(title='Bikes Sharing during Workingday')
st.pyplot(fig)

st.subheader('Question 4: How important is a bike sharing system or app?')

fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(df_count['Count'], labels=df_count['User'], autopct='%1.1f%%')
ax.set(title='Ratio Registered and Casual User')
st.pyplot(fig)

st.caption('Copyright (c) Adhisti 2024')
