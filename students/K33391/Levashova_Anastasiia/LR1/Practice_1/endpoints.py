# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, Field
# from typing import List, Optional
# from enum import Enum
# from datetime import datetime
#
# from models import Category, Note, Task
#
#
#
# # Эндпоинты для категорий
# @app.get("/categories", response_model=List[Category])
# def get_categories():
#     return db_categories
#
#
# @app.post("/category", response_model=Category)
# def create_category(category: Category):
#     db_categories.append(category)
#     return category
#
#
# @app.delete("/category/{category_id}")
# def delete_category(category_id: int):
#     for i, category in enumerate(db_categories):
#         if category.id == category_id:
#             db_categories.pop(i)
#             return {"status": "success", "message": "Category deleted"}
#     raise HTTPException(status_code=404, detail="Category not found")
#
#
# @app.put("/category/{category_id}", response_model=Category)
# def update_category(category_id: int, category: Category):
#     for i, cat in enumerate(db_categories):
#         if cat.id == category_id:
#             db_categories[i] = category
#             return category
#     raise HTTPException(status_code=404, detail="Category not found")
#
#
# # Эндпоинты для заметок
# @app.get("/notes", response_model=List[Note])
# def get_notes():
#     return db_notes
#
#
# @app.post("/note", response_model=Note)
# def create_note(note: Note):
#     db_notes.append(note)
#     return note
#
#
# @app.delete("/note/{note_id}")
# def delete_note(note_id: int):
#     for i, note in enumerate(db_notes):
#         if note.id == note_id:
#             db_notes.pop(i)
#             return {"status": "success", "message": "Note deleted"}
#     raise HTTPException(status_code=404, detail="Note not found")
#
#
# @app.put("/note/{note_id}", response_model=Note)
# def update_note(note_id: int, note: Note):
#     for i, nt in enumerate(db_notes):
#         if nt.id == note_id:
#             db_notes[i] = note
#             return note
#     raise HTTPException(status_code=404, detail="Note not found")