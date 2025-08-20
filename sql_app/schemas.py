# FASTAPI側のモデル定義
import datetime
from pydantic import BaseModel, Field


class BookingCreate(BaseModel):
    user_id: int
    room_id: int
    booked_num: int
    strat_date_time: datetime.datetime
    end_date_time: datetime.datetime

class Booking(BaseModel):
    booking_id: int

    # SQLAlchemyなどormapperにも対応するための設定
    class Config:
        from_attributes= True

class UserCreate(BaseModel):
    username: str = Field(max_length=12)

class User(UserCreate):
    user_id: int

    class Config:
        from_attributes = True

class RoomCreate(BaseModel):
    room_name: str = Field(max_length=12)
    capacity: int

class Room(RoomCreate):
    room_id: int

    class Config:
        from_attributes = True