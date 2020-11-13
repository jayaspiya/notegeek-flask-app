import sqlite3


def connectdb():
    return sqlite3.connect("notegeek.db")


def addUser(username, fname, lname, password):
    if doesUserExist(username) == False:
        insertQuery = f"""
            INSERT INTO users(username, first_name, last_name, password)
            VALUES("{username}","{fname}","{lname}","{password}")
        """
        con = connectdb()
        cursor = con.cursor()
        cursor.execute(insertQuery)
        con.commit()
        con.close()
        return True
    return False


def createNote(title, user_id):
    noteCreateQuery = f"""
        INSERT INTO notes(title, modified_date, user_id, description)
        VALUES("{title}",datetime('now'), {user_id}, "")
    """
    con = connectdb()
    cursor = con.cursor()
    cursor.execute(noteCreateQuery)
    con.commit()
    con.close()


def doesUserExist(username):
    con = connectdb()
    cursor = con.cursor()
    userQuery = f"""
        Select * FROM users WHERE username = "{username}";
    """
    cursor.execute(userQuery)
    user = cursor.fetchone()
    con.commit()
    con.close()
    if(user is None):
        return False
    return True


def getNoteUserId(noteId):
    con = connectdb()
    cursor = con.cursor()
    userQuery = f"""
        Select user_id from notes where id = {noteId};
    """
    cursor.execute(userQuery)
    userId = cursor.fetchone()
    con.commit()
    con.close()
    return userId[0]


def updateNote(title, description, noteId, userId):
    pass


def view():
    userQuery = "SELECT * FROM users;"
    noteQuery = "SELECT * FROM notes;"
    con = connectdb()
    cursor = con.cursor()
    cursor.execute(userQuery)
    users = cursor.fetchall()
    cursor.execute(noteQuery)
    notes = cursor.fetchall()
    for user in users:
        print(user)
    for note in notes:
        print(note)
    con.commit()
    con.close()


def createDB():
    con = connectdb()
    cursor = con.cursor()
    cursor.execute("""
    CREATE TABLE users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(20),
        first_name VARCHAR(20),
        last_name VARCHAR(20),
        password VARCHAR(30)
    );
    """)
    cursor.execute("""
    CREATE TABLE notes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(30),
        description VARCHAR(300),
        modified_date DATE,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    """)
    con.commit()
    con.close()


if __name__ == "__main__":
    # createDB()
    # addUser("lap", "Linaa", "Piya", "123aa456")
    # createNote("note4", 2)
    view()
    print("Script Completed")
