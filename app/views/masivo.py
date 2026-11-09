from pydantic import BaseModel


class PoblarRequest(BaseModel):
    cantidad: int


class PoblarResponse(BaseModel):
    message: str
    status: int

class ResetResponse(BaseModel):
    message: str
    deleted_count: int