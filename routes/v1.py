from fastapi import APIRouter, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import aiofiles
import uuid
import os

from db.db import fetch_query, insert_command
from models.image import Image

app_v1 = APIRouter()
app_v1.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app_v1.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app_v1.post("/grabimage")
async def read_item(file_name: str = Form(None), keywords: str = Form(None)):
    record = fetch_query(file_name, keywords)
    return FileResponse(f'static/{record[0][0]}')

@app_v1.post("/uploadimg")
async def upload_image(img: UploadFile = File(...), tags: str = Form(None)):

    try:
        if tags:
            check = tags.split()
            # check for 20 char max
            for tag in check:
                if len(tag) > 20:
                    raise Exception("Tag is more than 20 characters")

        thisid = str(uuid.uuid4())
        
        # check the name length
        if len(img.filename) > 50:
            raise Exception("Name is more than 50 characters")

        file_extention = img.filename.split(".")[-1]
        thisid += "." + file_extention

        # store hashed filename in file system
        async with aiofiles.open(f"static/{thisid}", 'wb') as out_file:
            content = await img.read()
            await out_file.write(content)

        # send information to db
        insert_command(thisid, img.filename, tags)

        this_upload = {"uuid": thisid, "name": img.filename, "tags": tags}
        this_upload_model = Image(**this_upload)

        return this_upload_model

    except Exception as e:
        print(e)