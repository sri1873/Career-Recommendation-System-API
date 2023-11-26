
import uuid

import db
import hashing

grade_mapping = {
    "A+": 4.0,
    "A": 3.7,
    "A-": 3.3,
    "B+": 3.0,
    "B": 2.7,
    "B-": 2.3,
    "C+": 2.0,
    "C": 1.7,
    "C-": 1.3,
    "D+": 1.0,
    "D": 0.7,
    "F": 0.0,
}


def convertMarks(file, markSys, year, semester):
    emails = []
    file["EMAIL"].fillna("False", inplace=True)
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
                    marks = grade_mapping.get(subjectMarks)
                    if marks != None:
                        marksObj["subject_marks"].append(
                            {column: grade_mapping.get(subjectMarks) * 25}
                        )
                    else:
                        marksObj["subject_marks"].append(
                            {column: grade_mapping.get(subjectMarks)}
                        )
                elif markSys == "OFF100":
                    marksObj["subject_marks"].append({column: subjectMarks})
                elif markSys == "CGPA_OFF_4":
                    marksObj["subject_marks"].append({column: subjectMarks * 25})
                elif markSys == "CGPA_OFF_10":
                    marksObj["subject_marks"].append({column: subjectMarks * 10})
        db.collection1.update_one(
            {"_id": id},
            {
                "$set": {
                    "user_name": userName,
                    "_id": id,
                    "email": email,
                    "password": hashed_password,
                    "academic_info": new_uuid,
                    "year": year,
                    "semester": semester,
                    "carrer_path": None,
                }
            },
            upsert=True,
        )
        db.collection2.update_one({"student_id": id}, {"$set": marksObj}, upsert=True)
        if email != "False":
            emails.append(email)
    return emails

def check_student_exists(year, semester):
    student = db.colection1.find_one({'year': year, 'semester': semester})
    return student is not None

def add_student_to_studentdetails_collection(student_details):
    db.collection1.insert_one(student_details)

def add_marks_to_softskill_collection(studentId, subjectMarks):
    db.collection5.insert_one({'student_id': studentId, 'marks_data': subjectMarks})

def parse_excel(file):
    
    for index in range(len(file)):
        userName = file.iloc[index]["STUDNAME"]
        id = file.iloc[index]["STUDENTID"]
        email = file.iloc[index]["EMAIL"]
        for column in file.columns:
            if column in ["S NO", "STUDNAME", "STUDENTID", "EMAIL", "PRGM"]:
                student_details = file.iloc[index]["S NO", "STUDNAME", "STUDENTID", "EMAIL", "PRGM"]
                continue
            else:
                subjectMarks = file.iloc[index][column]
        return student_details,subjectMarks

def uploadSoftSkill(file, year, semester):
    student_details, subjectMarks = parse_excel(file)

    student_exists = check_student_exists(year, semester)

    if student_exists:
        student = db.studentdetails.find_one({'year': year, 'semester': semester})
        add_marks_to_softskill_collection(student['_id'], marks_data)
    else:
        add_student_to_studentdetails_collection(student_details)

        new_student = db.studentdetails.find_one({'year': year, 'semester': semester})
        add_marks_to_softskill_collection(new_student['_id'], marks_data)

