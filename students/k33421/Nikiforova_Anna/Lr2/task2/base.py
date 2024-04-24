from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import httpx
from sqlalchemy import select
from database import Session
from models import Coctail, Ingredient, Property, ingredient_coctail_link


urls = ['https://luding.ru/cocktails/'] + [f'https://luding.ru/cocktails/?cocktails=page-{i}' for i in range(2, 12)]


class AbstractBaseScrapper(ABC):
    @abstractmethod
    def __str__(self) -> str:
        pass
    
    @abstractmethod
    def get_html(self, url: str) -> str:
        pass

    def parse_html(self, html: str) -> dict:
        soup = BeautifulSoup(html, features="html.parser")
    
        script_tags = soup.findAll('script')
        desired_script_tag = None

        for script_tag in script_tags:
            string_tag_repr = script_tag.string
            if string_tag_repr is not None and "JSCocktailsProducts" in string_tag_repr:
                desired_script_tag = string_tag_repr
                break
            
        if desired_script_tag:
            start_index = desired_script_tag.find("'ITEMS':")
            end_index = desired_script_tag.find(",'MARKUP':")

            json_string = '{' + desired_script_tag[start_index:end_index+1] + '}'
            return eval(json_string)
        
        return dict()
    
    @abstractmethod
    def save_data(self, data: dict) -> None:
        pass
    
    @abstractmethod
    def parse_and_save(self, urls: list[str]) -> None:
        pass


class AbstractSyncScrapper(AbstractBaseScrapper):
    @abstractmethod
    def __str__(self) -> str:
        pass
    
    def get_html(self, url: str) -> str:
        with httpx.Client() as client:
            response = client.get(url)
        assert response.status_code == 200
        return response.text

    def parse_html(self, html: str) -> dict:
        soup = BeautifulSoup(html, features="html.parser")
    
        script_tags = soup.findAll('script')
        desired_script_tag = None

        for script_tag in script_tags:
            string_tag_repr = script_tag.string
            if string_tag_repr is not None and "JSCocktailsProducts" in string_tag_repr:
                desired_script_tag = string_tag_repr
                break
            
        if desired_script_tag:
            start_index = desired_script_tag.find("'ITEMS':")
            end_index = desired_script_tag.find(",'MARKUP':")

            json_string = '{' + desired_script_tag[start_index:end_index+1] + '}'
            return eval(json_string)
        
        return dict()
    
    def save_data(self, raw_data: dict) -> None:
        with Session() as session:
            for coctail_data in raw_data["ITEMS"]:
                # Extract coctail data and keep only valid fields
                coctail_dict = {
                    "id": int(coctail_data.get("ID")),
                    "name": coctail_data.get("NAME"),
                    "name_ru": coctail_data.get("NAME_RU"),
                    "detail_text": coctail_data.get("DETAIL_TEXT", "").replace("<p>", "").replace("<\\/p>", "").replace(
                        "\t", ""),
                    "steps": "\n".join(coctail_data.get("STEPS", "")),
                    "price": coctail_data.get("PRICE")
                }

                # If this coctail already exists, we do not have to add it again
                statement = select(Coctail).where(Coctail.id == coctail_dict.get("id"))
                existing_coctail = session.execute(statement).scalar()
                if existing_coctail:
                    continue

                # Extract ingredient data
                ingredient_data = coctail_data.get("INGREDIENTS", [])
                ingredient_coctail_links = []

                # Extract property data 
                property_data = coctail_data.get("PROPERTIES", [])

                # Convert ingredient data into SQLAlchemy objects
                ingredients = []
                for ingredient_data_entry in ingredient_data:
                    # Check if ingredient already exists based on its name
                    statement = select(Ingredient).where(
                        Ingredient.name == ingredient_data_entry.get("NAME")
                    )
                    existing_ingredient = session.execute(statement).scalar()
                    if not existing_ingredient:
                        ingredient = Ingredient(
                            name=ingredient_data_entry.get("NAME")
                        )
                        session.add(ingredient)
                        session.commit()  # Commit to generate the ID
                    else:
                        ingredient = existing_ingredient
                        
                    # Create and cache ingredient_coctail_link object data
                    ingredient_coctail_link_entry = {
                        "ingredient_id": ingredient.id,
                        "coctail_id": coctail_dict["id"],
                        "unit": ingredient_data_entry.get("UNIT"),
                        "unit_value": ingredient_data_entry.get("UNIT_VALUE"),
                        "parts": ingredient_data_entry.get("PARTS")
                    }
                    ingredient_coctail_links.append(ingredient_coctail_link_entry)  # Will be possible to add only after coctail

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
                    existing_property = session.execute(statement).scalar()

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

                # Update the coctail_dict with converted properties
                coctail_dict["properties"] = properties

                # Create the Coctail object
                coctail = Coctail(**coctail_dict)
                session.add(coctail)
                session.commit()
                
                # Insert coctail-ingredinet data after the coctail has been added
                for ingredient_coctail_link_entry in ingredient_coctail_links:
                    session.execute(ingredient_coctail_link.insert().values(**ingredient_coctail_link_entry))
                
    
    @abstractmethod
    def parse_and_save(self, urls: list[str]) -> None:
        pass
    