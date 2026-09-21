import os
from pathlib import Path
from functools import wraps

from flask import Flask, jsonify, redirect, request, send_file, session
from flask_sqlalchemy import SQLAlchemy

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
app.config['SECRET_KEY'] = 'biblioteca-infantil-secret-key'

# Configuração do Banco de Dados SQLite local
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

ADMIN_USER = 'admin'
ADMIN_PASSWORD = '123'


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return jsonify({'erro': 'Autenticação necessária.'}), 401
        return f(*args, **kwargs)
    return decorated_function

# ---------------------------------------------------------
# MODELO DO BANCO DE DADOS
# ---------------------------------------------------------
class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    arquivo_url = db.Column(db.String(300), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "autor": self.autor,
            "categoria": self.categoria,
            "descricao": self.descricao,
            "arquivo_url": self.arquivo_url,
        }


# Criar o banco de dados e popular com alguns livros iniciais se estiver vazio
with app.app_context():
    db.create_all()
    if not Livro.query.first():
        livro_exemplo = Livro(
            titulo="Fábulas de Monteiro Lobato / Domínio Público",
            autor="Monteiro Lobato",
            categoria="Infantojuvenil",
            descricao="Histórias clássicas voltadas para o público infantil.",
            arquivo_url="https://www.dominiopublico.gov.br/download/texto/cv000131.pdf",
        )
        db.session.add(livro_exemplo)
        db.session.commit()


# ---------------------------------------------------------
# ROTAS DA API (ENDPOINTS)
# ---------------------------------------------------------

# 1. Rota raiz para servir a página inicial do frontend
@app.route('/', methods=['GET'])
def home():
    return send_file(BASE_DIR / 'index.html')


@app.route('/login', methods=['GET'])
def login_page():
    return send_file(BASE_DIR / 'login.html')


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('logged_in', None)
    return redirect('/login')


@app.route('/index.html', methods=['GET'])
def index_html():
    return send_file(BASE_DIR / 'index.html')


@app.route('/api/session', methods=['GET'])
def api_session():
    return jsonify({'logged_in': bool(session.get('logged_in'))}), 200


@app.route('/api/login', methods=['POST'])
def api_login():
    dados = request.get_json(silent=True) or request.form

    if not dados:
        return jsonify({'erro': 'Dados de login não informados.'}), 400

    username = str(dados.get('username', '')).strip()
    password = str(dados.get('password', '')).strip()

    if username == ADMIN_USER and password == ADMIN_PASSWORD:
        session['logged_in'] = True
        return jsonify({'mensagem': 'Login realizado com sucesso!'}), 200

    return jsonify({'erro': 'Credenciais inválidas.'}), 401


# 2. Listar todos os livros ou filtrar por categoria/busca
@app.route('/api/livros', methods=['GET'])
def listar_livros():
    pesquisa = request.args.get('busca', '')
    categoria = request.args.get('categoria', '')

    query = Livro.query
    if pesquisa:
        query = query.filter(Livro.titulo.ilike(f'%{pesquisa}%') | Livro.autor.ilike(f'%{pesquisa}%'))
    if categoria:
        query = query.filter(Livro.categoria.ilike(f'%{categoria}%'))

    livros = query.all()
    return jsonify([livro.to_dict() for livro in livros]), 200


# 3. Obter detalhes de um livro específico
@app.route('/api/livros/<int:id>', methods=['GET'])
def obter_livro(id):
    livro = Livro.query.get_or_404(id)
    return jsonify(livro.to_dict()), 200


# 4. Cadastrar um novo livro (para administradores ou curadores do projeto)
@app.route('/api/livros', methods=['POST'])
@login_required
def cadastrar_livro():
    dados = request.get_json()

    if not dados or 'titulo' not in dados or 'arquivo_url' not in dados:
        return jsonify({"erro": "Dados incompletos. Título e URL do arquivo são obrigatórios."}), 400

    novo_livro = Livro(
        titulo=dados['titulo'],
        autor=dados.get('autor', 'Desconhecido'),
        categoria=dados.get('categoria', 'Geral'),
        descricao=dados.get('descricao', ''),
        arquivo_url=dados['arquivo_url'],
    )

    db.session.add(novo_livro)
    db.session.commit()

    return jsonify({"mensagem": "Livro cadastrado com sucesso!", "livro": novo_livro.to_dict()}), 201


# 5. Atualizar um livro existente
@app.route('/api/livros/<int:id>', methods=['PUT'])
@login_required
def atualizar_livro(id):
    livro = Livro.query.get_or_404(id)
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Dados da requisição incompletos."}), 400

    titulo = dados.get('titulo', livro.titulo)
    arquivo_url = dados.get('arquivo_url', livro.arquivo_url)

    if not titulo or not arquivo_url:
        return jsonify({"erro": "Título e URL do arquivo são obrigatórios."}), 400

    livro.titulo = titulo
    livro.autor = dados.get('autor', livro.autor)
    livro.categoria = dados.get('categoria', livro.categoria)
    livro.descricao = dados.get('descricao', livro.descricao)
    livro.arquivo_url = arquivo_url

    db.session.commit()
    return jsonify({"mensagem": "Livro atualizado com sucesso!", "livro": livro.to_dict()}), 200


# 6. Remover um livro
@app.route('/api/livros/<int:id>', methods=['DELETE'])
@login_required
def excluir_livro(id):
    livro = Livro.query.get_or_404(id)
    db.session.delete(livro)
    db.session.commit()
    return jsonify({"mensagem": "Livro removido com sucesso!"}), 200


if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', '5000'))
    app.run(host=host, port=port, debug=False)
