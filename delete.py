import pymysql
import requests
import hashlib

#IP Adresse abrufen
IPAddr = requests.get('https://api.ipify.org').text

#MySQL Login
server = 'localhost'
database = 'useraccounts'
username = 'username'
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
    print("Benutzeraccount löschen:")
    username_inp = input("Benutzername: ")

    query = "SELECT * FROM useraccounts WHERE username=%s"
    cursor.execute(query, (username_inp))
    result = cursor.fetchone()

    if result:
        print("Sicher, dass du den Benutzer ",username_inp," wirklich löschen willst?")
        print("Wenn ja gib bitte dein Passwort ein")
        password_inp = input("Passwort: ")
    else:
        print("Dieser Benutzer existiert nicht!")

    #SHA512 Wert generieren
    password_inp2 = hashlib.sha512(password_inp.encode()).hexdigest()

    delete_user = 'DELETE FROM `useraccounts` WHERE username="{}" and password="{}"'.format(username_inp, password_inp2)
    cursor.execute(delete_user)
    conn.commit()

    query = "SELECT * FROM useraccounts WHERE username=%s AND password=%s"
    cursor.execute(query, (username_inp, password_inp2))
    result = cursor.fetchone()

    if result:
        print("Irgendwas ist schief gegangen :(")
    else:
        print("Benutzer ",username_inp," wurde erfolgreich gelöscht")

if lock==1:
    print("Du bist derzeit gesperrt")