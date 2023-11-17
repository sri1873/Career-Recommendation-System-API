import csv
from pathlib import Path

import db


def calculate_student_skill_gap(studentId):
    subjectMarks = db.collection2.find_one({"student_id": studentId})["subject_marks"]

    result_list1 = [marks for marks in subjectMarks]

    career_subjects = []
    path = Path(__file__).parent / "../data/CareerJobData.csv"

    with path.open("r", encoding="utf-8") as csv_file:
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
                mark_gaps[subject] = 100 - mark_gap

    return mark_gaps


def calculate_student_overall_performance(studentId):
    subjectMarks = db.collection2.find_one({"student_id": studentId})["subject_marks"]

    result_list1 = [marks for marks in subjectMarks]

    career_subjects = []
    path = Path(__file__).parent / "../data/CareerJobData.csv"

    with path.open("r", encoding="utf-8") as csv_file:
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

def getOverallPerformance(studentId):
    return db.collection4.find_one({"_id":studentId});

def recommendations(studentId):
    subjectMarks = db.collection2.find_one({"student_id": studentId})["subject_marks"]

    result_list1 = [marks for marks in subjectMarks]

    career_subjects = []
    path = Path(__file__).parent / "../data/CareerJobData.csv"

    with path.open("r", encoding="utf-8") as csv_file:
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

    recommendations = {}

    for subject, gap in mark_gaps.items():
        if gap >= 0:
            suggestions = []
            if gap > 50:
                suggestions.extend(
                    [
                        f"Consider Basics to intermediate courses in {subject}",
                        f"Explore real-world projects in {subject}",
                        f"Study more insights through practical implementations {subject}",
                        f"Work more on problem solving and logical thinking related to {subject}",
                        f"Be more focused on {subject} to achieve your dream job",
                    ]
                )

            elif 25 < gap <= 50:
                suggestions.extend(
                    [
                        f"Consider advanced courses in {subject}",
                        f"Explore real-world projects in {subject}",
                        f"Study more insights through practical implementations {subject}",
                    ]
                )

            elif 25 > gap < 0:
                suggestions.extend(
                    [
                        f"Brush up on {subject} wisely",
                        f"Practice more problems in {subject} in HackerRank or other platforms to keep consistency",
                    ]
                )

            elif gap == 0:
                continue

            recommendations[subject] = suggestions

    return recommendations


def get_rank_and_top3(studentId):
    student_job_role = db.collection1.find_one({"_id": studentId}).get("carrer_path")

    cursor = db.collection1.find({"carrer_path": student_job_role}, {"_id": 1})
    all_students = [student["_id"] for student in cursor]
    marks = db.collection4.find({"_id": {"$in": all_students}}, {"_id": 1, "performance": 1})

    all_marks = []
    for student in marks:
        latest_performance = sorted(student.get("performance", []), key=lambda x: x.get("label", ""), reverse=True)
        if latest_performance:
            all_marks.append({"_id": student["_id"], "actual_marks": latest_performance[-1].get("actual", 0)})

    print(all_marks)
    if len(all_marks) <= 1:
        return all_marks

    def quick_sort_descending(student_data):
        if len(student_data) <= 1:
            return student_data
        pivot = student_data[0]
        lesser = []
        equal = []
        greater = []
        for student in student_data:
            if student['actual_marks'] < pivot['actual_marks']:
                lesser.append(student)
            elif student['actual_marks'] == pivot['actual_marks']:
                equal.append(student)
            else:
                greater.append(student)
        return quick_sort_descending(greater) + equal + quick_sort_descending(lesser)

    pivot = all_marks[0]
    lesser = []
    equal = []
    greater = []
    for student in all_marks:
        if student['actual_marks'] < pivot['actual_marks']:
            lesser.append(student)
        elif student['actual_marks'] == pivot['actual_marks']:
            equal.append(student)
        else:
            greater.append(student)

    sorted_students = quick_sort_descending(greater) + equal + quick_sort_descending(lesser)

    rank_of_student = None
    for idx, student in enumerate(sorted_students, start=1):
        if student['_id'] == studentId:
            rank_of_student = idx
            break

    top_3_students = sorted_students[:3] if len(sorted_students) >= 3 else sorted_students

    if rank_of_student is not None and rank_of_student <= 3:
        top_3_students_formatted = [{
            "_id": student["_id"],
            "user_name": db.collection1.find_one({"_id": student["_id"]}).get("user_name"),
            "actual_marks": student["actual_marks"],
            "rank": idx + 1
        } for idx, student in enumerate(top_3_students)]
        return top_3_students_formatted
    else:
        student_rank = {
            "_id": studentId,
            "user_name": db.collection1.find_one({"_id": studentId}).get("user_name"),
            "actual_marks": sorted_students[rank_of_student - 1]["actual_marks"],
            "rank": rank_of_student
        }
        top_3_students_formatted = [{
            "_id": student["_id"],
            "user_name": db.collection1.find_one({"_id": student["_id"]}).get("user_name"),
            "actual_marks": student["actual_marks"],
            "rank": idx + 1
        } for idx, student in enumerate(top_3_students)]
        return top_3_students_formatted + [student_rank]