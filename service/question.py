from typing import List, Optional
import db
import requests
from fastapi import HTTPException

def get_all_questions_and_marks_by_subject(studentId, subject):
    try:
        questions_cursor = db.collection13.find({"subject": subject}, {"questions": 1, "_id": 0})

        formatted_questions = []
        for document in questions_cursor:
            questions_array = document.get("questions", [])
            for question in questions_array:
                formatted_question = {
                    "id": question.get("id"),
                    "question": question.get("question"),
                    "options": [
                        {"id": option.get("id"), "text": option.get("text")}
                        for option in question.get("options", [])
                    ],
                    "marks":question.get("marks")
                }
                formatted_questions.append(formatted_question)

        return formatted_questions
    except Exception as e:
        print('Error retrieving questions:', e)
        raise Exception('Internal Server Error')


def evaluate_answers(studentId,subject, submittedanswers):
    try:
        total_marks = 0
        questions = get_questions_by_subject(subject)
        if not questions:
            raise HTTPException(status_code=404, detail=f"No questions found for subject {subject}")

        for answer in submittedanswers.get("answers", []):
            question_id = answer.get("question_id")
            answer_id = answer.get("answer_id")

            question = next((q for q in questions if q["question_id"] == question_id), None)
            if question is None:
                raise HTTPException(status_code=404, detail=f"No question found with ID {question_id}")

            if answer_id == question["answer"]:
                total_marks += question["marks"]

        student_document  = db.collection2.find_one(
    {"student_id": studentId},
    {"subject_marks": 1, "_id": 0}
)

        subject_mark = None
        if student_document and 'subject_marks' in student_document:
          for mark_dict in student_document['subject_marks']:
            if subject in mark_dict:
             subject_mark = mark_dict[subject]
             break

        print(subject_mark)
        max_mock_marks = sum(question["marks"] for question in questions)
        scaling_factor = (100 - subject_mark) / max_mock_marks
        updated_marks = total_marks * scaling_factor
        final_marks = subject_mark + updated_marks
        print(final_marks)

        if subject_mark is not None:
          for mark_dict in student_document['subject_marks']:
            if subject in mark_dict:
               mark_dict[subject] = final_marks

        db.collection2.update_one(
    {"student_id": studentId},
    {"$set": {"subject_marks": student_document['subject_marks']}}
)  
        print(student_document)
        return {"total_marks": total_marks}
    except Exception as e:
        print('Error evaluating answers:', e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


def get_questions_by_subject(subject):
    try:
        questions_cursor = db.collection13.find({"subject": subject})
        questions = []
        for document in questions_cursor:
            for question_data in document.get("questions", []):
                question = {
                    "question_id": question_data.get("id"),
                    "answer": question_data.get("answer"),
                    "marks": question_data.get("marks")
                }
                questions.append(question)
        return questions
    except Exception as e:
        print('Error retrieving questions:', e)
       
