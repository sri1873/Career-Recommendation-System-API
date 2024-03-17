import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import analysis, careerfitting, user , Questionrouter

app = FastAPI()
origins = [
    "http://localhost:3000",
    "https://skill-edu.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user.router)
app.include_router(careerfitting.router)
app.include_router(analysis.router)
app.include_router(Questionrouter.router)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)
