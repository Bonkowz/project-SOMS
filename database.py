# database.py
import mysql.connector
from tkinter import messagebox

DB_CONFIG = {
    'host': 'localhost',
    'user': 'gift',
    'password': 'useruser',
    'database': 'soms'
}

class Database:
    def __init__(self, db_config):
        self.db_config = db_config

    def connect(self):
        try:
            return mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect to database: {err}")
            return None

    def execute_query(self, query, params=None, fetch_type=None): # Changed default fetch_type to None
        conn = self.connect()
        if conn is None:
            return None

        try:
            cursor = conn.cursor()
            cursor.execute(query, params)

            # Determine if it's a SELECT query or a DML query
            if query.strip().upper().startswith("SELECT"):
                if fetch_type == "all":
                    result = cursor.fetchall()
                elif fetch_type == "one":
                    result = cursor.fetchone()
                else: # Default for SELECT, can be adjusted
                    result = cursor.fetchall()
                return result
            else:
                # For INSERT, UPDATE, DELETE, commit and return rowcount
                conn.commit()
                return cursor.rowcount # Return the number of affected rows
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error executing query: {err}\nQuery: {query}\nParams: {params}")
            conn.rollback() # Rollback in case of error
            return -1 # Indicate an error by returning -1 or raising an exception
        finally:
            if conn:
                conn.close()

    def fetch_organizations_for_combo(self):
        # This will now correctly use fetch_type="all" within execute_query
        query = "SELECT organization_id, organization_name FROM organization ORDER BY organization_name"
        results = self.execute_query(query, fetch_type="all")
        if results:
            return {org_name: org_id for org_id, org_name in results}
        return {}

    def get_organization_info(self, org_name):
        # This will now correctly use fetch_type="one" within execute_query
        query = "SELECT organization_id, organization_name, organization_type, no_of_members FROM organization WHERE organization_name LIKE %s"
        return self.execute_query(query, ('%' + org_name + '%',), fetch_type="one")

    def get_next_student_id(self):
        # This will now correctly use fetch_type="one" within execute_query
        query = "SELECT COALESCE(MAX(student_id), 0) + 1 FROM member"
        result = self.execute_query(query, fetch_type="one")
        return result[0] if result else 1