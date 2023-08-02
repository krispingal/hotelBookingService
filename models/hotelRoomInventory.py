from dataclasses import dataclass
from app import db


@dataclass
class HotelRoomInventory(db.Model):
    __tablename__ = 'hotel_room_inventory'
    __table_args__ = (
        db.CheckConstraint('inventory >= booked'),
    )
    hotel_id: db.Mapped[int] = db.mapped_column(db.Integer, db.ForeignKey('hotel.id'), primary_key=True)
    room_id: db.Mapped[int] = db.mapped_column(db.Integer, db.ForeignKey('room.id'), primary_key=True)
    date: db.Mapped[date] = db.mapped_column(db.Date, primary_key=True)
    inventory: db.Mapped[int] = db.mapped_column(db.Integer, default=0)
    booked: db.Mapped[int] = db.mapped_column(db.Integer, default=0)