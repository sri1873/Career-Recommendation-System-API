from fastapi import FastAPI
from routers import initialize

app = FastAPI()




app.include_router(initialize.router)
