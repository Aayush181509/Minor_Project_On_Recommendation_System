from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open("data_files/popular.pkl", "rb"))

pt = pickle.load(open("data_files/pt.pkl","rb"))
books = pickle.load(open("data_files/books.pkl","rb"))
similarity_score = pickle.load(open("data_files/similarity_score.pkl","rb"))
app=Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html",
                            book_name=list(popular_df['Book-Title'].values),
                            author=list(popular_df['Book-Author'].values),
                            image=list(popular_df['Image-URL-M'].values),
                            votes=list(popular_df['num_ratings'].values),
                            rating=list(popular_df['avg_ratings'].values),

                            )
@app.route('/recommend')
def recommend_ui():
    return render_template("recommend.html",
    names = list(books['Book-Title'].values))


@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index==user_input)[0][0]
    distances = similarity_score[index]
    similar_items = sorted(list(enumerate(distances)),key=lambda x : x[1], reverse=True)[1:9]
    data=[]
    for i in similar_items:
        item=[]
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
    return render_template('recommend.html',data=data,names = list(books['Book-Title'].values))

if __name__=="__main__":
    app.run(debug=True)