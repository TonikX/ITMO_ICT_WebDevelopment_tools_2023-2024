from fastapi import FastAPI, HTTPException
import http3

app = FastAPI()


parser_url = "http://parser:8001/parse"


@app.get("/")
def main():
    return "That is the spirit"


@app.get("/parse-url/")
async def parse_url(url: str):
    url = url.strip('"')
    url = url.strip("'")
    async with http3.AsyncClient() as client:
        try:
            print("entered try")
            response = await client.post(parser_url, params={"url": url})
            print("recieved data from parser")
            response.raise_for_status()
            print("got status")
            return response.json()

        except http3.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code, detail=str(exc))

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"An error occurred: {str(e)}")
