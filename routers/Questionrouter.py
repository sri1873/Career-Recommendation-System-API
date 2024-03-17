import logging


from fastapi import APIRouter
from service.question import get_all_questions_and_marks_by_subject, evaluate_answers

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")

file_handler = logging.FileHandler("logs//user.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


router = APIRouter(tags=["Questions"], prefix="/questions")


@router.get("/getallquestions")
def getallquestions(studentId: str,subject: str):
    return get_all_questions_and_marks_by_subject(studentId,subject)


@router.put("/submitanswers")
def submitanswers(studentId: str,subject: str,submittedanswers: dict):
    return evaluate_answers(studentId,subject,submittedanswers)