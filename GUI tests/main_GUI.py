import tkinter
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("330x300")
app.title("MySQL User Management")

def create():
    import create
    app.destroy()

def login():
    import login
    app.destroy()

def delete():
    import delete
    app.destroy()

def unlock():
    import unlock_ip
    app.destroy()

# Use CTkButton instead of tkinter Button
button = customtkinter.CTkButton(master=app, text="Benutzer erstellen", command=create)
button.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)
button = customtkinter.CTkButton(master=app, text="Anmelden", command=login)
button.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)
button = customtkinter.CTkButton(master=app, fg_color="red", text="Benutzer löschen", command=delete)
button.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
button = customtkinter.CTkButton(master=app, fg_color="green", text="IP-Entsperren", command=unlock)
button.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

label = customtkinter.CTkLabel(master=app, text="https://github.com/M4RC-X/")
label.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)


app.mainloop()