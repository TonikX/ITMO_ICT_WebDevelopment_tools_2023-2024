#Парсер

    from fastapi import FastAPI, HTTPException, Request
    import requests
    from bs4 import BeautifulSoup
    
    app = FastAPI()
    
    
    @app.post("/parse")
    async def parse_url(request: Request):
        data = await request.json()
        url = data.get("url")
        if not url:
            raise HTTPException(status_code=400, detail="URL is required")
    
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else "No title found"
            return {"url": url, "title": title}
        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=str(e))
