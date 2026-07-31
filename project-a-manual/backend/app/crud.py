from sqlalchemy.orm import Session
from typing import List
import models, schemas

def stringify_taglist(tags: List[str]):
    return ",".join(tags)

def create_note(db: Session, note: schemas.NoteCreate):
    db_note = models.Note(title=note.title, body=note.body, tags=stringify_taglist(note.tags))
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note