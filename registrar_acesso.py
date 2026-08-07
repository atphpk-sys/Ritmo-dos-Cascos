"""
registrar_acesso.py
--------------------
Interpreta o User-Agent de uma visita e insere um registro na tabela
'acessos'. Pode ser chamado diretamente (teste) ou importado pelo app.py.
"""
from datetime import datetime, timedelta, timezone
from database import conectar
from user_agents import parse

FUSO_BRASILIA = timezone(timedelta(hours=-3))


def interpretar_user_agent(ua_texto):
    """Recebe o texto cru do User-Agent e devolve um dicionário organizado."""
    ua = parse(ua_texto)

    if ua.is_mobile:
        tipo = "Smartphone"
    elif ua.is_tablet:
        tipo = "Tablet"
    elif ua.is_pc:
        tipo = "Desktop"
    else:
        tipo = "Desconhecido"

    return {
        "navegador": ua.browser.family,
        "versao_navegador": ua.browser.version_string,
        "sistema_operacional": ua.os.family,
        "tipo_dispositivo": tipo,
        # Marca/modelo só vêm preenchidos quando o navegador realmente
        # informa isso no User-Agent (comum em Android, raro em iOS/Desktop).
        "marca_dispositivo": ua.device.brand or "",
        "modelo_dispositivo": ua.device.model or "",
    }


def registrar_acesso(ip, user_agent_bruto, pagina_visitada="/"):
    """Insere uma nova linha na tabela acessos (INSERT)."""
    dados = interpretar_user_agent(user_agent_bruto)
    agora = datetime.now(FUSO_BRASILIA).strftime("%Y-%m-%d %H:%M:%S")

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO acessos (
            data_hora, ip, navegador, versao_navegador,
            sistema_operacional, tipo_dispositivo,
            marca_dispositivo, modelo_dispositivo,
            pagina_visitada, user_agent_bruto
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        agora, ip, dados["navegador"], dados["versao_navegador"],
        dados["sistema_operacional"], dados["tipo_dispositivo"],
        dados["marca_dispositivo"], dados["modelo_dispositivo"],
        pagina_visitada, user_agent_bruto,
    ))

    conexao.commit()
    conexao.close()


if __name__ == "__main__":
    exemplo_ua = (
        "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0 Mobile Safari/537.36"
    )
    registrar_acesso("127.0.0.1", exemplo_ua, pagina_visitada="/")
    print("Acesso de teste registrado! Rode 'python consultar.py' para ver.")
