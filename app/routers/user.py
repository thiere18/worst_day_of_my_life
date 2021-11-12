from fastapi import APIRouter

router= APIRouter(prefix='/ffg',tags=['user'])


@router.get('/col')
def get_user():
    return {"message ": "user of my life"}
