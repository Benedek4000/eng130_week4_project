# by Benedek Kovacs

import psycopg2
import sys
import pandas as pd


# class used to connect to a postgresql database
class DBConnector:

    #used for print(db)
    def __str__(self):
        self.cursor.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
        return 60*'-'+'\n'+'\n\n'.join(list(f'{table[0].upper()}\n'+self.execute_query(f'SELECT * FROM {table[0]};').to_string() for table in self.cursor.fetchall()))+'\n'+60*'-'

    # enable usage of 'with'
    def __enter__(self):
        return self

    # runs upon end of 'with'
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close_db()

    # initialise connection to database
    def __init__(self, user, password, host, port, db_name):
        try:
            self.conn = psycopg2.connect(
                user=user,
                password=password,
                host=host,
                port=port,
                database=db_name
            )
            self.cursor = self.conn.cursor()
            print('Successfully connected to PostgreSQL Platform')
        except psycopg2.Error as e:
            print(f'Error connecting to PostgreSQL Platform: {e}')
            sys.exit(1)

    # close connection to database
    def close_db(self):
        if self.conn is not None:
            try:
                self.execute_query("COMMIT;")
                self.conn.close()
                print('Database connection closed.')
            except psycopg2.Error as e:
                print(f'Error closing connection to PostgreSQL Platform: {e}')
        else:
            print('Connection does not exist.')

    # execute query on database. returns a pandas dataframe
    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            df = pd.DataFrame(self.cursor)
            return df
        except psycopg2.ProgrammingError:
            pass
        except psycopg2.Error as e:
            print(f"Error: {e}")
            return e
