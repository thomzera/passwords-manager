from tkinter import Button, Tk, Label, Entry, Message
import sqlite3

# Cria o db caso não exista
conn = sqlite3.connect('services.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
    id integer PRIMARY KEY AUTOINCREMENT,
    service TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
''')

# Funcao que adiciona um servico


def add_new_service():
    newUsername = username.get()
    newPassword = password.get()
    newServico = servico.get()

    cursor.execute(
        "SELECT COUNT(*) from users WHERE username = '" + newUsername + "' ")
    result = cursor.fetchone()

    if int(result[0]) > 0:
        error["text"] = "Erro: Usuário já existe!"
    else:
        error["text"] = "Usuário adicionado!"
        cursor.execute(
            "INSERT INTO users(username,password,service) VALUES(?,?,?)",
            (newUsername, newPassword, newServico))
    conn.commit()


list_services = []


# Funcao que mostra os servicos salvos


def show_services():
    cursor.execute('''
        SELECT service FROM users;
    ''')
    for service in cursor.fetchall():
        print(service)
        list_services.append(service)

    return resposta.config(text=list_services)

# Funcao que recupera username e password


def get_password():
    oldServico = servico2.get()
    cursor.execute(f'''
    SELECT username, password FROM users
    WHERE service = '{oldServico}'
    ''')
    for user in cursor.fetchall():
        print(user)
        return resposta2.config(text=user)
    return resposta2.config(text='Nao encontrado')


window = Tk()
window.geometry('600x600')
window.title('Password Manager')
window.iconbitmap('passico.ico')

# Erros
error = Message(text="", width=160)

# Posicionando erros
error.place(x=30, y=200)

# Configurando erros
error.config(padx=0)


# Labels
label1 = Label(text='Enter Username: ')
label2 = Label(text='Enter Password: ')
label3 = Label(text='Enter Service: ')
label4 = Label(text='Enter Service: ')
label5 = Label(text='Quer resgatar uma senha? Procure pelo serviço')

# Labels de output
resposta = Label(window, font='Arial 15', text='')
resposta2 = Label(window, font='Arial 15', text='0')

# Posicionando labels
label1.place(x=30, y=40)
label2.place(x=30, y=80)
label3.place(x=30, y=120)
label4.place(x=30, y=280)
label5.place(x=30, y=240)

# Posicionando Labels de output
resposta.place(x=15, y=5, width=400, height=35)
resposta2.place(x=15, y=360, width=200, height=35)

# Configurando labels
label1.config(bg='lightgreen', padx=0)
label2.config(bg='lightgreen', padx=0)
label3.config(bg='lightgreen', padx=0)
label4.config(bg='lightgreen', padx=0)
label5.config(padx=0)

# Entrada Usuario
username = Entry(window, font='Arial 15', justify='center')

# Posicionando Entrada Usuario
username.place(x=150, y=40, width=200, height=25)

# Entrada Senha
password = Entry(window, font='Arial 15', justify='center')

# Posicionando Entrada Senha
password.place(x=150, y=80, width=200, height=25)

# Entrada Serviço
servico = Entry(window, font='Arial 15', justify='center')
servico2 = Entry(window, font='Arial 15', justify='center')  # recover pass

# Posicionando Entrada Serviço
servico.place(x=150, y=120, width=200, height=25)
servico2.place(x=150, y=280, width=200, height=25)  # recover pass

# Botoes
button1 = Button(text='Add service', command=add_new_service)
button2 = Button(text='Show services', command=show_services)
button3 = Button(text='Recover Password', command=get_password)

# Posicionando os botoes
button1.place(x=30, y=160, width=120, height=35)
button2.place(x=160, y=160, width=120, height=35)
button3.place(x=30, y=320, width=120, height=35)

window.mainloop()
conn.close()
