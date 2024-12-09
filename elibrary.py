import mysql.connector

# connecting my mySQL database with my Python code
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Myking3676$",
        database="E_LIBRARY" # my database's name
    )

# -----------------------------------------------------------------

def create_tables(): # creating five tables: BOOK, USER, LOAN, ARTICLE and REVIEW
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # SQL for creating tables
        queries = [
            """
            CREATE TABLE IF NOT EXISTS USER (
                User_ID     INT             NOT NULL,
                Age         INT             NOT NULL,
                First_name  VARCHAR(100)    NOT NULL,
                Last_name   VARCHAR(20),
                Email_ID    VARCHAR(100)    NOT NULL    UNIQUE,
                Username    VARCHAR(50)     NOT NULL    UNIQUE,
                Password    VARCHAR(100)    NOT NULL,
                PRIMARY KEY (User_ID)
            );
            """,

            """
            CREATE TABLE IF NOT EXISTS BOOK (
                Book_ID     INT             NOT NULL,
                Author      VARCHAR(100)    NOT NULL,
                Title       VARCHAR(100)    NOT NULL,
                Date_of_publication VARCHAR(20) NOT NULL,
                Yes         VARCHAR(3),
                No          VARCHAR(2),
                PRIMARY KEY (Book_ID)
            );
            """,

            """
            CREATE TABLE IF NOT EXISTS LOAN (
                User_ID     INT             NOT NULL,
                Book_ID     INT             NOT NULL,
                Date_of_issue VARCHAR(20)   NOT NULL,
                Due_date    VARCHAR(20)     NOT NULL,
                In_time     VARCHAR(3)      NOT NULL,
                Late        VARCHAR(3)      NOT NULL,
                PRIMARY KEY (User_ID, Book_ID),
                FOREIGN KEY (User_ID) REFERENCES USER(User_ID),
                FOREIGN KEY (Book_ID) REFERENCES BOOK(Book_ID)
            );
            """,

            """
            CREATE TABLE IF NOT EXISTS ARTICLE (
                Article_ID  INT             NOT NULL,
                Author      INT             NOT NULL,
                Date_of_publication VARCHAR(100) NOT NULL,
                Number_of_citations INT,
                Downloads   INT,
                PRIMARY KEY (Article_ID)
            );
            """,

            """
            CREATE TABLE IF NOT EXISTS REVIEW (
                User_ID          INT             NOT NULL,
                Book_ID          INT,
                Article_ID       INT,            
                Username         VARCHAR(50),
                Display_reviews  VARCHAR(100)    NOT NULL,
                Fname            VARCHAR(20)     NOT NULL,
                Lname            VARCHAR(20),
                Rating           INT             NOT NULL CHECK (Rating >= 1 AND Rating <= 5),
                PRIMARY KEY (User_ID),
                FOREIGN KEY (User_ID) REFERENCES USER(User_ID),
                FOREIGN KEY (Book_ID) REFERENCES BOOK(Book_ID),
                FOREIGN KEY (Article_ID) REFERENCES ARTICLE(Article_ID)
            );
            """
        ]

        for query in queries:
            cursor.execute(query)
            # print("Table created or already exists.")

        connection.commit()

    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# -----------------------------------------------------------------

def check_availability(book_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Function checks if the book with the specified ID is available to check out or not
        query = """
        SELECT b.Book_ID
        FROM BOOK b
        LEFT JOIN LOAN l ON b.Book_ID = l.Book_ID
        WHERE b.Book_ID = %s AND (l.Due_date IS NULL OR l.Due_date < CURDATE());
        """
        cursor.execute(query, (book_id,))
        result = cursor.fetchone()

        if result:
            return f"Book ID {book_id} is available."
        else:
            return f"Book ID {book_id} is not available."

    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        connection.close()

# -----------------------------------------------------------------

def loan_book(user_id, book_id, date_of_issue, due_date):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Function records loans for the specified book and user
        # First check availability of the book
        availability = check_availability(book_id)
        if "not available" in availability:
            return availability

        # Then insert a new loan record
        query = """
        INSERT INTO LOAN (User_ID, Book_ID, Date_of_issue, Due_date, In_time, Late)
        VALUES (%s, %s, %s, %s, 'YES', 'NO');
        """
        cursor.execute(query, (user_id, book_id, date_of_issue, due_date))

        connection.commit()
        return f"Book ID {book_id} has been loaned to User ID {user_id}."

    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        connection.close()

# -----------------------------------------------------------------

def review_book(user_id, book_id, rating, display_reviews):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Function records reviews for each book according to users
        # Insert a new review record
        query = """
        INSERT INTO REVIEW (User_ID, Book_ID, Username, Display_reviews, Rating)
        VALUES (%s, %s, %s, %s, %s);
        """
        cursor.execute(query, (user_id, book_id, user_id, display_reviews, rating))

        connection.commit()
        return f"Review for Book ID {book_id} has been added."
    
    except mysql.connector.Error as err:
        return f"Error: {err}"

    finally:
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()

# -----------------------------------------------------------------

# Function views book specified by given ID
def view_book(book_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Query to fetch book details based on Book_ID
        query = """
        SELECT Book_ID, Author, Title, Date_of_publication
        FROM BOOK
        WHERE Book_ID = %s;
        """
        cursor.execute(query, (book_id,))
        result = cursor.fetchone()

        if result:
            # If the book is found, return the details
            book_id, author, title, date_of_publication = result
            return f"Book ID: {book_id}\nAuthor: {author}\nTitle: {title}\nDate of Publication: {date_of_publication}"
        else:
            return f"Book with ID {book_id} not found."

    except mysql.connector.Error as err:
        return f"Error: {err}"
    
    finally:
        cursor.close()
        connection.close()

# -----------------------------------------------------------------

# Function views user specified by given ID
def view_user(user_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Query to fetch user details based on User_ID
        query = """
        SELECT User_ID, Age, First_name, Last_name, Email_ID, Username, Password
        FROM USER
        WHERE User_ID = %s;
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        if result:
            # If the user is found, return the details
            user_id, age, first_name, last_name, email, username, password = result
            return f"User ID: {user_id}\nAge: {age}\nFirst Name: {first_name}\nLast Name: {last_name}\nEmail ID: {email}\nUsername: {username}\nPassword: {password}"
        else:
            return f"User with ID {user_id} not found."

    except mysql.connector.Error as err:
        return f"Error: {err}"
    
    finally:
        cursor.close()
        connection.close()

# -----------------------------------------------------------------

def view_loan(user_id, book_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Query to fetch loan details based on User_ID and Book_ID
        query = """
        SELECT User_ID, Book_ID, Date_of_issue, Due_date, In_time, Late
        FROM LOAN
        WHERE User_ID = %s AND Book_ID = %s;
        """
        cursor.execute(query, (user_id, book_id))
        result = cursor.fetchone()

        if result:
            # If the loan is found, return the details
            user_id, book_id, date_of_issue, due_date, in_time, late = result
            return f"User ID: {user_id}\nBook ID: {book_id}\nDate of Issue: {date_of_issue}\nDue Date: {due_date}\nIn Time: {in_time}\nLate: {late}"
        else:
            return f"Loan for User_ID {user_id} and Book_ID {book_id} not found."

    except mysql.connector.Error as err:
        return f"Error: {err}"
    
    finally:
        cursor.close()
        connection.close()

# -----------------------------------------------------------------

# Function views article specified by given ID
def view_article(article_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Query to fetch article details based on Article_ID
        query = """
        SELECT Article_ID, Author, Date_of_publication, Number_of_citations, Downloads
        FROM ARTICLE
        WHERE Article_ID = %s;
        """
        cursor.execute(query, (article_id,))
        result = cursor.fetchone()

        if result:
            # If the article is found, return the details
            article_id, author, date_of_publication, num_citations, downloads = result
            return f"Article ID: {article_id}\nAuthor: {author}\nDate of Publication: {date_of_publication}\nNumber of Citations: {num_citations}\nDownloads: {downloads}"
        else:
            return f"Article with ID {article_id} not found."

    except mysql.connector.Error as err:
        return f"Error: {err}"
    
    finally:
        cursor.close()
        connection.close()

# -----------------------------------------------------------------

def view_review(user_id, book_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Query to fetch review details based on User_ID and Book_ID
        query = """
        SELECT User_ID, Book_ID, Username, Display_reviews, Fname, Lname, Rating
        FROM REVIEW
        WHERE User_ID = %s AND Book_ID = %s;
        """
        cursor.execute(query, (user_id, book_id))
        result = cursor.fetchone()

        if result:
            # If the review is found, return the details
            user_id, book_id, username, display_reviews, fname, lname, rating = result
            return f"User ID: {user_id}\nBook ID: {book_id}\nUsername: {username}\nReview: {display_reviews}\nFirst Name: {fname}\nLast Name: {lname}\nRating: {rating}"
        else:
            return f"Review for User_ID {user_id} and Book_ID {book_id} not found."

    except mysql.connector.Error as err:
        return f"Error: {err}"
    
    finally:
        cursor.close()
        connection.close()

# -----------------------------------------------------------------

if __name__ == "__main__":
    # Create tables (if they do not exist, this won't affect already existing ones)
    create_tables()
    
    # View all books in the library
    # The view_book function can also be used to view a specific book according to its ID
    print()
    print("Viewing all books in the library:")
    print(view_book(1))
    print()
    print(view_book(2))
    print()
    print(view_book(3))

    # View a specific user by ID
    print("\nViewing user with ID 1:")
    print(view_user(1))

    # View a specific loan by User_ID and Book_ID
    print("\nViewing loan for user with ID 2 and book with ID 2:")
    print(view_loan(2, 2))

    print("\nChecking availability for book with ID 3:")
    print(check_availability(3))

    # View a specific article by Article_ID
    print("\nViewing article with ID 1:")
    print(view_article(1))

    # View a specific review by User_ID and Book_ID
    print("\nViewing review for user with ID 1 and book with ID 1:")
    print(view_review(1, 1))
