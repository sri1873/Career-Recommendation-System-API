import logging
from io import BytesIO

import pandas as pd
from fastapi import APIRouter, File, HTTPException, UploadFile, status
from schema import Login, UserDetails
from starlette.responses import JSONResponse
import yagmail

from schema import EmailSchema
import auth
import db
import hashing
import model
from service import importCSV

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")

file_handler = logging.FileHandler("logs//user.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

router = APIRouter(tags=["Users"], prefix="/user")


@router.post("/login")
def login(formdata: Login):
    user: model.UserModel = db.collection1.find_one({"email": formdata.email_id})
    if not (user and hashing.verify_password(formdata.password, user["password"])):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    user["roles"]= [{"authority": "USER"}],
    access_token = auth.create_access_token(
        data = user
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/initialize")
def startUp(markSys: str, year: str, semester: str, file: UploadFile = File()):
    contents = file.file.read()
    buffer = BytesIO(contents)
    df = pd.read_csv(buffer, skip_blank_lines=True)
    studentMails = importCSV.convertMarks(df, markSys, year, semester)
    buffer.close()
    file.file.close()
    return studentMails


@router.put("/updateuser")
def startUp(studentId: str, user: UserDetails):
    return importCSV.updateUser(studentId, user)


@router.get("/getuser")
def startUp(studentId: str,):
    return db.collection1.find_one({"_id": studentId})


@router.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:
    subject = "FastAPI Email"
    print(email.email)
    body = f"Your password is Pa55w0rd. Click <a href='https://skill-edu.netlify.app/'>here</a> to access."
    try:
        yag = yagmail.SMTP("kssrikumar180703@gmail.com", "bddf cjjh xivz ipjk")
        yag.send(
            to=email.email,
            subject=subject,
            contents=body,
        )
        yag.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
    return JSONResponse(status_code=200, content={"message": "email has been sent"})


@router.post("/uploadsoftskills")
def uploadSoftSkill(year: str, semester: str, file: UploadFile = File()):
    contents = file.file.read()
    buffer = BytesIO(contents)
    df = pd.read_csv(buffer, skip_blank_lines=True)
    student = importCSV.uploadSoftSkill(df, year, semester)
    buffer.close()
    file.file.close()
    return JSONResponse(status_code=200, content={"Successfully updated the marks"})
