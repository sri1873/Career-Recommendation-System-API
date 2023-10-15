from fastapi import APIRouter,HTTPException, status,File, UploadFile
import logging
from service import importCSV
from io import BytesIO
import pandas as pd
import model, hashing,db,auth,schema
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('logs//user.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


# db = next(database.get_db())

router = APIRouter(
    tags=['Users'],
    prefix='/user'
)


@router.post('/login')
def login(form_data:schema.Login):
    user:model.UserModel = db.collection1.find_one({"email":form_data.email_id})
    if not(user and hashing.verify_password(form_data.password, user['password'])):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token = auth.create_access_token(
        data={"mail": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post('/initialize')
def startUp(file: UploadFile=File()):
    contents = file.file.read()
    buffer = BytesIO(contents)
    df = pd.read_csv(buffer,skip_blank_lines=True)
    importCSV.convertMarks(df)
    buffer.close()
    file.file.close()
    return {"access_token":"s", "token_type": "bearer"}