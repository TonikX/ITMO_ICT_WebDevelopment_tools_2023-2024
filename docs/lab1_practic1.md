!!! example "Задание"
    Пошагово реализовать проект и методы, описанные в практике

    Создать для временной базы данных модели и API для профессий

=== "Эндпоинты"

    ``` py
    from fastapi import FastAPI
    from models import Warrior, RaceType, Profession, Skill
    from typing_extensions import TypedDict, List
    
    app = FastAPI()
    
    temp_bd = {
        "warriors": [
            {
                "id": 1,
                "race": "director",
                "name": "Мартынов Дмитрий",
                "level": 12,
                "profession": 1,
                "skills": [
                    {
                        "id": 1,
                        "name": "Купле-продажа компрессоров",
                        "description": ""
                    },
                    {
                        "id": 2,
                        "name": "Оценка имущества",
                        "description": ""
                    }
                ]
            },
            {
                "id": 2,
                "race": "worker",
                "name": "Андрей Косякин",
                "level": 12,
                "profession": 2,
                "skills": []
            }],
    
        "professions": [
            {
                "id": 1,
                "title": "Влиятельный человек",
                "description": "Эксперт по всем вопросам"
            },
            {
                "id": 2,
                "title": "Дельфист-гребец",
                "description": "Уважаемый сотрудник"
            }
        ]
    }
    
    
    @app.get("/warriors_list")
    def warriors_list() -> List[Warrior]:
        warriors = temp_bd["warriors"]
        return warriors
    
    
    @app.get("/warrior/{warrior_id}")
    def warriors_get(warrior_id: int) -> List[Warrior]:
        warriors = temp_bd["warriors"]
        return [warrior for warrior in warriors if warrior.get("id") == warrior_id]
    
    
    @app.post("/warrior")
    def warriors_create(warrior: Warrior) -> TypedDict('Response', {"status": int, "data": Warrior}):
        warrior_to_append = warrior.model_dump()
        temp_bd["warriors"].append(warrior_to_append)
        return {"status": 200, "data": warrior}
    
    
    @app.delete("/warrior/delete{warrior_id}")
    def warrior_delete(warrior_id: int):
        warriors = temp_bd["warriors"]
        for i, warrior in enumerate(warriors):
            if warrior.get("id") == warrior_id:
                temp_bd["warriors"].pop(i)
                break
        return {"status": 201, "message": "deleted"}
    
    
    @app.put("/warrior{warrior_id}")
    def warrior_update(warrior_id: int, warrior: Warrior) -> List[Warrior]:
        warriors = temp_bd["warriors"]
        for war in warriors:
            if war.get("id") == warrior_id:
                warrior_to_append = warrior.model_dump()
                temp_bd["warriors"].remove(war)
                temp_bd["warriors"].append(warrior_to_append)
        return temp_bd["warriors"]
    
    
    @app.get("/professions_list")
    def professions_list() -> List[Profession]:
        professions = temp_bd["professions"]
        return professions
    
    
    @app.get("/profession/{profession_id}")
    def professions_get(profession_id: int) -> List[Profession]:
        professions = temp_bd["professions"]
        return [profession for profession in professions if profession.get("id") == profession_id]
    
    
    @app.post("/profession")
    def profession_create(profession: Profession) -> TypedDict('Response', {"status": int, "data": Profession}):
        profession_to_append = profession.model_dump()
        temp_bd["professions"].append(profession_to_append)
        return {"status": 200, "data": profession}
    
    
    @app.put("/profession{profession_id}")
    def profession_update(profession_id: int, profession: Profession) -> List[Profession]:
        professions = temp_bd["professions"]
        for prof in professions:
            if prof.get("id") == profession_id:
                profession_to_append = profession.model_dump()
                temp_bd["professions"].remove(prof)
                temp_bd["professions"].append(profession_to_append)
        return temp_bd["professions"]
    
    
    @app.delete("/profession/delete{profession_id}")
    def profession_delete(profession_id: int):
        professions = temp_bd["professions"]
        for i, profession in enumerate(professions):
            if profession.get("id") == profession_id:
                temp_bd["professions"].pop(i)
                break
        return {"status": 201, "message": "deleted"}
    ```
    Описание работы -  
    Импортируем  FastAPI основной класс для создания приложения, модели и typedict с List
    temp_bd - словарь который используется как временная база данных
    И эндпоинты для создания, изменения или просмотра информации о профессиях

![](http://ung1n.github.io/ITMO_ICT_WebDevelopment_tools_2023-2024/img/lab1_and_practics/practic_1_profession.png)  
    Выводим список профессий

![](http://ung1n.github.io/ITMO_ICT_WebDevelopment_tools_2023-2024/img/lab1_and_practics/practic_1_profession_id.png)  
    Выводим профессию по id

![](http://ung1n.github.io/ITMO_ICT_WebDevelopment_tools_2023-2024/img/lab1_and_practics/practic_1_create.png)  
    Создаем нового человека

![](http://ung1n.github.io/ITMO_ICT_WebDevelopment_tools_2023-2024/img/lab1_and_practics/practic_1_PUT.png)  
    Меняем информацию

![](http://ung1n.github.io/ITMO_ICT_WebDevelopment_tools_2023-2024/img/lab1_and_practics/practic_1_DELETE.png)  
    Удаляем 


=== "Классы"

    ``` py
    from enum import Enum
    from typing import Optional, List
    from pydantic import BaseModel
    
    
    class RaceType(Enum):
        director = "director"
        worker = "worker"
        junior = "junior"
    
    
    class Profession(BaseModel):
        id: int
        title: str
        description: str
    
    
    class Skill(BaseModel):
        id: int
        name: str
        description: str
    
    
    class Warrior(BaseModel):
        id: int
        race: RaceType
        name: str
        level: int
        profession: int
        skills: Optional[List[Skill]] = []
    ```
    Описание работы -  
    Импортируем нужные библиотеки - Enum для перечислений, BaseModel для возможности создавать модели данных с валидацией
    Создаем модели данных для работы с профессиями, навыками и воинами в приложении


Это приложение на FastAPI позволяет управлять двумя сущностями — воинами и профессиями — с помощью стандартных операций 
CRUD (создание, чтение, обновление и удаление). Временная база данных хранится в памяти 
и не сохраняется между перезапусками приложения.
