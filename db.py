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


collection1: Collection[model.UserModel] = database["StudentDetails"]
collection2: Collection = database["AcademicInfo"]
collection3: Collection = database["CareerPaths"]
collection4: Collection = database["OverallPerformance"]
