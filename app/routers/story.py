from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(prefix='/api/v1/stories',
                   tags=['stories']
                   )

@router.get('/')
def get_stories(db: Session= Depends(get_db), skip: int = 0, limit: int = 100):
    stories=db.query(models.Story).offset(skip).limit(limit).all()
    if not stories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No Stories for now")
    
    return stories


@router.get("/{id}", response_model=schemas.Story)
def get_story(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    story = db.query(models.Story).filter(models.Story.id == id).first()
    if not story:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"story with id: {id} was not found")
    return story


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Story)
def create_story(story: schemas.StoryCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_story = models.Story(owner_id=current_user.id, **story.dict())
    db.add(new_story)
    db.commit()
    db.refresh(new_story)

    return new_story


@router.put("/{id}", response_model=schemas.Story)
def update_story(id: int, updated_story: schemas.StoryCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    story_query = db.query(models.Story).filter(models.Story.id == id)

    story = story_query.first()

    if story == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"story with id: {id} does not exist")

    if story.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    story_query.update(updated_story.dict(), synchronize_session=False)

    db.commit()

    return story_query.first()




@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_story(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    story_query = db.query(models.Story).filter(models.Story.id == id)

    story = story_query.first()

    if story == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"story with id: {id} does not exist")

    if story.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    story_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)