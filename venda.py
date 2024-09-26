import sqlite3

conn = sqlite3.connect('vendas.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS venda (
                idvenda INTEGER PRIMARY KEY,
                data_venda DATE,
                valor_total REAL,
                idcliente INTEGER,
                idproduto INTEGER,
                funcionario TEXT,
                FOREIGN KEY (idcliente) REFERENCES cliente(idcliente),
                FOREIGN KEY (idproduto) REFERENCES produto(idproduto)
            )''')

def listar_vendas():
    c.execute("SELECT * FROM venda")
    print(c.fetchall())

def add_venda(data_venda, valor_total, idcliente, idproduto, funcionario):
    conn = sqlite3.connect('vendas.db')
    c = conn.cursor()
    c.execute("INSERT INTO venda (data_venda, valor_total, idcliente, idproduto, funcionario) VALUES (?, ?, ?, ?, ?)",
              (data_venda, valor_total, idcliente, idproduto, funcionario))
    conn.commit()
    listar_vendas()

def delete_venda(idvenda):
    conn = sqlite3.connect('vendas.db')
    c = conn.cursor()
    c.execute("DELETE FROM venda WHERE idvenda = ?", (idvenda,))
    conn.commit()
    listar_vendas()

def busca_venda_por_id(idvenda):
    c.execute("SELECT * FROM produto WHERE idproduto = ?", (idvenda,))
    resultado = c.fetchone()
    if resultado:
        print(resultado)
    else:
        print("Venda não encontrado")

def editar_venda(idvenda, data_venda, valor_total, idcliente, idproduto, funcionario):
    conn = sqlite3.connect('vendas.db')
    c = conn.cursor()
    c.execute("UPDATE venda SET data_venda=?, valor_total=?, idcliente=?, idproduto=?, funcionario=? WHERE idvenda=?",
              (data_venda, valor_total, idcliente, idproduto, funcionario, idvenda))
    conn.commit()
    conn.close()


add_venda("2024-03-17", 100.99, 1, 1, "João")
add_venda("2024-03-18", 50.50, 2, 2, "Junior")
add_venda("2024-03-19", 75.25, 3, 3, "Daniel")
add_venda("2024-03-20", 120.75, 4, 4, "João")
add_venda("2024-03-21", 90.90, 5, 5, "Junior")
