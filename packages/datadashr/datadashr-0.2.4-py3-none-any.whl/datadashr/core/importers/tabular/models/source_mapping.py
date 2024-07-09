from pydantic import BaseModel


class SourceMapping(BaseModel):
    source: str
    field: str
