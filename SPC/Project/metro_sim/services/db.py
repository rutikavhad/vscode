import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="metro",
        user="matrix",
        password="1234",
        host="localhost",
        port="5432"
    )