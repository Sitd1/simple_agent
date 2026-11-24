from pydantic import BaseModel, Field


class AgentSchema(BaseModel):
    message: str = Field(..., description='Message text')
