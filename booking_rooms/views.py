from datetime import datetime

from django.contrib import messages

from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from booking_rooms.models import Room, RoomBooking


#MAIN MENU ROOM
#VIEW ROOMS
class MainMenu(View):
    def get(self, request):
        rooms = Room.objects.all()
        bookedrooms = RoomBooking.objects.all().order_by('date')
        #bookedrooms = RoomBooking.objects.filter(room_id)
        current_date = str(datetime.today().strftime('%B %d, %Y'))

        # for room in rooms:
        #     reservation_dates = [bookedrooms.date for bookedrooms in room.roombooking_set.all()]
        #     room.reserved = datetime.today() in reservation_dates

        return render(request, 'booking_rooms_templates/main_menu_booking_rooms_html.html',
                      context={'rooms': rooms, 'bookedrooms': bookedrooms, 'current_date': current_date})



#ADDING NEW ROOMS FORM INTO DATABASE
class AddRoom(View):
    def get(self, request):

        #ADD ROOM FORM
        return render(request, 'booking_rooms_templates/add_room_html.html')



    def post(self, request):

        room_name = request.POST.get('room_name')
        room_capacity = request.POST.get('room_capacity')
        room_projector = request.POST.get('room_projector')

        #ROOM VALIDATE IS EXIST IN DATABASE
        if Room.objects.filter(name=room_name).first():
            error_name = f"That room exist: {room_name}"
            return render(request, 'booking_rooms_templates/add_room_html.html', context={'error_name': error_name})

        #ROOM FILL NAME/CAPACITY VALIDATION
        if room_name == '' or room_capacity == '':
            error_name = "No provided name or/and capacity, please try again"
            return render(request, 'booking_rooms_templates/add_room_html.html', context={'error_name': error_name})


        #SET PROJECTOR: FALSE TRUE BY CHECKBOX TYPE 'ON' 'OFF'
        if room_projector == 'on':
            room_projector = True
        else:
            room_projector = False

        #ROOM CAPACITY VALIDATION
        if int(room_capacity) <= 0:
            error_capacity = "Wrong capacity number (only integer and greater than 0, please try again"
            return render(request, 'booking_rooms_templates/add_room_html.html', context={'error_name': error_capacity})

        #ROOM ADD TO DATABASE
        Room.objects.create(name=room_name, capacity=room_capacity, projector=room_projector)
        #room = Room(name=room_name, capacity=room_capacity, projector=room_projector)
        #room.save()

        return redirect('/main-menu-rooms')


#DELETE ROOM
class DeleteRoom(View):
    def get(self, request, room_id):

        room_del = Room.objects.get(id=room_id)
        room_del.delete()

        #MESSAGE AFTER DELETE ROOM FROM DATABASE IN MAIN MENU
        messages.add_message(request, messages.INFO, f'Room {room_del.name} has been deleted')
        return redirect('/main-menu-rooms')

class ModifyRoom(View):
    def get(self, request, room_id):
        room_mod = Room.objects.get(id=room_id)


        return render(request, 'booking_rooms_templates/modify_room_html.html', context={'room_mod': room_mod})

    def post(self, request, room_id):

        room_name = request.POST.get('room_name')
        room_capacity = request.POST.get('room_capacity')
        room_projector = request.POST.get('room_projector')


        #ROOM FILL NAME/CAPACITY VALIDATION
        if room_name == '' or room_capacity == '':
            error_name = "No provided name or/and capacity, please try again"
            return render(request, 'booking_rooms_templates/modify_room_html.html', context={'error_name': error_name})
        # ROOM VALIDATE IS EXIST IN DATABASE
        if Room.objects.filter(name=room_name).first():
            error_name = f"That room exist: {room_name}, provide another"
            return render(request, 'booking_rooms_templates/modify_room_html.html', context={'error_name': error_name})

        #SET PROJECTOR: FALSE TRUE BY CHECKBOX TYPE 'ON' 'OFF'
        if room_projector == 'on':
            room_projector = True
        else:
            room_projector = False

        #ROOM CAPACITY VALIDATION
        if int(room_capacity) <= 0:
            error_capacity = "Wrong capacity number (only integer and greater than 0, please try again"
            return render(request, 'booking_rooms_templates/modify_room_html.html', context={'error_name': error_capacity})

        #ROOM MODIFY BY ROOM_ID TO DATABASE
        room = Room(id=room_id, name=room_name, capacity=room_capacity, projector=room_projector)
        room.save()

        return redirect('/main-menu-rooms')

class BookRoom(View):
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        bookedrooms = RoomBooking.objects.filter(room_id=room_id)


        return render(request, 'booking_rooms_templates/booking_room_html.html',
                      context={'room': room, 'bookedrooms': bookedrooms})


    def post(self, request, room_id):

        room = Room.objects.get(id=room_id)

        room_book_date = request.POST.get('room_book_date')
        comment = request.POST.get('comment')

        if room_book_date < str(datetime.today()):
            error_date = "Wrong data - from past, please try again"
            return render(request, 'booking_rooms_templates/booking_room_html.html',
                          context={'room': room, 'error_date': error_date})


        if RoomBooking.objects.filter(room_id_id=room, date=room_book_date):
            error_date = "Room already booked this date, please try again"
            return render(request, 'booking_rooms_templates/booking_room_html.html',
                          context={'room': room, 'error_date': error_date})


        RoomBooking.objects.create(room_id_id=room_id, date=room_book_date, comment=comment)

        return redirect('/main-menu-rooms')


class Search(View):
    def get(self, request):


        current_date = str(datetime.today().strftime('%B %d, %Y'))

        rooms = Room.objects.all()


        room_name = request.GET.get('room_name')
        room_capacity = request.GET.get('room_capacity')
        room_projector = request.GET.get('room_projector')

        # SET PROJECTOR: FALSE or TRUE BY CHECKBOX TYPE 'ON' 'OFF'
        if room_projector == 'on':
            room_projector = True
        else:
            room_projector = False


        if room_capacity == '':
            room_capacity = 0

        #QUERY FILTERS BY NAME CAPACITY PROJECTOR AVAILABLE
        rooms = rooms.filter(name__icontains=room_name)
        rooms = rooms.filter(capacity__gt=room_capacity)
        rooms = rooms.filter(projector=room_projector)

        bookedrooms = RoomBooking.objects.all().order_by('date')


        return render(request, 'booking_rooms_templates/main_menu_booking_rooms_html.html',
                      context={'rooms': rooms, 'bookedrooms': bookedrooms, 'current_date': current_date})
