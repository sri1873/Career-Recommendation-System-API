import logging
from io import BytesIO

import pandas as pd
from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from starlette.responses import JSONResponse

import auth
import db
import hashing
import model
import schema
from service import importCSV

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")

file_handler = logging.FileHandler("logs//user.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


conf = ConnectionConfig(
    MAIL_USERNAME="kssrikumar180703@gmail.com",
    MAIL_PASSWORD="bddf cjjh xivz ipjk",
    MAIL_FROM="kssrikumar180703@gmail.com",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

router = APIRouter(tags=["Users"], prefix="/user")


@router.post("/login")
def login(form_data: schema.Login):
    user: model.UserModel = db.collection1.find_one({"email": form_data.email_id})
    if not (user and hashing.verify_password(form_data.password, user["password"])):
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


@router.post("/email")
async def simple_send(email: schema.EmailSchema) -> JSONResponse:
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),
        body="Your password is Pa55w0rd",
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
