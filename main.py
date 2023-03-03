print("Was willst du machen?")
print("[1] Benutzer erstellen")
print("[2] Anmelden")
print("[3] Benutzer löschen")
print("[4] IP-Adresse enstsperren")
choice=int(input("Auswahl: "))

if choice==1: #Benutzer erstellen
    import create
elif choice==2: #Anmelden
    import login
elif choice==3: #Benutzer löschen
    import delete
elif choice==4: #IP-Adresse entsperren
    import unlock_ip
else:
    print("Ungültige Auswahl")