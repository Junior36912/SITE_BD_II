import sqlite3

conn = sqlite3.connect('vendas.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS produto (
                idproduto INTEGER PRIMARY KEY,
                nome TEXT,
                preco REAL,
                marca TEXT,
                categoria TEXT,
                qtd INTEGER
            )''')
conn.commit()

def listar_produtos():
    c.execute("SELECT * FROM produto")
    print(c.fetchall())

def add_produto(nome, preco, marca, categoria, qtd):
    c.execute("INSERT INTO produto (nome, preco, marca, categoria, qtd) VALUES (?, ?, ?, ?, ?)",
              (nome, preco, marca, categoria, qtd))
    conn.commit()
    listar_produtos()

def delete_produto(id_produto):
    c.execute("DELETE FROM produto WHERE idproduto = ?", (id_produto,))
    conn.commit()
    listar_produtos()

def busca_produto_por_id(id_produto):
    c.execute("SELECT * FROM produto WHERE idproduto = ?", (id_produto,))
    resultado = c.fetchone()
    if resultado:
        print(resultado)
    else:
        print("Produto não encontrado")


add_produto("Carne de Boi", 20.99, "Frigorífico X", "Carne", 50)
add_produto("Carne de Porco", 15.99, "Frigorífico Y", "Carne", 40)
add_produto("Frango", 12.99, "Frigorífico Z", "Carne", 30)
add_produto("Linguiça", 8.99, "Frigorífico X", "Embutidos", 20)
add_produto("Peixe", 18.99, "Frigorífico W", "Pescados", 25)
add_produto("Queijo Prato", 14.99, "Laticínio A", "Frios", 30)
add_produto("Presunto", 10.99, "Laticínio B", "Frios", 25)
add_produto("Peito de Peru", 18.99, "Laticínio C", "Frios", 20)
add_produto("Salsicha", 7.99, "Laticínio A", "Embutidos", 35)
add_produto("Hamburguer", 22.99, "Laticínio A", "Congelados", 15)
add_produto("Coxinha de Frango", 2.99, "Laticínio E", "Congelados", 40)
