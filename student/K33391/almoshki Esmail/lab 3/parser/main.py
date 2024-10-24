from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
import http3
import requests

app = FastAPI()


@app.get("/")
def main():
    return {"message": "Welcome To The Most Effective Parser of All Times"}


@app.post("/parse/")
async def parse(url: str):
    print("received", url)
    # Clean the URL to remove any unwanted characters
    # url = data.get('url')
    url = url.strip('"').strip("'")
    print(f"Received URL: {url}")  # Debugging output

    try:
        # Use httpx for asynchronous request
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        print(f"Response received from {url}")  # Debugging output

        # Parse the HTML response
        html = BeautifulSoup(response.text, features="html.parser")

        # Extract the title
        title = html.title.string if html.title else "Has no Title"
        print(f"Parsed title: {title}")  # Debugging output

        return {"message": "Parsing Completed", "parsed": title}

    except Exception as e:
        print(f"An unexpected error occurred: {
              str(e)}")  # Log unexpected errors")
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}")
