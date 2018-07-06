import psycopg2
import psycopg2.extras


def dbconn():
    connection = psycopg2.connect(dbname='andela',
                                  host='localhost',
                                  user='masha',
                                  password='bhakita')
    return connection


def create_tables():
    """
    Create tables for the database
    """
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            firstname VARCHAR(80) NOT NULL,
            lastname VARCHAR(80) NOT NULL,
            username VARCHAR(80) UNIQUE,
            email VARCHAR(80) UNIQUE,
            password VARCHAR(255) NOT NULL
        )
        """,
        """ 
        CREATE TABLE IF NOT EXISTS requests (
            request_id SERIAL PRIMARY KEY,
            ride_id INT NOT NULL,
            user_id INT NOT NULL,
            status VARCHAR(100) DEFAULT 'Pending'
        )
        """,
        """ 
        CREATE TABLE IF NOT EXISTS rides (
            ride_id SERIAL PRIMARY KEY,
            origin VARCHAR(80) NOT NULL,
            destination VARCHAR(80) NOT NULL,
            date VARCHAR(80) NOT NULL,
            time VARCHAR(80) NOT NULL)
        """)
    connection = None
    try:
        connection = dbconn()

        cursor = connection.cursor()
        # create tables
        for command in commands:
            cursor.execute(command)

        cursor.close()

        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()


if __name__ == '__main__':
    create_tables()
