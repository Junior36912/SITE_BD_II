import sqlite3
from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.secret_key = "123"

########################################################################################################################
########################################################################################################################
# SISTEMA DE LOGIN
class Usuario:
    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha

usuario1 = Usuario("Junior", "123")
usuario2 = Usuario("Joao", "123")
usuario3 = Usuario("Willyams", "123")

usuarios = { usuario1.nome : usuario1,
             usuario2.nome : usuario2,
             usuario3.nome : usuario3 }

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST', 'GET'])
def autenticar():
    usuario = usuarios.get(request.form['usuario'])
    if usuario and usuario.senha == request.form['senha']:
        session['usuario_logado'] = usuario.nome
        flash(usuario.nome + ' logado com sucesso!')
        proxima_pagina = request.form.get('proxima')
        if proxima_pagina:
            return redirect(proxima_pagina)
        return redirect('/')
    flash('Usuário não logado.')
    return redirect(url_for('login'))



@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('login'))


########################################################################################################################
########################################################################################################################


@app.route('/')
def rota():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect('/login')
    return render_template('home.html')

########################################################################################################################
########################################################################################################################
# TABELA CLIENTES


def carregar_dados_clientes():
    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM cliente")
    data_prod = cursor.fetchall()
    banco.close()
    flash('Dados Atualizado!')
    return data_prod


@app.route('/tab_cliente')
def raiz_clientes():
    data_prod = carregar_dados_clientes()
    return render_template('tabela_cliente.html', data=data_prod)


#PESQUISAR CLIENTES


@app.route('/pesquisar_cliente')
def pesquisar_cliente():
    id_cliente = request.args.get('search_id')
    if id_cliente:
        banco = sqlite3.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM cliente WHERE idcliente = ?", (id_cliente,))
        cliente = cursor.fetchone()
        banco.close()

        if cliente:
            return render_template('detalhes_cliente.html', cliente=cliente)
        else:
            flash("Cliente não encontrado", "danger")
            return render_template('cliente_nao_encontrado.html')
    else:
        return redirect(url_for('raiz_clientes'))


#ADICIONAR CLIENTES


@app.route('/adicionar')
def add_usuario():
    return render_template('adicionar.html')


@app.route("/adicionar_2", methods=["POST"])
def rota_adicionar():
    nome1 = request.form["nome"]
    email1 = request.form["email"]
    telefone1 = request.form["telefone"]
    data_nasc1 = request.form["data_nasc"]
    cidade1 = request.form["cidade"]

    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("INSERT INTO cliente (nome, email, telefone, data_nasc, cidade) VALUES (?, ?, ?, ?, ?)",
                   (nome1, email1, telefone1, data_nasc1, cidade1))
    banco.commit()
    banco.close()

    flash("Dados adicionados com sucesso")
    data_prod = carregar_dados_clientes()
    return render_template('tabela_cliente.html', data=data_prod)


#EXCLUIR CLIENTES


@app.route('/excluir/<int:idcliente>', methods=["GET"])
def rota_excluir_cliente(idcliente):
    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("DELETE FROM cliente WHERE idcliente = ?", (idcliente,))
    banco.commit()
    banco.close()
    flash("Dados deletados com sucesso")
    return redirect(url_for("raiz_clientes"))


#EDITAR CLIENTES


@app.route('/editar_cliente/<int:idcliente>', methods=['GET', 'POST'])
def rota_editar_cliente(idcliente):
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        data_nasc = request.form['data_nasc']
        cidade = request.form['cidade']

        banco = sqlite3.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute("UPDATE cliente SET nome=?, email=?, telefone=?, data_nasc=?, cidade=? WHERE idcliente=?",
                       (nome, email, telefone, data_nasc, cidade, idcliente))
        banco.commit()
        banco.close()

        flash("Cliente editado com sucesso", "success")
        return redirect(url_for('raiz_clientes'))
    else:
        banco = sqlite3.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM cliente WHERE idcliente=?", (idcliente,))
        cliente = cursor.fetchone()
        banco.close()

        return render_template('editar_cliente.html', cliente=cliente)


########################################################################################################################
########################################################################################################################
# TABELA PRODUTOS:


def carregar_dados_produtos():
    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM produto")
    data = cursor.fetchall()
    banco.close()
    return data



@app.route('/tab_produtos')
def raiz_produtos():
    data = carregar_dados_produtos()
    return render_template('tabela_prod.html', data=data)



# PESQUISANDO PRODUTOS:


@app.route('/pesquisar_produto')
def pesquisar_produto():
    id_produto = request.args.get('search_id')
    if id_produto:
        banco = sqlite3.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM produto WHERE idproduto = ?", (id_produto,))
        produto = cursor.fetchone()
        banco.close()

        if produto:
            return render_template('detalhes_produto.html', produto=produto)
        else:
            flash("Produto não encontrado", "danger")
            return render_template('produto_nao_encontrado.html')
    else:
        return redirect(url_for('raiz_produtos'))


#ADICIONAR PRODUTO


@app.route('/adicionar_produto')
def add_produto():
    return render_template('adicionar_produto.html')


@app.route("/adicionar_2_produto", methods=["POST"])
def rota_adicionar_produto():
    nome1 = request.form["nome"]
    preco1 = request.form["preco"]
    marca1 = request.form["marca"]
    categoria1 = request.form["categoria"]
    qtd1 = request.form["qtd"]

    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("INSERT INTO produto (nome, preco, marca, categoria, qtd) VALUES (?, ?, ?, ?, ?)",
                   (nome1, preco1, marca1, categoria1, qtd1))
    banco.commit()
    banco.close()

    flash("Dados adicionados com sucesso", "warning")
    data = carregar_dados_produtos()
    return render_template('tabela_prod.html', data=data)


#EXCLUIR PRODUTO


@app.route('/excluir_produtos/<int:idproduto>', methods=["GET"])
def rota_excluir_produto(idproduto):
    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("DELETE FROM produto WHERE idproduto = ?", (idproduto,))
    banco.commit()
    banco.close()
    flash("Dados deletados com sucesso", "warning")
    return redirect(url_for("raiz_produtos"))


#EDITAR PRODUTO


@app.route('/editar_produto/<int:idproduto>', methods=['GET', 'POST'])
def rota_editar_produto(idproduto):
    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        marca = request.form['marca']
        categoria = request.form['categoria']
        qtd = request.form['qtd']

        banco = sqlite3.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute("UPDATE produto SET nome=?, preco=?, marca=?, categoria=?, qtd=? WHERE idproduto=?",
                       (nome, preco, marca, categoria, qtd, idproduto))
        banco.commit()
        banco.close()

        flash("Produto editado com sucesso", "success")
        return redirect(url_for('raiz_produtos'))
    else:
        banco = sqlite3.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM produto WHERE idproduto=?", (idproduto,))
        produto = cursor.fetchone()
        banco.close()

        return render_template('editar_produto.html', produto=produto)


########################################################################################################################
########################################################################################################################
# TABELA VENDAS:


def carregar_dados_vendas():
    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM venda")
    vendas = cursor.fetchall()
    banco.close()
    return vendas



@app.route('/tab_venda')
def raiz_venda():
    vendas = carregar_dados_vendas()
    return render_template('tabela_venda.html', data=vendas)


# PESQUISANDO VENDAS:


@app.route('/pesquisar_venda')
def pesquisar_venda():
    id_venda = request.args.get('search_id')
    if id_venda:
        banco = sqlite3.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM venda WHERE idvenda = ?", (id_venda,))
        venda = cursor.fetchone()
        banco.close()

        if venda:
            return render_template('detalhes_venda.html', venda=venda)
        else:
            flash("Venda não encontrada", "danger")
            return render_template('venda_nao_encontrada.html')
    else:
        return redirect(url_for('raiz_venda'))



@app.route('/adicionar_venda')
def add_venda():
    return render_template('adicionar_venda.html')


#ADICIONAR VENDA


@app.route('/adicionar_venda_2', methods=['GET', 'POST'])
def rota_adicionar_venda():
    if request.method == 'POST':
        data_venda1 = request.form['data_venda']
        valor_total1 = request.form['valor_total']
        idcliente1 = request.form['idcliente']
        idproduto1 = request.form['idproduto']
        funcionario1 = request.form['funcionario']

        banco = sqlite3.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute(
            "INSERT INTO venda (data_venda, valor_total, idcliente, idproduto, funcionario) VALUES (?, ?, ?, ?, ?)",
            (data_venda1, valor_total1, idcliente1, idproduto1, funcionario1))
        banco.commit()
        banco.close()

        flash('Venda adicionada com sucesso!', 'success')
        return redirect(url_for('raiz_venda'))
    return render_template('adicionar_venda.html')


#EXCLUIR VENDA


@app.route('/excluir_venda/<int:idvenda>', methods=['GET'])
def rota_excluir_venda(idvenda):
    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("DELETE FROM venda WHERE idvenda = ?", (idvenda,))
    banco.commit()
    banco.close()
    flash("Dados deletados com sucesso", "warning")
    return redirect(url_for("raiz_venda"))


# EDITAR VENDA


@app.route('/editar_venda/<int:idvenda>', methods=['GET', 'POST'])
def editar_venda(idvenda):
    if request.method == 'POST':
        data_venda = request.form['data_venda']
        valor_total = request.form['valor_total']
        idcliente = request.form['idcliente']
        idproduto = request.form['idproduto']
        funcionario = request.form['funcionario']

        banco = sqlite3.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute(
            "UPDATE venda SET data_venda=?, valor_total=?, idcliente=?, idproduto=?, funcionario=? WHERE idvenda=?",
            (data_venda, valor_total, idcliente, idproduto, funcionario, idvenda))
        banco.commit()
        banco.close()

        flash("Venda editada com sucesso", "success")
        return redirect(url_for('raiz_venda'))
    else:
        banco = sqlite3.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM venda WHERE idvenda=?", (idvenda,))
        venda = cursor.fetchone()
        banco.close()

        return render_template('editar_venda.html', venda=venda)



# FUNCIONAR O APP

if __name__ == '__main__':
    app.run(debug=True)