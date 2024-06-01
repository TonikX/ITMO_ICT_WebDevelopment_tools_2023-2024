from fastapi import FastAPI, HTTPException
from parser_threading import parse_and_save

app = FastAPI()


@app.post("/parse")
def run_parser():
    try:
        result = parse_and_save()
        return {"message": "Parser ran successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
