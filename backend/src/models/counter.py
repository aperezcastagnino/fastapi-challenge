from pydantic import BaseModel


class CounterPresentation(BaseModel):
    endpoint_name: str
    count: int
