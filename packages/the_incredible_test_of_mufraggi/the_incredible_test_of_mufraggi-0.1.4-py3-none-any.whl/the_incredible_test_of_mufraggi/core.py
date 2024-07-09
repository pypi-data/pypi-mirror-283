from typing import Dict, Any
from pymongo import MongoClient
from pymongo.database import Database


def get_database(connection_string: str, db_name: str) -> Database:
    client = MongoClient(connection_string)
    return client[db_name]


def insert_document(db: Database, collection: str, document: Dict[str, Any]) -> str:
    result = db[collection].insert_one(document)
    return str(result.inserted_id)


def find_document(db: Database, collection: str, query: Dict[str, Any]) -> Dict[str, Any]:
    return db[collection].find_one(query)
