from fastapi import FastAPI
from .routers import user,story,auth
from .import models
from .database import engine 
app = FastAPI(
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redocs",
    title="Worst_day_of_my_life API",
    openapi_url="/api/v1/openapi.json"
)

# models.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"Hello": "Worst day of my life"}


app.include_router(user.router)
app.include_router(story.router)
app.include_router(auth.router)
