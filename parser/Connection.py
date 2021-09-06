import psycopg2
import config

def connect(db_name):
    try:
        return psycopg2.connect(
                    user = config.user,
                    password = config.password,
                    host = config.host,
                    port = config.port)
    except "Error" as e:
        print(e)