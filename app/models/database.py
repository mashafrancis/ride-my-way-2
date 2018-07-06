from app.models import dbconn


class Database(object):
    @staticmethod
    def insert(collection, data):
        """
        This inserts data into the database
        :param collection: INSERT INTO table(column1, column2, …) VALUES (value1, value2, …);
        :param data: value1, value2,...
        :return:
        """
        connection = dbconn()
        cursor = connection.cursor()

        cursor.execute(collection, data)

        connection.commit()
        connection.close()

    @staticmethod
    def find(collection, query):
        pass

    @staticmethod
    def find_one(collection, query):
        pass

    @staticmethod
    def update(collection, query):
        pass

    @staticmethod
    def remove(collection, query):
        pass

    @classmethod
    def find_by_email(cls, email):
        connection = dbconn()
        cursor = connection.cursor()
        cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
        row = cursor.fetchone()
        if not row:
            return {'error': 'Authentication failed user unknown'}

    @classmethod
    def find_by_username(cls, username):
        connection = dbconn()
        cursor = connection.cursor()
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        password = cursor.fetchone()

