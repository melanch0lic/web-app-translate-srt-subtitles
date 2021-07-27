from typing import Optional
from os import listdir
import os.path
from fastapi import FastAPI
from schemas import Translate
from slugify import slugify


app = FastAPI()


def read_srt(path):
    content = ""
    with open(os.path.join('data', path), 'r', encoding="utf-8") as f:
        for i in range(12):
            content += f.readline()
    return content


@app.get("/api/v1/files")
def read_files(language: Optional[str] = "en", page: Optional[int] = None):
    directory_srt_list = listdir('data')
    return [
        {
            "id": slugify(directory_srt_list[file_name_index]),
            "name": directory_srt_list[file_name_index],
            "content": read_srt(directory_srt_list[file_name_index])} for
            file_name_index in range(len(directory_srt_list))
    ]


@app.get("/api/v1/files/{file_id}")
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
                "content": content
            }
    return None


@app.post("/api/v1/files/{file_id}")
def add_record(file_id: str, item: Translate):
    files_list = read_files()
    path_to_file = ""
    for file in files_list:
        if file["id"] == file_id:
            path_to_file = os.path.join('data', file["name"])
            with open(path_to_file, 'r', encoding="utf-8") as f:
                lines = f.read().splitlines()
            break
    if lines:
        for i in range(len(lines)):
            if lines[i] == item.record_timeframe:
                lines[i+1] = item.record
                if lines[i+2] != "":
                    lines[i+2] = ""
                break
        with open(os.path.join('data', file["name"]), "w", encoding="utf-8") as f:
            f.writelines("%s\n" % line for line in lines)
    return item
