from flask import Flask, jsonify, request

app = Flask(__name__)
postagens = [
    {
        'tíulo': 'Minha História',
        'autor': 'Amanda Dias'
    },
    {
        'tíulo': 'Novo Dispositivo',
        'autor': 'Ariany Carvalho'
    },
    {
        'tíulo': 'Lançamento do Ano',
        'autor': 'Juan Murta'
    }
]


# rota padrão - GET http://localhost:5000
@app.route('/')
def obter_postagens():
    return jsonify(postagens)


# obter postagem por id - GET http://localhost:5000/postagem/1
@app.route('/postagem/<int:indice>', methods=['GET'])
def obter_postagem_por_indice(indice):
    return jsonify(postagens[indice])


# Criar uma nova postagem - POST http://localhost:5000/postagem
@app.route('/postagem', methods=['POST'])
def nova_postagem():
    postagem = {
        'tíulo': 'Lançamento do Ano',
        'autor': 'Juan Murta'
    }
    postagens.append(postagem)
    return jsonify(postagem, 200)


# Alterar uma postagem existente - PUT
@app.route('/postagem/<int:indice>', methods=['PUT'])
def atualiza_postagem_por_indice(indice):
    postagem_alterada = request.get_json()
    postagens[indice].update(postagem_alterada)
    return jsonify(postagens[indice], 200)


# Excluindo uma postagem - Delete
@app.route('/postagem/<int:indice>', methods=['DELETE'])
def excluir_postagem(indice):
    if postagens[indice] is not None:
        del postagens[indice]
        return jsonify(f'Foi excluído a postagem {postagens[indice]}', 200)
    return jsonify('Não foi encontrada a postagem', 404)



app.run(debug=True)
