from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
import model

# Replace these with your MongoDB connection details
mongo_host = "localhost"
mongo_port = 27017
mongo_db_name = "your_database_name"

# Create a MongoDB client and connect to your database
client = MongoClient(mongo_host, mongo_port)
database: Database = client[mongo_db_name]

# Create multiple collections
collection1_name = "collection1"
collection2_name = "collection2"

collection1: Collection[model.UserModel] = database["StudentDetails"]
collection2: Collection = database[collection2_name]
