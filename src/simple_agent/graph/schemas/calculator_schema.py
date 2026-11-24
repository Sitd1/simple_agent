from pydantic import BaseModel, Field


class CalculateInput(BaseModel):
    expression: str = Field(
        description="Арифметическое выражение, например '(2 + 3) * 4 / 5'. "
        "Поддерживаются + - * / // % ** и скобки."
    )
