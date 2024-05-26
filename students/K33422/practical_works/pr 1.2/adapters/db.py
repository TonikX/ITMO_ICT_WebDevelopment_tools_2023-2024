import typing

from fastapi import HTTPException


class SqlalchemyWorker:

    def __init__(self, session):
        self.session = session

    def create_object(self, created_object: typing.Any):
        self.session.add(created_object)
        self.session.commit()
        self.session.refresh(created_object)
        return created_object

    def get_object(self, query):
        response = self.session.exec(query).first()
        if not response:
            raise HTTPException(status_code=404, detail="Object not found")
        return response

    def get_objects(self, query):
        return self.session.exec(query).all()

    def patch_object(self, query, updated_data):
        get_object = self.get_object(query)
        profile_data = updated_data.model_dump(exclude_unset=True)
        for key, value in profile_data.items():
            setattr(get_object, key, value)
        self.session.add(get_object)
        self.session.commit()
        self.session.refresh(get_object)
        return get_object

    def delete_object(self, query):
        get_object = self.get_object(query)
        get_object.is_active = False
        self.session.commit()
