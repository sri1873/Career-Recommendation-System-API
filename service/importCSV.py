import db, hashing
import uuid
import csv
import csv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from io import BytesIO
import json
from pathlib import Path


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


def careerFit(studentId):
    subjectMarks = db.collection2.find_one({"student_id": studentId})["subject_marks"]
    result_list1 = [marks for marks in subjectMarks]

    career_subjects = []
    path = Path(__file__).parent / "../data/CareerJobData.csv"

    with path.open("r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            career_subjects.append(row)

    result_list2 = []
    for subject_marks in result_list1:
        for subject_name, mark in subject_marks.items():
            result_list2.append((subject_name, mark))

    career_subject_set = set(career_subjects[0][1:])

    filtered_result_list2 = []

    for subject in career_subjects[0][1:]:
        mark = 0.0
        if subject in career_subject_set:
            for subj, m in result_list2:
                if subj == subject:
                    mark = m
                    break
        filtered_result_list2.append((subject, mark))

    updated_marks = {}
    for subject, mark in filtered_result_list2:
        if subject in career_subject_set:
            career_subject_index = career_subjects[0].index(subject)
            career_subject_weight = float(career_subjects[1][career_subject_index])
            updated_mark = (mark / 100) * career_subject_weight
            updated_marks[subject] = updated_mark

    updated_marks_dict = {
        subject: updated_mark
        for subject, updated_mark in updated_marks.items()
        if subject
    }
    headers_updated_marks = career_subjects[0][1:]

    updated_marks_values = [
        updated_marks_dict.get(subject, 0.0) for subject in headers_updated_marks
    ]
    print(updated_marks_values)
    updated_marks_array = np.array(updated_marks_values).reshape(1, -1)
    career_subjects_array = np.array(career_subjects[1][1:]).reshape(1, -1)

    recommended_job_roles = []
    percentage_similarities = []

    # Calculate cosine similarity
    for i, job_role in enumerate(career_subjects[1:]):
        career_subject_values = np.array(job_role[1:], dtype=float).reshape(1, -1)
        cosine_sim = cosine_similarity(updated_marks_array, career_subject_values)

        if cosine_sim.shape == (1, 1):
            percentage_similarity = cosine_sim[0, 0] * 100
            recommended_job_roles.append(job_role[0])
            percentage_similarities.append(percentage_similarity)

    if recommended_job_roles:
        # top 3
        sorted_recommendations = sorted(
            zip(recommended_job_roles, percentage_similarities),
            key=lambda x: x[1],
            reverse=True,
        )[:3]
        top_3_recommendations = [
            {**db.collection3.find_one({"role": job}), "similarity": similarity}
            for job, similarity in sorted_recommendations
        ]
        return top_3_recommendations
    else:
        return "No job roles found in the career_subjects dataset."


def calculate_student_skill_gap(studentId):
    subjectMarks = db.collection2.find_one({"student_id": studentId})["subject_marks"]

    result_list1 = [marks for marks in subjectMarks]

    career_subjects = []
    with open(
        "C:/Users/grvn1/OneDrive/Desktop/Capstone/CareerJobData.csv",
        "r",
        encoding="utf-8",
    ) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            career_subjects.append([str(item) for item in row])

    student_job_role = db.collection1.find_one({"_id": studentId}).get("carrer_path")
    job_role_index = career_subjects[0].index("Job Title")
    job_role_subjects = None

    for idx, row in enumerate(career_subjects):
        if row[0] == student_job_role:
            job_role_index = idx
            break

    if job_role_index is None:
        return "Job role not found in the career data."

    job_role_subjects = {
        subject: float(mark)
        for subject, mark in zip(
            career_subjects[0][1:], career_subjects[job_role_index][1:]
        )
    }

    result_list2 = []
    for subject_marks in result_list1:
        for subject_name, mark in subject_marks.items():
            result_list2.append((subject_name, mark))

    career_subject_set = job_role_subjects

    filtered_result_list2 = []

    for subject in career_subjects[0][1:]:
        mark = 0.0
        if subject in career_subject_set:
            for subj, m in result_list2:
                if subj == subject:
                    mark = m
                    break
        filtered_result_list2.append((subject, mark))

    updated_marks = {}

    for subject, mark in filtered_result_list2:
        if subject in career_subject_set:
            career_subject_index = career_subjects[0].index(subject)
            career_subject_weight = float(
                career_subjects[job_role_index][career_subject_index]
            )
            updated_mark = (mark / 100) * career_subject_weight
            updated_marks[subject] = updated_mark

    mark_gaps = {}
    for subject, updated_mark in updated_marks.items():
        if subject in job_role_subjects:
            expected_marks = job_role_subjects[subject]
            if expected_marks != 0:
                mark_gap = ((expected_marks - updated_mark) / expected_marks) * 100
                mark_gaps[subject] = mark_gap
            else:
                mark_gaps[subject] = 0
    return mark_gaps


def calculate_student_overall_performance(studentId):
    subjectMarks = db.collection2.find_one({"student_id": studentId})["subject_marks"]

    result_list1 = [marks for marks in subjectMarks]

    career_subjects = []
    with open(
        "C:/Users/grvn1/OneDrive/Desktop/Capstone/CareerJobData.csv",
        "r",
        encoding="utf-8",
    ) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            career_subjects.append([str(item) for item in row])

    student_job_role = db.collection1.find_one({"_id": studentId}).get("carrer_path")

    job_role_index = career_subjects[0].index("Job Title")
    job_role_subjects = None

    for idx, row in enumerate(career_subjects):
        if row[0] == student_job_role:
            job_role_index = idx
            break

    if job_role_index is None:
        return "Job role not found in the career data."

    job_role_subjects = {
        subject: float(mark)
        for subject, mark in zip(
            career_subjects[0][1:], career_subjects[job_role_index][1:]
        )
    }

    result_list2 = []
    for subject_marks in result_list1:
        for subject_name, mark in subject_marks.items():
            result_list2.append((subject_name, mark))

    career_subject_set = job_role_subjects

    filtered_result_list2 = []

    for subject in career_subjects[0][1:]:
        mark = 0.0
        if subject in career_subject_set:
            for subj, m in result_list2:
                if subj == subject:
                    mark = m
                    break
        filtered_result_list2.append((subject, mark))

    updated_marks = {}

    for subject, mark in filtered_result_list2:
        if subject in career_subject_set:
            career_subject_index = career_subjects[0].index(subject)
            career_subject_weight = float(
                career_subjects[job_role_index][career_subject_index]
            )
            updated_mark = (mark / 100) * career_subject_weight
            updated_marks[subject] = updated_mark
    if subject in job_role_subjects:
        expected_marks = job_role_subjects[subject]

    overall_performance = sum(
        (
            expected_marks
            * (100 - ((expected_marks - updated_mark) / expected_marks) * 100)
        )
        / 100
        for subject, updated_mark in updated_marks.items()
        if subject in job_role_subjects and updated_mark != 0
    )
    return {"overall_performance": overall_performance}


def add_careerpath(studentId, careerpath):
    db.collection1.update_one({"_id": studentId}, {"$set": {"carrer_path": careerpath}})
    student = db.collection1.find_one({"_id": studentId})
    if student:
        print(f"Updated career path for student {studentId}: {student['carrer_path']}")
    else:
        print("Student not found.")


def getCareerPaths():
    return list(db.collection3.find())
