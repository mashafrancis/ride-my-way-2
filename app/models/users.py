import psycopg2


def user():
    connection = None
    try:
        connection = psycopg2.connect(dbname='andela',
                                      host='localhost',
                                      user='masha',
                                      password='bhakita')

        cursor = connection.cursor()

        app_user = ('Rose', 'Kilosy', 'jumpy', 'rose@gmail.com', 'bhakita', 'KCB778')
        cursor.execute("INSERT INTO users (id, first_name, last_name, username, email, password, car_plate_number)"
                       "VALUES(DEFAULT, %s, %s, %s, %s, %s, %s)", app_user)

        connection.commit()
        connection.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()


if __name__ == '__main__':
    user()
