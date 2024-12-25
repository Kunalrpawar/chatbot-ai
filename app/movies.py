import streamlit as st
import random

# Mock movie data (replace with a real API or database in a production app)
movies = [
    {"title": "Inception", "genre": "Sci-Fi", "rating": 8.8},
    {"title": "The Shawshank Redemption", "genre": "Drama", "rating": 9.3},
    {"title": "The Dark Knight", "genre": "Action", "rating": 9.0},
    {"title": "Pulp Fiction", "genre": "Crime", "rating": 8.9},
    {"title": "Forrest Gump", "genre": "Drama", "rating": 8.8},
    {"title": "The Matrix", "genre": "Sci-Fi", "rating": 8.7},
    {"title": "Goodfellas", "genre": "Crime", "rating": 8.7},
    {"title": "The Silence of the Lambs", "genre": "Thriller", "rating": 8.6},
    {"title": "Interstellar", "genre": "Sci-Fi", "rating": 8.6},
    {"title": "The Lord of the Rings: The Fellowship of the Ring", "genre": "Fantasy", "rating": 8.8},
]

def display_movies():
    st.title("🍿 Browse Movies")
    
    # Filter options
    genres = list(set(movie["genre"] for movie in movies))
    selected_genre = st.selectbox("Filter by genre", ["All"] + genres)
    
    # Sort options
    sort_option = st.selectbox("Sort by", ["Rating", "Title"])
    
    # Filter and sort movies
    filtered_movies = movies if selected_genre == "All" else [movie for movie in movies if movie["genre"] == selected_genre]
    sorted_movies = sorted(filtered_movies, key=lambda x: x["rating" if sort_option == "Rating" else "title"], reverse=(sort_option == "Rating"))
    
    # Display movies
    for movie in sorted_movies:
        st.markdown(f"""
        <div style="border:1px solid #ddd; padding:10px; margin-bottom:10px; border-radius:5px;">
            <h3>{movie['title']}</h3>
            <p>Genre: {movie['genre']}</p>
            <p>Rating: {movie['rating']}/10</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Recommend a random movie
    if st.button("Recommend a Random Movie"):
        random_movie = random.choice(movies)
        st.success(f"We recommend: {random_movie['title']} ({random_movie['genre']}, Rating: {random_movie['rating']})")
