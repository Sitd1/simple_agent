from pydantic import BaseModel, Field


class ExampleSchema(BaseModel):
    message: str = Field(..., description='Message text')
