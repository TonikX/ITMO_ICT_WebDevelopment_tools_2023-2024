**Подзадача 2: Вызов парсера из FastAPI**
- Эндпоинт в FastAPI для вызова парсера:
Необходимо добавить в FastAPI приложение ендпоинт, который будет принимать запросы с URL для парсинга от клиента, отправлять запрос парсеру (запущенному в отдельном контейнере) и возвращать ответ с результатом клиенту.

**Зачем:** Это позволит интегрировать функциональность парсера в ваше веб-приложение, предоставляя возможность пользователям запускать парсинг через API.

<hr>
<hr>

Парсер выведен в отдельный файл **parser.py** и, закономерно, прописан без использования sql уже.
```
from bs4 import BeautifulSoup
import requests
import re
from sqlalchemy.orm import Session
from models import Author, Title, Category


def parse_and_save(url: str, db: Session):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    recipe_blocks = soup.find_all('div', class_='emotion-etyz2y')

    for block in recipe_blocks:
        try:
            title = block.find('span', class_="emotion-1bs2jj2").text
            ingredients_text = block.find('button', class_="emotion-d6nx0p").text
            servings_text = block.find('span', class_="emotion-tqfyce").text
            cook_time = block.find('span', class_="emotion-14gsni6").text
            author_block = block.find('div', class_="emotion-ah73gc")
            author_name = author_block.find('span', class_="emotion-14tqfr").text.replace("Автор:", "").strip()
            author_link = author_block.find('a')['href']
            author_url = f"https://eda.ru{author_link}"  # Создаем полный URL для автора
            servings = int(re.search(r'\d+', servings_text).group())
            ingredients = int(re.search(r'\d+', ingredients_text).group())

            # Найти URL рецепта
            recipe_link = block.find('a', class_="emotion-18hxz5k")
            if recipe_link:
                recipe_url = recipe_link['href']
                cur_url = f"https://eda.ru{recipe_url}"  # Добавить базовый URL
            else:
                cur_url = None

            # Вставить данные автора и получить его id
            author = db.query(Author).filter_by(name=author_name).first()
            if not author:
                author = Author(name=author_name, author_url=author_url)
                db.add(author)
                db.commit()
                db.refresh(author)

            author_id = author.id

            # Вставить данные рецепта с id автора
            title_entry = Title(
                url=url,
                title=title,
                ingredients=ingredients,
                servings=servings,
                cook_time=cook_time,
                author_id=author_id,
                cur_url=cur_url
            )
            db.add(title_entry)
            db.commit()
            db.refresh(title_entry)

            # Парсинг и вставка категорий
            categories_block = block.find('ul', class_='emotion-1mceoyq')
            if categories_block:
                categories = categories_block.find_all('li')
                for category in categories:
                    category_name = category.find('span', class_='emotion-1h6i17m').text
                    category_link = category.find('a')['href']
                    category_url = f"https://eda.ru{category_link}"

                    # Вставить данные категории и получить ее id
                    category_entry = db.query(Category).filter_by(name=category_name).first()
                    if not category_entry:
                        category_entry = Category(name=category_name, url=category_url)
                        db.add(category_entry)
                        db.commit()
                        db.refresh(category_entry)

                    # Вставить связь между рецептом и категорией
                    title_entry.categories.append(category_entry)
                    db.commit()

        except AttributeError as e:
            print(f"Failed to parse block: {e}")
```

В **main.py** добавлен следующий путь:
```
@app.post("/parse/")
def parse_url(url: str, db: Session = Depends(get_db)):
    try:
        parse_and_save(url, db)
        return {"message": "Parser ran successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

Где-то здесь для оценки происходящего (и того, что все действительно работает) сначала в main.py появился следующий путь
```
@app.get("/сount/")
def count_titles(db: Session = Depends(get_db)):
    titles = db.query(Title).all()
    return {"message": f"Found {len(titles)} recipes"}
```
Чтобы убеждаться, что количество строк увеличилось => парсер действительно отработал. 

А потом мне стало интересно подглядывать, что вообще собирается, и потому добавила возможность открывать pgAdmin. Для этого в docker-compose.yml добавлено следующее:

```
  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    depends_on:
      - db
```