from pymongo import MongoClient

MONGO_URI = "mongodb+srv://ashutoshkumarchy2002_db_user:Ashu%409128@cluster0.8vdcjdu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)

db = client["healthcare_db"]

predictions_collection = db["predictions"]

print("MongoDB Connected Successfully!")