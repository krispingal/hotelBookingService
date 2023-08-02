from dataclasses import dataclass
from .hotelRoomInventory import HotelRoomInventory
from .booking import Booking
from app import db


@dataclass
class Room(db.Model):
    __tablename__ = 'room'
    id: db.Mapped[int] = db.mapped_column(db.Integer, primary_key=True)
    hotel_id: db.Mapped[int] = db.Column(db.Integer, db.ForeignKey('hotel.id'))
    name: db.Mapped[str] = db.mapped_column(db.String, nullable=False)
    rate: db.Mapped[int] = db.mapped_column(db.Integer, db.CheckConstraint('rate >= 0'))
    room_inventories: db.Mapped[list[HotelRoomInventory]] = db.relationship(backref='room', lazy='select')
    bookings: db.Mapped[list[Booking]] = db.relationship(backref='room', lazy='select')