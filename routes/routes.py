from flask import Blueprint, request, jsonify
from database import get_db_connection

produtos_bp = Blueprint('produtos', __name__, url_prefix='/produtos')

# CREATE
@produtos_bp.route('', methods=['POST'])
def criar_produto():
    dados = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO produtos 
        (nome, cod, categoria, marca, preco, preco_venda, qtd_estoque, min_estoque, unidade)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        dados.get('nome'),
        dados.get('cod'),
        dados.get('categoria'),
        dados.get('marca'),
        float(dados.get('preco', 0)),
        float(dados.get('precoVenda', 0)),
        int(dados.get('qtdEstoque', 0)),
        int(dados.get('minEstoque', 0)),
        dados.get('unidade')
    ))

    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Produto criado"}), 201


# READ (todos)
@produtos_bp.route('', methods=['GET'])
def listar_produtos():
    conn = get_db_connection()
    produtos = conn.execute('SELECT * FROM produtos').fetchall()
    conn.close()

    return jsonify([dict(p) for p in produtos])


# READ (1)
@produtos_bp.route('/<int:id>', methods=['GET'])
def obter_produto(id):
    conn = get_db_connection()
    produto = conn.execute('SELECT * FROM produtos WHERE id = ?', (id,)).fetchone()
    conn.close()

    if produto is None:
        return jsonify({"erro": "Produto não encontrado"}), 404

    return jsonify(dict(produto))


# UPDATE
@produtos_bp.route('/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    dados = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE produtos SET
        nome = ?, cod = ?, categoria = ?, marca = ?,
        preco = ?, preco_venda = ?, qtd_estoque = ?, min_estoque = ?, unidade = ?
        WHERE id = ?
    ''', (
        dados.get('nome'),
        dados.get('cod'),
        dados.get('categoria'),
        dados.get('marca'),
        float(dados.get('preco', 0)),
        float(dados.get('precoVenda', 0)),
        int(dados.get('qtdEstoque', 0)),
        int(dados.get('minEstoque', 0)),
        dados.get('unidade'),
        id
    ))

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"erro": "Produto não encontrado"}), 404

    conn.close()
    return jsonify({"mensagem": "Produto atualizado"})


# DELETE
@produtos_bp.route('/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM produtos WHERE id = ?', (id,))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"erro": "Produto não encontrado"}), 404

    conn.close()
    return jsonify({"mensagem": "Produto deletado"})