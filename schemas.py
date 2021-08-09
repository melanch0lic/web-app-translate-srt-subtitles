from pydantic import BaseModel


class Translate(BaseModel):
    record_id: str
    record: str