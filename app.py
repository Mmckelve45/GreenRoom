from flask import Flask, render_template, json, request, redirect, flash
import os
import database.db_connector as db
# import MySQLdb

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

# Routes 

@app.route('/')
def root():
    return render_template("index.j2")

@app.route('/Performers')
def Performers():
    query = "SELECT * FROM Performers;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("Performers.j2", Performers=results)

@app.route('/seachPerformer', methods=('GET', 'POST'))
def searchPerformer():
    if request.method == 'POST':
        
        last_name = request.form['performer_last_name']
        print(last_name)
        # query = "SELECT performer_id, performer_first_name, performer_last_name, performer_city, performer_state, performer_height_in, performer_hair_color, performer_eye_color, performer_weight_lbs, performer_rating, performer_dob, performer_gender, performer_ethnicity FROM Performers WHERE `performer_last_name` Like " + last_name + ";"
        query = "SELECT * FROM Performers WHERE performer_last_name = " + "'" + str(last_name) + "'"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("Performers.j2", Performers=results)
    # return render_template("Performerse.j2", performer=results)


@app.route('/createPerformer',  methods = ('GET', 'POST'))
def createPerformer():
    if request.method == 'POST':
        first_name = request.form['performer_first_name']
        last_name = request.form['performer_last_name']
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
        # cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(first_name, last_name, dob, gender, ethnicity))
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(first_name, last_name, city, state, height, hair_color, eye_color, weight, rating, dob, gender, ethnicity))
        # results = cursor.fetchall()
        cursor.fetchall()
        return redirect('/Performers')
    # return render_template("/Performers")

def getPerformer(id):
    # query = "SELECT employee_id, first_name, last_name, title, date_of_hire, date_of_termination, phone, email FROM Employees WHERE employee_id =" + str(id)
    query = "SELECT performer_id, performer_first_name, performer_last_name, performer_city, performer_state, performer_height_in, performer_hair_color, performer_eye_color, performer_weight_lbs, performer_rating, performer_dob, performer_gender, performer_ethnicity FROM Performers WHERE performer_id =" +str(id)
    # query = "SELECT * FROM Performers WHERE performer_id=" + str(id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    performer = cursor.fetchone()
    cursor.close()
    return performer


@app.route('/deletePerformer/<int:id>', methods=('GET', 'POST'))
def deletePerformer(id):
    print("DELETE FROM Performers WHERE performer_id=" + str(id))
    query = "DELETE FROM Performers WHERE performer_id = " + str(id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    cursor.fetchall()

    return redirect('/Performers')



@app.route('/updatePerformer/<id>', methods=('GET', 'POST'))
def updatePerformer(id):
    performer = getPerformer(id)
    if request.method == 'POST':
        first_name = request.form['performer_first_name']
        last_name = request.form['performer_last_name']
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
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(first_name, last_name, city, state, height, hair_color, eye_color, weight, rating, dob, gender, ethnicity))
        results = cursor.fetchall()
        return redirect('/Performers')
    return render_template("updatePerformer.j2", performer=performer)



@app.route('/Movies')
def Movies():
    query = "SELECT * FROM Movies;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("Movies.j2", Movies=results)

def getMovie(id):
    # query = "SELECT employee_id, first_name, last_name, title, date_of_hire, date_of_termination, phone, email FROM Employees WHERE employee_id =" + str(id)
    # query = "SELECT movie_title, movie_release_date, movie_runtime, movie_budget, movie_director_first_name, movie_director_last_name, movie_rating_tomatoes_critic, movie_rating_tomatoes_audience, movie_rating_imdb_critic, movie_rating_imdb_audience, movie_rating_meta_critic, movie_rating_meta_audience FROM Movies WHERE movie_id =" +str(id)
    query = "SELECT * FROM Movies WHERE movie_id=" + str(id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    movie = cursor.fetchone()
    cursor.close()
    return movie

@app.route('/seachMovie', methods=('GET', 'POST'))
def searchMovie():
    if request.method == 'POST':
        
        title = request.form['movie_title']
        # print(last_name)
        # query = "SELECT performer_id, performer_first_name, performer_last_name, performer_city, performer_state, performer_height_in, performer_hair_color, performer_eye_color, performer_weight_lbs, performer_rating, performer_dob, performer_gender, performer_ethnicity FROM Performers WHERE `performer_last_name` Like " + last_name + ";"
        query = "SELECT * FROM Movies WHERE movie_title = " + "'" + str(title) + "'"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        # if cursor.fetchall() not undefinedError
        return render_template("Movies.j2", Movies=results)

@app.route('/createMovie',  methods = ('GET', 'POST'))
def createMovie():
    if request.method == 'POST':
        title = request.form['movie_title']
        release_date = request.form['movie_release_date']
        runtime = request.form['movie_runtime']
        budget = request.form['movie_budget']
        director_first_name = request.form['movie_director_first_name']
        director_last_name = request.form['movie_director_last_name']
        tomatoes_critic = request.form['movie_rating_tomatoes_critic']
        tomatoes_audience = request.form['movie_rating_tomatoes_audience']
        imdb_critic = request.form['movie_rating_imdb_critic']
        imdb_audience = request.form['movie_rating_imdb_audience']
        meta_critic = request.form['movie_rating_meta_critic']
        meta_audience = request.form['movie_rating_meta_audience']
        
        query = "INSERT INTO Movies (movie_title, movie_release_date, movie_runtime, movie_budget, movie_director_first_name, movie_director_last_name, movie_rating_tomatoes_critic, movie_rating_tomatoes_audience, movie_rating_imdb_critic, movie_rating_imdb_audience, movie_rating_meta_critic, movie_rating_meta_audience) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(first_name, last_name, dob, gender, ethnicity))
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(title, release_date, runtime, budget, director_first_name, director_last_name, tomatoes_critic, tomatoes_audience, imdb_critic, imdb_audience, meta_critic, meta_audience))
        # results = cursor.fetchall()
        cursor.fetchall()
        return redirect('/Movies')

@app.route('/updateMovie/<id>', methods=('GET', 'POST'))
def updateMovie(id):
    movie = getMovie(id)
    print("hello outside POST")
    if request.method == 'POST':
        print("HELLO IN UPDATEMOVE POST ROUTE")
        title = request.form['movie_title']
        release_date = request.form['movie_release_date']
        runtime = request.form['movie_runtime']
        budget = request.form['movie_budget']
        director_first_name = request.form['movie_director_first_name']
        director_last_name = request.form['movie_director_last_name']
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
    cursor = db.execute_query(db_connection=db_connection, query=query)
    cursor.fetchall()
    return redirect('/Movies')

@app.route('/Movie_Credits')
def Movies_Credits():
    query = "SELECT * FROM Movie_Credits;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("Movie_Credits.j2", MovieCredits=results)

def getMovieCredit(id):
    # query = "SELECT employee_id, first_name, last_name, title, date_of_hire, date_of_termination, phone, email FROM Employees WHERE employee_id =" + str(id)
    # query = "SELECT movie_title, movie_release_date, movie_runtime, movie_budget, movie_director_first_name, movie_director_last_name, movie_rating_tomatoes_critic, movie_rating_tomatoes_audience, movie_rating_imdb_critic, movie_rating_imdb_audience, movie_rating_meta_critic, movie_rating_meta_audience FROM Movies WHERE movie_id =" +str(id)
    query = "SELECT * FROM Movie_Credits WHERE movie_credit_id=" + str(id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    movieCredits = cursor.fetchone()
    cursor.close()
    return movieCredits

@app.route('/seachMovieCredit', methods=('GET', 'POST'))
def searchMovieCredit():
    if request.method == 'POST':
        
        performer_id = request.form['performer_id']
        # print(last_name)
        # query = "SELECT performer_id, performer_first_name, performer_last_name, performer_city, performer_state, performer_height_in, performer_hair_color, performer_eye_color, performer_weight_lbs, performer_rating, performer_dob, performer_gender, performer_ethnicity FROM Performers WHERE `performer_last_name` Like " + last_name + ";"
        query = "SELECT * FROM Movie_Credits WHERE performer_id = " + "'" + str(performer_id) + "'"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        # if cursor.fetchall() not undefinedError
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
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(performer_id, movie_id, payment, role, lead, oscar))
        # results = cursor.fetchall()
        cursor.fetchall()
        return redirect('/Movie_Credits')

@app.route('/updateMovieCredits/<id>', methods=('GET', 'POST'))
def updateMovieCredits(id):
    movieCredit = getMovieCredit(id)
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
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(performer_id, movie_id, payment, role, lead, oscar))
        results = cursor.fetchall()
        return redirect('/Movie_Credits')
    return render_template("updateMovieCredits.j2", movieCredit = movieCredit)

@app.route('/deleteMovieCredit/<int:id>', methods=('GET', 'POST'))
def deleteMovieCredit(id):
    print("DELETE FROM Movie_Credits WHERE movie_credit_id=" + str(id))
    query = "DELETE FROM Movie_Credits WHERE movie_credit_id = " + str(id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    cursor.fetchall()
    return redirect('/Movie_Credits')

@app.route('/Movie_Credit_User_Reviews')
def Movies_Credit_User_Reviews():
    query = "SELECT * FROM Movie_Credit_User_Reviews;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("Movie_Credit_User_Reviews.j2", MovieCreditUserReviews=results)

def getMovieCreditUserReview(id):
    # query = "SELECT employee_id, first_name, last_name, title, date_of_hire, date_of_termination, phone, email FROM Employees WHERE employee_id =" + str(id)
    # query = "SELECT movie_title, movie_release_date, movie_runtime, movie_budget, movie_director_first_name, movie_director_last_name, movie_rating_tomatoes_critic, movie_rating_tomatoes_audience, movie_rating_imdb_critic, movie_rating_imdb_audience, movie_rating_meta_critic, movie_rating_meta_audience FROM Movies WHERE movie_id =" +str(id)
    query = "SELECT * FROM Movie_Credit_User_Reviews WHERE movie_credit_user_review_id=" + str(id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    movieCreditUserReviews = cursor.fetchone()
    cursor.close()
    return movieCreditUserReviews

@app.route('/searchMovieCreditUserReview', methods=('GET', 'POST'))
def searchMovieCreditUserReview():
    if request.method == 'POST':
        movie_credit_id = request.form['movie_credit_id']
        # print(last_name)
        # query = "SELECT performer_id, performer_first_name, performer_last_name, performer_city, performer_state, performer_height_in, performer_hair_color, performer_eye_color, performer_weight_lbs, performer_rating, performer_dob, performer_gender, performer_ethnicity FROM Performers WHERE `performer_last_name` Like " + last_name + ";"
        query = "SELECT * FROM Movie_Credit_User_Reviews WHERE movie_credit_id = " + "'" + str(movie_credit_id) + "'"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        # if cursor.fetchall() not undefinedError
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
        # cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(first_name, last_name, dob, gender, ethnicity))
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(user_id, movie_credit_id, rating, description, date))
        # results = cursor.fetchall()
        cursor.fetchall()
        return redirect('/Movie_Credit_User_Reviews')

# movie_credit_user_review_id, user_id, movie_credit_id, movie_credit_user_review_performer_rating, movie_credit_user_review_description, movie_credit_user_review_date
@app.route('/updateMovieCreditUserReviews/<id>', methods=('GET', 'POST'))
def updateMovieCreditUserReviews(id):
    movieCreditUserReview = getMovieCreditUserReview(id)
    if request.method == 'POST':
        user_id = request.form['user_id']
        movie_credit_id = request.form['movie_credit_id']
        rating = request.form['movie_credit_user_review_performer_rating']
        description = request.form['movie_credit_user_review_description']
        date = request.form['movie_credit_user_review_date']
        print("HERE")
        query = "UPDATE Movie_Credit_User_Reviews SET user_id=%s, movie_credit_id=%s, movie_credit_user_review_performer_rating=%s, movie_credit_user_review_description=%s, movie_credit_user_review_date=%s WHERE movie_credit_user_review_id = " + str(id)
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(user_id, movie_credit_id, rating, description, date))
        results = cursor.fetchall()
        return redirect('/Movie_Credit_User_Reviews')
    return render_template("updateMovieCreditUserReviews.j2", movieCreditUserReview = movieCreditUserReview)

@app.route('/deleteMovieCreditUserReview/<int:id>', methods=('GET', 'POST'))
def deleteMovieCreditUserReview(id):
    query = "DELETE FROM Movie_Credit_User_Reviews WHERE movie_credit_user_review_id = " + str(id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    cursor.fetchall()
    return redirect('/Movie_Credit_User_Reviews')



@app.route('/TV_Show_Credit_User_Reviews')
def TV_Show_Credit_User_Reviews():
    query = "SELECT * FROM TV_Show_Credit_User_Reviews;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("TV_Show_Credit_User_Reviews.j2", TVShowCreditUserReviews=results)

def getTVShowCreditUserReview(id):
    # query = "SELECT employee_id, first_name, last_name, title, date_of_hire, date_of_termination, phone, email FROM Employees WHERE employee_id =" + str(id)
    # query = "SELECT movie_title, movie_release_date, movie_runtime, movie_budget, movie_director_first_name, movie_director_last_name, movie_rating_tomatoes_critic, movie_rating_tomatoes_audience, movie_rating_imdb_critic, movie_rating_imdb_audience, movie_rating_meta_critic, movie_rating_meta_audience FROM Movies WHERE movie_id =" +str(id)
    query = "SELECT * FROM TV_Show_Credit_User_Reviews WHERE tv_show_credit_user_review_id=" + str(id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    TVShowCreditUserReview = cursor.fetchone()
    cursor.close()
    return TVShowCreditUserReview

@app.route('/searchTVShowCreditUserReview', methods=('GET', 'POST'))
def searchTVShowCreditUserReview():
    if request.method == 'POST':
        tv_show_credit_id = request.form['tv_show_credit_id']
        # print(last_name)
        # query = "SELECT performer_id, performer_first_name, performer_last_name, performer_city, performer_state, performer_height_in, performer_hair_color, performer_eye_color, performer_weight_lbs, performer_rating, performer_dob, performer_gender, performer_ethnicity FROM Performers WHERE `performer_last_name` Like " + last_name + ";"
        query = "SELECT * FROM TV_Show_Credit_User_Reviews WHERE tv_show_credit_id = " + "'" + str(tv_show_credit_id) + "'"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        # if cursor.fetchall() not undefinedError
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
        # cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(first_name, last_name, dob, gender, ethnicity))
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(user_id, tv_show_credit_id, rating, description, date))
        # results = cursor.fetchall()
        cursor.fetchall()
        return redirect('/TV_Show_Credit_User_Reviews')

# user_id, tv_show_credit_id, tv_show_credit_user_review_performer_rating, tv_show_credit_user_review_description, tv_show_credit_user_review_date
# movie_credit_user_review_id, user_id, movie_credit_id, movie_credit_user_review_performer_rating, movie_credit_user_review_description, movie_credit_user_review_date
@app.route('/updateTVShowCreditUserReview/<id>', methods=('GET', 'POST'))
def updateTVShowCreditUserReview(id):
    TVShowCreditUserReview = getTVShowCreditUserReview(id)
    if request.method == 'POST':
        user_id = request.form['user_id']
        tv_show_credit_id = request.form['tv_show_credit_id']
        rating = request.form['tv_show_credit_user_review_performer_rating']
        description = request.form['tv_show_credit_user_review_description']
        date = request.form['tv_show_credit_user_review_date']
        print("HERE")
        query = "UPDATE TV_Show_Credit_User_Reviews SET user_id=%s, tv_show_credit_id=%s, tv_show_credit_user_review_performer_rating=%s, tv_show_credit_user_review_description=%s, tv_show_credit_user_review_date=%s WHERE tv_show_credit_user_review_id = " + str(id)
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(user_id, tv_show_credit_id, rating, description, date))
        results = cursor.fetchall()
        return redirect('/TV_Show_Credit_User_Reviews')
    return render_template("updateTVShowCreditUserReview.j2", TVShowCreditUserReview = TVShowCreditUserReview)

@app.route('/deleteTVShowCreditUserReview/<int:id>', methods=('GET', 'POST'))
def deleteTVShowCreditUserReview(id):
    query = "DELETE FROM TV_Show_Credit_User_Reviews WHERE tv_show_credit_user_review_id = " + str(id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    cursor.fetchall()
    return redirect('/TV_Show_Credit_User_Reviews')



@app.route('/Users')
def Users():
    query = "SELECT * FROM Users;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("Users.j2", Users=results)

@app.route('/seachUsers', methods=('GET', 'POST'))
def searchUsers():
    if request.method == 'POST':
        
        last_name = request.form['user_last_name']
        # print(last_name)
        # query = "SELECT performer_id, performer_first_name, performer_last_name, performer_city, performer_state, performer_height_in, performer_hair_color, performer_eye_color, performer_weight_lbs, performer_rating, performer_dob, performer_gender, performer_ethnicity FROM Performers WHERE `performer_last_name` Like " + last_name + ";"
        query = "SELECT * FROM Users WHERE user_last_name = " + "'" + str(last_name) + "'"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("Users.j2", Users=results)
    # return render_template("Performerse.j2", performer=results)

@app.route('/createUser',  methods = ('GET', 'POST'))
def createUser():
    if request.method == 'POST':
        first_name = request.form['user_first_name']
        last_name = request.form['user_last_name']
        dob = request.form['user_dob']
        email = request.form['user_email']
        ethnicity = request.form['user_ethnicity']
        gender = request.form['user_gender']
        login_id = request.form['user_login_id']
        password = request.form['user_password']

        
        query = "INSERT INTO Users (user_first_name, user_last_name, user_dob, user_email, user_ethnicity, user_gender, user_login_id, user_password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        # cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(first_name, last_name, dob, gender, ethnicity))
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(first_name, last_name, dob, email, ethnicity, gender, login_id, password))
        # results = cursor.fetchall()
        cursor.fetchall()
        return redirect('/Users')
    # return render_template("/Performers")


def getUser(id):
    # query = "SELECT employee_id, first_name, last_name, title, date_of_hire, date_of_termination, phone, email FROM Employees WHERE employee_id =" + str(id)
    query = "SELECT user_id, user_first_name, user_last_name, user_dob, user_email, user_ethnicity, user_gender, user_login_id, user_password FROM Users WHERE user_id =" +str(id)
    # query = "SELECT * FROM Performers WHERE performer_id=" + str(id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    user = cursor.fetchone()
    cursor.close()
    return user


@app.route('/deleteUser/<int:id>', methods=('GET', 'POST'))
def deleteUser(id):
    # print("DELETE FROM Performers WHERE performer_id=" + str(id))
    query = "DELETE FROM Users WHERE user_id = " + str(id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    cursor.fetchall()
    return redirect('/Users')



@app.route('/updateUser/<id>', methods=('GET', 'POST'))
def updateUser(id):
    user = getUser(id)
    if request.method == 'POST':
        first_name = request.form['user_first_name']
        last_name = request.form['user_last_name']
        dob = request.form['user_dob']
        email = request.form['user_email']
        ethnicity = request.form['user_ethnicity']
        gender = request.form['user_gender']
        login_id = request.form['user_login_id']
        password = request.form['user_password']

        query = "UPDATE Users SET user_first_name=%s, user_last_name=%s, user_dob=%s, user_email=%s, user_ethnicity=%s, user_gender=%s, user_login_id=%s, user_password=%s WHERE user_id=" + str(id)
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(first_name, last_name, dob, email, ethnicity, gender, login_id, password))
        results = cursor.fetchall()
        return redirect('/Users')
    return render_template("updateUser.j2", user=user)


@app.route('/TV_Shows')
def TV_Shows():
    query = "SELECT * FROM TV_Shows;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("TV_Shows.j2", TV_Shows=results)

@app.route('/searchTV_Shows', methods=('GET', 'POST'))
def searchTV_Shows():
    if request.method == 'POST':
        
        title = request.form['tv_show_title']
        print(title)
        # query = "SELECT performer_id, performer_first_name, performer_last_name, performer_city, performer_state, performer_height_in, performer_hair_color, performer_eye_color, performer_weight_lbs, performer_rating, performer_dob, performer_gender, performer_ethnicity FROM Performers WHERE `performer_last_name` Like " + last_name + ";"
        query = "SELECT * FROM TV_Shows WHERE tv_show_title = " + "'" + str(title) + "'"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("TV_Shows.j2", TV_Shows=results)
    # return render_template("Performerse.j2", performer=results)


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
        director_first_name = request.form['tv_show_director_first_name'] 
        director_last_name = request.form['tv_show_director_last_name']
        rating_tomatoes_audience = request.form['tv_show_rating_tomatoes_audience']
        rating_tomatoes_critic = request.form['tv_show_rating_tomatoes_critic']
        rating_imdb_audience = request.form['tv_show_rating_imdb_audience']
        rating_imdb_critic = request.form['tv_show_rating_imdb_critic']
        rating_meta_audience = request.form['tv_show_rating_meta_audience']
        rating_meta_critic = request.form['tv_show_rating_meta_critic']
        print("hello")
        
        query = "INSERT INTO TV_Shows (tv_show_title, tv_show_release_date, tv_show_season, tv_show_episode, tv_show_runtime, tv_show_episode_part, tv_show_budget, tv_show_director_first_name, tv_show_director_last_name, tv_show_rating_tomatoes_audience, tv_show_rating_tomatoes_critic, tv_show_rating_imdb_audience, tv_show_rating_imdb_critic, tv_show_rating_meta_audience, tv_show_rating_meta_critic) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(first_name, last_name, dob, gender, ethnicity))
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(title, release_date, season, episode, runtime, episode_part, budget, director_first_name, director_last_name, rating_tomatoes_audience, rating_tomatoes_critic, rating_imdb_audience, rating_imdb_critic, rating_meta_audience, rating_meta_critic))
        # results = cursor.fetchall()
        cursor.fetchall()
        return redirect('/TV_Shows')
    # return render_template("/Performers")

def getTV_Show(id):
    # query = "SELECT employee_id, first_name, last_name, title, date_of_hire, date_of_termination, phone, email FROM Employees WHERE employee_id =" + str(id)
    query = "SELECT tv_show_id, tv_show_title, tv_show_release_date, tv_show_season, tv_show_episode, tv_show_runtime, tv_show_episode_part, tv_show_budget, tv_show_director_first_name, tv_show_director_last_name, tv_show_rating_tomatoes_audience, tv_show_rating_tomatoes_critic, tv_show_rating_imdb_audience, tv_show_rating_imdb_critic, tv_show_rating_meta_audience, tv_show_rating_meta_critic FROM TV_Shows WHERE tv_show_id =" +str(id)
    # query = "SELECT * FROM Performers WHERE performer_id=" + str(id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    tv_show = cursor.fetchone()
    cursor.close()
    return tv_show



@app.route('/deleteTV_Show/<int:id>', methods=('GET', 'POST'))
def deleteTV_Show(id):
    print("DELETE FROM TV_Shows WHERE tv_show_id=" + str(id))
    query = "DELETE FROM TV_Shows WHERE tv_show_id = " + str(id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    cursor.fetchall()

    return redirect('/TV_Shows')

@app.route('/updateTV_Show/<id>', methods=('GET', 'POST'))
def updateTV_Show(id):
    tv_show = getTV_Show(id)
    if request.method == 'POST':
        title = request.form['tv_show_title']
        release_date = request.form['tv_show_release_date']
        season = request.form['tv_show_season']
        episode = request.form['tv_show_episode']
        runtime = request.form['tv_show_runtime']
        episode_part = request.form['tv_show_episode_part']
        budget = request.form['tv_show_budget']
        director_first_name = request.form['tv_show_director_first_name']
        director_last_name = request.form['tv_show_director_last_name']
        rating_tomatoes_audience = request.form['tv_show_rating_tomatoes_audience']
        rating_tomatoes_critic = request.form['tv_show_rating_tomatoes_critic']
        rating_imdb_audience = request.form['tv_show_rating_imdb_audience']
        rating_imdb_critic = request.form['tv_show_rating_imdb_critic']
        rating_meta_audience = request.form['tv_show_rating_meta_audience']
        rating_meta_critic = request.form['tv_show_rating_meta_critic']
        
        query = "UPDATE TV_Shows SET tv_show_title=%s, tv_show_release_date=%s, tv_show_season=%s, tv_show_episode=%s, tv_show_runtime=%s, tv_show_episode_part=%s, tv_show_budget=%s, tv_show_director_first_name=%s, tv_show_director_last_name=%s, tv_show_rating_tomatoes_audience=%s, tv_show_rating_tomatoes_critic=%s, tv_show_rating_imdb_audience=%s, tv_show_rating_imdb_critic=%s, tv_show_rating_meta_audience=%s, tv_show_rating_meta_critic=%s WHERE tv_show_id=" + str(id)
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(title, release_date, season, episode, runtime, episode_part, budget, director_first_name, director_last_name, rating_tomatoes_audience, rating_tomatoes_critic, rating_imdb_audience, rating_imdb_critic, rating_meta_audience, rating_meta_critic))
        results = cursor.fetchall()
        return redirect('/TV_Shows')
    return render_template("updateTV_Show.j2", tv_show=tv_show)

##################################################### TV_Show_Credits Routes ###########################################################################

@app.route('/TV_Show_Credits')
def TV_Show_Credits():
    query = "SELECT * FROM TV_Show_Credits;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("TV_Show_Credits.j2", TV_Show_Credits=results)

@app.route('/searchTV_Show_Credits', methods=('GET', 'POST'))
def searchTV_Show_Credits():
    if request.method == 'POST':
        
        last_name = request.form['performer_last_name']
        print(last_name)
        # query = "SELECT performer_id, performer_first_name, performer_last_name, performer_city, performer_state, performer_height_in, performer_hair_color, performer_eye_color, performer_weight_lbs, performer_rating, performer_dob, performer_gender, performer_ethnicity FROM Performers WHERE `performer_last_name` Like " + last_name + ";"
        query = "SELECT * FROM TV_Show_Credits \
                JOIN Performers ON TV_Show_Credits.performer_id = Performers.performer_id \
                WHERE Performers.performer_last_name = " + "'" + str(last_name) + "'"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
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
        # cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(first_name, last_name, dob, gender, ethnicity))
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(performer_id, tv_show_id, payment, role, leading_role, emmy))
        # results = cursor.fetchall()
        cursor.fetchall()
        return redirect('/TV_Show_Credits')
    # return render_template("/Performers")

def getTV_Show_Credit(id):
    # query = "SELECT employee_id, first_name, last_name, title, date_of_hire, date_of_termination, phone, email FROM Employees WHERE employee_id =" + str(id)
    query = "SELECT tv_show_credit_id, performer_id, tv_show_id, tv_show_credit_payment, tv_show_credit_role, tv_show_credit_leading_role, tv_show_credit_emmy FROM TV_Show_Credits WHERE tv_show_credit_id =" +str(id)
    # query = "SELECT * FROM Performers WHERE performer_id=" + str(id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    tv_show_credit = cursor.fetchone()
    cursor.close()
    return tv_show_credit


@app.route('/deleteTV_Show_Credit/<int:id>', methods=('GET', 'POST'))
def deleteTV_Show_Credit(id):
    print("DELETE FROM TV_Show_Credits WHERE tv_show_credit_id=" + str(id))
    query = "DELETE FROM TV_Show_Credits WHERE tv_show_credit_id = " + str(id)
    cursor = db.execute_query(db_connection=db_connection, query=query)
    cursor.fetchall()

    return redirect('/TV_Show_Credits')

@app.route('/updateTV_Show_Credit/<id>', methods=('GET', 'POST'))
def updateTV_Show_Credit(id):
    tv_show_credit = getTV_Show_Credit(id)
    if request.method == 'POST':
        performer_id = request.form['performer_id']
        tv_show_id = request.form['tv_show_id']
        payment = request.form['tv_show_credit_payment']
        role = request.form['tv_show_credit_role']
        leading_role = request.form['tv_show_credit_leading_role']
        emmy = request.form['tv_show_credit_emmy']
        
        query = "UPDATE TV_Show_Credits SET performer_id=%s, tv_show_id=%s, tv_show_credit_payment=%s, tv_show_credit_role=%s, tv_show_credit_leading_role=%s, tv_show_credit_emmy=%s WHERE tv_show_credit_id=" + str(id)
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(performer_id, tv_show_id, payment, role, leading_role, emmy))
        results = cursor.fetchall()
        return redirect('/TV_Show_Credits')
    return render_template("updateTV_Show_Credit.j2", tv_show_credit=tv_show_credit)


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8511))
    app.run(port=port, debug=True)

