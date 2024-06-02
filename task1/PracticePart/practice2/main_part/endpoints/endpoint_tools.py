from fastapi import HTTPException
import models
from sqlmodel import Session, select, SQLModel
import typing as tp


def add_object_to_db_and_refresh(session: Session, object: SQLModel):
    session.add(object)
    session.commit()
    session.refresh(object)


class ProjectValidator:
    _object = None

    def __init__(self, session, user_id, object_id):
        self._session = session
        self._user_id = user_id
        self._object_id = object_id
        self._project = self._retrieve_project()


    @property
    def object(self) -> models.Project:
        if self._object is None:
            self._object = self._retrieve_object_or_exception()
        return self._object

    def _retrieve_project(self) -> models.Project:
        return self.object

    def _retrieve_object_or_exception(self) -> models.Project:
        project = self._session.get(models.Project, self._object_id)
        if project is None:
            raise HTTPException(
                status_code=404,
                detail=f'Project with id={self.object.id} is not found'
            )
        return project

    def is_admin_or_exception(self):
        statement = select(models.ProjectUserLink) \
            .where(models.ProjectUserLink.user_id == self._user_id) \
            .where(models.ProjectUserLink.user_id == self._project.id)
        user_entries: tp.List[models.ProjectUserLink] = list(
            self._session.exec(statement).all()
        )
        for entry in user_entries:
            if entry.role == models.Role.admin:
                return
        raise HTTPException(
            status_code=403,
            detail=f'you\'re not admin of project with id={self._project.id}'
        )

    def is_in_project_or_exception(self):
        statement = select(models.ProjectUserLink) \
            .where(models.ProjectUserLink.user_id == self._user_id) \
            .where(models.ProjectUserLink.user_id == self._project.id)
        user_entries: tp.List[models.ProjectUserLink] = list(self._session.exec(statement).all())
        if len(user_entries) == 0:
            raise HTTPException(
                status_code=403,
                detail=f'You\'re not allowed to view project with id={self._project.id}'
            )


class CategoryValidator(ProjectValidator):

    def _retrieve_project(self) -> models.Project:
        return self.object.project

    def _retrieve_object_or_exception(self) -> models.Category:
        category = self._session.get(models.Category, self._object_id)
        if category is None:
            raise HTTPException(
                status_code=404,
                detail=f'Category with id={self._object_id} is not found'
            )
        return category


class TaskValidator(CategoryValidator):
    def _retrieve_project(self) -> models.Project:
        return self.object.category.project

    def _retrieve_object_or_exception(self) -> models.Task:
        task = self._session.get(models.Task, self._object_id)
        if task is None:
            raise HTTPException(
                status_code=404,
                detail=f'Task with id={self._object_id} is not found'
            )
        return task


#
# class ProjectValidator:
#     _object = None
#     super_instance = None
#
#     def __init__(self, session, user_id, object_id):
#         super_class = self.__class__.__bases__[0]
#         if super_class != object:
#             self.super_instance = super_class(session, user_id, object_id)
#         self._session = session
#         self._user_id = user_id
#         self._object_id = object_id
#         self._project = self._retrieve_project(object_id)
#
    # @property
    # def object(self):
    #     if self._object is None:
    #         self._object = self._retrieve_object_or_exception()
    #     return self._object
#
#
#     def _retrieve_project(self) -> models.Project:
#         return self.object
#
#     def _retrieve_object_or_exception(self, ) -> models.Project:
#         project = self._session.get(models.Project, self._object_id)
#         if project is None:
#             raise HTTPException(
#                 status_code=404,
#                 detail=f'Project with id={self.object.id} is not found'
#             )
#         return project
#
#     def is_admin_or_exception(self):
#         statement = select(models.ProjectUserLink) \
#             .where(models.ProjectUserLink.user_id == self._user_id) \
#             .where(models.ProjectUserLink.user_id == self._project.id)
#         user_entries: tp.List[models.ProjectUserLink] = list(
#             self._session.exec(statement).all()
#         )
#         for entry in user_entries:
#             if entry.role == models.Role.admin:
#                 return
#         raise HTTPException(
#             status_code=403,
#             detail=f'you\'re not admin of project with id={self._project.id}'
#         )
#
#     def is_in_project_or_exception(self):
#         statement = select(models.ProjectUserLink) \
#             .where(models.ProjectUserLink.user_id == self._user_id) \
#             .where(models.ProjectUserLink.user_id == self._project.id)
#         user_entries: tp.List[models.ProjectUserLink] = list(self._session.exec(statement).all())
#         if len(user_entries) == 0:
#             raise HTTPException(
#                 status_code=403,
#                 detail=f'You\'re not allowed to view project with id={self._project.id}'
#             )
#
#
# class CategoryValidator(ProjectValidator):
#
#     def _retrieve_project(self) -> models.Project:
#         category = self.object
#         project_id = category.project.id
#         return self.super_instance._retrieve_project(project_id)
#
#     def _retrieve_object_or_exception(self) -> models.Category:
#         category = self._session.get(models.Category, self._object_id)
#         if category is None:
#             raise HTTPException(
#                 status_code=404,
#                 detail=f'Category with id={category_id} is not found'
#             )
#         return category
#
#
# class TaskValidator(CategoryValidator):
#     def _retrieve_project(self, task_id: int) -> models.Project:
#         task = self._retrieve_object_or_exception(task_id)
#         category_id = task.category.id
#         return self.super_instance._retrieve_project(category_id)
#
#     def _retrieve_object_or_exception(self, task_id:int) -> models.Task:
#         task = self._session.get(models.Task, task_id)
#         if task is None:
#             raise HTTPException(
#                 status_code=404,
#                 detail=f'Task with id={task_id} is not found'
#             )
#         return task
