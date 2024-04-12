import random

from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
async def get_qa():
    try:
        with open("data.csv", "r", encoding="utf-8") as f:
            lines = f.readlines()
            if not lines:
                raise HTTPException(status_code=404, detail="No QA pairs found.")
            line = lines[random.randint(0, len(lines)-1)].strip()
            qa = line.split(",")
            if len(qa) < 2:
                raise HTTPException(status_code=500, detail="QA format error.")
            return {'q':qa[0], 'a':qa[1]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
