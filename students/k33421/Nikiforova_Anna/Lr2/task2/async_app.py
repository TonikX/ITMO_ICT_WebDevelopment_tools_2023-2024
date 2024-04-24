from base import AbstractBaseScrapper, urls
from database import AsyncSession
from models import Coctail, Ingredient, Property, ingredient_coctail_link
import httpx
import time
import asyncio
from sqlalchemy import select, func
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
                coctail_dict = {
                    "id": int(coctail_data.get("ID")),
                    "name": coctail_data.get("NAME"),
                    "name_ru": coctail_data.get("NAME_RU"),
                    "detail_text": coctail_data.get("DETAIL_TEXT", "").replace("<p>", "").replace("<\\/p>", "").replace(
                        "\t", ""),
                    "steps": "\n".join(coctail_data.get("STEPS", "")),
                    "price": coctail_data.get("PRICE")
                }

                statement = select(Coctail).where(Coctail.id == coctail_dict.get("id"))
                existing_coctail = (await session.execute(statement)).scalar()
                if existing_coctail:
                    continue

                ingredient_data = coctail_data.get("INGREDIENTS", [])
                ingredient_coctail_links = []

                property_data = coctail_data.get("PROPERTIES", [])

                for ingredient_data_entry in ingredient_data:
                    statement = select(Ingredient).where(Ingredient.name == ingredient_data_entry.get("NAME"))
                    existing_ingredient = (await session.execute(statement)).scalar()
                    
                    if not existing_ingredient:
                        ingredient = Ingredient(
                            name=ingredient_data_entry.get("NAME")
                        )
                        session.add(ingredient)
                        await session.flush()  # Flush to generate the ID
                    else:
                        ingredient = existing_ingredient

                    ingredient_coctail_link_entry = {
                        "ingredient_id": ingredient.id,
                        "coctail_id": coctail_dict["id"],
                        "unit": ingredient_data_entry.get("UNIT"),
                        "unit_value": ingredient_data_entry.get("UNIT_VALUE"),
                        "parts": ingredient_data_entry.get("PARTS")
                    }
                    ingredient_coctail_links.append(ingredient_coctail_link_entry)

                properties = []
                for property_key, property_value in property_data.items():
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

                coctail_dict["properties"] = properties

                coctail = Coctail(**coctail_dict)
                session.add(coctail)
                await session.flush()

                # Insert multiple rows into ingredient_coctail_link
                await session.execute(
                    ingredient_coctail_link.insert(),
                    [ic_link_entry for ic_link_entry in ingredient_coctail_links]
                )

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
