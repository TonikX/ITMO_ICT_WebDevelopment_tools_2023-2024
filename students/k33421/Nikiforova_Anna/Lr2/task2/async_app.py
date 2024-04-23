from base import AbstractBaseScrapper, urls
from database import AsyncSession
from models import Coctail, Ingredient, Property
import httpx
import time
import asyncio
from sqlalchemy import select
import os


if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class AsyncScrapper(AbstractBaseScrapper):
    def __str__(self) -> str:
        return "AsyncScrapper"
    
    async def get_html(self, url: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        assert response.status_code == 200
        return response.text
    
    async def save_data(self, raw_data: dict) -> None:
        async with AsyncSession() as session:
            for coctail_data in raw_data["ITEMS"]:
                # Extract coctail data and keep only valid fields
                coctail_dict = {
                    "id": int(coctail_data.get("ID")),
                    "name": coctail_data.get("NAME"),
                    "name_ru": coctail_data.get("NAME_RU"),
                    "detail_text": coctail_data.get("DETAIL_TEXT", "").replace("<p>", "").replace("<\\/p>", "").replace("\t", ""),
                    "steps": "\n".join(coctail_data.get("STEPS", "")),
                    "price": coctail_data.get("PRICE")
                }
                
                # If this coctail already exists, we do not have to add it again
                statement = select(Coctail).where(Coctail.id == coctail_dict.get("id"))
                existing_coctail = (await session.execute(statement)).scalar()
                if existing_coctail:
                    continue
                
                # Extract ingredient data and keep only valid fields
                ingredient_data = coctail_data.get("INGREDIENTS", [])
                
                # Extract property data and keep only valid fields
                property_data = coctail_data.get("PROPERTIES", [])

                # Convert ingredient data into SQLAlchemy objects
                ingredients = []
                for ingredient_data_entry in ingredient_data:
                    # Check if ingredient already exists based on all available fields except for id
                    statement = select(Ingredient).where(
                        (Ingredient.name == ingredient_data_entry.get("NAME")) &
                        (Ingredient.unit == ingredient_data_entry.get("UNIT")) &
                        (Ingredient.unit_value == ingredient_data_entry.get("UNIT_VALUE")) &
                        (Ingredient.parts == ingredient_data_entry.get("PARTS"))
                    )
                    existing_ingredient = (await session.execute(statement)).scalar()
                    
                    if not existing_ingredient:
                        ingredient = Ingredient(
                            name=ingredient_data_entry.get("NAME"),
                            unit=ingredient_data_entry.get("UNIT"),
                            unit_value=ingredient_data_entry.get("UNIT_VALUE"),
                            parts=ingredient_data_entry.get("PARTS")
                        )
                        session.add(ingredient)
                    else:
                        ingredient = existing_ingredient

                    ingredients.append(ingredient)

                # Convert property data into SQLAlchemy objects
                properties = []
                for property_key, property_value in property_data.items():
                    # Check if property already exists based on all available fields except for id
                    statement = select(Property).where(
                        (Property.property_name == property_key) &
                        (Property.class_name == property_value.get("CLASS_NAME")) &
                        (Property.name == property_value.get("NAME")) &
                        (Property.value == property_value.get("VALUE"))
                    )
                    existing_property = (await session.execute(statement)).scalar()

                    if not existing_property:
                        property = Property(
                            property_name=property_key,
                            class_name=property_value.get("CLASS_NAME"),
                            name=property_value.get("NAME"),
                            value=property_value.get("VALUE")
                        )
                        session.add(property)
                    else:
                        property = existing_property

                    properties.append(property)

                # Update the coctail_dict with converted ingredients and properties
                coctail_dict["ingredients"] = ingredients
                coctail_dict["properties"] = properties

                # Create the Coctail object
                coctail = Coctail(**coctail_dict)
                session.add(coctail)

            # Commit changes after all coctails, ingredients, and properties are added
            await session.commit()
            
    async def process_url(self, url: str) -> None:
        html = await self.get_html(url)
        raw_data = self.parse_html(html)
        await self.save_data(raw_data)

    async def parse_and_save(self, urls: list[str]) -> float:
        start_time = time.time()
        await asyncio.gather(*(self.process_url(url) for url in urls))
        end_time = time.time()
        execution_time = end_time - start_time
        return execution_time


if __name__ == '__main__':
    print("Time:", asyncio.run(AsyncScrapper().parse_and_save(urls)))
