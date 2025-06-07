from flask import Flask, jsonify, request, make_response
from estrutura_banco import Autor, Postagem, app, db
import jwt
import json
from functools import wraps
from datetime import datetime, timedelta


def token_obrigatorio(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Verificar se um token foi enviado
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'mensagem': 'Token não foi encontrado'}), 401
        # Se temos um token, validar acesso consultando o BD
        try:
            resultado = jwt.decode(token, app.config['SECRET_KEY'])
            autor = Autor.query.filter_by(id_autor=resultado['id_autor']).first()
        except:
            return jsonify({'mensagem': 'Token invalido'}), 401
        return f(autor, *args, **kwargs)
    return decorated


@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Login inválido', 401, {'WWW-Authenticate': 'Basic realm="Login Obrigatório"'})
    usuario = Autor.query.filter_by(nome=auth.username).first()
    if not usuario:
        return make_response('Login inválido', 401, {'WWW-Authenticate': 'Basic realm="Login Obrigatório"'})
    if auth.password == usuario.senha:
        token = jwt.encode({'id_autor': usuario.id_autor, 'exp': datetime.now() + timedelta(minutes=30)}, app.config[
            'SECRET_KEY'])
        return jsonify({'token': token})
    return make_response('Login inválido', 401, {'WWW-Authenticate': 'Basic realm="Login Obrigatório"'})


# rota padrão - GET http://localhost:5000
@app.route('/')
@token_obrigatorio
def obter_postagens(autor):
    postagens = Postagem.query.all()

    lista_postagens = []
    for postagem in postagens:
        postagem_atual = {'titulo': postagem.titulo, 'id_autor': postagem.id_autor}
        lista_postagens.append(postagem_atual)
    return jsonify({'postagens': lista_postagens})


# obter postagem por id - GET http://localhost:5000/postagem/1
@app.route('/postagem/<int:id_postagem>', methods=['GET'])
@token_obrigatorio
def obter_postagem_por_indice(autor, id_postagem):
    postagem = Postagem.query.filter_by(id_postagem=id_postagem).first()
    postagem_atual = {}
    try:
        postagem_atual['titulo'] = postagem.titulo
    except:
        pass
    postagem_atual['id_autor'] = postagem.id_autor
    return jsonify({'postagens': postagem_atual})


# Criar uma nova postagem - POST http://localhost:5000/postagem
@app.route('/postagem', methods=['POST'])
@token_obrigatorio
def nova_postagem(autor):
    nova_postagem = request.get_json()
    postagem = Postagem(titulo=nova_postagem['titulo'], id_autor=novo_autor['id_autor'])

    db.session.add(postagem)
    db.session.commit()

    return jsonify(f'A postagem foi criada com sucesso', 200)


# Alterar uma postagem existente - PUT
@app.route('/postagem/<int:id_postagem>', methods=['PUT'])
@token_obrigatorio
def atualiza_postagem_por_indice(autor, id_postagem):
    alterar_postagem = request.get_json()
    postagem = Postagem.query.filter_by(id_postagem=id_postagem).first()
    try:
        postagem.titulo = alterar_postagem['titulo']
    except:
        pass
    try:
        postagem.id_autor = alterar_postagem['id_autor']
    except:
        pass

    db.session.commit()
    return jsonify(f'A postagem foi atualizada com sucesso', 200)


# Excluindo uma postagem - Delete
@app.route('/postagem/<int:id_postagem>', methods=['DELETE'])
@token_obrigatorio
def excluir_postagem(autor, id_postagem):
    postagem_a_excluir = Postagem.query.filter_by(id_postagem=id_postagem).first()
    if not postagem_a_excluir:
        return jsonify('Não foi encontrada postagem com este id')
    db.session.delete(postagem_a_excluir)
    db.session.commit()

    return jsonify('Postagem excluida com sucesso')


@app.route('/autores')
@token_obrigatorio
def obeter_autores(autor):
    autores = Autor.query.all()
    lista_autores = []
    for autor in autores:
        autor_atual = {'id_autor': autor.id_autor, 'nome': autor.nome, 'email': autor.email}
        lista_autores.append(autor_atual)
    return jsonify(lista_autores)


@app.route('/autores/<int:id_autor>', methods=['GET'])
@token_obrigatorio
def obeter_autor_id(autor, id_autor):
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor:
        return jsonify('Autor não encontrado', 404)
    autor_atual = {'id_autor': autor.id_autor, 'nome': autor.nome, 'email': autor.email}
    return jsonify(f'Você buscou pelo autor: {autor_atual}')


@app.route('/autores', methods=['POST'])
@token_obrigatorio
def novo_autor(autor):
    novo_autor = request.get_json()
    autor = Autor(nome=novo_autor['nome'], senha=novo_autor, email=novo_autor['email'])

    db.session.add(autor)
    db.session.commit()

    return jsonify(f'O autor foi criado com sucesso', 200)


@app.route('/autores/<int:id_autor>', methods=['PUT'])
@token_obrigatorio
def alterar_autor(autor, id_autor):
    alterar_autor = request.get_json()
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor:
        return jsonify('Autor não encontrado', 404)
    try:
        autor.nome = alterar_autor['nome']
    except:
        pass
    try:
        autor.email = alterar_autor['email']
    except:
        pass
    try:
        autor.senha = alterar_autor['senha']
    except:
        pass

    db.session.commit()
    return jsonify(f'O autor foi alterado com sucesso', 200)


@app.route('/autores/<int:id_autor>', methods=['DELETE'])
@token_obrigatorio
def excluir_autor(autor, id_autor):
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor:
        return jsonify('Esse autor não foi encontrado', 404)

    db.session.delete(autor)
    db.session.commit()

    return jsonify(f'O autor foi deletado com sucesso', 200)


app.run(debug=True)
