import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent

con = sqlite3.connect('meu_banco_de_dados.db')
cursor = con.cursor()
cursor.row_factory = sqlite3.Row

try:
    cursor.execute("INSERT INTO clientes (nome, email) VALUES (?, ?)", ("Teste 3", 'teste3@gmail.com'))
    cursor.execute("INSERT INTO clientes (id, nome, email) VALUES (?, ?, ?)", (3, "Teste 4", 'teste4@gmail.com'))
    con.commit()
except Exception as exc:
    print(f"Ops! um erro ocorreu! {exc}")
    con.rollback()
