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
        return resposta.config(text=user)
    return resposta.config(text='Serviço não encontrado!')


# Funcao que limpa o label de output 'resposta'


def clean_resposta():
    return resposta.config(text='')


window = Tk()
window.geometry('900x600')          # Largura x Altura + dist esq + dist dir
window.title('Password Manager')    # Titulo da pagina
window.iconbitmap('passico.ico')    # Icone superior esquerdo da pagina
# Trava redimensionamento da janela
window.resizable(height=False, width=False)

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
resposta = Label(window, font='Arial 15', text='', wraplength=500)

# Posicionando labels
label1.place(x=30, y=40)
label2.place(x=30, y=80)
label3.place(x=30, y=120)
label4.place(x=30, y=280)
label5.place(x=30, y=240)

# Posicionando Labels de output
resposta.place(x=380, y=40, width=400, height=400)

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
button4 = Button(text='Clean', command=clean_resposta)

# Posicionando os botoes
button1.place(x=30, y=160, width=120, height=35)
button2.place(x=160, y=160, width=120, height=35)
button3.place(x=30, y=320, width=120, height=35)
button4.place(x=30, y=440, width=120, height=35)


# Roda o programa e fecha conexao com banco de dados
window.mainloop()
conn.close()
