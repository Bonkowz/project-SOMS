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
            messagebox.showerror("Database Error", str(err))
            return None

    def execute_query(self, query, params=None, fetch_type="all"):
        conn = self.connect()
        if conn is None:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch_type == "all":
                result = cursor.fetchall()
            elif fetch_type == "one":
                result = cursor.fetchone()
            else:
                result = None
            conn.commit() # Commit changes for INSERT, UPDATE, DELETE
            return result
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
            conn.rollback() # Rollback in case of error
            return None
        finally:
            if conn:
                conn.close()

    def fetch_organizations_for_combo(self):
        query = '''
            SELECT organization_id, organization_name FROM organization ORDER BY organization_name
                '''
        results = self.execute_query(query, fetch_type="all")
        if results:
            return {org_name: org_id for org_id, org_name in results}
        return {}

    def get_organization_info(self, org_name):
        query = '''
            SELECT organization_id, organization_name, organization_type, no_of_members
            FROM organization 
            WHERE organization_name LIKE %s
                '''
        return self.execute_query(query, ('%' + org_name + '%',), fetch_type="one")

    def get_next_student_id(self):
        query = '''
            SELECT COALESCE(MAX(student_id), 0) + 1 FROM member
                '''
        result = self.execute_query(query, fetch_type="one")
        return result[0] if result else 1