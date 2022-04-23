#Tady bude komunikace se serverem
import psycopg2

connection = None
cursor = None


def Connect():
    global connection, cursor
    connection = psycopg2.connect("dbname=suppliers user=postgres password=hujni")
    cursor = connection.cursor()

    print('PostgreSQL database version:')
    cursor.execute('SELECT version()')
    db_version = cursor.fetchone()
    print(db_version)

    cursor.close()

Connect()