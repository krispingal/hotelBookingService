from flask import jsonify, request
from app import create_app, db
from models import Guest
from hotel import Hotel
from room import Room
from hotelRoomInventory import HotelRoomInventory
from booking import Booking
import random
from datetime import date, datetime, timedelta
from faker import Faker


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
    """For testing"""
    guests = Guest.query.all()
    return jsonify(guests)


# @app.route("/api/v1/hotel")
# def get_hotels():
#     """For testing"""
#     hotels = Hotel.query.all()
#     return jsonify(hotels)


@app.route("/api/v1/hotel", methods=['GET'])
def get_hotel():
    city = request.args.get("city")
    if not city: raise InvalidAPIUsage("City not provided!")
    hotels = Hotel.query.filter_by(city=city).all()
    return jsonify(hotels)


@app.route("/api/v1/room", methods=['GET'])
def get_rooms():
    hotel_id = request.args.get("hotelId")
    if not hotel_id: raise InvalidAPIUsage("HotelId not provided!")
    hotel = Room.query.filter_by(hotel_id=hotel_id).all()
    return jsonify(hotel)


@app.post("/api/v1/bookRoom")
def book_room():
    data = request.get_json()
    hotel_id = data['hotelId']
    guest_id = data['guestId']
    room_id = data['roomId']
    start_date = datetime.strptime(data['startDate'], '%m-%d-%Y').date()
    end_date = datetime.strptime(data['endDate'], '%m-%d-%Y').date()

    hotel = Hotel.query.filter_by(id=hotel_id)
    # room = hotel.rooms.
    print(hotel_id, guest_id, room_id, start_date, end_date)
    return jsonify({'bookingId': 2})
    

@app.post("/api/v1/cancelBooking")
def cancel_booking():
    data = request.get_json()
    print(data['bookingId'])
# @app.get("/hotelInventory/<int:hotel_id>")
# def get_hotel_room_inventory(hotel_id):
#     hotel_inventory = HotelRoomInventory.query.filter_by(hotel_id=hotel_id).all()
#     return jsonify(hotel_inventory)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

with app.app_context():
    db.create_all()
    
    start_date = date(2022, 6, 1)
    end_date = date(2022, 9, 1)
    start_id, end_id = 4, 309
    print(f'Starting data generation starting from {start_id} to {end_id}')
    
    for _ in range(1):
        h = Hotel.query.filter_by(id=random.randint(1, 308)).first()
        chosenRoom = random.choice(h.rooms)
        g = Guest.query.filter_by(id=random.randint(1, 101)).first()
        s = start_date + timedelta(random.randint(0, 86))
        e = s + timedelta(random.randint(0, 1))
        booking = Booking(hotel=h, guest=g, room=chosenRoom, start_date=s, end_date=e, status="ACTIVE")
        db.session.add(booking)
        for d in daterange(s, e):
            numUpdated = HotelRoomInventory.query.filter_by(hotel_id=h, room=chosenRoom, date=d)
        db.session.commit()
    print('Done')



    
    for i in range(start_id, end_id):
        
        for r in h.rooms:
            numRooms = random.randint(20, 50)
            for d in daterange(start_date, end_date):             
                newInventory = HotelRoomInventory(hotel=h, room=r, date=d, inventory=numRooms, booked=0)
                db.session.add(newInventory)
            db.session.commit()
    print(f'Completed data generation')


if __name__ == '__main__':
    app.run(debug=False)