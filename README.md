# Proiect-Python-M1
Proiectul este o implementare simplă a unui sistem de gestionare a utilizatorilor, studenților și cursurilor, utilizând concepte de programare orientată pe obiecte în limbajul Python.

În proiect, avem următoarele clase principale:
1. `Persoana`: Aceasta este clasa de bază pentru utilizatori, studenți și profesori. Are un atribut `nume` și metode pentru serializare și deserializare.
2. `Utilizator`: Această clasă moștenește clasa `Persoana` și adaugă atribute specifice unui utilizator, cum ar fi `nume_utilizator`, `parola` și `rol`. De asemenea, are metode pentru serializare și deserializare.
3. `Student`: Această clasă moștenește clasa `Persoana` și adaugă atribute specifice unui student, cum ar fi `varsta` și `cod`. De asemenea, are metode pentru serializare și deserializare.
4. `Curs`: Această clasă reprezintă un curs și are atribute precum `nume` și `profesor`. `profesor` este un obiect de tip `Profesor`. Clasa `Curs` are metode pentru serializare și deserializare.
5. `Profesor`: Această clasă moștenește clasa `Persoana` și reprezintă un profesor. Are metode pentru serializare și deserializare.

În cadrul proiectului, fiecare clasă are metode pentru conversia obiectelor într-un format serializabil (dicționar) și conversia obiectelor din formatul serializat (dicționar) înapoi în obiecte.

Această arhitectură de clasă permite gestionarea utilizatorilor, inclusiv studenților și profesorilor, și a cursurilor asociate cu profesorii. Datele pot fi salvate și încărcate utilizând metodele de serializare și deserializare ale claselor.

Proiectul poate fi extins pentru a include funcționalități suplimentare, cum ar fi adăugarea de metode pentru manipularea datelor, stocarea datelor într-o bază de date sau adăugarea de interfețe de utilizator pentru interacțiunea cu sistemul.
