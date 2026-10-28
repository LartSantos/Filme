# Catálogo de Filmes

Sistema CRUD feito com Flask e SQLite.

## Como rodar localmente

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
python app.py
```

Abra http://127.0.0.1:5000

## Funcionalidades
- Cadastrar filme (título, gênero, ano, nota de 1 a 10)
- Listar filmes
- Editar filme
- Excluir filme

## Deploy
Publicado no Render (Build: `pip install -r requirements.txt` | Start: `gunicorn app:app`).
