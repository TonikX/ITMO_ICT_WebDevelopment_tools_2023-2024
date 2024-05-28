# Эндпоинты
Для прямого добавления изображений используется два эндпоинта из предыдущей лабораторной работы:
```Python
@router.post("/add_imgsource")
async def add_imgsource(imgsrc: BaseImageSource, session=Depends(get_session)):
    imgsrc = ImageSource.model_validate(imgsrc)
    cmd = select(ImageSource).where(ImageSource.url == imgsrc.url)
    if db_imgsrc := session.scalars(cmd).first():
        return db_imgsrc
    else:
        session.add(imgsrc)
        session.commit()
        session.refresh(imgsrc)
        return imgsrc


@router.post("/add_img")
async def add_img(img: BaseImage, session=Depends(get_session)):
    img = Image.model_validate(img)
    cmd = select(Image).where(Image.url == img.url)
    if not session.scalars(cmd).first():
        session.add(img)
        session.commit()
        session.refresh(img)
        return img
    raise HTTPException(status_code=409, detail="Row already exists")
```
Однако данные реализации работают с помощью Depends и сессий, а значит вызов их отдельным порядком может привести к ошибкам. Для решения возможных проблем будем производить передачу сессии при вызове API внутри функции:
```Python
@app.post("/scrape")
async def root(url: str, start: str, end: str, session=Depends(get_session)):
    if args := validate_input(None, url, start, end):
        c = AsyncScrape(*args)
        await c._calculate_async()
        for i in c.rows:
            print(f"append row: {i}")
            temp = await append_row(*i, session)
            print(temp)
        return {"message": "completed successfully"}
    return {"message": "invalid input"}


@app.get("/")
async def append_row(img_source, img_link, session=Depends(get_session)):
    img_source = BaseImageSource(url=img_source)
    img_source_json = await add_imgsource(img_source, session)
    if img_source_json.id:
        img = BaseImage(imagesource_id=img_source_json.id, url=img_link)
        result = await add_img(img, session)
        return f"Success, added data to db"
    return f"Somethin' went wrong"
```
Итого эндпоинт /scrape вызывает скрапер, класс скрапера в свою очередь возвращает список с данными для сохранения в БД по окончанию своей работы, append_row с декоратором эндпоинта FastAPI заносит данные возвращенные скрапером в БД с помощью передачи зависимости по цепочке к эндпоинтам /add_img и /add_imgsource.