import logging

from fastapi import APIRouter

from service import analysisService

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")

file_handler = logging.FileHandler("logs//user.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


router = APIRouter(tags=["Analysis"], prefix="/analysis")


@router.post("/skill-Gap-Analysis")
def SkilGap(studentId: str):
    return analysisService.calculate_student_skill_gap(studentId)


@router.post("/overallperformance")
def overall_performance(studentId: str):
    return analysisService.calculate_student_overall_performance(studentId)


@router.post("/recommendations")
def recommendations(studentId: str):
    return analysisService.recommendations(studentId)
