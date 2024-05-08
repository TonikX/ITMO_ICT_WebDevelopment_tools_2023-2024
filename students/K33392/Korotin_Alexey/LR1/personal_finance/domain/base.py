from typing import List, Any


class Entity:
    id: int

    def __init__(self, id: int) -> None:
        self.id = id

    def __eq__(self, __value) -> bool:
        if not isinstance(__value, self.__class__):
            return False

        return self.id == __value.id


class AggregateRoot(Entity):
    def __init__(self, id: int) -> None:
        super().__init__(id)


class ValueObject:

    @property
    def _equality_attributes(self) -> List[Any]:
        raise NotImplementedError("Value object must implement equality attributes.")

    def __eq__(self, __value) -> bool:
        if not isinstance(__value, ValueObject):
            return False

        return self._equality_attributes == __value._equality_attributes


