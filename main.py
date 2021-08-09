from typing import Optional
from os import listdir
import os.path
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from schemas import Translate
from slugify import slugify


app = FastAPI()
templates = Jinja2Templates(directory="templates")

def read_srt(path):
    content = ""
    with open(os.path.join('data', path), 'r', encoding="utf-8") as f:
        for i in range(12):
            content += f.readline()
    return content


@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('index.html', {"request": request, "id": id})


@app.get("/api/v2/files/get_slugify_id/{file_name}")
def get_slugify(file_name: str):
    return {"id" : slugify(file_name)}


@app.get("/api/v2/files")
def read_files(language: Optional[str] = "en", page: Optional[int] = None):
    directory_srt_list = listdir('data')
    if len(directory_srt_list) < 1:
        raise HTTPException(status_code=404, detail="Items not found")
    return [
        {
            "id": slugify(file_name),
            "name": file_name,
            "content": read_srt(file_name)} for
            file_name in directory_srt_list
    ]


@app.get("/api/v2/files/{file_id}")
def read_file_by_id(file_id: str):
    files_list = read_files()
    content = ""
    for file in files_list:
        if file["id"] == file_id:
            with open(os.path.join('data', file["name"]), 'r', encoding="utf-8") as f:
                for i in f.read():
                    content += i
            return{
                "id": file_id,
                "name": file["name"],
                "content": content.split("\n")
            }
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/api/v2/files/{file_id}")
def add_record(file_id: str, item: Translate):
    files_list = read_files()
    path_to_file = ""
    lines = None
    for file in files_list:
        if file["id"] == file_id:
            path_to_file = os.path.join('data', file["name"])
            with open(path_to_file, 'r', encoding="utf-8") as f:
                lines = f.read().splitlines()
            break
    if lines:
        for i in range(len(lines)):
            if lines[i] == item.record_id:
                lines[i+2] = item.record
                if lines[i+3] != "":
                    lines.pop(i+3)
                break
        with open(path_to_file, "w", encoding="utf-8") as f:
            f.writelines("%s\n" % line for line in lines)
        return item
    else: raise HTTPException(status_code=404, detail="Item not found")