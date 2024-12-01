import uvicorn
from fastapi import FastAPI, Query, Body

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router_hotels
from src.api.auth import router_auth
from src.database import *

# from src.config import settings


# print(f'{settings.DB_NAME=}')

app = FastAPI()


app.include_router(router_auth)
app.include_router(router_hotels)



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)