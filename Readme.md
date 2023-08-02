# Hotel Booking Service

This is a MVP made to handle booking rooms for Hotels.
Flask will act as a the API server that will handle the requests.
Currently supported APIs

1. GetGuests
1. GetHotelsByCity
1. GetRoomsByHotel
1. GetBookings (for a single guest)
1. BookRoom
1. CancelBooking 

Entrypoint of the code is `routes.py`

## Stack

1. Flask
2. SqlAlchemy (for ORM)
3. Sqlite3

## Possible extensions
1. Update booking table to have `updatedOn` column and a current flag which would indicate the active record.
1. Expand booking functionality to handle booking of multiple rooms. Booking table can include number of rooms booked.
1. Use a city table and have it joined to hotel table.


