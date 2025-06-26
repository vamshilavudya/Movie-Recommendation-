import streamlit as st
import pickle
import requests
import streamlit.components.v1 as components


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except Exception as e:
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=Error"


movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values


st.set_page_config(page_title="Movie Recommender", layout="wide")
st.header("🎬 Movie Recommender System")


imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

# List of movie IDs for carousel
carousel_movie_ids = [1632, 299536, 17455, 2830, 429422, 9722, 13972, 240, 155, 598, 914, 255709, 572154]
imageUrls = [fetch_poster(mid) for mid in carousel_movie_ids]

imageCarouselComponent(imageUrls=imageUrls, height=200)



selectvalue = st.selectbox("🎥 Select a movie to get recommendations", movies_list)



def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommend_movie = []
    recommend_poster = []

    for i in distance[1:6]: 
        movie_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movie_id))

    return recommend_movie, recommend_poster


if st.button("🎯 Show Recommendations"):
    movie_name, movie_poster = recommend(selectvalue)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])
