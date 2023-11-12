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
                suggestions.extend(
                    [
                        f"You are fit for {subject}",
                        f"Don't lose your confidence, prepare for other subjects to achieve your dream job",
                    ]
                )

            recommendations[subject] = suggestions

    return recommendations
