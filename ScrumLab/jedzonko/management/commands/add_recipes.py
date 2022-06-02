from django.core.management import BaseCommand
from jedzonko.models import Recipe


class Command(BaseCommand):
    def handle(self, *args, **options):
        Recipe.objects.create(name='Rosół z kurczaka',
                              ingredients='świeża natka pietruszki, marchewka, korzeń pietruszki, '
                                          'Rosół z kury Knorr, krótki makaron',
                              method_of_preparing="Ugotuj makaron wg wskazówek na opakowaniu. Obierz i pokrój w plasterki marchewkę i pietruszkę."
                                          "Dodaj kostki rosołowe Knorr do 1 l wody. Zagotuj. Dodaj warzywa i gotuj przez 10 min."
                                          "Dodaj makaron i jeszcze raz zagotuj.Zupę serwuj posypaną posiekaną zieloną pietruszką.",
                              description='Dobry Przepis',
                              preparation_time=40,
                              votes=4
                              )

        Recipe.objects.create(name='Zapiekanki ala fastfood',
                              ingredients='dwie bagietki, ser zółty, salami, pieczarki , sol, pieprz',
                              method_of_preparing="Pieczarki i cebulę kroimy w drobną kostkę (ilość zależna od"
                                          " gustu i ilości zapiekanek, należy jednak pamiętać, że pieczarki "
                                          "po usmażeniu tracą na objętości).Smażymy na maśle/oleju doprawiając solą i pieprzem. Ja zawsze smażę około 10 minut. Odlewamy nadmiar wody, gdy już gotowe.",
                              description='Bardzo Dobry Przepis',
                              preparation_time=60,
                              votes=5
                              )

        Recipe.objects.create(name='Słoik do pracy',
                              ingredients='arbuz, mięta, cytryna, mleko kokosowe',
                              method_of_preparing="Dodaję 1 łyżkę 18% mleka kokosowego i tak samo miksuję w sport-blenderze",
                              description='Dobry Przepis',
                              preparation_time=5,
                              votes=5
                              )
