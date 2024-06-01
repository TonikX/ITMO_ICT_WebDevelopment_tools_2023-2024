from fastapi import FastAPI, HTTPException
from typing import List
from models import Hackathon, HackathonCreate, HackathonUpdate
from temp_bd import temp_bd

app = FastAPI()

hackathons_db: List[Hackathon] = temp_bd


@app.post("/hackathons/", response_model=Hackathon)
def create_hackathon(hackathon: HackathonCreate):
    hackathon_id = len(hackathons_db) + 1
    new_hackathon = Hackathon(hackathon_id=hackathon_id, **hackathon.dict())
    hackathons_db.append(new_hackathon)
    return new_hackathon


@app.get("/hackathons/", response_model=List[Hackathon])
def read_hackathons() -> List[Hackathon]:
    return hackathons_db


@app.get("/hackathons/{hackathon_id}", response_model=Hackathon)
def read_hackathon(hackathon_id: int) -> Hackathon:
    for hackathon in hackathons_db:
        if hackathon["hackathon_id"] == hackathon_id:
            return hackathon
    raise HTTPException(status_code=404, detail="Hackathon not found")


@app.put("/hackathons/{hackathon_id}", response_model=Hackathon)
def update_hackathon(hackathon_id: int, hackathon_update: HackathonUpdate):
    for index, hackathon in enumerate(hackathons_db):
        if hackathon["hackathon_id"] == hackathon_id:
            updated_hackathon_data = hackathon.copy(update=hackathon_update.dict(exclude_unset=True))
            hackathons_db[index] = updated_hackathon_data
            return updated_hackathon_data
    raise HTTPException(status_code=404, detail="Hackathon not found")


@app.delete("/hackathons/{hackathon_id}", response_model=None)
def delete_hackathon(hackathon_id: int):
    for index, hackathon in enumerate(hackathons_db):
        if hackathon["hackathon_id"] == hackathon_id:
            del hackathons_db[index]
            return
    raise HTTPException(status_code=404, detail="Hackathon not found")
