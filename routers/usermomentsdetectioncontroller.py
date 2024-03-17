# import logging


# from fastapi import APIRouter
# from service import usermomentsdetection

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

# formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")

# file_handler = logging.FileHandler("logs//user.log")
# file_handler.setFormatter(formatter)

# logger.addHandler(file_handler)


# router = APIRouter(tags=["Mock Test"], prefix="/momentdetection")


# @router.post("/userlivemomentsdetection")
# def livemomentdetection():
#     return usermomentsdetection.capture_video() 