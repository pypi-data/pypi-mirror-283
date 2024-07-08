from typing import Optional, List, Dict, Any,Union
import pandas as pd
import json
from pymongo import MongoClient


class MongoDBOperation:
    """
    MongoDB operations for creating client, database, collections, and performing CRUD operations.

    Attributes:
    - client_uri (str): The URI for connecting to the MongoDB client.
    - database_name (str): The name of the database to operate on.
    - collection_name (Optional[str]): The default collection name to use for operations if not specified.

    Methods:
    - create_client() -> MongoClient:
        Creates and returns a MongoDB client.
    - create_database() -> Database:
        Creates and returns the MongoDB database.
    - create_collection(collection_name: str) -> Collection:
        Creates and returns the MongoDB collection.
    - insert_record(record: Dict[str, Any], collection_name: str) -> None:
        Inserts a single record or a list of records into the specified collection.
    - bulk_insert(datafile: str, collection_name: Optional[str] = None) -> None:
        Bulk inserts records from a CSV or Excel file into the specified collection.
    - find(query: Optional[Dict[str, Any]] = None, collection_name: Optional[str] = None) -> List[Dict[str, Any]]:
        Finds and returns records matching the query from the specified collection. Returns all records if no query is provided.
    - delete(query: Optional[Dict[str, Any]] = None, collection_name: Optional[str] = None) -> None:
        Deletes records matching the query from the specified collection. Deletes all records if no query is provided.
    - update(query: Dict[str, Any], update_values: Dict[str, Any], collection_name: Optional[str] = None) -> None:
        Updates records matching the query with the specified update values in the specified collection.
    """

    def __init__(
        self, client_uri: str, database_name: str, collection_name: Optional[str] = None
    ):
        self.client_uri = client_uri
        self.database_name = database_name
        self.collection_name = collection_name

    def create_client(self) -> MongoClient:
        """
        Creates a MongoDB client.
        """
        client: MongoClient = MongoClient(self.client_uri)
        return client

    def create_database(self) -> Any:
        """
        Creates and returns the MongoDB database.
        """
        client = self.create_client()
        database = client[self.database_name]
        return database

    def create_collection(self, collection_name: str) -> Any:
        """
        Creates and returns the MongoDB collection.
        """
        database = self.create_database()
        collection = database[collection_name]
        return collection

    def insert_record(self, record: Union[Dict[str, Any], List[Dict[str, Any]]], collection_name: str) -> None:
        """
        Inserts a single record or multiple records into the specified collection.

        Parameters:
        - record (Union[Dict[str, Any], List[Dict[str, Any]]]): The record or list of records to insert.
        - collection_name (str): The name of the collection to insert the record(s) into.

        Raises:
        - TypeError: If any record in the list is not a dictionary.
        """
        collection = self.create_collection(collection_name)
        
        if isinstance(record, list):
            for data in record:
                if not isinstance(data, dict):
                    raise TypeError("Each record must be a dictionary")
            collection.insert_many(record)
        elif isinstance(record, dict):
            collection.insert_one(record)
        else:
            raise TypeError("record must be a dictionary or a list of dictionaries")

    def bulk_insert(self, datafile: str, collection_name: Optional[str] = None) -> None:
        """
        Bulk inserts records from a file (CSV or Excel) into the specified collection.
        """
        if collection_name is None:
            if self.collection_name is None:
                raise ValueError("Collection name must be provided")
            collection_name = self.collection_name
        if datafile.endswith(".csv"):
            data = pd.read_csv(datafile, encoding="utf-8")
        elif datafile.endswith(".xlsx"):
            data = pd.read_excel(datafile, encoding="utf-8")
        else:
            raise ValueError("Unsupported file format. Use CSV or Excel files.")
        data_json = json.loads(data.to_json(orient="records"))
        collection = self.create_collection(collection_name)
        collection.insert_many(data_json)

    def find(self, query: Optional[Dict[str, Any]] = None, collection_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Finds and returns records matching the query from the specified collection.
        If no query is provided, returns all records in the collection.

        Parameters:
        - query (Optional[Dict[str, Any]]): The query to match records. If None, returns all records.
        - collection_name (Optional[str]): The name of the collection to find the records in. Defaults to the instance's collection_name.

        Returns:
        - List[Dict[str, Any]]: The list of records matching the query or all records if no query is provided.

        Raises:
        - ValueError: If no collection name is provided.
        """
        if collection_name is None:
            if self.collection_name is None:
                raise ValueError("Collection name must be provided")
            collection_name = self.collection_name

        collection = self.create_collection(collection_name)
        query = query or {}
        result = collection.find(query)
        return list(result)

    def delete(self, query: Optional[Dict[str, Any]] = None, collection_name: Optional[str] = None) -> None:
        """
        Deletes records matching the query from the specified collection.
        If no query is provided, deletes all records in the collection.

        Parameters:
        - query (Optional[Dict[str, Any]]): The query to match records to delete. If None, deletes all records.
        - collection_name (Optional[str]): The name of the collection to delete the records from. Defaults to the instance's collection_name.

        Raises:
        - ValueError: If no collection name is provided.
        """
        if collection_name is None:
            if self.collection_name is None:
                raise ValueError("Collection name must be provided")
            collection_name = self.collection_name

        collection = self.create_collection(collection_name)
        query = query or {}
        collection.delete_many(query)

    def update(
        self, query: Dict[str, Any], update_values: Dict[str, Any], collection_name: Optional[str] = None
    ) -> None:
        """
        Updates records matching the query with the specified update values in the specified collection.
        """
        if collection_name is None:
            if self.collection_name is None:
                raise ValueError("Collection name must be provided")
            collection_name = self.collection_name

        collection = self.create_collection(collection_name)
        collection.update_one(query, {"$set": update_values})
