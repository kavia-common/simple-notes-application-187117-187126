from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List

from fastapi import APIRouter, HTTPException, status

from .models import Note, NoteCreate, NoteUpdate

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
    responses={
        404: {"description": "Note not found"},
        422: {"description": "Validation Error"},
    },
)

# Lightweight in-memory store for notes
# This keeps data only for the lifecycle of the process (suitable for preview/testing).
_STORE: Dict[int, Note] = {}
_NEXT_ID: int = 1


def _now() -> datetime:
    """Return current UTC time with timezone info."""
    return datetime.now(timezone.utc)


def _allocate_id() -> int:
    """Allocate the next available integer ID for a note."""
    global _NEXT_ID
    nid = _NEXT_ID
    _NEXT_ID += 1
    return nid


# PUBLIC_INTERFACE
@router.post(
    "",
    response_model=Note,
    status_code=status.HTTP_201_CREATED,
    summary="Create a note",
    description="Create a new note with title and content.",
    responses={
        201: {"description": "Note created successfully"},
        400: {"description": "Bad request"},
    },
)
def create_note(payload: NoteCreate) -> Note:
    """
    Create and store a new note.

    Parameters:
    - payload: NoteCreate - The title and content for the note.

    Returns:
    - Note: The newly created note with assigned id and timestamps.
    """
    nid = _allocate_id()
    now = _now()
    note = Note(id=nid, title=payload.title, content=payload.content, created_at=now, updated_at=now)
    _STORE[nid] = note
    return note


# PUBLIC_INTERFACE
@router.get(
    "",
    response_model=List[Note],
    summary="List notes",
    description="Retrieve all notes in reverse chronological order (most recently updated first).",
)
def list_notes() -> List[Note]:
    """
    Retrieve all notes.

    Returns:
    - List[Note]: A list of notes sorted by updated_at descending.
    """
    return sorted(_STORE.values(), key=lambda n: n.updated_at, reverse=True)


# PUBLIC_INTERFACE
@router.get(
    "/{note_id}",
    response_model=Note,
    summary="Get a note",
    description="Retrieve a single note by its id.",
)
def get_note(note_id: int) -> Note:
    """
    Retrieve a single note by ID.

    Parameters:
    - note_id: int - The id of the note.

    Returns:
    - Note: The note with the requested id.

    Raises:
    - HTTPException 404 if not found.
    """
    note = _STORE.get(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


# PUBLIC_INTERFACE
@router.put(
    "/{note_id}",
    response_model=Note,
    summary="Replace a note",
    description="Replace a note's title and content entirely.",
)
def replace_note(
    note_id: int,
    payload: NoteCreate = ...,
) -> Note:
    """
    Replace an existing note (full update).

    Parameters:
    - note_id: int - The id of the note to replace
    - payload: NoteCreate - The new title and content

    Returns:
    - Note: The updated note

    Raises:
    - HTTPException 404 if the note is not found.
    """
    existing = _STORE.get(note_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    now = _now()
    updated = Note(
        id=note_id,
        title=payload.title,
        content=payload.content,
        created_at=existing.created_at,
        updated_at=now,
    )
    _STORE[note_id] = updated
    return updated


# PUBLIC_INTERFACE
@router.patch(
    "/{note_id}",
    response_model=Note,
    summary="Update a note",
    description="Partially update a note's title and/or content.",
)
def update_note(
    note_id: int,
    payload: NoteUpdate = ...,
) -> Note:
    """
    Partially update an existing note.

    Parameters:
    - note_id: int - The id of the note to update
    - payload: NoteUpdate - Fields to update

    Returns:
    - Note: The updated note

    Raises:
    - HTTPException 404 if the note is not found.
    """
    existing = _STORE.get(note_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    new_title = payload.title if payload.title is not None else existing.title
    new_content = payload.content if payload.content is not None else existing.content

    updated = Note(
        id=existing.id,
        title=new_title,
        content=new_content,
        created_at=existing.created_at,
        updated_at=_now(),
    )
    _STORE[note_id] = updated
    return updated


# PUBLIC_INTERFACE
@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a note",
    description="Delete a note by id.",
    responses={204: {"description": "Note deleted"}},
)
def delete_note(note_id: int) -> None:
    """
    Delete a note by ID.

    Parameters:
    - note_id: int - The id of the note to delete

    Returns:
    - None (204 No Content on success)

    Raises:
    - HTTPException 404 if the note is not found.
    """
    if note_id not in _STORE:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    del _STORE[note_id]
    return None
