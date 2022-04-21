from crypt import methods
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import movies
from operator import itemgetter


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies-database.db"
db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<Books %r>' % self.title

db.create_all()


class MovieForm(FlaskForm):
    rating = StringField('Your Rating', validators=[DataRequired()])
    review = StringField('Your Review', validators=[DataRequired()])
    submit = SubmitField('Done')

class AddMovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')

''''
new_movie = Movie(  title = "Phone Booth",
                    year = 2002,
                    description = "Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
                    rating = 7.3,
                    ranking = 10,
                    review = "My favourite character was the caller.",
                    img_url = "https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
                )
db.session.add(new_movie)
db.session.commit()

'''

@app.route("/")
def home():
    movies = db.session.query(Movie).order_by(Movie.rating).all()
    movies_count = len(movies)
    for movie in movies:
        new_ranking = Movie.query.get(movie.id)
        new_ranking.ranking = movies_count
        db.session.commit()
        movies_count -= 1
    movies = db.session.query(Movie).order_by(Movie.rating).all()
    return render_template("index.html", movies=movies)


@app.route("/edit/<int:id>", methods=['GET','POST'])
def edit(id):
    form = MovieForm()
    if form.validate_on_submit():
        rating = form.rating.data
        review = form.review.data
        new_rating = Movie.query.get(id)
        new_rating.rating = float(rating)
        new_rating.review = review
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template("edit.html", form=form)

@app.route('/delete/<int:id>', methods=['GET','POST'])
def delete(id):
    movie = Movie.query.get(id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/add', methods=['GET','POST'])
def add():
    form = AddMovieForm()
    if form.validate_on_submit():
        movies_list = movies.search_movie(form.title.data)
        return render_template('select.html', movies=movies_list)
    return render_template('add.html', form=form)

@app.route('/add/<int:id>', methods=['GET','POST'])
def add_movie(id):
    title, img_url, year, description = movies.get_movie_detail(id)
    new_movie = Movie(title=title, year=year, description=description, img_url=img_url, rating=0, ranking=0, review=" ")
    db.session.add(new_movie)
    db.session.flush()
    id_movie = new_movie.id
    db.session.commit()
    return redirect(url_for('edit',id=id_movie))

if __name__ == '__main__':
    app.run(debug=True)
