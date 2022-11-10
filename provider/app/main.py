import asyncio
import uvicorn
import json

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.config import settings

app = FastAPI(title=settings.SERVICE_NAME)

@app.post("/search")
async def search():
    await asyncio.sleep(settings.SLEEP_TIME)
    with open(settings.SOURCE_FILE, 'r') as f:
        data = f.read()
    json_data = json.loads(data)
    return JSONResponse(json_data)


if __name__ == "__main__":
    uvicorn.run('main:app', host=settings.SERVICE_HOST, port=settings.SERVICE_PORT)
