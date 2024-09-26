# Flask SQLite3 Base

Este repositório é uma base simples da framework Flask, implementada utilizando o banco de dados SQLite3. Oferece um ponto de partida ideal para desenvolvedores que desejam criar aplicativos web em Python, aproveitando as vantagens do Flask e do SQLite3.

## Estrutura de Arquivos

- **app.py**: Arquivo central que inicia a aplicação Flask e define as rotas.
- **cliente.py**, **venda.py** e **produto.py**: Estes arquivos contêm a lógica referente a cada tabela do banco de dados, incluindo funções auxiliares para facilitar a integração com o SQLite3.
- **templates/**: Esta pasta contém todos os templates utilizados para renderizar as páginas do site.

## Funcionalidades

- **Exclusão**: Permite excluir um item da tabela.
- **Edição**: Possibilita editar um item da tabela.
- **Pesquisa por ID**: Através de um campo identificado, é possível pesquisar um item da tabela pelo seu ID.
- **Login**: Tela de login adicionada, com função de logout integrada ao sistema.

## Integração Flask e SQLite3

Flask é um framework web leve e flexível em Python, ideal para o desenvolvimento rápido de aplicativos web. SQLite3 é uma biblioteca embutida que fornece um banco de dados SQL leve e autônomo. A integração entre Flask e SQLite3 é feita de forma simples e eficiente, permitindo o uso de consultas SQL diretamente em aplicativos Flask.

## Credenciais

- **Usuários**: "Junior", "Joao" ou "Thiago".
- **Senhas**: "123".
