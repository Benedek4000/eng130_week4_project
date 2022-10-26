/*
by Benedek Kovacs
*/

CREATE TABLE Users(
	user_id INT GENERATED ALWAYS AS IDENTITY,
	password VARCHAR(60) NOT NULL,
	first_name VARCHAR(20) NOT NULL,
	last_name VARCHAR(20) NOT NULL,
	email VARCHAR(40) NOT NULL,
	is_admin BOOLEAN NOT NULL DEFAULT FALSE,
	PRIMARY KEY (user_id)
);

CREATE TABLE Sessions(
	session_id INT GENERATED ALWAYS AS IDENTITY,
	user_id INT,
	posting_date DATE NOT NULL DEFAULT CURRENT_DATE,
	posting_time TIME NOT NULL DEFAULT CURRENT_TIME,
	location VARCHAR(50) NOT NULL,
	PRIMARY KEY (session_id),
	CONSTRAINT fk_user
		FOREIGN KEY (user_id)
			REFERENCES Users(user_id)
);