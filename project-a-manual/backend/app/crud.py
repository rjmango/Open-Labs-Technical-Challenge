from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas

def fetch_db_note(note_id: int, db: Session) -> models.Note:
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return db_note

def stringify_taglist(tags: List[str]):
    return ",".join(tags)

def create_note(note: schemas.NoteCreate, db: Session):
    db_note = models.Note(title=note.title, body=note.body, tags=stringify_taglist(note.tags))
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_all_notes(skip:int, limit: int, db: Session):
    return db.query(models.Note).order_by(models.Note.updated_at.desc()).offset(skip).limit(limit).all()

def get_one_note(note_id: int, db: Session):
    return fetch_db_note(note_id, db)

def update_note(note_id: int, note: schemas.NoteUpdate, db: Session):
    db_note = fetch_db_note(note_id, db)
    db_note.title = note.title
    db_note.body = note.body
    db_note.tags = stringify_taglist(note.tags)
    db.commit()
    db.refresh(db_note)
    return db_note

def delete_note(note_id: int, db: Session):
    db_note = fetch_db_note(note_id, db)
    db.delete(db_note)
    db.commit()

def search_notes(tag: str | None, q: str | None, db: Session):
    query = db.query(models.Note)
    if tag:
        query = query.filter(models.Note.tags.ilike(f"%{tag}%"))
    if q:
        query = query.filter(
            (models.Note.title.ilike(f"%{q}%")) | (models.Note.body.ilike(f"%{q}%"))
        )
    return query.all()