"""
database.py
------------
Responsável por conectar ao banco SQLite e criar a tabela 'acessos'.
Rode `python database.py` uma vez para preparar o banco antes de usar
o resto do sistema.
"""
import sqlite3

NOME_BANCO = "acessos.db"


def conectar():
    """Abre (ou cria) o arquivo do banco de dados e retorna a conexão."""
    conexao = sqlite3.connect(NOME_BANCO)
    return conexao


def criar_tabela():
    """Cria a tabela 'acessos' no banco, caso ela ainda não exista."""
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS acessos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT NOT NULL,
            ip TEXT,
            navegador TEXT,
            versao_navegador TEXT,
            sistema_operacional TEXT,
            tipo_dispositivo TEXT,
            marca_dispositivo TEXT,
            modelo_dispositivo TEXT,
            pagina_visitada TEXT,
            user_agent_bruto TEXT
        )
    """)

    conexao.commit()
    conexao.close()


if __name__ == "__main__":
    criar_tabela()
    print("Banco de dados e tabela criados com sucesso! (arquivo acessos.db)")
