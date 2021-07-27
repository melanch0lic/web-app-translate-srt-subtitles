from typing import Optional
from os import listdir
import os.path
from fastapi import FastAPI

app = FastAPI()


def read_srt(path):
    content = ""
    with open(os.path.join('data', path), 'r') as f:
        for i in range(12):
            content += f.readline()
    return content


@app.get("/files")
def read_files(language: Optional[str] = "en", page: Optional[int] = None):
    directory_srt_list = listdir('data')
    return [
        {
            "id": file_name_index,
            "name": directory_srt_list[file_name_index],
            "content": read_srt(directory_srt_list[file_name_index])} for
            file_name_index in range(len(directory_srt_list))
    ]


@app.get("/files/{file_id}")
def read_file_by_id(file_id: int):
    directory_srt_list = listdir('data')
    content = ""
    try:
        with open(os.path.join('data', directory_srt_list[file_id]), 'r') as f:
            for i in f.read():
                content += i
        return{
            "id": file_id,
            "name": directory_srt_list[file_id],
            "content": content
        }
    except Exception:
        return None


@app.post("/files/{file_id}")
def add_record():
    pass
