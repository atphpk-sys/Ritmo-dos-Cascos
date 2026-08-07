"""
consultar.py
------------
Funções utilitárias para ler, buscar, atualizar e excluir registros da
tabela 'acessos'. Rode este arquivo diretamente para ver um pequeno
demo no terminal.
"""
from database import conectar


def listar_todos():
    """SELECT * -> retorna todas as linhas da tabela."""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM acessos ORDER BY id DESC")
    linhas = cursor.fetchall()
    conexao.close()
    return linhas


def buscar_por_sistema(sistema):
    """SELECT ... WHERE sistema_operacional = ? """
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT * FROM acessos WHERE sistema_operacional = ?",
        (sistema,)
    )
    resultado = cursor.fetchall()
    conexao.close()
    return resultado


def buscar_por_ip(ip):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM acessos WHERE ip = ?", (ip,))
    resultado = cursor.fetchall()
    conexao.close()
    return resultado


def atualizar_tipo_dispositivo(id_registro, novo_tipo):
    """UPDATE ... SET tipo_dispositivo = ? WHERE id = ?"""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE acessos SET tipo_dispositivo = ? WHERE id = ?",
        (novo_tipo, id_registro)
    )
    conexao.commit()
    conexao.close()


def excluir_registro(id_registro):
    """DELETE FROM acessos WHERE id = ?"""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM acessos WHERE id = ?", (id_registro,))
    conexao.commit()
    conexao.close()


def _imprimir_linhas(linhas):
    colunas = ["id", "data_hora", "ip", "navegador", "versao_navegador",
               "sistema_operacional", "tipo_dispositivo",
               "marca_dispositivo", "modelo_dispositivo",
               "pagina_visitada", "user_agent_bruto"]
    for linha in linhas:
        print(dict(zip(colunas, linha)))


if __name__ == "__main__":
    print("== Todos os acessos ==")
    _imprimir_linhas(listar_todos())
