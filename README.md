
 #### Zadanie rekrutacyjne - System do rezerwacji miejsc w hotelu.
 
![Screenshot 2021-09-16](https://user-images.githubusercontent.com/62106309/133615433-4ac6c2de-b797-4cd6-a6f7-12810c5201fa.png)


<ul>
 <li><a href="https://kamsec-django-hotel.herokuapp.com/">https://kamsec-django-hotel.herokuapp.com/</a> - Front end</li>
 <li><a href="https://kamsec-django-hotel.herokuapp.com/api">https://kamsec-django-hotel.herokuapp.com/api</a> - API</li>
 <li><a href="https://kamsec-django-hotel.herokuapp.com/swagger">https://kamsec-django-hotel.herokuapp.com/swagger</a> - dokumentacja</li>
 <li><a href="https://github.com/kamsec/django-hotel">https://github.com/kamsec/django-hotel</a> - repozytorium na GitHubie (ta strona)</li>
 <li><a href="https://github.com/kamsec/django-hotel/blob/master/hotel/tests.py">https://github.com/kamsec/django-hotel/blob/master/hotel/tests.py</a> - testy</li>
</ul>


##### Treść zadania:

Z wykorzystaniem
- Python 3.x
- Django 1.x
- Django REST Framework
- Baza danych (dowolna)

Napisać API aplikacji webowej, która służyć będzie do obsługi hotelu. Stworzone API ma umożliwiać aplikacji:
- wyświetlanie tabeli ze wszystkimi pokojami
- wyświetlenie tabeli ze wszystkimi rezerwacjami
- dodanie, edycję, usunięcie nowego pokoju do bazy (z podstawową walidacją danych)
- dodanie, edycję, usunięcie rezerwacji (z podstawową walidacją danych)
- wyszukanie wszystkich rezerwacji spełniających określone kryteria (np. numer pokoju, nazwisko osoby na którą zrobiono rezerwację, datę rezerwacji)
- wskazanie ile czasu w dniach trwa dana rezerwacja
- wskazanie ile wynosi koszt danej rezerwacji

Założenia:
- tabela rezerwacji powinna zawierać między innymi początek i koniec trwania rezerwacji 
- za pomocą jednej rezerwacji można zarezerwować kilka pokojów
- przy tworzeniu rezerwacji API oczekuje konkretnego numeru pokoju (pokojów) do zarezerwowani
- pokoje posiadają klasy, każda klasa ma przyporządkowaną cenę za dzień; dla uproszczenia przyjmijmy ustalone ceny za klasy pokoi: A = 200, B = 150, C = 100 i D = 50

Rozwiązujący może poczynić dodatkowe założenia o ile nie są sprzeczne z powyższymi.

Aplikacja powinna mieć napisane testy. 

Opcjonalnie:
- aplikacja dysponuje prostym front endem (a nie tylko REST API)
- aplikacja działa i jest widoczna pod jakimś adresem URL (nie jest to tylko kod na githubie)
- aplikacja umożliwia użytkownikowi logowanie, wyróżniamy kategorie użytkowników: "klient" i "obsługa", tylko użytkownik należący do kategorii "obsługa" może dodawać, edytować i usuwać pokoje
- API jest udokumentowane zgodne z Open API
