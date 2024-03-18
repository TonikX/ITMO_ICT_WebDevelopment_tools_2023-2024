## что значит "создать api для профессий?"

from fastapi import FastAPI

from models import *

app = FastAPI()

temp_bd = [
    Warrior(id=1,
            race="director",
            name="Мартынов Дмитрий",
            level=12,
            profession=Profession(
                id=1,
                title="Влиятельный человек",
                description="Эксперт по всем вопросам"
            ),

            skills=[
                Skill(id=1,
                      name="Купле-продажа компрессоров",
                      description=""),

                Skill(id=2,
                      name="Оценка имущества",
                      description="")

            ]
            ),

    Warrior(
        id=2,
        race="worker",
        name="Андрей Косякин",
        level=12,
        profession=Profession(
            id=1,
            title="Дельфист-гребец",
            description="Уважаемый сотрудник"
        ),
        skills=[]

    )
]


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/warriors_list")
def warriors_list() -> List[Warrior]:
    return temp_bd


@app.get("/warrior/{warrior_id}")
def warriors_get(warrior_id: int) -> List[Warrior]:
    return [warrior for warrior in temp_bd if warrior.id == warrior_id]


@app.post("/warrior")
def warriors_create(warrior: Warrior) -> TypedDict("Response", {"status": int, "data": Warrior}):
    warrior_to_append = warrior.model_dump()
    temp_bd.append(warrior_to_append)

    return {"status": 200, "data": warrior}


@app.delete("/warrior/delete{warrior_id}")
def warrior_delete(warrior_id: int):
    for i, warrior in enumerate(temp_bd):
        if warrior.id == warrior_id:
            temp_bd.pop(i)
            break

    return {"status": 201, "message": "deleted"}


@app.put("/warrior{warrior_id}")
def warrior_update(warrior_id: int, warrior: Warrior) -> List[Warrior]:
    for war in temp_bd:
        if war.id == warrior_id:
            warrior_to_append = warrior.model_dump()
            temp_bd.remove(war)
            temp_bd.append(warrior_to_append)

    return temp_bd
