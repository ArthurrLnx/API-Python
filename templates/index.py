from flask import Flask, jsonify, request

app = Flask(__name__)

# Dados temporários (em uma aplicação real, usaria um banco de dados)
produtos = [
    {"id": 1, "nome": "Smartphone", "preco": 1500.00},
    {"id": 2, "nome": "Notebook", "preco": 3500.00},
    {"id": 3, "nome": "Tablet", "preco": 1200.00}
]

# Rota raiz
@app.route('/')
def home():
    return "Bem-vindo à API de Produtos!"

# Obter todos os produtos
@app.route('/produtos', methods=['GET'])
def get_produtos():
    return jsonify({"produtos": produtos, "total": len(produtos)})

# Obter um produto específico por ID
@app.route('/produtos/<int:produto_id>', methods=['GET'])
def get_produto(produto_id):
    produto = next((p for p in produtos if p['id'] == produto_id), None)
    if produto:
        return jsonify(produto)
    return jsonify({"erro": "Produto não encontrado"}), 404

# Adicionar um novo produto
@app.route('/produtos', methods=['POST'])
def add_produto():
    dados = request.get_json()
    
    # Validação mais robusta
    if not dados:
        return jsonify({"erro": "Dados não fornecidos"}), 400
        
    if not isinstance(dados, dict):
        return jsonify({"erro": "Dados devem ser um objeto JSON"}), 400
        
    nome = dados.get('nome')
    preco = dados.get('preco')
    
    if not nome or not isinstance(nome, str):
        return jsonify({"erro": "Nome do produto inválido ou faltando"}), 400
        
    if preco is None or not isinstance(preco, (int, float)) or preco <= 0:
        return jsonify({"erro": "Preço deve ser um número positivo"}), 400
    
    # Verifica se produto já existe pelo nome
    if any(p['nome'].lower() == nome.lower() for p in produtos):
        return jsonify({"erro": "Produto com este nome já existe"}), 409
    
    novo_id = max(p['id'] for p in produtos) + 1 if produtos else 1
    novo_produto = {
        "id": novo_id,
        "nome": nome,
        "preco": float(preco)
    }
    
    produtos.append(novo_produto)
    return jsonify(novo_produto), 201

# Atualizar um produto existente
@app.route('/produtos/<int:produto_id>', methods=['PUT'])
def update_produto(produto_id):
    dados = request.get_json()
    
    if not dados:
        return jsonify({"erro": "Dados não fornecidos"}), 400
        
    produto = next((p for p in produtos if p['id'] == produto_id), None)
    
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404
    
    # Validações para atualização
    if 'nome' in dados:
        novo_nome = dados['nome']
        if not isinstance(novo_nome, str) or not novo_nome.strip():
            return jsonify({"erro": "Nome do produto inválido"}), 400
            
        # Verifica se novo nome já existe (excluindo o próprio produto)
        if any(p['id'] != produto_id and p['nome'].lower() == novo_nome.lower() for p in produtos):
            return jsonify({"erro": "Outro produto com este nome já existe"}), 409
    
    if 'preco' in dados:
        novo_preco = dados['preco']
        if not isinstance(novo_preco, (int, float)) or novo_preco <= 0:
            return jsonify({"erro": "Preço deve ser um número positivo"}), 400
    
    produto.update(dados)
    # Garante que o ID não seja alterado
    produto['id'] = produto_id
    
    return jsonify(produto)

# Deletar um produto
@app.route('/produtos/<int:produto_id>', methods=['DELETE'])
def delete_produto(produto_id):
    global produtos
    
    produto = next((p for p in produtos if p['id'] == produto_id), None)
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404
    
    produtos = [p for p in produtos if p['id'] != produto_id]
    return jsonify({"mensagem": "Produto deletado com sucesso", "produto": produto}), 200

if __name__ == '__main__':
    app.run(debug=True)