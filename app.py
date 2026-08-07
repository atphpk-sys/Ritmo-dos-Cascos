"""
app.py — Site (Ritmo-Dos-Cascos) com registro de acessos e painel admin.
"""
import os
from functools import wraps
from flask import Flask, request, render_template, redirect, url_for, session

from registrar_acesso import registrar_acesso
from database import criar_tabela
import consultar

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "troque-esta-chave-em-producao")
SENHA_ADMIN = os.environ.get("SENHA_ADMIN", "cavalo123")  # troque em produção!

criar_tabela()

ROTAS_IGNORADAS = ("/admin", "/static")


@app.before_request
def registrar_visita():
    if request.path.startswith(ROTAS_IGNORADAS):
        return
    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent", "")
    registrar_acesso(ip, user_agent, pagina_visitada=request.path)


def login_obrigatorio(funcao):
    @wraps(funcao)
    def verificar(*args, **kwargs):
        if not session.get("logado"):
            return redirect(url_for("admin_login"))
        return funcao(*args, **kwargs)
    return verificar


# ---------- Seu site ----------

@app.route("/")
def home():
    return render_template("index.html")


# ---------- Painel administrativo ----------

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    erro = None
    if request.method == "POST":
        if request.form.get("senha", "") == SENHA_ADMIN:
            session["logado"] = True
            return redirect(url_for("admin_painel"))
        erro = "Senha incorreta."
    return render_template("admin_login.html", erro=erro)


@app.route("/admin/logout")
def admin_logout():
    session.pop("logado", None)
    return redirect(url_for("admin_login"))


@app.route("/admin")
@login_obrigatorio
def admin_painel():
    registros = consultar.listar_todos()
    return render_template("admin_painel.html", registros=registros)


if __name__ == "__main__":
    app.run(debug=True)
