import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent

con = sqlite3.connect('meu_banco_de_dados.db')
cursor = con.cursor()


def criar_tabela(cursor):
    cursor.execute('CREATE TABLE clientes (id INTEGER PRIMARY KEY \
                   AUTOINCREMENT,nome VARCHAR(100), email VARCHAR(150))')


def inserir_registro(conexao, cursor, nome, email):
    data = (nome, email)
    cursor.execute('INSERT INTO clientes (nome, email) VALUES (?,?);', data)
    conexao.commit()


def atualizar_registro(conexao, cursor, nome, email, id):
    data = (nome, email, id)
    cursor.execute('UPDATE clientes SET nome=?, email=? WHERE id=?;', data)
    conexao.commit()


def excluir_registro(conexao, cursor, id):
    data = (id,)
    cursor.execute('DELETE FROM clientes WHERE id=?;', data)
    conexao.commit()


def inserir_varios_registros(conexao, cursor, dados):
    cursor.executemany('INSERT INTO clientes (nome, email) VALUES (?, ?)', dados)
    conexao.commit()


def recuperar_cliente(conexao, cursor, id):
    cursor.row_factory = sqlite3.Row
    cursor.execute('SELECT * from clientes WHERE id=?', (id,))
    return cursor.fetchone()


def listar_clientes(cursor):
    return cursor.execute("SELECT * FROM clientes ORDER BY nome DESC;")

cliente = dict(recuperar_cliente(con, cursor, 1))
print(cliente)
print(f'Seja bem vido ao sistema {cliente["nome"]}')
cli = listar_clientes(cursor)
for cliente in cli:
    print(dict(cliente))

# dados = [('Guilherme', 'gui@gmail.com'),
#          ('Ana', 'ana@gmail.com'),
#          ('Otavio', 'ota@gmail.com')]

# inserir_varios_registros(con, cursor, dados)
