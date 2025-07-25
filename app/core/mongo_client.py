from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB", "shipment_system")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
