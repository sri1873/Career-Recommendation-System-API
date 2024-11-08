import csv
from pathlib import Path

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

import db

import service.analysisService 


def careerFit(result_list1):

    career_subjects = []
    path = Path(__file__).parent / "../data/CareerJobDatafinal.csv"

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

def semwise_marks(studentId):
        student_current_sem= int(db.collection1.find_one({"_id": studentId}).get("semester"))
        sem=student_current_sem
        print(student_current_sem)
        if sem == 1:
            subjectMarks = db.collection2.find_one({"student_id": studentId})["subject_marks"]
            result_list1 = [marks for marks in subjectMarks]
            return careerFit(result_list1)
        elif sem == 2:
            subjectMarksSem1 = db.collection2.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem2 = db.collection6.find_one({"student_id": studentId})["subject_marks"]
            subjectMarks=subjectMarksSem1+subjectMarksSem2
            result_list1 = [marks for marks in subjectMarks]
            return careerFit(result_list1)
        elif sem==3:
            subjectMarksSem1 = db.collection2.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem2 = db.collection6.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem3 = db.collection7.find_one({"student_id": studentId})["subject_marks"]
            subjectMarks=subjectMarksSem1+subjectMarksSem2+subjectMarksSem3
            result_list1 = [marks for marks in subjectMarks]
            return careerFit(result_list1)
        elif sem==4:
            subjectMarksSem1 = db.collection2.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem2 = db.collection6.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem3 = db.collection7.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem4 = db.collection8.find_one({"student_id": studentId})["subject_marks"]
            subjectMarks=subjectMarksSem1+subjectMarksSem2+subjectMarksSem3+subjectMarksSem4
            result_list1 = [marks for marks in subjectMarks]
            return careerFit(result_list1)
        elif sem==5:
            subjectMarksSem1 = db.collection2.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem2 = db.collection6.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem3 = db.collection7.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem4 = db.collection8.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem5 = db.collection9.find_one({"student_id": studentId})["subject_marks"]
            subjectMarks=subjectMarksSem1+subjectMarksSem2+subjectMarksSem3+subjectMarksSem4+subjectMarksSem5
            result_list1 = [marks for marks in subjectMarks]
            return careerFit(result_list1)
        elif sem==6:
            subjectMarksSem1 = db.collection2.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem2 = db.collection6.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem3 = db.collection7.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem4 = db.collection8.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem5 = db.collection9.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem6 = db.collection10.find_one({"student_id": studentId})["subject_marks"]
            subjectMarks=subjectMarksSem1+subjectMarksSem2+subjectMarksSem3+subjectMarksSem4+subjectMarksSem5+subjectMarksSem6
            result_list1 = [marks for marks in subjectMarks]
            return careerFit(result_list1)
        elif sem==7:
            subjectMarksSem1 = db.collection2.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem2 = db.collection6.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem3 = db.collection7.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem4 = db.collection8.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem5 = db.collection9.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem6 = db.collection10.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem7 = db.collection11.find_one({"student_id": studentId})["subject_marks"]
            subjectMarks=subjectMarksSem1+subjectMarksSem2+subjectMarksSem3+subjectMarksSem4+subjectMarksSem5+subjectMarksSem6+subjectMarksSem7
            result_list1 = [marks for marks in subjectMarks]
            return careerFit(result_list1)
        elif sem==8:
            subjectMarksSem1 = db.collection2.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem2 = db.collection6.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem3 = db.collection7.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem4 = db.collection8.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem5 = db.collection9.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem6 = db.collection10.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem7 = db.collection11.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem8 = db.collection12.find_one({"student_id": studentId})["subject_marks"]
            subjectMarks=subjectMarksSem1+subjectMarksSem2+subjectMarksSem3+subjectMarksSem4+subjectMarksSem5+subjectMarksSem6+subjectMarksSem7+subjectMarksSem8
            result_list1 = [marks for marks in subjectMarks]
            return careerFit(result_list1)
        else:
            print("no sem details of student")

def getCareerPaths():
    return list(db.collection3.find())


def add_careerpath(studentId, careerpath):
    db.collection1.update_one({"_id": studentId}, {"$set": {"carrer_path": careerpath}})
    student = db.collection1.find_one({"_id": studentId})
    if student:
        print(f"Updated career path for student {studentId}: {student['carrer_path']}")
    else:
        print("Student not found.")

    service.analysisService.semwise_overallperformance(studentId)


