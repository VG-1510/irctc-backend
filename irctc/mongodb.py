from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["irctc_logs"]

api_logs = db["api_logs"]