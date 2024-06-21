#Миграции. Alembic

Настройка системы миграций с помощью библиотеки Alembic.

SQLModel был импортирован в файл `script.py.mako`

Для динамического получения пути к базе данных из файла `.env` в файле `env.py` был подгружен этот путь:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

config.set_main_option("sqlalchemy.url", os.getenv('DB_ADMIN'))
```

Далее переменная с путем была подтянута в файле `alembic.ini`:
```
sqlalchemy.url = %(DB_ADMIN)s
```