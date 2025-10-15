from sqlalchemy import Column, Integer, String, Float
from backend.db.database import Base


class Item(Base):
    __tablename__ = "items"
    item_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    value = Column(Float, nullable=False)
