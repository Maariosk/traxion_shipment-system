import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
mongo_db = os.getenv("MONGO_DB", "shipment_db")

client = MongoClient(mongo_uri)
db = client[mongo_db]
