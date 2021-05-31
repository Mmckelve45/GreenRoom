DROP TABLE IF EXISTS `Performers`;

CREATE TABLE `Performers` (
    `performer_id` int(11) NOT NULL AUTO_INCREMENT,
    `performer_first_name` varchar(255) NOT NULL,
    `performer_last_name` varchar(255) NOT NULL,
    `performer_city` varchar(255),
    `performer_state` varchar(255), 
    `performer_height_in` int(5), 
    `performer_hair_color` varchar(255), 
    `performer_eye_color` varchar(255), 
    `performer_weight_lbs` decimal(5,2),
    `performer_rating` decimal(3,2) NOT NULL,
    `performer_dob` date NOT NULL,
    `performer_gender` varchar(255) NOT NULL,
    `performer_ethnicity` varchar(255) NOT NULL,
    PRIMARY KEY (`performer_id`)
) ENGINE=INNODB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `Users`;

CREATE TABLE `Users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_first_name` varchar(255) NOT NULL,
  `user_last_name` varchar(255) NOT NULL,
  `user_dob` date NOT NULL,
  `user_email` varchar(255) NOT NULL,
  `user_ethnicity` varchar(255),         		# did not add NOT NULL here on purpose
  `user_gender` varchar(255),         			# did not add NOT NULL here on purpose
  `user_login_id` varchar(255) NOT NULL,         
  `user_password` varchar(255) NOT NULL,         
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_login_id` (`user_login_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `TV_Shows`;

CREATE TABLE `TV_Shows` (
    `tv_show_id` int(11) NOT NULL AUTO_INCREMENT,
    `tv_show_title` varchar(255) NOT NULL,
    `tv_show_release_date` date NOT NULL,
    `tv_show_season` int(11) NOT NULL,
    `tv_show_episode` int(11) NOT NULL,
    `tv_show_runtime` int(11) NOT NULL,
    `tv_show_episode_part` int(11) NOT NULL,
    `tv_show_budget` decimal(11,2) NOT NULL,
    `tv_show_director_first_name` varchar(255) NOT NULL,
    `tv_show_director_last_name` varchar(255) NOT NULL,
    `tv_show_rating_tomatoes_audience` decimal(3,2) NOT NULL,
    `tv_show_rating_tomatoes_critic` decimal(3,2) NOT NULL,
    `tv_show_rating_imdb_audience` decimal(3,2) NOT NULL,
    `tv_show_rating_imdb_critic` decimal(3,2) NOT NULL,
    `tv_show_rating_meta_audience` decimal(3,2) NOT NULL,
    `tv_show_rating_meta_critic` decimal(3,2) NOT NULL,
    PRIMARY KEY (`tv_show_id`)
) ENGINE=INNODB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `Movies`;

CREATE TABLE `Movies` (
  `movie_id` int(11) NOT NULL AUTO_INCREMENT,
  `movie_title` varchar(255) NOT NULL,
  `movie_release_date` date NOT NULL,
  `movie_runtime` int(11) NOT NULL,
  `movie_budget` decimal(11,2) NOT NULL,
  `movie_director_first_name` varchar(255) NOT NULL,
  `movie_director_last_name` varchar(255) NOT NULL,
  `movie_rating_tomatoes_critic` decimal(3, 2) NOT NULL,         		
  `movie_rating_tomatoes_audience` decimal(3, 2) NOT NULL,          
  `movie_rating_imdb_critic` decimal(3, 2) NOT NULL,               
  `movie_rating_imdb_audience` decimal(3, 2) NOT NULL,             
  `movie_rating_meta_critic` decimal(3, 2) NOT NULL,               
  `movie_rating_meta_audience` decimal(3, 2) NOT NULL,                        
  PRIMARY KEY (`movie_id`),
  UNIQUE KEY `movie_title` (`movie_title`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `Movie_Credits`;

CREATE TABLE `Movie_Credits` (
  `movie_credit_id` int(11) NOT NULL AUTO_INCREMENT,
  `performer_id` int(11),                                         # did not add NOT NULL here on purpose
  `movie_id` int(11),                                             # did not add NOT NULL here on purpose
  `movie_credit_payment` decimal(10, 2) NOT NULL,
  `movie_credit_role` varchar(255) NOT NULL,
  `movie_credit_lead_role` tinyint(1) NOT NULL,
  `movie_credit_oscar` tinyint(1) NOT NULL,                        
  PRIMARY KEY (`movie_credit_id`),
  CONSTRAINT `movie_credits_ibfk_1` FOREIGN KEY (`performer_id`) REFERENCES `Performers` (`performer_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `movie_credits_ibfk_2` FOREIGN KEY (`movie_id`) REFERENCES `Movies` (`movie_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `TV_Show_Credits`;

CREATE TABLE `TV_Show_Credits` (
    `tv_show_credit_id` int(11) NOT NULL AUTO_INCREMENT,
    `performer_id` int(11),                                                # did not add NOT NULL here on purpose
    `tv_show_id` int(11),                                                  # did not add NOT NULL here on purpose
    `tv_show_credit_payment` decimal(11,2) NOT NULL,
    `tv_show_credit_role` varchar(255) NOT NULL,
    `tv_show_credit_leading_role` tinyint(1) NOT NULL,
    `tv_show_credit_emmy` tinyint(1) NOT NULL,
    PRIMARY KEY (`tv_show_credit_id`),
    CONSTRAINT `tv_show_credit_ibfk_1` FOREIGN KEY (`performer_id`) REFERENCES `Performers` (`performer_id`) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT `tv_show_credit_ibfk_2` FOREIGN KEY (`tv_show_id`) REFERENCES `TV_Shows` (`tv_show_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=INNODB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `Movie_Credit_User_Reviews`;

CREATE TABLE `Movie_Credit_User_Reviews` (
  `movie_credit_user_review_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11),                                                  # did not add NOT NULL here on purpose
  `movie_credit_id` int(11),                                          # did not add NOT NULL here on purpose
  `movie_credit_user_review_performer_rating` decimal(3, 2) NOT NULL,
  `movie_credit_user_review_description` varchar(255) NOT NULL,
  `movie_credit_user_review_date` date NOT NULL,             
  PRIMARY KEY (`movie_credit_user_review_id`),
  CONSTRAINT `movie_credit_user_review_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `Users` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `movie_credit_user_review_ibfk_2` FOREIGN KEY (`movie_credit_id`) REFERENCES `Movie_Credits` (`movie_credit_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `TV_Show_Credit_User_Reviews`;

CREATE TABLE `TV_Show_Credit_User_Reviews` (
    `tv_show_credit_user_review_id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11),                                                          # did not add NOT NULL here on purpose
    `tv_show_credit_id` int(11),                                                # did not add NOT NULL here on purpose
    `tv_show_credit_user_review_performer_rating` decimal(3,2) NOT NULL,
    `tv_show_credit_user_review_description` varchar(255) NOT NULL,
    `tv_show_credit_user_review_date` datetime NOT NULL,
    PRIMARY KEY (`tv_show_credit_user_review_id`),
    CONSTRAINT `tv_show_credit_user_review_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `Users` (`user_id`) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT `tv_show_credit_user_review_ibfk_2` FOREIGN KEY (`tv_show_credit_id`) REFERENCES `TV_Show_Credits` (`tv_show_credit_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=INNODB DEFAULT CHARSET=latin1;




# Dummy data for performers
INSERT INTO Performers (`performer_first_name`, `performer_last_name`, `performer_city`, `performer_state`, `performer_height_in`, `performer_hair_color`, `performer_eye_color`, `performer_weight_lbs`, `performer_rating`, `performer_dob`, `performer_gender`, `performer_ethnicity`) 
			VALUES ('Angelina', 'Jolie', "LA", "California", 60, "Brown", "Brown", 130.5, 0.88, '1975-10-02', 'Female', 'Caucasian');

INSERT INTO Performers (`performer_first_name`, `performer_last_name`, `performer_city`, `performer_state`, `performer_height_in`, `performer_hair_color`, `performer_eye_color`, `performer_weight_lbs`, `performer_rating`, `performer_dob`, `performer_gender`, `performer_ethnicity`) 
			VALUES ('Denzel', 'Washington', "LA", "California", 70, "Brown", "Brown", 220, 0.93, '1972-02-15', 'Male', 'African-American');

INSERT INTO Performers (`performer_first_name`, `performer_last_name`, `performer_city`, `performer_state`, `performer_height_in`, `performer_hair_color`, `performer_eye_color`, `performer_weight_lbs`, `performer_rating`, `performer_dob`, `performer_gender`, `performer_ethnicity`)
			VALUES ('Mario', 'Lopez', "LA", "California", 65, "Brown", "Brown", 200, 0.73, '1982-04-24', 'Male', 'Mexican');


# Dummy data for Users
INSERT INTO Users (`user_first_name`, `user_last_name`, `user_dob`, `user_email`, `user_ethnicity`, `user_gender`, `user_login_id`, `user_password`) 
			VALUES ("Matthew", "McKelvey", '1990-04-12', 'matt@gmail.com', 'Caucasian', 'Male', 'mattymatt', 'BillyBobGoat2');

INSERT INTO Users (`user_first_name`, `user_last_name`, `user_dob`, `user_email`, `user_ethnicity`, `user_gender`, `user_login_id`, `user_password`) 
			VALUES ("Tammy", "Kraber", '1940-01-02', 'Tammy@gmail.com', 'Pacific-Islander', 'Female', 'TamTam', 'timToTheTamTimThisTime');

INSERT INTO Users (`user_first_name`, `user_last_name`, `user_dob`, `user_email`, `user_ethnicity`, `user_gender`, `user_login_id`, `user_password`) 
			VALUES ("Sam", "Salami", '2005-12-16', 'SamSalami@yahoo.com', NULL, 'Male', 'SammySalami', 'Password123');


#Movies Insert Dummy data
INSERT INTO Movies (`movie_title`, `movie_release_date`, `movie_runtime`, `movie_budget`, `movie_director_first_name`, `movie_director_last_name`, `movie_rating_tomatoes_critic`, 
					`movie_rating_tomatoes_audience`, `movie_rating_imdb_critic`, `movie_rating_imdb_audience`, `movie_rating_meta_critic`, `movie_rating_meta_audience`) 
			VALUES ("Bourne Identity", "2000-11-15", 115, 50000000, 'Tom', 'Brady', 0.75, 0.90, 0.67, 0.65, 0.56, 0.99);

INSERT INTO Movies (`movie_title`, `movie_release_date`, `movie_runtime`, `movie_budget`, `movie_director_first_name`, `movie_director_last_name`, `movie_rating_tomatoes_critic`, 
					`movie_rating_tomatoes_audience`, `movie_rating_imdb_critic`, `movie_rating_imdb_audience`, `movie_rating_meta_critic`, `movie_rating_meta_audience`) 
			VALUES ("Pride and Joy", "1996-02-22", 122, 5000000, 'Sarah', 'Jones', 0.66, 0.98, 0.36, 0.42, 0.62, 0.56);

INSERT INTO Movies (`movie_title`, `movie_release_date`, `movie_runtime`, `movie_budget`, `movie_director_first_name`, `movie_director_last_name`, `movie_rating_tomatoes_critic`, 
					`movie_rating_tomatoes_audience`, `movie_rating_imdb_critic`, `movie_rating_imdb_audience`, `movie_rating_meta_critic`, `movie_rating_meta_audience`) 
			VALUES ("Iron Man", "2006-05-01", 145, 100000000, 'Mark', 'Mahem', 0.90, 0.93, 0.86, 0.92, 0.88, 1.00);


#TV_Shows Insert Dummy Data
INSERT INTO TV_Shows (`tv_show_title`, `tv_show_release_date`, `tv_show_season`, `tv_show_episode`, `tv_show_runtime`, `tv_show_episode_part`, 
					  `tv_show_budget`, `tv_show_director_first_name`, `tv_show_director_last_name`, `tv_show_rating_tomatoes_critic`, `tv_show_rating_tomatoes_audience`, `tv_show_rating_imdb_critic`, 
					  `tv_show_rating_imdb_audience`, `tv_show_rating_meta_critic`, `tv_show_rating_meta_audience`) 
			VALUES ("The Best Show", '2001-02-22', 1, 24, 90, 1, 3000456220.45, "Steven", "Spielberg", 0.44, 0.75, 0.12, 0.70, 0.45, 0.98);

INSERT INTO TV_Shows (`tv_show_title`, `tv_show_release_date`, `tv_show_season`, `tv_show_episode`, `tv_show_runtime`, `tv_show_episode_part`, 
					  `tv_show_budget`, `tv_show_director_first_name`, `tv_show_director_last_name`, `tv_show_rating_tomatoes_critic`, `tv_show_rating_tomatoes_audience`, `tv_show_rating_imdb_critic`, 
					  `tv_show_rating_imdb_audience`, `tv_show_rating_meta_critic`, `tv_show_rating_meta_audience`) 
			VALUES ("Your Mom's Favorite", '1980-04-22', 4, 12, 120, 4, 995856220.45, "Mike", "Mossy", 0.44, 0.75, 0.12, 0.70, 0.45, 0.98);

INSERT INTO TV_Shows (`tv_show_title`, `tv_show_release_date`, `tv_show_season`, `tv_show_episode`, `tv_show_runtime`, `tv_show_episode_part`, 
					  `tv_show_budget`, `tv_show_director_first_name`, `tv_show_director_last_name`, `tv_show_rating_tomatoes_critic`, `tv_show_rating_tomatoes_audience`, `tv_show_rating_imdb_critic`, 
					  `tv_show_rating_imdb_audience`, `tv_show_rating_meta_critic`, `tv_show_rating_meta_audience`) 
			VALUES ("Why Am I Here?", '2021-12-22', 5, 2, 60, 3, 300048890, "Bellow", "Masterdon", 0.60, 0.95, 0.34, 0.73, 0.15, 0.92);


#Movie_Credits Dummy data insert
INSERT INTO Movie_Credits (`performer_id`, `movie_id`,`movie_credit_payment`, `movie_credit_role`, `movie_credit_lead_role`, `movie_credit_oscar`) 
			VALUES (1, 1, 500000, "Assasin", 1, 1);


INSERT INTO Movie_Credits (`performer_id`, `movie_id`,`movie_credit_payment`, `movie_credit_role`, `movie_credit_lead_role`, `movie_credit_oscar`) 
			VALUES (2, 3, 25000, "Daughter", 0, 1);

INSERT INTO Movie_Credits (`performer_id`, `movie_id`,`movie_credit_payment`, `movie_credit_role`, `movie_credit_lead_role`, `movie_credit_oscar`) 
			VALUES (3, 2, 60000, "Army General", 0, 0);

#TV_Show_Credits Dummy data inserts
INSERT INTO TV_Show_Credits (`performer_id`, `tv_show_id`, `tv_show_credit_payment`, `tv_show_credit_role`, `tv_show_credit_leading_role`, `tv_show_credit_emmy`) 
            VALUES (3, 2, 20000, "Blind Nun", 1, 1);

INSERT INTO TV_Show_Credits (`performer_id`, `tv_show_id`,`tv_show_credit_payment`, `tv_show_credit_role`, `tv_show_credit_leading_role`, `tv_show_credit_emmy`) 
            VALUES (1, 3, 45000, "Tom cat", 0, 1);

INSERT INTO TV_Show_Credits (`performer_id`, `tv_show_id`,`tv_show_credit_payment`, `tv_show_credit_role`, `tv_show_credit_leading_role`, `tv_show_credit_emmy`) 
            VALUES (2, 1, 100000, "Cloaked Man", 0, 0);


#Insert into Movie_Credit_User_Reviews dummy data
INSERT INTO Movie_Credit_User_Reviews (`user_id`,`movie_credit_id`, `movie_credit_user_review_performer_rating`, `movie_credit_user_review_description`, `movie_credit_user_review_date`) 
			VALUES (3, 1, 0.89, "Plays a role as action packed as Keanu Reaves in John Wick", '2020-02-15 10:52:01');

INSERT INTO Movie_Credit_User_Reviews (`user_id`,`movie_credit_id`, `movie_credit_user_review_performer_rating`, `movie_credit_user_review_description`, `movie_credit_user_review_date`) 
			VALUES (2, 2, 0.68, "Is she actually human?!?", '2018-05-30 08:12:41');

INSERT INTO Movie_Credit_User_Reviews (`user_id`,`movie_credit_id`, `movie_credit_user_review_performer_rating`, `movie_credit_user_review_description`, `movie_credit_user_review_date`) 
			VALUES (1, 3, 0.21, "This guy cannot even keep a straight face in serious scenes.  He is horrible!", '2014-10-05 22:14:43');



#Insert TV_Show_Credit_User_Reviews dummy data
INSERT INTO TV_Show_Credit_User_Reviews (`user_id`,`tv_show_credit_id`,`tv_show_credit_user_review_performer_rating`, `tv_show_credit_user_review_description`, `tv_show_credit_user_review_date`) 
			VALUES (3, 1, 0.89, "This tv show has changed my life!", '2002-09-20 4:43:02');

INSERT INTO TV_Show_Credit_User_Reviews (`user_id`,`tv_show_credit_id`,`tv_show_credit_user_review_performer_rating`, `tv_show_credit_user_review_description`, `tv_show_credit_user_review_date`) 
			VALUES (2, 2, 0.34, "This tv show has changed my life! FOR THE WORSE!", '22010-12-20 22:23:02');

INSERT INTO TV_Show_Credit_User_Reviews (`user_id`,`tv_show_credit_id`,`tv_show_credit_user_review_performer_rating`, `tv_show_credit_user_review_description`, `tv_show_credit_user_review_date`) 
			VALUES (1, 3, 1.00, "This TV show was so scary it literally killed me, it's my ghost writing this.", '2016-10-31 18:29:52');