from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from booking_rooms.models import Room


#MAIN MENU ROOM
class MainMenu(View):
    def get(self, request):
        return render(request, 'booking_rooms_templates/main_menu_booking_rooms_html.html')

#ADDING NEW ROOMS FORM INTO DATABASE
class AddRoom(View):
    def get(self, request):

        #ADD ROOM FORM
        return render(request, 'booking_rooms_templates/add_room_html.html')

    #sprawdzić, czy nazwa sali, nie jest pusta,#}
    #sprawdzić, czy sala o podanej nazwie, nie istnieje już w bazie danych,#}
    #sprawdzić, czy pojemność sali jest liczbą dodatnią;#}
    #jeśli dane są poprawne, zapisać nową salę do bazy i przekierować użytkownika na stronę główną,#}
    #jeśli są niepoprawne, powinien wyświetlić użytkownikowi odpowiedni komunikat.#}

    def post(self, request):

        room_name = request.POST.get('room_name')
        room_capacity = request.POST.get('room_capacity')
        room_projector = request.POST.get('room_projector')


        #ROOM NAME VALIDATION
        if room_name == '' or room_capacity == '':
            error_name = "No provided name or/and capacity, please try again"
            return render(request, 'booking_rooms_templates/add_room_html.html', context={'error_name': error_name})

        #SET PROJECTOR: FALSE TRUE BY CHECKBOX TYPE 'ON' 'OFF'
        if room_projector == 'on':
            room_projector = True
        else:
            room_projector = False

        if int(room_capacity) <= 0:
            error_capacity = "Wrong capacity number (only integer and greater than 0, please try again"
            return render(request, 'booking_rooms_templates/add_room_html.html', context={'error_name': error_capacity})

        #room = Room.objects.all()
        room = Room(name=room_name, capacity=room_capacity, projector=room_projector)
        room.save()

        return redirect('/main-menu-rooms')

        # convertionType = request.POST.get('convertionType')
        # if convertionType == 'celcToFahr':
        #     celcToFahr = int(request.POST.get('degrees'))
        #     celc = f'Temperatura: {(celcToFahr - 32) / 2}'
        #     return render(request, 'temperature_class.html', context={'celc': celc})
        #
        # if convertionType == 'FahrToCelc':
        #     FahrToCelc = int(request.POST.get('degrees'))
        #     fahr = f'Fahrenheit: {FahrToCelc * 2 + 32}'
        #     return render(request, 'temperature_class.html', context={'fahr': fahr})