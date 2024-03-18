# from service.JobsService import getalljobtitles, add_job
# import model.Job
# import logging


# from fastapi import APIRouter

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

# formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")

# file_handler = logging.FileHandler("logs//user.log")
# file_handler.setFormatter(formatter)

# logger.addHandler(file_handler)


# router = APIRouter(tags=["Jobs"], prefix="/jobs")

# @router.post("/addjobs")
# def addjob(job: Job):
#     return add_job(job)