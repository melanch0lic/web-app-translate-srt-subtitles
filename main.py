from typing import Optional

from fastapi import FastAPI
from slugify import slugify

app = FastAPI()

files = [
    ("rick and morty 1", "content-1"),
    ("rick and morty 2", "content-2"),
    ("rick and morty 3", "content-3")]
test_data = [
    (slugify(file_name), file_name, file_content) for
    file_name,
    file_content in files]


@app.get("/files")
def read_files(language: Optional[str] = "en", page: Optional[int] = None):
    return [
        {
            "id": id_name, "name": file_name, "content": file_content} for
            id_name,
            file_name,
            file_content in test_data
    ]


@app.get("/files/{file_id}")
def read_file_by_id(file_id: str):
    for i in test_data:
        if i[0] == file_id:
            return{
                 "id": i[0], "name": i[1], "content": i[2]
            }
        return None


@app.post("/files/{file_id}")
def add__record():
    pass


    



