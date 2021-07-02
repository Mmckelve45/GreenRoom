from flask import Flask, render_template, json, request, redirect, flash
import os

from flask.helpers import url_for
import database.db_connector as db
# import MySQLdb

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

# Global Variable for search message.

searchMessage = "Nothing matched your search."

# General Purpose functions

def runQuery(query, query_params=None):
    try:
        if query_params == None:
            cursor = db.execute_query(db_connection=db_connection, query=query)
            results = cursor.fetchall()
        else:
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=query_params)
            results = cursor.fetchall()
    except db.MySQLdb.Error as err:
        print("ERROR, ERROR, ERROR:", str(err))
        
        return 'error', err
    return results
    
def getEntityInstance(table, id):
    print(id)
    query = "SELECT * FROM " + table + " WHERE " + table[:-1].lower() + "_id = " + id
    try:
        cursor = db.execute_query(db_connection=db_connection, query=query)
        entityInstance = cursor.fetchone()
    except db.MySQLdb.Error as err:
        print("ERROR, ERROR, ERROR:", str(err))
        return 'error', err
    return entityInstance

def getEntity(table):
    query = "SELECT * FROM " + table
    try:    
        cursor = db.execute_query(db_connection=db_connection, query=query)
        entity = cursor.fetchall()
    except db.MySQLdb.Error as err:
        print("ERROR, ERROR, ERROR:", str(err))
        return 'error', err
    return entity



# Routes 



@app.route('/')
def root():
    return render_template("index.j2")

@app.route('/Performers')
def Performers():
    query = "SELECT * FROM Performers;"
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])
    return render_template("Performers.j2", Performers=results)

@app.route('/seachPerformer', methods=('GET', 'POST'))
def searchPerformer():
    query = "SELECT * FROM Performers ORDER BY performer_id;"

    # Set search query string
    last_name = request.args.get('performer_last_name')

    # Set query to return rows specified by search term, else set the query to return all rows
    if last_name:
        query = f'SELECT * FROM Performers WHERE performer_first_name LIKE "%%{last_name}%%" OR performer_last_name LIKE "%%{last_name}%%" ORDER BY performer_last_name;'
    elif not last_name:
        query = "SELECT * FROM Performers ORDER BY performer_last_name;"

    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])
    if not results:
        return render_template("Performers.j2", Performers=results, searchMessage=searchMessage)
    return render_template("Performers.j2", Performers=results)


@app.route('/createPerformer',  methods = ('GET', 'POST'))
def createPerformer():
    if request.method == 'POST':
        first_name = request.form['performer_first_name'].lower()
        first_name = first_name.capitalize()
        last_name = request.form['performer_last_name'].lower()
        last_name = last_name.capitalize()
        city = request.form['performer_city']
        state = request.form['performer_state']
        height = request.form['performer_height_in']
        hair_color = request.form['performer_hair_color']
        eye_color = request.form['performer_eye_color']
        weight = request.form['performer_weight_lbs']
        rating = request.form['performer_rating']
        dob = request.form['performer_dob']
        gender = request.form['performer_gender']
        ethnicity = request.form['performer_ethnicity']
        print("hello")
        
        
        
        query = "INSERT INTO Performers (performer_first_name, performer_last_name, performer_city, performer_state, performer_height_in, performer_hair_color, performer_eye_color, performer_weight_lbs, performer_rating, performer_dob, performer_gender, performer_ethnicity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        results = runQuery(query=query, query_params=(first_name, last_name, city, state, height, hair_color, eye_color, weight, rating, dob, gender, ethnicity))
        if results:
            if results[0] == 'error':
                return render_template("error.j2", err=results[1])
        return redirect('/Performers')
   


@app.route('/deletePerformer/<int:id>', methods=('GET', 'POST'))
def deletePerformer(id):
    print("DELETE FROM Performers WHERE performer_id=" + str(id))
    query = "DELETE FROM Performers WHERE performer_id = " + str(id)
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])

    query = "DELETE FROM Movie_Credits WHERE performer_id is NULL"
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])

    query = "DELETE FROM Movie_Credit_User_Reviews WHERE movie_credit_id is NULL"
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])

    query = "DELETE FROM TV_Show_Credits WHERE performer_id is NULL"
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])

    query = "DELETE FROM TV_Show_Credit_User_Reviews WHERE tv_show_credit_id is NULL"
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])

    return redirect('/Performers')



@app.route('/updatePerformer/<id>', methods=('GET', 'POST'))
def updatePerformer(id):
    performer = getEntityInstance("Performers", id)
    if request.method == 'POST':
        first_name = request.form['performer_first_name'].lower()
        first_name = first_name.capitalize()
        last_name = request.form['performer_last_name'].lower()
        last_name = last_name.capitalize()
        city = request.form['performer_city']
        state = request.form['performer_state']
        height = request.form['performer_height_in']
        hair_color = request.form['performer_hair_color']
        eye_color = request.form['performer_eye_color']
        weight = request.form['performer_weight_lbs']
        rating = request.form['performer_rating']
        dob = request.form['performer_dob']
        gender = request.form['performer_gender']
        ethnicity = request.form['performer_ethnicity']

        query = "UPDATE Performers SET performer_first_name=%s, performer_last_name=%s, performer_city=%s, performer_state=%s, performer_height_in=%s, performer_hair_color=%s, performer_eye_color=%s, performer_weight_lbs=%s, performer_rating=%s, performer_dob=%s, performer_gender=%s, performer_ethnicity=%s WHERE performer_id=" + str(id)
        results = runQuery(query=query, query_params=(first_name, last_name, city, state, height, hair_color, eye_color, weight, rating, dob, gender, ethnicity))
        if results:
            if results[0] == 'error':
                return render_template("error.j2", err=results[1])
        return redirect('/Performers')
    return render_template("updatePerformer.j2", performer=performer)


@app.route('/Movies')
def Movies():
    query = "SELECT * FROM Movies;"
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])
    return render_template("Movies.j2", Movies=results)


@app.route('/seachMovie', methods=('GET', 'POST'))
def searchMovie():

    query = "SELECT * FROM Movies ORDER BY movie_title;"

    # Set search query string
    title = request.args.get('movie_title')

    if title:
        query = f'SELECT * FROM Movies WHERE movie_title LIKE "%%{title}%%" ORDER BY movie_title;'

    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])
    if not results:
        return render_template("Movies.j2", Movies=results, searchMessage=searchMessage)

    return render_template("Movies.j2", Movies=results)


@app.route('/createMovie',  methods = ('GET', 'POST'))
def createMovie():
    if request.method == 'POST':
        title = request.form['movie_title']
        release_date = request.form['movie_release_date']
        runtime = request.form['movie_runtime']
        budget = request.form['movie_budget']
        director_first_name = request.form['movie_director_first_name'].lower()
        director_first_name = director_first_name.capitalize()
        director_last_name = request.form['movie_director_last_name'].lower()
        director_last_name = director_last_name.capitalize()
        tomatoes_critic = request.form['movie_rating_tomatoes_critic']
        tomatoes_audience = request.form['movie_rating_tomatoes_audience']
        imdb_critic = request.form['movie_rating_imdb_critic']
        imdb_audience = request.form['movie_rating_imdb_audience']
        meta_critic = request.form['movie_rating_meta_critic']
        meta_audience = request.form['movie_rating_meta_audience']
        
        query = "INSERT INTO Movies (movie_title, movie_release_date, movie_runtime, movie_budget, movie_director_first_name, movie_director_last_name, movie_rating_tomatoes_critic, movie_rating_tomatoes_audience, movie_rating_imdb_critic, movie_rating_imdb_audience, movie_rating_meta_critic, movie_rating_meta_audience) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(first_name, last_name, dob, gender, ethnicity))
        results = runQuery(query=query, query_params=(title, release_date, runtime, budget, director_first_name, director_last_name, tomatoes_critic, tomatoes_audience, imdb_critic, imdb_audience, meta_critic, meta_audience))
        if results:
            if results[0] == 'error':
                return render_template("error.j2", err=results[1])
        return redirect('/Movies')


@app.route('/updateMovie/<id>', methods=('GET', 'POST'))
def updateMovie(id):
    movie = getEntityInstance("Movies", id)
    print("hello outside POST")
    if request.method == 'POST':
        print("HELLO IN UPDATEMOVE POST ROUTE")
        title = request.form['movie_title']
        release_date = request.form['movie_release_date']
        runtime = request.form['movie_runtime']
        budget = request.form['movie_budget']
        director_first_name = request.form['movie_director_first_name'].lower()
        director_first_name = director_first_name.capitalize()
        director_last_name = request.form['movie_director_last_name'].lower()
        director_last_name = director_last_name.capitalize()
        tomatoes_critic = request.form['movie_rating_tomatoes_critic']
        tomatoes_audience = request.form['movie_rating_tomatoes_audience']
        imdb_critic = request.form['movie_rating_imdb_critic']
        imdb_audience = request.form['movie_rating_imdb_audience']
        meta_critic = request.form['movie_rating_meta_critic']
        meta_audience = request.form['movie_rating_meta_audience']
        query = "UPDATE Movies SET movie_title=%s, movie_release_date=%s, movie_runtime=%s, movie_budget=%s, movie_director_first_name=%s, movie_director_last_name=%s, movie_rating_tomatoes_critic=%s, movie_rating_tomatoes_audience=%s, movie_rating_imdb_critic=%s, movie_rating_imdb_audience=%s, movie_rating_meta_critic=%s, movie_rating_meta_audience=%s WHERE movie_id = " + str(id)
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(title, release_date, runtime, budget, director_first_name, director_last_name, tomatoes_critic, tomatoes_audience, imdb_critic, imdb_audience, meta_critic, meta_audience))
        results = cursor.fetchall()
        return redirect('/Movies')
    return render_template("updateMovie.j2", movie = movie)


@app.route('/deleteMovie/<int:id>', methods=('GET', 'POST'))
def deleteMovie(id):
    print("DELETE FROM Movies WHERE movie_id=" + str(id))
    query = "DELETE FROM Movies WHERE movie_id = " + str(id)
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])

    query = "DELETE FROM Movie_Credits WHERE movie_id is NULL"
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])

    query = "DELETE FROM Movie_Credit_User_Reviews WHERE movie_credit_id is NULL"
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])
    
    return redirect('/Movies')


@app.route('/Movie_Credits')
def Movies_Credits():
    Performers = getEntity("Performers")
    Movies = getEntity("Movies")
    query = "SELECT * FROM Movie_Credits;"
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])
    return render_template("Movie_Credits.j2", MovieCredits=results, Performers=Performers, Movies=Movies)


@app.route('/seachMovieCredit', methods=('GET', 'POST'))
def searchMovieCredit():

    query = "SELECT * FROM Movie_Credits;"

    # Set search query string
    last_name = request.args.get('performer_last_name')
    columns = 'Movie_Credits.movie_credit_id, Movie_Credits.performer_id, Movie_Credits.movie_id, Movie_Credits.movie_credit_payment, Movie_Credits.movie_credit_role, Movie_Credits.movie_credit_lead_role, Movie_Credits.movie_credit_oscar'

    if last_name:
        query = f'SELECT {columns} FROM Movie_Credits \
                JOIN Performers ON Movie_Credits.performer_id = Performers.performer_id \
                WHERE Performers.performer_last_name LIKE "%%{last_name}%%";'

    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])
    if not results:
        return render_template("Movie_Credits.j2", Movies=results, searchMessage=searchMessage)
    return render_template("Movie_Credits.j2", MovieCredits=results)


@app.route('/createMovieCredit',  methods = ('GET', 'POST'))
def createMovieCredit():
    # performer_id, movie_id, movie_credit_payment, movie_credit_role, movie_credit_leading_role, movie_credit_oscar_award
    if request.method == 'POST':
        performer_id = request.form['performer_id']
        movie_id = request.form['movie_id']
        payment = request.form['movie_credit_payment']
        role = request.form['movie_credit_role']
        lead = request.form['movie_credit_lead_role']
        oscar = request.form['movie_credit_oscar']
 
        
        query = "INSERT INTO Movie_Credits (performer_id, movie_id, movie_credit_payment, movie_credit_role, movie_credit_lead_role, movie_credit_oscar) VALUES (%s, %s, %s, %s, %s, %s)"
        # cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(first_name, last_name, dob, gender, ethnicity))
        query_params = (performer_id, movie_id, payment, role, lead, oscar)
        

        results = runQuery(query=query, query_params=query_params)
        if results:
            if results[0] == 'error':
                return render_template("error.j2", err=results[1])
        return redirect('/Movie_Credits')


@app.route('/updateMovieCredits/<id>', methods=('GET', 'POST'))
def updateMovieCredits(id):
    movie_credit = getEntityInstance("Movie_Credits", id)
    Movies = getEntity("Movies")
    Performers = getEntity("Performers")

    print("hello outside POST")
    if request.method == 'POST':
        # print("HELLO IN UPDATEMOVE POST ROUTE")
        performer_id = request.form['performer_id']
        movie_id = request.form['movie_id']
        payment = request.form['movie_credit_payment']
        role = request.form['movie_credit_role']
        lead = request.form['movie_credit_lead_role']
        oscar = request.form['movie_credit_oscar']
        query = "UPDATE Movie_Credits SET performer_id=%s, movie_id=%s, movie_credit_payment=%s, movie_credit_role=%s, movie_credit_lead_role=%s, movie_credit_oscar=%s WHERE movie_credit_id = " + str(id)
        results = runQuery(query=query, query_params=(performer_id, movie_id, payment, role, lead, oscar))
        if results:
            if results[0] == 'error':
                return render_template("error.j2", err=results[1])
        return redirect('/Movie_Credits')
    return render_template("updateMovieCredits.j2", movie_credit = movie_credit, Movies=Movies, Performers=Performers)


@app.route('/deleteMovieCredit/<int:id>', methods=('GET', 'POST'))
def deleteMovieCredit(id):
    print("DELETE FROM Movie_Credits WHERE movie_credit_id=" + str(id))
    query = "DELETE FROM Movie_Credits WHERE movie_credit_id = " + str(id)
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])

    query = "DELETE FROM Movie_Credit_User_Reviews WHERE movie_credit_id is NULL"
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])

    return redirect('/Movie_Credits')


@app.route('/Movie_Credit_User_Reviews')
def Movies_Credit_User_Reviews():
    query = "SELECT * FROM Movie_Credit_User_Reviews;"
    Users = getEntity("Users")
    Movie_Credit_User_Reviews_and_Performers_and_Movies = runQuery("SELECT Movie_Credits.movie_credit_id, Movie_Credits.movie_credit_id, Performers.performer_first_name, Performers.performer_last_name, Movies.movie_title FROM Movie_Credits \
                                                    JOIN Movies on Movies.movie_id = Movie_Credits.movie_id \
                                                    JOIN Performers on Movie_Credits.performer_id = Performers.performer_id \
                                                    ORDER BY Movie_Credits.movie_credit_id")

    if Movie_Credit_User_Reviews_and_Performers_and_Movies:
        if Movie_Credit_User_Reviews_and_Performers_and_Movies[0] == 'error':
            return render_template("error.j2", err=Movie_Credit_User_Reviews_and_Performers_and_Movies[1])
    
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])
    return render_template("Movie_Credit_User_Reviews.j2", MovieCreditUserReviews=results, Users=Users, Movie_Credit_User_Reviews_and_Performers_and_Movies=Movie_Credit_User_Reviews_and_Performers_and_Movies)


@app.route('/searchMovieCreditUserReview', methods=('GET', 'POST'))
def searchMovieCreditUserReview():
    query = "SELECT * FROM Movie_Credit_User_Reviews;"

    # Set search query string
    user_login = request.args.get('user_login_id')
    columns = 'movie_credit_user_review_id, Movie_Credit_User_Reviews.user_id, movie_credit_id, movie_credit_user_review_performer_rating, movie_credit_user_review_description, movie_credit_user_review_date'
    if user_login:
        # query = f'SELECT * FROM Movies WHERE movie_title LIKE "%%{title}%%" ORDER BY movie_title;'

        # query = f'SELECT movie_credit_id, movie_credit_user_review_performer_rating, movie_credit_user_review_description, movie_credit_user_review_date FROM Movie_Credit_User_Reviews \
        #         JOIN Users ON Movie_Credit_User_Reviews.user_id = Users.user_id \
        #         WHERE Users.user_login_id LIKE "%%{user_login}%%";'

        query = f'SELECT {columns} FROM Movie_Credit_User_Reviews \
                JOIN Users ON Movie_Credit_User_Reviews.user_id = Users.user_id \
                WHERE Users.user_login_id LIKE "%%{user_login}%%";'

    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])
    if not results:
        return render_template("Movie_Credit_User_Reviews.j2", Movies=results, searchMessage=searchMessage)
    return render_template("Movie_Credit_User_Reviews.j2", MovieCreditUserReviews=results)


@app.route('/createMovieCreditUserReview',  methods = ('GET', 'POST'))
def createMovieCreditUserReview():
    
    if request.method == 'POST':
        user_id = request.form['user_id']
        movie_credit_id = request.form['movie_credit_id']
        rating = request.form['movie_credit_user_review_performer_rating']
        description = request.form['movie_credit_user_review_description']
        date = request.form['movie_credit_user_review_date']
 
        
        query = "INSERT INTO Movie_Credit_User_Reviews (user_id, movie_credit_id, movie_credit_user_review_performer_rating, movie_credit_user_review_description, movie_credit_user_review_date) VALUES (%s, %s, %s, %s, %s)"
        results = runQuery(query=query, query_params=(user_id, movie_credit_id, rating, description, date))
        if results:
            if results[0] == 'error':
                return render_template("error.j2", err=results[1])
        return redirect('/Movie_Credit_User_Reviews')


# movie_credit_user_review_id, user_id, movie_credit_id, movie_credit_user_review_performer_rating, movie_credit_user_review_description, movie_credit_user_review_date
@app.route('/updateMovieCreditUserReviews/<id>', methods=('GET', 'POST'))
def updateMovieCreditUserReviews(id):
    movie_credit_user_review = getEntityInstance("Movie_Credit_User_Reviews", id)
    Users = getEntity("Users")
    Movie_Credit_User_Reviews_and_Performers_and_Movies = runQuery("SELECT Movie_Credits.movie_credit_id, Movie_Credits.movie_credit_id, Performers.performer_first_name, Performers.performer_last_name, Movies.movie_title FROM Movie_Credits \
                                                    JOIN Movies on Movies.movie_id = Movie_Credits.movie_id \
                                                    JOIN Performers on Movie_Credits.performer_id = Performers.performer_id \
                                                    ORDER BY Movie_Credits.movie_credit_id")

    if Movie_Credit_User_Reviews_and_Performers_and_Movies:
        if Movie_Credit_User_Reviews_and_Performers_and_Movies[0] == 'error':
            return render_template("error.j2", err=Movie_Credit_User_Reviews_and_Performers_and_Movies[1])

    if request.method == 'POST':
        user_id = request.form['user_id']
        movie_credit_id = request.form['movie_credit_id']
        rating = request.form['movie_credit_user_review_performer_rating']
        description = request.form['movie_credit_user_review_description']
        date = request.form['movie_credit_user_review_date']
        query = "UPDATE Movie_Credit_User_Reviews SET user_id=%s, movie_credit_id=%s, movie_credit_user_review_performer_rating=%s, movie_credit_user_review_description=%s, movie_credit_user_review_date=%s WHERE movie_credit_user_review_id = " + str(id)
        results = runQuery(query=query, query_params=(user_id, movie_credit_id, rating, description, date))
        if results:
            if results[0] == 'error':
                return render_template("error.j2", err=results[1])
        return redirect('/Movie_Credit_User_Reviews')
    return render_template("updateMovieCreditUserReviews.j2", movie_credit_user_review = movie_credit_user_review, Users=Users, Movie_Credit_User_Reviews_and_Performers_and_Movies=Movie_Credit_User_Reviews_and_Performers_and_Movies)


@app.route('/deleteMovieCreditUserReview/<int:id>', methods=('GET', 'POST'))
def deleteMovieCreditUserReview(id):
    query = "DELETE FROM Movie_Credit_User_Reviews WHERE movie_credit_user_review_id = " + str(id)
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])
    return redirect('/Movie_Credit_User_Reviews')


@app.route('/TV_Show_Credit_User_Reviews')
def TV_Show_Credit_User_Reviews():
    query = "SELECT * FROM TV_Show_Credit_User_Reviews;"
    Users = getEntity("Users")
    TV_Show_Credits_and_Performers_and_TV_Shows = runQuery("SELECT TV_Show_Credits.tv_show_credit_id, Performers.performer_first_name, Performers.performer_last_name, TV_Shows.tv_show_title, TV_Shows.tv_show_season, TV_Shows.tv_show_episode, TV_Shows.tv_show_episode_part FROM TV_Show_Credits \
                                JOIN Performers ON TV_Show_Credits.performer_id = Performers.performer_id \
                                JOIN TV_Shows on TV_Show_Credits.tv_show_id = TV_Shows.tv_show_id \
                                ORDER BY TV_Show_Credits.tv_show_credit_id")
    
    if TV_Show_Credits_and_Performers_and_TV_Shows:
        if TV_Show_Credits_and_Performers_and_TV_Shows[0] == 'error':
            return render_template("error.j2", err=TV_Show_Credits_and_Performers_and_TV_Shows[1])

    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])
    return render_template("TV_Show_Credit_User_Reviews.j2", TVShowCreditUserReviews=results, Users=Users, TV_Show_Credits_and_Performers_and_TV_Shows=TV_Show_Credits_and_Performers_and_TV_Shows)


@app.route('/searchTVShowCreditUserReview', methods=('GET', 'POST'))
def searchTVShowCreditUserReview():

    query = "SELECT * FROM TV_Show_Credit_User_Reviews;"

    # Set search query string
    user_login = request.args.get('user_login_id')
    columns = 'TV_Show_Credit_User_Reviews.tv_show_credit_user_review_id, TV_Show_Credit_User_Reviews.user_id, TV_Show_Credit_User_Reviews.tv_show_credit_id, \
        TV_Show_Credit_User_Reviews.tv_show_credit_user_review_performer_rating, TV_Show_Credit_User_Reviews.tv_show_credit_user_review_description, \
        TV_Show_Credit_User_Reviews.tv_show_credit_user_review_date'

    if user_login:
        # query = f'SELECT * FROM Movies WHERE movie_title LIKE "%%{title}%%" ORDER BY movie_title;'

        query = f'SELECT {columns} FROM TV_Show_Credit_User_Reviews \
                JOIN Users ON TV_Show_Credit_User_Reviews.user_id = Users.user_id \
                WHERE Users.user_login_id LIKE "%%{user_login}%%";'

    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])
    if not results:
        return render_template("TV_Show_Credit_User_Reviews.j2", Movies=results, searchMessage=searchMessage)
    return render_template("TV_Show_Credit_User_Reviews.j2", TVShowCreditUserReviews=results)


@app.route('/createTVShowCreditUserReview',  methods = ('GET', 'POST'))
def createTVShowCreditUserReview():
    
    if request.method == 'POST':
        user_id = request.form['user_id']
        tv_show_credit_id = request.form['tv_show_credit_id']
        rating = request.form['tv_show_credit_user_review_performer_rating']
        description = request.form['tv_show_credit_user_review_description']
        date = request.form['tv_show_credit_user_review_date']
 
        query = "INSERT INTO TV_Show_Credit_User_Reviews (user_id, tv_show_credit_id, tv_show_credit_user_review_performer_rating, tv_show_credit_user_review_description, tv_show_credit_user_review_date) VALUES (%s, %s, %s, %s, %s)"
        results = runQuery(query=query, query_params=(user_id, tv_show_credit_id, rating, description, date))
        if results:
            if results[0] == 'error':
                return render_template("error.j2", err=results[1])
        return redirect('/TV_Show_Credit_User_Reviews')


# user_id, tv_show_credit_id, tv_show_credit_user_review_performer_rating, tv_show_credit_user_review_description, tv_show_credit_user_review_date
# movie_credit_user_review_id, user_id, movie_credit_id, movie_credit_user_review_performer_rating, movie_credit_user_review_description, movie_credit_user_review_date
@app.route('/updateTVShowCreditUserReview/<id>', methods=('GET', 'POST'))
def updateTVShowCreditUserReview(id):
    tv_show_credit_user_review = getEntityInstance("TV_Show_Credit_User_Reviews", id)
    Users = getEntity("Users")
    TV_Show_Credits_and_Performers_and_TV_Shows = runQuery("SELECT TV_Show_Credits.tv_show_credit_id, Performers.performer_first_name, Performers.performer_last_name, TV_Shows.tv_show_title, TV_Shows.tv_show_season, TV_Shows.tv_show_episode, TV_Shows.tv_show_episode_part FROM TV_Show_Credits \
                                JOIN Performers ON TV_Show_Credits.performer_id = Performers.performer_id \
                                JOIN TV_Shows on TV_Show_Credits.tv_show_id = TV_Shows.tv_show_id \
                                ORDER BY TV_Show_Credits.tv_show_credit_id")
    
    if TV_Show_Credits_and_Performers_and_TV_Shows:
        if TV_Show_Credits_and_Performers_and_TV_Shows[0] == 'error':
            return render_template("error.j2", err=TV_Show_Credits_and_Performers_and_TV_Shows[1])

    if request.method == 'POST':
        user_id = request.form['user_id']
        tv_show_credit_id = request.form['tv_show_credit_id']
        rating = request.form['tv_show_credit_user_review_performer_rating']
        description = request.form['tv_show_credit_user_review_description']
        date = request.form['tv_show_credit_user_review_date']
        query = "UPDATE TV_Show_Credit_User_Reviews SET user_id=%s, tv_show_credit_id=%s, tv_show_credit_user_review_performer_rating=%s, tv_show_credit_user_review_description=%s, tv_show_credit_user_review_date=%s WHERE tv_show_credit_user_review_id = " + str(id)
        results = runQuery(query=query, query_params=(user_id, tv_show_credit_id, rating, description, date))
        if results:
            if results[0] == 'error':
                return render_template("error.j2", err=results[1])
        return redirect('/TV_Show_Credit_User_Reviews')
    return render_template("updateTVShowCreditUserReview.j2", tv_show_credit_user_review = tv_show_credit_user_review, Users=Users, TV_Show_Credits_and_Performers_and_TV_Shows=TV_Show_Credits_and_Performers_and_TV_Shows)


@app.route('/deleteTVShowCreditUserReview/<int:id>', methods=('GET', 'POST'))
def deleteTVShowCreditUserReview(id):
    query = "DELETE FROM TV_Show_Credit_User_Reviews WHERE tv_show_credit_user_review_id = " + str(id)
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])
    return redirect('/TV_Show_Credit_User_Reviews')


@app.route('/Users')
def Users():
    query = "SELECT * FROM Users;"
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])
    return render_template("Users.j2", Users=results)


@app.route('/searchUsers', methods=('GET', 'POST'))
def searchUsers():
    query = "SELECT * FROM Users;"

    # Set search query string
    name = request.args.get('user_name')

    # Set query to return rows specified by search term, else set the query to return all rows
    if name:
        query = f'SELECT * FROM Users WHERE user_first_name LIKE "%%{name}%%" OR user_last_name LIKE "%%{name}%%" ORDER BY user_last_name;'

    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])
    if not results:
        return render_template("Users.j2", Movies=results, searchMessage=searchMessage)
    return render_template("Users.j2", Users=results)


@app.route('/createUser',  methods = ('GET', 'POST'))
def createUser():
    if request.method == 'POST':
        first_name = request.form['user_first_name'].lower()
        first_name = first_name.capitalize()
        last_name = request.form['user_last_name'].lower()
        last_name = last_name.capitalize()
        dob = request.form['user_dob']
        email = request.form['user_email']
        ethnicity = request.form['user_ethnicity']
        gender = request.form['user_gender']
        login_id = request.form['user_login_id']
        password = request.form['user_password']

        
        query = "INSERT INTO Users (user_first_name, user_last_name, user_dob, user_email, user_ethnicity, user_gender, user_login_id, user_password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        results = runQuery(query=query, query_params=(first_name, last_name, dob, email, ethnicity, gender, login_id, password))
        if results:
            if results[0] == 'error':
                return render_template("error.j2", err=results[1])
        return redirect('/Users')
    # return render_template("/Performers")


@app.route('/deleteUser/<int:id>', methods=('GET', 'POST'))
def deleteUser(id):
    # print("DELETE FROM Performers WHERE performer_id=" + str(id))
    query = "DELETE FROM Users WHERE user_id = " + str(id)
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])

    query = "DELETE FROM Movie_Credit_User_Reviews WHERE user_id is NULL"
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])

    query = "DELETE FROM TV_Show_Credit_User_Reviews WHERE user_id is NULL"
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])

    return redirect('/Users')


@app.route('/updateUser/<id>', methods=('GET', 'POST'))
def updateUser(id):
    user = getEntityInstance("Users", id)
    if request.method == 'POST':
        first_name = request.form['user_first_name'].lower()
        first_name = first_name.capitalize()
        last_name = request.form['user_last_name'].lower()
        last_name = last_name.capitalize()
        dob = request.form['user_dob']
        email = request.form['user_email']
        ethnicity = request.form['user_ethnicity']
        gender = request.form['user_gender']
        login_id = request.form['user_login_id']
        password = request.form['user_password']

        query = "UPDATE Users SET user_first_name=%s, user_last_name=%s, user_dob=%s, user_email=%s, user_ethnicity=%s, user_gender=%s, user_login_id=%s, user_password=%s WHERE user_id=" + str(id)
        results = runQuery(query=query, query_params=(first_name, last_name, dob, email, ethnicity, gender, login_id, password))
        if results:
            if results[0] == 'error':
                return render_template("error.j2", err=results[1])
        return redirect('/Users')
    return render_template("updateUser.j2", user=user)


@app.route('/TV_Shows')
def TV_Shows():
    query = "SELECT * FROM TV_Shows;"
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])
    return render_template("TV_Shows.j2", TV_Shows=results)


@app.route('/searchTV_Shows', methods=('GET', 'POST'))
def searchTV_Shows():
    query = "SELECT * FROM TV_Shows ORDER BY tv_show_title;"

    # Set search query string
    title = request.args.get('tv_show_title')
    columns = 'TV_Show_Credits.tv_show_credit_id, TV_Show_Credits.performer_id, TV_Show_Credits.tv_show_id, TV_Show_Credits.tv_show_credit_payment, TV_Show_Credits.tv_show_credit_role, TV_Show_Credits.tv_show_credit_leading_role, TV_Show_Credits.tv_show_credit_emmy'
    if title:
        query = f'SELECT {columns} FROM TV_Shows WHERE tv_show_title LIKE "%%{title}%%" ORDER BY tv_show_title;'

    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])
    if not results:
        return render_template("TV_Shows.j2", Movies=results, searchMessage=searchMessage)
    return render_template("TV_Shows.j2", TV_Shows=results)


@app.route('/createTV_Show',  methods = ('GET', 'POST'))
def createTV_Show():
    if request.method == 'POST':
        title = request.form['tv_show_title']
        release_date = request.form['tv_show_release_date']
        season = request.form['tv_show_season']
        episode = request.form['tv_show_episode']
        runtime = request.form['tv_show_runtime']
        episode_part = request.form['tv_show_episode_part']
        budget = request.form['tv_show_budget']
        director_first_name = request.form['tv_show_director_first_name'].lower()
        director_first_name = director_first_name.capitalize()
        director_last_name = request.form['tv_show_director_last_name'].lower()
        director_last_name = director_last_name.capitalize()
        rating_tomatoes_audience = request.form['tv_show_rating_tomatoes_audience']
        rating_tomatoes_critic = request.form['tv_show_rating_tomatoes_critic']
        rating_imdb_audience = request.form['tv_show_rating_imdb_audience']
        rating_imdb_critic = request.form['tv_show_rating_imdb_critic']
        rating_meta_audience = request.form['tv_show_rating_meta_audience']
        rating_meta_critic = request.form['tv_show_rating_meta_critic']
        print("hello")
        
        query = "INSERT INTO TV_Shows (tv_show_title, tv_show_release_date, tv_show_season, tv_show_episode, tv_show_runtime, tv_show_episode_part, tv_show_budget, tv_show_director_first_name, tv_show_director_last_name, tv_show_rating_tomatoes_audience, tv_show_rating_tomatoes_critic, tv_show_rating_imdb_audience, tv_show_rating_imdb_critic, tv_show_rating_meta_audience, tv_show_rating_meta_critic) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        results = runQuery(query=query, query_params=(title, release_date, season, episode, runtime, episode_part, budget, director_first_name, director_last_name, rating_tomatoes_audience, rating_tomatoes_critic, rating_imdb_audience, rating_imdb_critic, rating_meta_audience, rating_meta_critic))
        if results:
            if results[0] == 'error':
                return render_template("error.j2", err=results[1])
        return redirect('/TV_Shows')
    # return render_template("/Performers")


@app.route('/deleteTV_Show/<int:id>', methods=('GET', 'POST'))
def deleteTV_Show(id):
    print("DELETE FROM TV_Shows WHERE tv_show_id=" + str(id))
    query = "DELETE FROM TV_Shows WHERE tv_show_id = " + str(id)
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])

    query = "DELETE FROM TV_Show_Credits WHERE tv_show_id is NULL"
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])

    query = "DELETE FROM TV_Show_Credit_User_Reviews WHERE tv_show_credit_id is NULL"
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])

    return redirect('/TV_Shows')


@app.route('/updateTV_Show/<id>', methods=('GET', 'POST'))
def updateTV_Show(id):
    tv_show = getEntityInstance("TV_Shows", id)
    if request.method == 'POST':
        title = request.form['tv_show_title']
        release_date = request.form['tv_show_release_date']
        season = request.form['tv_show_season']
        episode = request.form['tv_show_episode']
        runtime = request.form['tv_show_runtime']
        episode_part = request.form['tv_show_episode_part']
        budget = request.form['tv_show_budget']
        director_first_name = request.form['tv_show_director_first_name'].lower()
        director_first_name = director_first_name.capitalize()
        director_last_name = request.form['tv_show_director_last_name'].lower()
        director_last_name = director_last_name.capitalize()
        rating_tomatoes_audience = request.form['tv_show_rating_tomatoes_audience']
        rating_tomatoes_critic = request.form['tv_show_rating_tomatoes_critic']
        rating_imdb_audience = request.form['tv_show_rating_imdb_audience']
        rating_imdb_critic = request.form['tv_show_rating_imdb_critic']
        rating_meta_audience = request.form['tv_show_rating_meta_audience']
        rating_meta_critic = request.form['tv_show_rating_meta_critic']
        
        query = "UPDATE TV_Shows SET tv_show_title=%s, tv_show_release_date=%s, tv_show_season=%s, tv_show_episode=%s, tv_show_runtime=%s, tv_show_episode_part=%s, tv_show_budget=%s, tv_show_director_first_name=%s, tv_show_director_last_name=%s, tv_show_rating_tomatoes_audience=%s, tv_show_rating_tomatoes_critic=%s, tv_show_rating_imdb_audience=%s, tv_show_rating_imdb_critic=%s, tv_show_rating_meta_audience=%s, tv_show_rating_meta_critic=%s WHERE tv_show_id=" + str(id)
        results = runQuery(query=query, query_params=(title, release_date, season, episode, runtime, episode_part, budget, director_first_name, director_last_name, rating_tomatoes_audience, rating_tomatoes_critic, rating_imdb_audience, rating_imdb_critic, rating_meta_audience, rating_meta_critic))
        if results:
            if results[0] == 'error':
                return render_template("error.j2", err=results[1])
        return redirect('/TV_Shows')
    return render_template("updateTV_Show.j2", tv_show=tv_show)


##################################################### TV_Show_Credits Routes ###########################################################################


@app.route('/TV_Show_Credits')
def TV_Show_Credits():
    Performers = getEntity("Performers")
    TV_Shows = getEntity("TV_Shows")
    query = "SELECT * FROM TV_Show_Credits;"
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])
    return render_template("TV_Show_Credits.j2", TV_Show_Credits=results, Performers=Performers, TV_Shows=TV_Shows)


@app.route('/searchTV_Show_Credits', methods=('GET', 'POST'))
def searchTV_Show_Credits():
    query = "SELECT * FROM TV_Show_Credits;"

    # Set search query string
    last_name = request.args.get('performer_last_name')

    if last_name:
        # query = f'SELECT * FROM Movies WHERE movie_title LIKE "%%{title}%%" ORDER BY movie_title;'

        query = f'SELECT * FROM TV_Show_Credits \
                JOIN Performers ON TV_Show_Credits.performer_id = Performers.performer_id \
                WHERE Performers.performer_last_name LIKE "%%{last_name}%%";'

    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])
    if not results:
        return render_template("TV_Show_Credits.j2", Movies=results, searchMessage=searchMessage)
    return render_template("TV_Show_Credits.j2", TV_Show_Credits=results)


@app.route('/createTV_Show_Credit',  methods = ('GET', 'POST'))
def createTV_Show_Credit():
    if request.method == 'POST':
        performer_id = request.form['performer_id']
        tv_show_id = request.form['tv_show_id']
        payment = request.form['tv_show_credit_payment']
        role = request.form['tv_show_credit_role']
        leading_role = request.form['tv_show_credit_leading_role']
        emmy = request.form['tv_show_credit_emmy']
        
        print("hello")
        
        query = "INSERT INTO TV_Show_Credits (performer_id, tv_show_id, tv_show_credit_payment, tv_show_credit_role, tv_show_credit_leading_role, tv_show_credit_emmy) VALUES (%s, %s, %s, %s, %s, %s)"
        results = runQuery(query=query, query_params=(performer_id, tv_show_id, payment, role, leading_role, emmy))
        if results:
            if results[0] == 'error':
                return render_template("error.j2", err=results[1])
        return redirect('/TV_Show_Credits')
    # return render_template("/Performers")


@app.route('/deleteTV_Show_Credit/<int:id>', methods=('GET', 'POST'))
def deleteTV_Show_Credit(id):
    print("DELETE FROM TV_Show_Credits WHERE tv_show_credit_id=" + str(id))
    query = "DELETE FROM TV_Show_Credits WHERE tv_show_credit_id = " + str(id)
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])

    query = "DELETE FROM TV_Show_Credit_User_Reviews WHERE tv_show_credit_id is NULL"
    results = runQuery(query=query)
    if results:
        if results[0] == 'error':
            return render_template("error.j2", err=results[1])

    return redirect('/TV_Show_Credits')


@app.route('/updateTV_Show_Credit/<id>', methods=('GET', 'POST'))
def updateTV_Show_Credit(id):
    tv_show_credit = getEntityInstance("TV_Show_Credits", id)
    Performers = getEntity("Performers")
    TV_Shows = getEntity("TV_Shows")
    if request.method == 'POST':
        performer_id = request.form['performer_id']
        tv_show_id = request.form['tv_show_id']
        payment = request.form['tv_show_credit_payment']
        role = request.form['tv_show_credit_role']
        leading_role = request.form['tv_show_credit_leading_role']
        emmy = request.form['tv_show_credit_emmy']
        
        query = "UPDATE TV_Show_Credits SET performer_id=%s, tv_show_id=%s, tv_show_credit_payment=%s, tv_show_credit_role=%s, tv_show_credit_leading_role=%s, tv_show_credit_emmy=%s WHERE tv_show_credit_id=" + str(id)
        results = runQuery(query=query, query_params=(performer_id, tv_show_id, payment, role, leading_role, emmy))
        if results:
            if results[0] == 'error':
                return render_template("error.j2", err=results[1])
        return redirect('/TV_Show_Credits')
    return render_template("updateTV_Show_Credit.j2", tv_show_credit=tv_show_credit, Performers=Performers, TV_Shows=TV_Shows)


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8511))
    app.run(port=port, debug=True)

