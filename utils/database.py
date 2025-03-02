# utils/database.py
import mysql.connector
import configparser
import os

class Database:
    _instance = None  # Singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = None  # Initialize connection
        return cls._instance

    def connect(self):
        if self.connection is None: # Check if a connection exists before attempting to create a new one
            try:
                config = configparser.ConfigParser()
                config.read("config.ini")

                self.connection = mysql.connector.connect(
                    host=config["Database"]["host"],
                    user=config["Database"]["user"],
                    password=config["Database"]["password"],
                    database=config["Database"]["database"]
                )
                print("Database connection established.")
            except mysql.connector.Error as err:
                print(f"Error connecting to the database: {err}")
                self.connection = None # Set connection to None to avoid further errors
        return self.connection

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None # Ensure connection is set to None after closing
            print("Database connection closed.")

    def get_connection(self):
        if not self.connection:
            self.connect() # Establish connection if not already connected
        return self.connection

    def execute_query(self, query, values=None, fetch=False):
        """Executes a SQL query.  fetch=True for SELECT queries."""
        connection = self.get_connection() # Get the connection, creating one if necessary
        cursor = None  # Initialize cursor

        try:
            cursor = connection.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)

            if fetch:
                result = cursor.fetchall()
                return result
            else:
                connection.commit()  # Commit changes for non-SELECT queries
                return None
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            if connection:
                connection.rollback()  # Rollback in case of errors
            return None
        finally:
            if cursor:
                cursor.close()
            # DO NOT close the connection here. The connection should be closed only when application shuts down

# Example usage (Singleton):
# db = Database()
# conn = db.get_connection()