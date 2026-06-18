from pymongo import MongoClient
from pymongo.server_api import ServerApi
from . import get_settings,Settings
from fastapi import Depends
def connect_mongodb(
    app_settings: Settings = get_settings()
):
    client = MongoClient(
        app_settings.MONGODB_URI,
        server_api=ServerApi("1")
    )

    try:
        client.admin.command("ping")
        print("Connected to MongoDB")
        return client
    except Exception as e:
        print(e)
        return None