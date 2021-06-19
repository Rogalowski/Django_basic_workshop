from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from booking_rooms.models import Room


#MAIN MENU ROOM
#VIEW ROOMS
class MainMenu(View):
    def get(self, request):
        rooms = Room.objects.all()

        return render(request, 'booking_rooms_templates/main_menu_booking_rooms_html.html', context={'rooms': rooms})



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
        room = Room(name=room_name, capacity=room_capacity, projector=room_projector)
        room.save()

        return redirect('/main-menu-rooms')


#DELETE ROOM
class DeleteRoom(View):
    def get(self, request, room_id):

        room_del = Room.objects.get(id=room_id)

        rooms = Room.objects.all()
        html_response_delete_room = f"Room {room_del.id} - {room_del.name} has   been deleted from database"

        room_del.delete()

        #time.sleep(5)
        return render(request, 'booking_rooms_templates/main_menu_booking_rooms_html.html', context={'html_response_delete_room': html_response_delete_room, 'rooms': rooms})

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