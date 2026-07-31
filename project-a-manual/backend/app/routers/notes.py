from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List

import schemas
from database import get_db
import crud

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/", response_model=schemas.NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    return crud.create_note(note, db)

@router.get("/", response_model=List[schemas.NoteOut])
def get_all_notes(skip: int = Query(0, ge=0), limit: int = Query(20, ge=20, le=100), db: Session = Depends(get_db)):
    return crud.get_all_notes(skip, limit, db)

@router.get('/{note_id}', response_model=schemas.NoteOut)
def get_one_note(note_id: int, db: Session = Depends(get_db)):
    return crud.get_one_note(note_id, db)

@router.put("/{note_id}", response_model=schemas.NoteOut)
def update_note(note_id: int, note: schemas.NoteUpdate, db: Session = Depends(get_db)):
    return crud.update_note(note_id, note, db)