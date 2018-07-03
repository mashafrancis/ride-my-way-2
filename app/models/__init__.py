import psycopg2
import psycopg2.extras

db = psycopg2.connect(dbname='andela',
                      host='localhost',
                      user='masha',
                      password='bhakita')


def create_tables():
    """
    Create tables for the database
    """
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(80) NOT NULL,
            last_name VARCHAR(80) NOT NULL,
            username VARCHAR(80) UNIQUE,
            email VARCHAR(80) UNIQUE,
            password VARCHAR(80) NOT NULL,
            car_plate_number VARCHAR(80) NULL
        )
        """,
        """ 
        CREATE TABLE IF NOT EXISTS requests (
            request_id SERIAL primary key,
            user_id int references users_test(user_id),
            status VARCHAR(100) NOT NULL,
            accepted BOOLEAN NOT NULL
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
        connection = db

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
