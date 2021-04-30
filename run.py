from fastapi import FastAPI
from db.db import init_image_db
from routes.v1 import app_v1

import time

time.sleep(15)

init_image_db()

app = FastAPI()
app.include_router(app_v1)

