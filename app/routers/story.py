from fastapi import APIRouter


router = APIRouter(prefix='/ff',tags=['stories'])

@router.get('/ffg')
def get_story():
    return {"message": "Storyf my life"}
