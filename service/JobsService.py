import db



def get_students(careerpath):
        if careerpath: 
              students = db.collection1.find({"roles":"STUD", "carrer_path": careerpath})
        else:
              students = db.collection1.find({"roles":"STUD"})
    
        students_list = list(students)

        return students_list
