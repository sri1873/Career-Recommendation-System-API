from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

import model

# Replace these with your MongoDB connection details

mongo_uri = "mongodb+srv://kssrikumar180703:Pa55w0rd@cluster0.tehiwwb.mongodb.net/Skill_Edu"
mongo_db_name = "Skill_Edu"

# Create a MongoDB client and connect to your database
client = MongoClient(mongo_uri)
database: Database = client[mongo_db_name]


collection1: Collection[model.UserModel] = database["StudentDetails"]
collection2: Collection = database["AcademicInfo"]
collection3: Collection = database["CareerPaths"]
collection4: Collection = database["OverallPerformance"]
