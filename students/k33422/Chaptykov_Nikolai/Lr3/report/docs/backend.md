# Запросы к бекенду
Создадим класс, чтобы отправлять пост-запросы на сохранение данных в БД и объявим инстанс этого класса
```Python
class BackendHandler:
    def __init__(self):
        self.url = "http://127.0.0.1:8000/" # базовый url
        self.session = requests.session() # можно добавить аутентификацию в дальнейшем

    def append_row(self, img_source, img_link):
        data = json.dumps({"url": img_source})
         # запрос на сохранения источника
        imgsource_req = self.session.post(self.url + 'add_imgsource', data=data)
        if imgsource_req.status_code == 200:
            data = json.dumps({"url": img_link, "imagesource_id": imgsource_req.json()['id']})
            # запрос на сохранение адреса изображения
            img_req = self.session.post(self.url + 'add_img', data=data)
            if img_req.status_code == 200:
                print('Added to backend')
            else:
                print(f"Image failed: {img_req.content}")
        else:
            print(f"Image source failed: {imgsource_req.content}")


backend = BackendHandler() # создаем инстанс
```