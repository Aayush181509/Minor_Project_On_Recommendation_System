import json
from flask import Flask, render_template,request,redirect,session, url_for
import pickle
import numpy as np
import pandas as pd
import requests
import os
import mysql.connector

app=Flask(__name__)

app.secret_key=os.urandom(24)



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


@app.route('/')
def index():
    if 'user_id' in session:
        # user_info=eval(name)
        print(session["user_name"])
        return render_template("movie_templates/index.html",movie_title = movie_title[:50],
                                                        popularity_val=popularity_val[:50],
                                                        movie_poster=movie_poster,
                                                        overview=overview,
                                                        name=session)
    else:
        return redirect('/login')


@app.route('/recommend/')
def recommend_ui():
    if 'user_id' in session:

        return render_template("movie_templates/recommend.html",movie_title = movie_title[:50],
                                                        popularity_val=popularity_val[:50],
                                                        movie_poster=movie_poster,
                                                        overview=overview,
                                                        name=session)
    else:
        return redirect('/login')

@app.route('/recommend_movies',methods=['post'])
def recommend_movie():
    user_input=request.form.get('user_input')
    movie_index = movies[movies['title']==user_input].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x : x[1])[1:6]


    recommended_movies = []
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return render_template("movie_templates/recommend.html",
                                                        typed_value = user_input,
                                                        movie_title = movie_title,
                                                        popularity_val=popularity_val,
                                                        movie_poster=movie_poster,
                                                        overview=overview,
                                                        recommended_movies=recommended_movies,
                                                        recommended_movies_posters=recommended_movies_posters,
                                                        name=session

                                                        )

@app.route('/login')
def login():
    if 'user_id' not in session:
        return render_template("movie_templates/login.html",)
    else:
        return redirect('/')

@app.route('/register')
def about():
    return render_template("movie_templates/register.html",)


@app.route('/login_validation',methods=['POST'])
def login_validation():
    email=request.form.get("email")
    password=request.form.get("password")
    conn = mysql.connector.connect(host='localhost',database='my_db',user='root',password='A@yush@8131')
    cursor = conn.cursor()

    cursor.execute("""SELECT * from `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))
    users = cursor.fetchall()
    cursor.close()
    print('Database Closed')
    if len(users) > 0:
        session['user_id']=users[0][0]
        session['user_name']=users[0][1]
        session['user_email']= users[0][2]
        
        # print(session['user_email'])
        return redirect('/')
    else:
        return redirect('/login')
    
@app.route('/add_user',methods=['POST'])
def add_user():
    name=request.form.get("uname")
    email=request.form.get("uemail")
    password=request.form.get('upassword')
    conn = mysql.connector.connect(host='localhost',database='my_db',user='root',password='A@yush@8131')
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO `users` (`user_id`,`name`,`email`,`password`) VALUES
    (NULL,'{}','{}','{}')""".format(name,email,password))

    conn.commit()
    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
    myuser=cursor.fetchall()
    cursor.close()

    session['user_id']=myuser[0][0]
    session['user_name']=myuser[0][1]
    session['user_email']=myuser[0][2]

    return redirect('/')

@app.route("/logout")
def logout():
    session.pop("user_id")
    session.pop("user_name")
    session.pop("user_email")

    return redirect("/login")


if __name__=="__main__":
    app.run(debug=True) 