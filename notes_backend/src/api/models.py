from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# PUBLIC_INTERFACE
class NoteBase(BaseModel):
    """Base fields shared by create and update models for a Note."""
    title: str = Field(..., description="Title of the note", min_length=1, max_length=200)
    content: str = Field(..., description="Content/body of the note", min_length=0)


# PUBLIC_INTERFACE
class NoteCreate(NoteBase):
    """Payload model to create a new note."""
    pass


# PUBLIC_INTERFACE
class NoteUpdate(BaseModel):
    """Payload model to update an existing note (partial update allowed)."""
    title: Optional[str] = Field(None, description="Updated title of the note", min_length=1, max_length=200)
    content: Optional[str] = Field(None, description="Updated content/body of the note", min_length=0)


# PUBLIC_INTERFACE
class Note(NoteBase):
    """Represents a Note resource returned by the API."""
    id: int = Field(..., description="Unique identifier for the note")
    created_at: datetime = Field(..., description="Timestamp when the note was created (UTC)")
    updated_at: datetime = Field(..., description="Timestamp when the note was last updated (UTC)")

    class Config:
        from_attributes = True
