from flask import Flask, render_template,request
import pickle
import numpy as np
import pandas as pd
import requests

movies_dict = pickle.load(open("data_files/movie_dict.pkl","rb"))
movies = pd.DataFrame(movies_dict)
similarity=pickle.load(open("data_files/similarity.pkl","rb"))
popularity_df=pickle.load(open("data_files/popularity_df.pkl","rb"))
movie_poster=pickle.load(open("data_files/movie_poster.pkl","rb"))

overview = list(popularity_df['overview'])

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    # st.text(data)
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']



def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x : x[1])[1:6]


    recommended_movies = []
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

movie_title = list(popularity_df['title'].values)
popularity_val = list(popularity_df['popularity'].values)


# for i in movie_title:
#     movie_index=movies[movies['title']==i].index[0]
#     # print(movie_index)
#     new_movie_id=movies.iloc[movie_index].movie_id
#     movie_poster.append(fetch_poster(new_movie_id))


app=Flask(__name__)

@app.route('/')
def index():
    return render_template("movie_templates/index.html",movie_title = movie_title[:50],
                                                        popularity_val=popularity_val[:50],
                                                        movie_poster=movie_poster,
                                                        overview=overview)

if __name__=="__main__":
    app.run(debug=True)