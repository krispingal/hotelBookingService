from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from app import create_app, db
from models import Guest, HotelRoomInventory, Hotel, Room, Booking

# Create an application instance
app = create_app()


class InvalidAPIUsage(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    return jsonify(e.to_dict()), e.status_code


@app.route("/api/v1/guest")
def get_guest():
    guests = Guest.query.all()
    return jsonify(guests)


@app.route("/api/v1/hotel", methods=['GET'])
def get_hotel():
    city = request.args.get("city")
    if not city: raise InvalidAPIUsage("City not provided as arg!")
    hotels = Hotel.query.filter_by(city=city).all()
    return jsonify(hotels)


@app.route("/api/v1/room", methods=['GET'])
def get_rooms():
    hotel_id = request.args.get("hotelId")
    if not hotel_id: raise InvalidAPIUsage("HotelId not provided as arg!")
    hotel = Room.query.filter_by(hotel_id=hotel_id).all()
    return jsonify(hotel)


@app.route("/api/v1/booking", methods=['GET'])
def get_bookings():
    guest_id: int = request.args.get("guestId")
    if not guest_id: raise InvalidAPIUsage("GuestId not provided as arg!")
    bookings = Guest.query.filter_by(id=guest_id).all()
    return jsonify(bookings)


@app.post("/api/v1/bookRoom")
def book_room():
    data = request.get_json()
    hotel_id: int = data['hotelId']
    guest_id: int = data['guestId']
    room_id: int = data['roomId']
    start_date = util.parseDate(data['startDate'])
    end_date = util.parseDate(data['endDate'])

    hotel: Hotel = db.session.execute(db.select(Hotel).filter_by(id=hotel_id)).scalar_one()
    guest: Guest = db.session.execute(db.select(Guest).filter_by(id=guest_id)).scalar_one()
    room: Room = db.session.execute(db.select(Room).filter_by(id=room_id)).scalar_one()

    try:
        for date in util.daterange(start_date=start_date, end_date=end_date):
            hotelRoomInventory = db.session.execute(db.select(HotelRoomInventory).filter_by(hotel=hotel, room=room, date=date)).scalar_one()
            hotelRoomInventory.booked += num_rooms
        booking = Booking(hotel=hotel, guest=guest, room=room, start_date=start_date, end_date=end_date, status="ACTIVE")
        db.session.add(booking)
        db.session.commit()
        return jsonify({'bookingId': booking.id, 'status': 'Booked'})
    except IntegrityError:
        print('Failed booking transaction')
        db.session.rollback()


@app.post("/api/v1/cancelBooking")
def cancel_booking():
    data = request.get_json()
    booking_id: int = data['bookingId']
    booking: Booking = db.session.execute(db.select(Booking).filter_by(id=booking_id)).scalar_one()
    hotel: Booking = db.session.execute(db.select(Booking).filter_by(id=booking.hotel_id)).scalar_one()
    room: Booking = db.session.execute(db.select(Booking).filter_by(id=booking.room_id)).scalar_one()
    try:
        start_date, end_date = booking.start_date, booking.end_date
        for date in util.daterange(start_date=start_date, end_date=end_date):
            hotelRoomInventory = db.session.execute(db.select(HotelRoomInventory).filter_by(hotel=hotel, room=room, date=date)).scalar_one()
            hotelRoomInventory.booked -= 1
        booking.status = 'CANCELLED'
        db.session.commit()
        return jsonify({'bookingId': booking.id, 'status': 'Cancelled'})
    except Exception:
        print(f'Failed cancelling booking: {booking_id}')
        db.session.rollback()

if __name__ == '__main__':
    app.run(debug=True)