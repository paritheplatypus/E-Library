CREATE DATABASE E_LIBRARY;
USE E_LIBRARY;

CREATE TABLE LOAN(
	User_ID			INT				NOT NULL,
	Book_ID			INT				NOT NULL,
	Date_of_issue	VARCHAR(20)		NOT NULL,
	Due_date		VARCHAR(20)		NOT NULL,
	In_time			VARCHAR(3)		NOT NULL,
	Late			VARCHAR(3)		NOT NULL,
	PRIMARY KEY (User_ID, Book_ID),
    FOREIGN KEY (User_ID) REFERENCES USER(User_ID),
    FOREIGN KEY (Book_ID) REFERENCES BOOK(Book_ID)
);

CREATE TABLE BOOK(
	Book_ID				INT				NOT NULL,
	Author				VARCHAR(100)	NOT NULL,
	Title				VARCHAR(100)	NOT NULL,
	Date_of_publication	VARCHAR(20)		NOT NULL,
	Yes					VARCHAR(3),
	No					VARCHAR(2),
	PRIMARY KEY (Book_ID)
);

CREATE TABLE USER(
	User_ID				INT				NOT NULL,
	Age					INT				NOT NULL,
	First_name			VARCHAR(100)	NOT NULL,
	Last_name			VARCHAR(20),
	Email_ID			VARCHAR(3)		NOT NULL,
	Username			VARCHAR(50)		NOT NULL,
	Password			VARCHAR(100)	NOT NULL,
	PRIMARY KEY (User_ID)
);

CREATE TABLE ARTICLE(
	Article_ID			INT				NOT NULL,
	Author				INT				NOT NULL,
	Date_of_publication	VARCHAR(100)	NOT NULL,
	Number_of_citations	INT,
	Downloads			INT,
	PRIMARY KEY (Article_ID)
);

CREATE TABLE REVIEW(
	User_ID				INT				NOT NULL,
    Book_ID				INT,
    Article_ID			INT,
    Username			VARCHAR(50),
    Display_reviews		VARCHAR(100)	NOT NULL,
    Fname				VARCHAR(20)		NOT NULL,
    Lname				VARCHAR(3),
    Rating				INT				NOT NULL,
    PRIMARY KEY (User_ID, Username),
    FOREIGN KEY (Book_ID) REFERENCES BOOK(Book_ID),
    FOREIGN KEY (Article_ID) REFERENCES ARTICLE(Article_ID)
);

INSERT INTO BOOK (Book_ID, Author, Title, Date_of_publication)
VALUES
(3, 'J.R.R. Tolkien', 'The Hobbit', '1937');

SELECT * FROM BOOK; 

INSERT INTO USER (User_ID, Age, First_name, Last_name, Email_ID, Username, Password)
VALUES
(1, 25, 'John', 'Doe', 'johndoe@example.com', 'johndoe', 'password123'),
(2, 30, 'Alice', 'Smith', 'alice.smith@example.com', 'alicesmith', 'password456'),
(3, 28, 'Bob', 'Brown', 'bobbrown@example.com', 'bobbrown', 'password789');

SELECT * FROM USER;

INSERT INTO LOAN (User_ID, Book_ID, Date_of_issue, Due_date, In_time, Late)
VALUES
(1, 1, '2024-12-01', '2024-12-15', 'YES', 'NO'),
(2, 2, '2024-12-02', '2024-12-16', 'YES', 'NO'),
(3, 3, '2024-12-03', '2024-12-17', 'NO', 'YES');

SELECT * FROM LOAN;

INSERT INTO ARTICLE (Article_ID, Author, Date_of_publication, Number_of_citations, Downloads)
VALUES
(1, 1, '2023-05-10', 100, 500),
(2, 2, '2023-06-15', 150, 400),
(3, 3, '2023-07-20', 200, 350);

SELECT * FROM ARTICLE;

INSERT INTO REVIEW (User_ID, Book_ID, Username, Display_reviews, Fname, Lname, Rating)
VALUES
(1, 1, 'johndoe', 'Amazing book! Highly recommended.', 'John', 'Doe', 5),
(2, 2, 'alicesmith', 'A thought-provoking read.', 'Alice', 'Smith', 4),
(3, 3, 'bobbrown', 'A classic tale worth revisiting.', 'Bob', 'Brown', 5);

SELECT * FROM REVIEW;
