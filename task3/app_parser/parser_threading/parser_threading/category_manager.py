import threading
from sqlalchemy import select
from parser_threading import models

class CategoryManager:
    def __init__(self, project_id, category_none_id):
        self._category_none_id = category_none_id
        self._project_id = project_id
        self._category_locks = {}
        self._category_ids = {}

    def _get_lock(self, category):
        """Retrieve a unique lock for each category."""
        if category not in self._category_locks:
            self._category_locks[category] = threading.Lock()
        return self._category_locks[category]

    def _find_category_obj_db(self, session, category_title):
        query = (
            select(models.Category)
            .where(models.Category.title == category_title)
            .where(models.Category.project_id == self._project_id)
        )
        results = session.exec(query)
        category_obj = results.first()
        if category_obj is None:
            return None
        return category_obj[0].id

    def _create_category_obj(self, session, category_title):
        category_data = {
            "project_id": self._project_id,
            "title": category_title,
            "description": None,
        }
        category_obj = models.Category.model_validate(category_data)
        session.add(category_obj)
        session.commit()
        session.refresh(category_obj)
        return category_obj.id


    def _get_id(self, session, category_title):
        
        category_id = self._category_ids.get(category_title)
        if category_id is not None:
            return category_id
        
        category_id = self._find_category_obj_db(session, category_title)
        if category_id is not None:
            return category_id
        
        category_id = self._create_category_obj(session, category_title)
        return category_id
    
    def get_id(self, session, category_title):
        if category_title is None:
            return self._category_none_id

        with self._get_lock(category_title):
            category_id = self._get_id(session, category_title)
            self._category_ids[category_title] = category_id
            return category_id
            
