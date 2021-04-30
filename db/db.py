import psycopg2

from typing import List

def init_image_db():
    try:
        connection = get_db_object()
        cursor = connection.cursor()

        command = ( "CREATE TABLE IF NOT EXISTS imgs ("
                    "uuid VARCHAR(70) NOT NULL PRIMARY KEY," 
                    "name VARCHAR(50) NOT NULL," 
                    "tags VARCHAR(110)"
                    ");")

        cursor.execute(command)
        connection.commit()
    except Exception as e:
        print(e)

def get_db_object():
    try:
        connection = psycopg2.connect(  user="admin",
                                    password="admin",
                                    host="db",
                                    port=5432,
                                    database="imagedb")
        return connection
    except:
        print('Unable to create db connection object')
    
def insert_command(thisuuid: str, thisname: str, tags: List):

    command = ("INSERT INTO imgs ("
             "  uuid,"
             "  name,"
             "  tags"
             ") VALUES ("
            )

    command += f"\'{thisuuid}\', \'{thisname}\'"

    if tags:
        command += f",\'{tags}\'"

    command += ");"

    try:
        connection = get_db_object()
        cursor = connection.cursor()
        cursor.execute(command)
        connection.commit()
    except Exception as e:
        print('Failed to execute sql command', e)
        print(command)

def fetch_query(thisname: str, tags: List):

    command = "SELECT * FROM imgs WHERE"

    if thisname:
        command += f" name = \'{thisname}\'"
    elif tags:
        tags = tags.split(" ")
        for i, tag in enumerate(tags):
            command += f" tags LIKE \'%{tag}%\'"
            if i < len(tags) - 1:
                command += " OR "
    command += f" ORDER BY random() LIMIT 1;"

    try:
        connection = get_db_object()
        cursor = connection.cursor()
        cursor.execute(command)
        record = cursor.fetchall()
        return record
    except Exception as e:
        print('Failed to execute sql command', e)
        print(command)