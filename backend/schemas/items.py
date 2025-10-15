from pydantic import BaseModel, field_validator


class ItemBase(BaseModel):
    name: str
    category: str
    value: float

    @field_validator("name", "category")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Field must not be empty")
        return v

    @field_validator("value")
    def positive_value(cls, v):
        if v <= 0:
            raise ValueError("Value must be positive")
        return v


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    item_id: int

    class Config:
        orm_mode = True
