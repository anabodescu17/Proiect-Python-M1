import json
from tkinter import *
from tkinter import messagebox
from datetime import datetime


class Persoana:
    def __init__(self, nume):
        self.nume = nume

    to_dict = lambda self: {"nume": self.nume}

    @staticmethod
    def from_dict(data):
        return Persoana(data["nume"])


class Utilizator:
    def __init__(self, nume_utilizator, parola, rol):
        self.nume_utilizator = nume_utilizator
        self.parola = parola
        self.rol = rol

    def to_dict(self):
        return {
            "nume_utilizator": self.nume_utilizator,
            "parola": self.parola,
            "rol": self.rol
        }

    @staticmethod
    def from_dict(data):
        return Utilizator(data["nume_utilizator"], data["parola"], data["rol"])


class Student(Persoana):
    def __init__(self, nume, varsta):
        super().__init__(nume)
        self.varsta = varsta
        self.cod = datetime.now().timestamp()

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "varsta": self.varsta,
            "cod": self.cod
        })
        return data

    @staticmethod
    def from_dict(data):
        return Student(data["nume"], data["varsta"])


class Curs:
    def __init__(self, nume, profesor):
        self.nume = nume
        self.profesor = profesor

    def to_dict(self):
        return {
            "nume": self.nume,
            "profesor": self.profesor.to_dict()
        }

    @staticmethod
    def from_dict(data):
        profesor = Profesor.from_dict(data["profesor"])
        return Curs(data["nume"], profesor)


class Profesor(Persoana):
    def __init__(self, nume):
        super().__init__(nume)

    def to_dict(self):
        return super().to_dict()

    @staticmethod
    def from_dict(data):
        return Profesor(data["nume"])


def incarca_utilizatori():
    try:
        with open("utilizatori.json", "r") as file:
            data = json.load(file)
            date_utilizatori = data.get("utilizatori", [])
            utilizatori = (Utilizator.from_dict(utilizator_data) for utilizator_data in date_utilizatori)
            return list(utilizatori)
    except FileNotFoundError:
        return []


def salveaza_utilizatori(utilizatori):
    data = {"utilizatori": [utilizator.to_dict() for utilizator in utilizatori]}
    with open("utilizatori.json", "w") as file:
        json.dump(data, file)


def incarca_date():
    try:
        with open("date.json", "r") as file:
            data = json.load(file)
            date_studenti = data.get("studenti", [])
            date_cursuri = data.get("cursuri", [])

            studenti = [Student.from_dict(student_data) for student_data in date_studenti]
            cursuri = [Curs.from_dict(curs_data) for curs_data in date_cursuri]

            return studenti, cursuri
    except FileNotFoundError:
        return [], []


def salveaza_date(studenti, cursuri):
    data = {}
    with open("date.json", "r") as file:
        data = json.load(file)

    data["studenti"] = [student.to_dict() for student in studenti]

    # Păstrăm cursurile existente în fișier
    date_cursuri = data.get("cursuri", [])
    cursuri_existente = [Curs.from_dict(curs_data) for curs_data in date_cursuri]
    cursuri_existente.extend(cursuri)
    data["cursuri"] = [curs.to_dict() for curs in cursuri_existente]

    with open("date.json", "w") as file:
        json.dump(data, file)


def autentificare(nume_utilizator, parola):
    utilizatori = incarca_utilizatori()
    for utilizator in utilizatori:
        if utilizator.nume_utilizator == nume_utilizator and utilizator.parola == parola:
            return utilizator
    return None


class FereastraAutentificare:
    def __init__(self, root):
        self.root = root
        self.label_nume_utilizator = Label(root, text="Nume utilizator:")
        self.label_nume_utilizator.pack()

        self.entry_nume_utilizator = Entry(root)
        self.entry_nume_utilizator.pack()

        self.label_parola = Label(root, text="Parola:")
        self.label_parola.pack()

        self.entry_parola = Entry(root, show="*")
        self.entry_parola.pack()

        self.button_autentificare = Button(root, text="Autentificare", command=self.autentificare)
        self.button_autentificare.pack()

    def autentificare(self):
        nume_utilizator = self.entry_nume_utilizator.get()
        parola = self.entry_parola.get()
        utilizator = autentificare(nume_utilizator, parola)
        if utilizator is None:
            messagebox.showerror("Eroare", "Nume utilizator sau parolă incorectă")
        else:
            self.root.destroy()
            FereastraPrincipala(utilizator)


class FereastraPrincipala:
    def __init__(self, utilizator):
        self.utilizator = utilizator

        self.root = Tk()
        self.root.title("Sistem de Gestionare a Studenților")

        self.label_student = Label(self.root, text="Nume student:")
        self.label_student.pack()

        self.entry_student = Entry(self.root)
        self.entry_student.pack()

        self.label_varsta = Label(self.root, text="Vârsta student:")
        self.label_varsta.pack()

        self.entry_varsta = Entry(self.root)
        self.entry_varsta.pack()

        self.button_adauga_student = Button(self.root, text="Adaugă student", command=self.adauga_student)
        self.button_adauga_student.pack()

        self.label_curs = Label(self.root, text="Nume curs:")
        self.label_curs.pack()

        self.entry_curs = Entry(self.root)
        self.entry_curs.pack()

        self.label_profesor = Label(self.root, text="Nume profesor:")
        self.label_profesor.pack()

        self.entry_profesor = Entry(self.root)
        self.entry_profesor.pack()

        if self.utilizator.rol == "admin":
            self.button_adauga_curs = Button(self.root, text="Adaugă curs", command=self.adauga_curs)
            self.button_adauga_curs.pack()

        self.label_studenti = Label(self.root, text="Studenți:")
        self.label_studenti.pack()

        self.listbox_studenti = Listbox(self.root)
        self.listbox_studenti.pack()

        self.label_cursuri = Label(self.root, text="Cursuri:")
        self.label_cursuri.pack()

        self.listbox_cursuri = Listbox(self.root)
        self.listbox_cursuri.pack()

        self.incarca_studenti()
        self.incarca_cursuri()

        self.root.mainloop()


    def incarca_studenti(self):
        studenti, _ = incarca_date()
        for student in studenti:
            self.listbox_studenti.insert(END, f"{student.nume} - {student.varsta} - {student.cod:.6f}")


    def incarca_cursuri(self):
        _, cursuri = incarca_date()
        for curs in cursuri:
            self.listbox_cursuri.insert(END, f"{curs.nume} - {curs.profesor.nume}")


    def adauga_student(self):
        nume = self.entry_student.get()
        varsta = self.entry_varsta.get()
        student = Student(nume, varsta)
        studenti, _ = incarca_date()
        studenti.append(student)
        self.listbox_studenti.insert(END, f"{student.nume} - {student.varsta}")
        self.entry_student.delete(0, END)
        self.entry_varsta.delete(0, END)
        salveaza_date(studenti, [])


    def adauga_curs(self):
        nume = self.entry_curs.get()
        nume_profesor = self.entry_profesor.get()
        profesor = Profesor(nume_profesor)
        _, cursuri = incarca_date()
        curs = Curs(nume, profesor)
        cursuri.append(curs)
        self.listbox_cursuri.insert(END, f"{curs.nume} - {curs.profesor.nume}")
        self.entry_curs.delete(0, END)
        self.entry_profesor.delete(0, END)
        salveaza_date([], cursuri)


root = Tk()
fereastra_autentificare = FereastraAutentificare(root)
root.mainloop()