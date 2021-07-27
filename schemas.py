from pydantic import BaseModel


class Translate(BaseModel):
    record_id: int
    record_timeframe: str
    record: str