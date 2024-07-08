# File: src/dan_db_connect/sql_crud.py

import mysql.connector
from mysql.connector import Error
from typing import Dict, Any, Optional, List
import pandas as pd


class MySQLDBOperation:
    """
    MySQL operations for creating connection and performing CRUD operations.

    Attributes:
    - host (str): The host for the MySQL database.
    - user (str): The username for the MySQL database.
    - password (str): The password for the MySQL database.
    - database (str): The name of the MySQL database.

    Methods:
    - create_connection() -> mysql.connector.connection.MySQLConnection:
        Creates and returns a MySQL database connection.
    - execute_query(query: str) -> None:
        Executes a single query in the database.
    - insert_record(table: str, record: Dict[str, Any]) -> None:
        Inserts a single record into the specified table.
    - bulk_insert(table: str, datafile: str) -> None:
        Bulk inserts records from a file (CSV or Excel) into the specified table.
    - find(query: Optional[str] = None, table: Optional[str] = None) -> List[Dict[str, Any]]:
        Finds and returns records matching the query from the specified table. Returns all records if no query is provided.
    - delete(condition: Optional[str] = None, table: Optional[str] = None) -> None:
        Deletes records matching the condition from the specified table. Deletes all records if no condition is provided.
    - update(table: str, updates: Dict[str, Any], condition: str) -> None:
        Updates records matching the condition with the specified updates in the specified table.
    """

    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def create_connection(self):
        """
        Creates and returns the MySQL database connection.
        """
        connection = None
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            if connection.is_connected():
                print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
        return connection

    def execute_query(self, query: str) -> None:
        """
        Executes a single query in the database.
        """
        connection = self.create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def insert_record(self, table: str, record: Any) -> None:
    
        connection = self.create_connection()
        cursor = connection.cursor()

        def execute_insert(record: Dict[str, Any]) -> None:
            columns = ", ".join(record.keys())
            values = ", ".join(["%s"] * len(record))
            sql = f"INSERT INTO {table} ({columns}) VALUES ({values})"
            cursor.execute(sql, tuple(record.values()))

        try:
            if isinstance(record, list):
                for rec in record:
                    if not isinstance(rec, dict):
                        raise TypeError("Each record must be a dictionary")
                    execute_insert(rec)
            elif isinstance(record, dict):
                execute_insert(record)
            else:
                raise TypeError("Record must be a dictionary or a list of dictionaries")
            
            connection.commit()
            print("Record(s) inserted successfully")
        except Error as e:
            print(f"The error '{e}' occurred")
        finally:
            cursor.close()
            connection.close()


    def bulk_insert(self, table: str, datafile: str) -> None:
        """
        Bulk inserts records from a file (CSV or Excel) into the specified table.
        """
        if datafile.endswith(".csv"):
            data = pd.read_csv(datafile, encoding="utf-8")
        elif datafile.endswith(".xlsx"):
            data = pd.read_excel(datafile, encoding="utf-8")
        else:
            raise ValueError("Unsupported file format. Use CSV or Excel files.")
        records = data.to_dict(orient="records")
        for record in records:
            self.insert_record(table, record)

    def find(self, query: Optional[str] = None, table: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Finds and returns records matching the query from the specified table. 
        Returns all records if no query is provided.
        """
        if query is None:
            if table is None:
                raise ValueError("Table name must be provided")
            query = f"SELECT * FROM {table}"
        connection = self.create_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def delete(self, condition: Optional[str] = None, table: Optional[str] = None) -> None:
        """
        Deletes records matching the condition from the specified table. 
        Deletes all records if no condition is provided.
        """
        if table is None:
            raise ValueError("Table name must be provided")
        if condition is None:
            query = f"DELETE FROM {table}"
        else:
            query = f"DELETE FROM {table} WHERE {condition}"
        self.execute_query(query)

    def update(self, table: str, updates: Dict[str, Any], condition: str) -> None:
        """
        Updates records matching the condition with the specified updates in the specified table.
        """
        set_clause = ", ".join([f"{key} = %s" for key in updates.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        connection = self.create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(sql, tuple(updates.values()))
            connection.commit()
            print("Record updated successfully")
        except Error as e:
            print(f"The error '{e}' occurred")
