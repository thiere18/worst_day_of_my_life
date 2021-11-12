from fastapi import FastAPI
from .routers import user , story
from .import models
from .database import engine 
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"Hello": "Worst day of my life"}


app.include_router(user.router)
app.include_router(story.router)
