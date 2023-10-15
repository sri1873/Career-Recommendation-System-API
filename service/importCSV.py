import db,hashing

def convertMarks (file):
    
    for index in range(len(file)):
        hashed_password = hashing.get_password_hash("Pa55w0rd")
        userName=file.iloc[index]["STUDNAME"]
        id=file.iloc[index]["STUDENTID"]   
        email=(file.iloc[index]["EMAIL"])
        db.collection1.update_one({"_id": id},{"$set":{"user_name":userName,"_id":id,"email":email,"password":hashed_password}},upsert=True)
