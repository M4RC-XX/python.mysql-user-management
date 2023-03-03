import pymysql
import requests
import hashlib

#IP Adresse abrufen
IPAddr = requests.get('https://api.ipify.org').text

#Variablen anlegen
x = 0
success = 0
lock=0

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

#Loginversuche
while x<3 and success == 0 and lock==0:
    username_inp = input("Benutzername: ")
    password_inp = input("Passwort: ")
    #SHA512 Wert generieren
    password_inp2 = hashlib.sha512(password_inp.encode()).hexdigest()

    query = "SELECT * FROM useraccounts WHERE username=%s AND password=%s"
    cursor.execute(query, (username_inp, password_inp2))
    result = cursor.fetchone()

    if result:
        success = 1
    else:
        #Hochzählung der Versuche bei falscher Eingabe
        x = x + 1
        print("Login-Daten falsch!")
        print("Noch",3-x,"Anmeldeversuche übrig!")

#Login erfolgreich
if x<3 and lock==0:
    print("Anmeldung war erfolgreich!")

#Benutzer wird gesperrt (IP-Adresse wird auf die Blacklist geschrieben)
elif x==3 and lock==0:
    sperren = "insert into blacklist (ip) value ('{}')".format(IPAddr)
    cursor.execute(sperren)
    conn.commit()

    print("------------------------------------------")
    print("Du wurdest für 24 Stunden gesperrt!")
    print("Der Admin wird in kürze informiert.")
    #time.sleep(1)
    telegram_chat_id=YOUR_CHAT_ID
    telegram_bot_id='YOUR_BOT_ID'

    r = requests.get('https://api.telegram.org/bot{}/sendMessage?chat_id={}&text=Ein Benutzer mit der IP-Adresse {} hat sich versucht unauthorisiert einzuloggen -- Bitte überprüfen'.format(telegram_bot_id, telegram_chat_id, IPAddr))

#Benutzer hat bereits eine Sperre und somit direkt keine berechtigung sich anzumelden
else:
    print("Dein Zugang ist noch blockiert!")
    print("Versuche es morgen noch einmal!")

#Verbindung zur Datenbank wird wieder geschlossen
conn.close()
