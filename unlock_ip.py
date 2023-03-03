import pymysql
import requests

#IP Adresse abrufen
IPAddr = requests.get('https://api.ipify.org').text

#MySQL Login
server = 'localhost'
database = 'useraccounts'
username = 'username'
password = 'password'

telegram_chat_id=#YOUR_CHAT_ID#
telegram_bot_id='YOUR_BOT_ID'

master="YOUT_MASTER_PASWWORD"

conn = pymysql.connect(host=server, user=username, password=password, database=database)
cursor = conn.cursor()

#IP-Adresse auf Sperre überprüfen
query = "SELECT ip FROM blacklist WHERE ip = %s"
cursor.execute(query, (IPAddr,))
result = cursor.fetchone()
if result:
    print("Deine IP-Adresse ({}) ist derzeit gesperrt".format(IPAddr))
    print("Zum entsperren bitte das Masterpasswort eingeben")
    master_pw=input("Master-Passwort: ")
    if master_pw==master:
        unlock = 'DELETE FROM `blacklist` WHERE ip="{}"'.format(IPAddr)
        cursor.execute(unlock)
        conn.commit()
        print("Du wurdest entsperrt! :)")
        r = requests.get('https://api.telegram.org/bot{}/sendMessage?chat_id={}&text=Jemand hat mithilfe des Master-Passworts seine IP-Adresse ({}) entsperrt!'.format(telegram_bot_id, telegram_chat_id, IPAddr))
    else:
        print("Das Master-Passwort ist falsch!")
        r = requests.get('https://api.telegram.org/bot{}/sendMessage?chat_id={}&text=Ein Benutzer mit der IP-Adresse {} hat sich versucht als Admin anzumelden'.format(telegram_bot_id, telegram_chat_id, IPAddr))

else:
    print("Deine IP-Adresse ({}) ist nicht gesperrt".format(IPAddr))