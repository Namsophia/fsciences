#imports
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#define the sql uri
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbs.db'

#define database
db = SQLAlchemy(app)

#define the user model,check the columns needed
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(58), nullable=False)
    genre = db.Column(db.String(58), nullable=False)
    actors = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.String(58), nullable=False)

def create_db():
    with app.app_context():
        db.create_all()

    #create the routes
@app.route('/')
def movies():
    movies = Movie.query.all()
    return render_template('movies.html', movies=movies)

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        actors = request.form['actors']
        publication_year = request.form['publication_year']

        new_movie = Movie(title=title, genre=genre, actors=actors, publication_year=publication_year)
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('movies'))
    return render_template('add_movies.html', title='Add a movie')

if __name__ == '__main__':
    create_db()
    app.run(port=8080, debug=True)
