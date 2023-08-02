from dataclasses import dataclass
from .room import Room
from .hotelRoomInventory import HotelRoomInventory
from .booking import Booking
from app import db


@dataclass
class Hotel(db.Model):
    __tablename__ = 'hotel'
    id: db.Mapped[int] = db.mapped_column(db.Integer, primary_key=True)
    name: db.Mapped[str] = db.mapped_column(db.String, nullable=False)
    address: db.Mapped[str] = db.mapped_column(db.String, nullable=False)
    city: db.Mapped[str] = db.mapped_column(db.String, nullable=False)
    zipcode: db.Mapped[str] = db.mapped_column(db.String, nullable=False)
    rooms: db.Mapped[list[Room]] = db.relationship(backref='hotel', lazy='select')
    hotel_room_inventories: db.Mapped[list[HotelRoomInventory]] = db.relationship(backref='hotel', lazy='select')
    bookings: db.Mapped[list[Booking]] = db.relationship(backref='hotel', lazy='select')

