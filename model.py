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


def createNote(user_id, title, description=""):
    noteCreateQuery = f"""
        INSERT INTO notes(title, modified_date, user_id, description)
        VALUES("{title}",datetime('now'), {user_id}, "{description}")
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


def getUserId(username, password):
    searchQuery = f"""
        SELECT id FROM users WHERE username = "{username}" and password = "{password}";
    """
    con = connectdb()
    cursor = con.cursor()
    cursor.execute(searchQuery)
    userId = cursor.fetchone()
    con.commit()
    con.close()
    if userId is None:
        return None
    return userId


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
    return userId


def getNote(note_id):
    noteQuery = f"""
        SELECT * FROM notes where id = {note_id};
    """
    con = connectdb()
    cursor = con.cursor()
    cursor.execute(noteQuery)
    note = cursor.fetchone()
    con.commit()
    con.close()
    return note


def getAllNotes(user_id):
    userNoteQuery = f"""
        SELECT * FROM notes where user_id = {user_id} ORDER BY modified_date DESC
    """
    con = connectdb()
    cursor = con.cursor()
    cursor.execute(userNoteQuery)
    notes = cursor.fetchall()
    con.commit()
    con.close()
    return notes


def updateNote(title, description, noteId, userId):
    if userId == getNoteUserId(noteId):
        updateQuery = f"""
            UPDATE notes
            SET title = "{title}", description = "{description}", modified_date = datetime('now')
            WHERE id = {noteId}
        """
        con = connectdb()
        cursor = con.cursor()
        cursor.execute(updateQuery)
        con.commit()
        con.close()
    else:
        print(f"{userId} doesnot match")


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
    print("-----------------------------------")
    for note in notes:
        print(note)
    print("-----------------------------------")
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
    # updateNote("Java", "Java is Good", 2, 1)
    print("Script Completed")
