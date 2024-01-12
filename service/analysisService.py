import csv
from pathlib import Path
from bson import ObjectId
import db
def calculate_student_skill_gap(result_list1,studentId):


    career_subjects = []
    path = Path(__file__).parent / "../data/CareerJobDatafinal.csv"

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


def calculate_student_overall_performance(result_list1,studentId):
    career_subjects = []
    path = Path(__file__).parent / "../data/CareerJobDatafinal.csv"

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
    print(job_role_subjects)
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
            if mark != 0.0:
             updated_mark = (mark / 100) * career_subject_weight
             updated_marks[subject] = updated_mark
    print("--------------------------updated marks---------------------")
    print(updated_marks)
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
    
    target_subjects = []
    path = Path(__file__).parent / "../data/TargetvaluesFinal.csv"
    with path.open( "r", encoding="utf-8") as target_file:
        target_reader = csv.reader(target_file)
        for row in target_reader:
            target_subjects.append([str(item) for item in row])

    job_role_index = target_subjects[0].index("Job Title")
    job_role_subjects_target = None

    for idx, row in enumerate(target_subjects):
        if row[0] == student_job_role:
            job_role_index = idx
            break

    if job_role_index is None:
        return "Job role not found in the target data."

    job_role_subjects_target = {
        subject: float(mark) 
        for subject, mark in zip(
            target_subjects[0][1:], target_subjects[job_role_index][1:]
        )
    }
    overall_performance_target = sum(
        (
            job_role_subjects[subject]
            * (100 - ((job_role_subjects[subject] - job_role_subjects_target[subject]) / job_role_subjects[subject]) * 100)
        )
        / 100
        for subject in job_role_subjects_target
        if subject in updated_marks and job_role_subjects_target[subject] != 0
    )
    
    return overall_performance,overall_performance_target

def serialize_doc(doc):
    # Convert ObjectId to string for serialization
    if "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])
    return doc

def semwise_overallperformance(studentId):
    student_current_sem= int(db.collection1.find_one({"_id": studentId}).get("semester"))
    print(student_current_sem)
    overall_results = {
        "_id": studentId,  
        "results": {}  
    }
    for sem in range(1, student_current_sem+1):
        if sem == 1:
            subjectMarks = db.collection2.find_one({"student_id": studentId})["subject_marks"]
            result_list1 = [marks for marks in subjectMarks]
        elif sem == 2:
            subjectMarksSem1 = db.collection2.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem2 = db.collection6.find_one({"student_id": studentId})["subject_marks"]
            subjectMarks=subjectMarksSem1+subjectMarksSem2
            result_list1 = [marks for marks in subjectMarks]
        elif sem==3:
            subjectMarksSem1 = db.collection2.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem2 = db.collection6.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem3 = db.collection7.find_one({"student_id": studentId})["subject_marks"]
            subjectMarks=subjectMarksSem1+subjectMarksSem2+subjectMarksSem3
            result_list1 = [marks for marks in subjectMarks]
        elif sem==4:
            subjectMarksSem1 = db.collection2.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem2 = db.collection6.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem3 = db.collection7.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem4 = db.collection8.find_one({"student_id": studentId})["subject_marks"]
            subjectMarks=subjectMarksSem1+subjectMarksSem2+subjectMarksSem3+subjectMarksSem4
            result_list1 = [marks for marks in subjectMarks]
        elif sem==5:
            subjectMarksSem1 = db.collection2.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem2 = db.collection6.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem3 = db.collection7.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem4 = db.collection8.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem5 = db.collection9.find_one({"student_id": studentId})["subject_marks"]
            subjectMarks=subjectMarksSem1+subjectMarksSem2+subjectMarksSem3+subjectMarksSem4+subjectMarksSem5
            result_list1 = [marks for marks in subjectMarks]
        elif sem==6:
            subjectMarksSem1 = db.collection2.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem2 = db.collection6.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem3 = db.collection7.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem4 = db.collection8.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem5 = db.collection9.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem6 = db.collection10.find_one({"student_id": studentId})["subject_marks"]
            subjectMarks=subjectMarksSem1+subjectMarksSem2+subjectMarksSem3+subjectMarksSem4+subjectMarksSem5+subjectMarksSem6
            result_list1 = [marks for marks in subjectMarks]
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
        else:
            print("no sem details of student")
        
        overall_perf, overall_perf_target = calculate_student_overall_performance(result_list1,studentId)
        
        semester_result = {
            "Object": {
                "target": overall_perf_target,
                "actual": overall_perf,
                "SEM": f"{sem}"
            }
        }
        overall_results["results"][f"SEM-{sem}"] = semester_result["Object"]
        
    serialized_result = serialize_doc(overall_results)

    existing_doc = db.collection4.find_one({"_id": studentId})

    if existing_doc:
        serialized_existing = serialize_doc(existing_doc)
        db.collection4.replace_one(serialized_existing, serialized_result)
    else:
        db.collection4.insert_one(serialized_result)

    return overall_results["results"]


def getOverallPerformance(studentId):
    semwise_overallperformance(studentId)
    semresults= db.collection4.find_one({"_id":studentId});
    if semresults:
        results_list = []
        for sem, data in semresults['results'].items():
            semr=data['SEM']
            results_list.append({
                'target': data['target'],
                'actual': data['actual'],
                'label': f"SEM-{semr}"
            })
        return {
            "_id": semresults["_id"],
            "results": results_list
        }
    else:
        return None


def recommendations(result_list1,studentId):

    career_subjects = []
    path = Path(__file__).parent / "../data/CareerJobDatafinal.csv"

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
    s_current_sem=db.collection1.find_one({"_id": studentId}).get("semester")
    cursor = db.collection1.find({"carrer_path": student_job_role,"semester":s_current_sem,},{"_id": 1})
    all_students = [student["_id"] for student in cursor]

    marks = db.collection4.find({"_id": {"$in": all_students}}, {"_id": 1, "results": 1})

    all_marks = []
    for student in marks:
     print(f"Processing student: {student['_id']}")
     results = student.get("results", {})
     sem=f"SEM-{s_current_sem}"
     current_sem_results = results.get(sem, {}) 
     if isinstance(current_sem_results, dict):
        label = current_sem_results.get("SEM", "")
        actual = current_sem_results.get("actual", 0)
        if label:
            all_marks.append({"_id": student["_id"], "actual_marks": actual})
     else:
        print(f"Ignoring non-dictionary result entry for semester {s_current_sem}: {current_sem_results}")

    sorted_marks = sorted(all_marks, key=lambda x: x.get("actual_marks", 0), reverse=True)
    print(f"Sorted Marks: {sorted_marks}")

    if len(sorted_marks) <= 1:
     print(f"Returning Marks: {sorted_marks}")
     return sorted_marks
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

def semwise_marks(studentId):
        student_current_sem= int(db.collection1.find_one({"_id": studentId}).get("semester"))
        sem=student_current_sem
        print(student_current_sem)
        if sem == 1:
            subjectMarks = db.collection2.find_one({"student_id": studentId})["subject_marks"]
            result_list1 = [marks for marks in subjectMarks]
            return recommendations(result_list1,studentId)
        elif sem == 2:
            subjectMarksSem1 = db.collection2.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem2 = db.collection6.find_one({"student_id": studentId})["subject_marks"]
            subjectMarks=subjectMarksSem1+subjectMarksSem2
            result_list1 = [marks for marks in subjectMarks]
            return recommendations(result_list1,studentId)
        elif sem==3:
            subjectMarksSem1 = db.collection2.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem2 = db.collection6.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem3 = db.collection7.find_one({"student_id": studentId})["subject_marks"]
            subjectMarks=subjectMarksSem1+subjectMarksSem2+subjectMarksSem3
            result_list1 = [marks for marks in subjectMarks]
            return recommendations(result_list1,studentId)
        elif sem==4:
            subjectMarksSem1 = db.collection2.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem2 = db.collection6.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem3 = db.collection7.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem4 = db.collection8.find_one({"student_id": studentId})["subject_marks"]
            subjectMarks=subjectMarksSem1+subjectMarksSem2+subjectMarksSem3+subjectMarksSem4
            result_list1 = [marks for marks in subjectMarks]
            return recommendations(result_list1,studentId)
        elif sem==5:
            subjectMarksSem1 = db.collection2.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem2 = db.collection6.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem3 = db.collection7.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem4 = db.collection8.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem5 = db.collection9.find_one({"student_id": studentId})["subject_marks"]
            subjectMarks=subjectMarksSem1+subjectMarksSem2+subjectMarksSem3+subjectMarksSem4+subjectMarksSem5
            result_list1 = [marks for marks in subjectMarks]
            return recommendations(result_list1,studentId)
        elif sem==6:
            subjectMarksSem1 = db.collection2.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem2 = db.collection6.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem3 = db.collection7.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem4 = db.collection8.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem5 = db.collection9.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem6 = db.collection10.find_one({"student_id": studentId})["subject_marks"]
            subjectMarks=subjectMarksSem1+subjectMarksSem2+subjectMarksSem3+subjectMarksSem4+subjectMarksSem5+subjectMarksSem6
            result_list1 = [marks for marks in subjectMarks]
            return recommendations(result_list1,studentId)
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
            return recommendations(result_list1,studentId)
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
            return recommendations(result_list1,studentId)
        else:
            print("no sem details of student")


def semwise_marks_for_skill_gap(studentId):
        student_current_sem= int(db.collection1.find_one({"_id": studentId}).get("semester"))
        sem=student_current_sem
        print(student_current_sem)
        if sem == 1:
            subjectMarks = db.collection2.find_one({"student_id": studentId})["subject_marks"]
            result_list1 = [marks for marks in subjectMarks]
            return calculate_student_skill_gap(result_list1,studentId)
        elif sem == 2:
            subjectMarksSem1 = db.collection2.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem2 = db.collection6.find_one({"student_id": studentId})["subject_marks"]
            subjectMarks=subjectMarksSem1+subjectMarksSem2
            result_list1 = [marks for marks in subjectMarks]
            return calculate_student_skill_gap(result_list1,studentId)
        elif sem==3:
            subjectMarksSem1 = db.collection2.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem2 = db.collection6.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem3 = db.collection7.find_one({"student_id": studentId})["subject_marks"]
            subjectMarks=subjectMarksSem1+subjectMarksSem2+subjectMarksSem3
            result_list1 = [marks for marks in subjectMarks]
            return calculate_student_skill_gap(result_list1,studentId)
        elif sem==4:
            subjectMarksSem1 = db.collection2.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem2 = db.collection6.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem3 = db.collection7.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem4 = db.collection8.find_one({"student_id": studentId})["subject_marks"]
            subjectMarks=subjectMarksSem1+subjectMarksSem2+subjectMarksSem3+subjectMarksSem4
            result_list1 = [marks for marks in subjectMarks]
            return calculate_student_skill_gap(result_list1,studentId)
        elif sem==5:
            subjectMarksSem1 = db.collection2.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem2 = db.collection6.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem3 = db.collection7.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem4 = db.collection8.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem5 = db.collection9.find_one({"student_id": studentId})["subject_marks"]
            subjectMarks=subjectMarksSem1+subjectMarksSem2+subjectMarksSem3+subjectMarksSem4+subjectMarksSem5
            result_list1 = [marks for marks in subjectMarks]
            return calculate_student_skill_gap(result_list1,studentId)
        elif sem==6:
            subjectMarksSem1 = db.collection2.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem2 = db.collection6.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem3 = db.collection7.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem4 = db.collection8.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem5 = db.collection9.find_one({"student_id": studentId})["subject_marks"]
            subjectMarksSem6 = db.collection10.find_one({"student_id": studentId})["subject_marks"]
            subjectMarks=subjectMarksSem1+subjectMarksSem2+subjectMarksSem3+subjectMarksSem4+subjectMarksSem5+subjectMarksSem6
            result_list1 = [marks for marks in subjectMarks]
            return calculate_student_skill_gap(result_list1,studentId)
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
            return calculate_student_skill_gap(result_list1,studentId)
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
            return calculate_student_skill_gap(result_list1,studentId)
        else:
            print("no sem details of student")