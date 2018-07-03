from app.models import dbconn


class User:
    def __init__(self, _id, first_name, last_name, username, email, password):
        self.id = _id
        self.firstname = first_name
        self.lastname = last_name
        self.username = username
        self.email = email
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = dbconn()
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = dbconn()
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM users WHERE id=%s", (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user



