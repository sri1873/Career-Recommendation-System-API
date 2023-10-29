import db, hashing
import uuid


grade_mapping = {"A+": 4.0,"A": 3.7,"A-": 3.3,"B+": 3.0,"B": 2.7,"B-": 2.3,"C+": 2.0,"C": 1.7,"C-": 1.3,"D+": 1.0,"D": 0.7,"F": 0.0,}
def convertMarks(file, markSys,year,semester):
    emails=[]
    file["EMAIL"].fillna("False",inplace=True)
    for index in range(len(file)):
        new_uuid = str(uuid.uuid4())
        hashed_password = hashing.get_password_hash("Pa55w0rd")
        userName = file.iloc[index]["STUDNAME"]
        id = file.iloc[index]["STUDENTID"]
        email = file.iloc[index]["EMAIL"]
        marksObj = {"_id": new_uuid, "student_id": id, "subject_marks": []}
        for column in file.columns:
            if column in ["S NO", "STUDNAME", "STUDENTID", "EMAIL", "PRGM"]:
                continue
            else:
                subjectMarks = file.iloc[index][column]
                if markSys == "GRADE":
                    marks=grade_mapping.get(subjectMarks)
                    if marks != None:
                        marksObj["subject_marks"].append({column: grade_mapping.get(subjectMarks)*25})
                    else:
                        marksObj["subject_marks"].append({column: grade_mapping.get(subjectMarks)})
                elif(markSys=="OFF100"):
                    marksObj["subject_marks"].append({column: subjectMarks})
                elif(markSys=="CGPA_OFF_4"):
                    marksObj["subject_marks"].append({column: subjectMarks*25})
                elif(markSys=="CGPA_OFF_10"):
                    marksObj["subject_marks"].append({column: subjectMarks*10})
        db.collection1.update_one(
            {"_id": id},
            {
                "$set": {
                    "user_name": userName,
                    "_id": id,
                    "email": email,
                    "password": hashed_password,
                    "academic_info": new_uuid,
                    "year":year,
                    "semester":semester,
                    "carrer_path":None
                }
            },
            upsert=True,
        )
        db.collection2.update_one({"student_id": id}, {"$set": marksObj}, upsert=True)
        if(email!="False"):emails.append(email)
    return emails


def careerFit(studentId):
    subjectMarks=db.collection2.find_one({"student_id":studentId})["subject_marks"]
    result_list = [value for marks in subjectMarks for value in marks.values()]
    result_list1 = [marks for marks in subjectMarks]
    print(result_list )
    print(result_list1 )

