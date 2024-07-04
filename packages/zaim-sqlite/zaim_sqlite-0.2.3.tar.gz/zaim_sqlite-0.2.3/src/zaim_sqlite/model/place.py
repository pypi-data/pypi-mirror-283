from sqlalchemy import Column, String
from zaim_sqlite.model import BaseModel


class Place(BaseModel):
    """
    お店情報モデル
    """

    __tablename__ = "places"
    __table_args__ = {"comment": "お店情報のマスターテーブル"}

    name = Column(String(255), nullable=False)
    place_uid = Column(String(255), nullable=False)
