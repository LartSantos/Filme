# Catálogo de Filmes - Flask + SQLite
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# Função para conectar no banco de dados
def conectar():
    conexao = sqlite3.connect("filmes.db")
    conexao.row_factory = sqlite3.Row  # deixa pegar os dados pelo nome da coluna
    return conexao


# Cria a tabela quando o programa começa (se ela ainda não existir)
conexao = conectar()
conexao.execute("""
    CREATE TABLE IF NOT EXISTS filmes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        genero TEXT NOT NULL,
        ano INTEGER NOT NULL,
        nota INTEGER NOT NULL
    )
""")
conexao.commit()
conexao.close()


# LISTAR os filmes (página inicial)
@app.route("/")
def index():
    conexao = conectar()
    filmes = conexao.execute("SELECT * FROM filmes").fetchall()
    conexao.close()
    return render_template("index.html", filmes=filmes)


# CADASTRAR um filme novo
@app.route("/novo", methods=["GET", "POST"])
def novo():
    # Se a pessoa enviou o formulário, salva no banco
    if request.method == "POST":
        titulo = request.form["titulo"]
        genero = request.form["genero"]
        ano = request.form["ano"]
        nota = request.form["nota"]

        conexao = conectar()
        conexao.execute(
            "INSERT INTO filmes (titulo, genero, ano, nota) VALUES (?, ?, ?, ?)",
            (titulo, genero, ano, nota)
        )
        conexao.commit()
        conexao.close()
        return redirect("/")

    # Se só abriu a página, mostra o formulário vazio
    return render_template("form.html", filme=None)


# EDITAR um filme que já existe
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conexao = conectar()

    # Se a pessoa enviou o formulário, atualiza no banco
    if request.method == "POST":
        titulo = request.form["titulo"]
        genero = request.form["genero"]
        ano = request.form["ano"]
        nota = request.form["nota"]

        conexao.execute(
            "UPDATE filmes SET titulo = ?, genero = ?, ano = ?, nota = ? WHERE id = ?",
            (titulo, genero, ano, nota, id)
        )
        conexao.commit()
        conexao.close()
        return redirect("/")

    # Se só abriu a página, busca o filme e mostra o formulário preenchido
    filme = conexao.execute("SELECT * FROM filmes WHERE id = ?", (id,)).fetchone()
    conexao.close()
    return render_template("form.html", filme=filme)


# EXCLUIR um filme
@app.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    conexao = conectar()
    conexao.execute("DELETE FROM filmes WHERE id = ?", (id,))
    conexao.commit()
    conexao.close()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
