from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import aiohttp

from connection import get_session
from utilities import extract_user_data
from models import User, UserSerialized

app = FastAPI()

@app.get("/")
async def home(session: AsyncSession = Depends(get_session)) -> UserSerialized:
    url = "https://randomuser.me/api/"
    
    async with aiohttp.ClientSession() as http_client:
        async with http_client.get(url) as response:
            if response.status == 200:
                data = await response.json()
            else:
                return {"error": f"Request failed with status code {response.status}."}
    
    user_data = extract_user_data(data["results"][0])
    user = User(email=user_data["email"],
                hashed_password=user_data["hashed_password"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"])
    
    session.add(user)
    await session.commit()
    await session.refresh(user)
    
    return UserSerialized(id=user.id,
                          email=user.email,
                          first_name=user.first_name,
                          last_name=user.last_name)
