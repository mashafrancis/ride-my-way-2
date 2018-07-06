from werkzeug.security import generate_password_hash
from app.models import create_tables, dbconn


class User(object):
    def __init__(self, _id, firstname, lastname, username, email, password):
        self.id = _id
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def register_user(self):
        create_tables()
        connection = dbconn()
        cursor = connection.cursor()

        user = (['firstname'],
                ['lastname'],
                ['username'],
                ['email'],
                ['password'])

        cursor.execute("INSERT INTO users (user_id, firstname, lastname, username, email, password)"
                       "VALUES(DEFAULT, %s, %s, %s, %s, %s)", user)

        connection.commit()
        connection.close()

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
