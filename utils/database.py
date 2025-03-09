import sqlite3
import os,re

class SQLiteDB:
    """
    Vi tri cua file .db duoc su dung
    project/
    |-- db/
    |   |-- hotel7-3.db
    |-- utils/
    |   |-- database.py
    |-- ...
    
    =========================================
    doc tiep huong dan su dung trang must_read 
    """
    # def __init__(self, db_filename="db/hotel7-3.db") day la vi tri cua file .db
    
    def __init__(self, db_filename="db/hotel7-3.db"): #added default filename.
        """
        Initializes the database connection.

        Args:
            db_filename (str): The filename of the SQLite database file. Defaults to "my_database.db".
        """
        self.db_filename = db_filename
        self.db_path = os.path.join(os.getcwd(), db_filename) #construct full path
        self.conn = None
        self.cursor = None

    def connect(self):
        """
        Establishes a connection to the SQLite database.
        """
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            return True
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return False

    def disconnect(self):
        """
        Closes the database connection.
        """
        if self.conn:
            self.cursor.close()
            self.conn.close()
            self.conn = None
            self.cursor = None

    def execute_query(self, query, params=None, return_last_row=False):
        if not self.conn:
            if not self.connect():
                return None

        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            if query.lower().startswith("select"):
                results = self.cursor.fetchall()
                return results
            else:
                self.conn.commit()
                if return_last_row:
                    table_name = self.get_table_name(query)
                    if table_name:
                        last_row_id = self.cursor.lastrowid
                        self.cursor.execute(f"SELECT * FROM {table_name} WHERE rowid = ?", (last_row_id,))
                        return self.cursor.fetchone()
                    else:
                        print("Could not extract table name from query")
                        return None
                else:
                    return None

        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            if not query.lower().startswith("select"):
                self.disconnect()
                
    def execute_many(self, query, params_list):
        """
        Executes an SQL query multiple times with different parameters.

        Args:
            query (str): The SQL query to execute.
            params_list (list): A list of tuples, each representing parameters for a query execution.

        Returns:
            bool: True if all queries were executed successfully, False otherwise.
        """
        if not self.conn:
            if not self.connect():
                return False

        try:
            self.cursor.executemany(query, params_list)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error executing many queries: {e}")
            return False
        finally:
            self.disconnect()

    def get_table_name(self, query):
        match = re.search(r'INSERT INTO (\w+)', query)
        if match:
            return match.group(1)
        else:
            raise ValueError("Could not extract table name from query")