import streamlit as st
import pickle
import pandas as pd
import numpy as np
import requests
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('API_KEY')

try:
    movies = pickle.load(open("movies.pkl", "rb"))
    similarity = pickle.load(open("similarity.pkl", "rb"))
except FileNotFoundError:
    st.error("Error loading data.")
    st.stop()

st.title("Movie Recommender System")
selected_movie_name = st.selectbox('Enter movie name: ', movies["title"].values)

def recommend(movie):
    try:
        movie_index = movies[movies["title"]==movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[0:6]
        recommended_movies = []
        movie_ids = []
        for i in movies_list:
            movie_ids.append(movies.iloc[i[0]].movie_id)
            recommended_movies.append(movies.iloc[i[0]].title)
        return recommended_movies,movie_ids
    except:
        st.error("Something went wrong, try again!")
        return [],[]

def fetch_poster(movie_id):
    try:
        response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US")
        data = response.json()
        return "https://image.tmdb.org/t/p/w185/" + data["poster_path"]
    except:
        return "./default_img.png"

if st.button("Recommend"):
    movie_names,movie_ids = recommend(selected_movie_name)
    if movie_names and movie_ids:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image(fetch_poster(movie_ids[0]), use_container_width=True)
            st.text(movie_names[0])
        with col2:
            st.image(fetch_poster(movie_ids[1]), use_container_width=True)
            st.text(movie_names[1])
        with col3:
            st.image(fetch_poster(movie_ids[2]), use_container_width=True)
            st.text(movie_names[2])
        st.divider()
        col4, col5, col6 = st.columns(3)
        with col4:
            st.image(fetch_poster(movie_ids[3]), use_container_width=True)
            st.text(movie_names[3])
        with col5:
            st.image(fetch_poster(movie_ids[4]), use_container_width=True)
            st.text(movie_names[4])
        with col6:
            st.image(fetch_poster(movie_ids[5]), use_container_width=True)
            st.text(movie_names[5])
    else:
        st.error("Error, try again!")
