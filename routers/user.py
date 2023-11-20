import logging
from io import BytesIO

import pandas as pd
from fastapi import APIRouter, File, HTTPException, UploadFile, status
from schema import EmailBody
from starlette.responses import JSONResponse
from smtplib import SMTP_SSL
from email.mime.text import MIMEText

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
OWN_EMAIL = ("kssrikumar180703@gmail.com",)
OWN_EMAIL_PASSWORD = "bddf cjjh xivz ipjk"

router = APIRouter(tags=["Users"], prefix="/user")


@router.post("/login")
def login(emailId: str, password: str):
    user: model.UserModel = db.collection1.find_one({"email": emailId})
    if not (user and hashing.verify_password(password, user["password"])):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token = auth.create_access_token(
        data={
            "mail": user["email"],
            "careerPath": user["carrer_path"],
            "user_id": user["_id"],
            "roles": [{"authority": "USER"}],
        }
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


# @router.post("/email")
# async def simple_send(body: EmailBody) -> JSONResponse:
#     msg = MIMEText(body.message, "html")
#     msg["Subject"] = body.subject
#     msg["From"] = f"Denolyrics <{OWN_EMAIL}>"
#     msg["To"] = body.to

#     port = 465  # For SSL

#     # Connect to the email server
#     server = SMTP_SSL("kssrikumar180703@gmail.com", port)
#     server.login(OWN_EMAIL, OWN_EMAIL_PASSWORD)

#     # Send the email
#     server.send_message(msg)
#     server.quit()
#     return JSONResponse(status_code=200, content={"message": "email has been sent"})
