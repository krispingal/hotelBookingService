from dataclasses import dataclass
from .booking import Booking
from app import db


@dataclass
class Guest(db.Model):
    __tablename__ = 'guest'
    id: db.Mapped[int] = db.mapped_column(db.Integer, primary_key=True)
    first_name: db.Mapped[str] = db.mapped_column(db.String, nullable=False)
    last_name: db.Mapped[str] = db.mapped_column(db.String, nullable=False)
    age: db.Mapped[int] = db.mapped_column(db.Integer, nullable=False)
    phone: db.Mapped[str] = db.mapped_column(db.String, nullable=False)
    bookings: db.Mapped[list[Booking]] = db.relationship(backref='guest', lazy='select')
