import sqlite3
import json

class SQLiteDatabase:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self, db_file):
        try:
            # Set a timeout to avoid "database is locked" error
            self.connection = sqlite3.connect(db_file, timeout=40)
            self.cursor = self.connection.cursor()
            print("Database connection successful.")
        except sqlite3.Error as error:
            print(f"Error: {error}")

    def create_database(self, new_dbname):
        self.connect(new_dbname)
        print(f"Database {new_dbname} created successfully.")

    def create_json_table(self,table_name):
        print('Function started')
        
        # Ensure connection and cursor are valid
        if self.connection is None:
            print("Connection is not open.")
            return
        
        if self.cursor is None:
            print("Cursor is not initialized.")
            return
        
        create_table_sql = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            json_data TEXT NOT NULL
        );
        '''
        
        try:
            print('Executing query...')
            self.cursor.execute(create_table_sql)
            print('Query executed successfully.')
            
            self.connection.commit()  # Commit after table creation
            print("JSON table created successfully.")
        except sqlite3.Error as error:
            print(f"Error: {error}")
            self.connection.rollback()  # Rollback on error
            print("Error occurred, rollback done.")

    def insert_json(self, json_text, table_name='titanic_json'):
        try:
            # Insert the JSON string as a record in the table
            self.cursor.execute(f"INSERT INTO {table_name} (json_data) VALUES (?)", (json_text,))
            self.connection.commit()  # Commit after insert
            print(f"JSON data inserted successfully into table: {table_name}")
        except sqlite3.Error as error:
            print(f"Error: {error}")
            self.connection.rollback()
            
    def retrieve_all_json(self, table_name='titanic_json'):
        try:
            # Retrieve all records from the table
            self.cursor.execute(f"SELECT json_data FROM {table_name}")
            rows = self.cursor.fetchall()  # Fetch all rows
            data = [row[0] for row in rows]  # Extract JSON data from each row
            print(f"Retrieved {len(data)} records from table: {table_name}")
            return data
        except sqlite3.Error as error:
            print(f"Error: {error}")
            return None

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed.")

# # Usage example
db = SQLiteDatabase()
db.connect('titanic_data.db')
# db.create_database('titanic_data.db')
db.create_json_table('new_table_df')  # Call the function that creates the table

# text = 'helo how are your'
# db.insert_json(text,'new_table_df')
# d = db.retrieve_all_json('new_table_df')
# print('the file',d)

# # Close the connection after the table is created
# db.close()
