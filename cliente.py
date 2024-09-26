import sqlite3

conn = sqlite3.connect('vendas.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS cliente (
                idcliente INTEGER PRIMARY KEY,
                nome TEXT,
                email TEXT,
                telefone TEXT,
                data_nasc DATE,
                cidade TEXT
            )''')
conn.commit()

def listar_contatos():
    c.execute("SELECT * FROM cliente")
    print(c.fetchall())

def add_contato(nome1, email1, telefone1, data_nasc1, cidade1):
    c.execute("INSERT INTO cliente (nome, email, telefone, data_nasc, cidade) VALUES (?, ?, ?, ?, ?)",
              (nome1, email1, telefone1, data_nasc1, cidade1))
    conn.commit()
    listar_contatos()

def delete(id_cliente1):
    c.execute("DELETE FROM cliente WHERE idcliente = ?", (id_cliente1,))
    conn.commit()
    listar_contatos()

def busca_por_id(id_cliente1):
    c.execute("SELECT * FROM cliente WHERE idcliente = ?", (id_cliente1,))
    resultado = c.fetchone()
    if resultado:
        print(resultado)
    else:
        print("Contato não encontrado")

add_contato("João Marcos", "joao@example.com", "(11) 98765-4321", "1990-05-15", "Piripiri")
add_contato("Raiana", "raiana@example.com", "(11) 98765-4322", "1995-08-20", "Pedro II")
add_contato("Kaua", "kaua@example.com", "(11) 98765-4323", "1988-03-10", "Lagoa de São Francisco")
add_contato("Dulce", "dulce@example.com", "(11) 98765-4324", "1980-12-05", "Assunção do Piaui")
add_contato("Luciene", "luciene@example.com", "(11) 98765-4325", "1975-07-25", "Assunção do Piaui")