from dataclasses import dataclass
import datetime
from app import db


@dataclass
class Booking(db.Model):
    __tablename__ = 'booking'
    id: db.Mapped[int] = db.Column(db.Integer, primary_key=True)
    hotel_id: db.Mapped[int]  = db.mapped_column(db.ForeignKey('hotel.id'))
    room_id: db.Mapped[int] = db.mapped_column(db.ForeignKey('room.id'))
    start_date: db.Mapped[datetime.date] = db.mapped_column(db.Date)
    end_date: db.Mapped[datetime.date] = db.mapped_column(db.Date)
    guest_id: db.Mapped['Guest'] = db.Column(db.ForeignKey('guest.id'))
    status: db.Mapped[str] = db.mapped_column(db.String, nullable=False)