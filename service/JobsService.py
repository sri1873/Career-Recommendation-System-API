import db
from model import carrer_path

def get_students(careerpath):
        if careerpath: 
              students = db.collection1.find({"roles":"STUD", "carrer_path": careerpath})
        else:
              students = db.collection1.find({"roles":"STUD"})
    
        students_list = list(students)

        return students_list


def createcareerpath(career_path):
    try:
        db.collection3.add(carrer_path)
        return {"message": "Career path added successfully"}
    except Exception as e:
        return {"error": str(e)}
