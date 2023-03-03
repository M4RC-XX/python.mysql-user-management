import pymysql
import requests
import hashlib
import tkinter
import customtkinter
from win10toast import ToastNotifier

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

createwin = customtkinter.CTk()  # create CTk window like you do with the Tk window
createwin.geometry("200x250")
createwin.title("Benutzer erstellen")

username_inp = customtkinter.CTkEntry(master=createwin, placeholder_text="Benutzername")
username_inp.pack(pady=10, padx=10)
username_inp.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

password_inp = customtkinter.CTkEntry(master=createwin, placeholder_text="Passwort")
password_inp.pack(pady=10, padx=10)
password_inp.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

toast = ToastNotifier()

def create():
    #IP Adresse abrufen
    IPAddr = requests.get('https://api.ipify.org').text

    #MySQL Login
    server = 'localhost'
    database = 'useraccounts'
    username = 'admin'
    password = 'password'

    conn = pymysql.connect(host=server, user=username, password=password, database=database)
    cursor = conn.cursor()

    #IP-Adresse auf Sperre überprüfen
    query = "SELECT ip FROM blacklist WHERE ip = %s"
    cursor.execute(query, (IPAddr,))
    result = cursor.fetchone()
    if result:
        lock=1
    else:
        lock=0

    if lock==0:
        print("Benutzeraccount erstellen:")
        #SHA512 Wert generieren
        password_inp2 = hashlib.sha512(password_inp.get().encode()).hexdigest()

        create_user = "insert into useraccounts (username, password) value ('{}', '{}')".format(username_inp.get(), password_inp2)
        cursor.execute(create_user)
        conn.commit()

        query = "SELECT * FROM useraccounts WHERE username=%s AND password=%s"
        cursor.execute(query, (username_inp.get(), password_inp2))
        result = cursor.fetchone()

        if result:
            print("Benutzer ",username_inp.get()," wurde erfolgreich erstellt")
            
            toast.show_toast(
                "Erfolgreich",
                "Das Benutzerkonto wurde erfolgreich angelegt.",
                duration = 20,
                threaded = True,
            )

        else:
            print("Irgendwas ist schief gegangen :(")

    if lock==1:
        print("Du bist derzeit gesperrt")

 
button = customtkinter.CTkButton(master=createwin, fg_color="green", text="Registrieren", command=create)
button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

createwin.mainloop()