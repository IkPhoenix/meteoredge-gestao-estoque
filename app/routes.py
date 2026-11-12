from flask import Blueprint, jsonify, request
from .models import db, Produto, Fornecedor, Lote
from .services import entrada, saida, RegraEstoqueError

api = Blueprint('api', __name__, url_prefix='/api')


def json_body():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise RegraEstoqueError('Envie um objeto JSON válido.')
    return data


@api.errorhandler(RegraEstoqueError)
def bad_request(error):
    return jsonify({'erro': str(error)}), 400


@api.get('/produtos')
def produtos():
    return jsonify([{'id': p.id, 'nome': p.nome, 'categoria': p.categoria}
                    for p in db.session.query(Produto).order_by(Produto.nome).all()])


@api.get('/lotes')
def lotes():
    return jsonify([{'id': l.id, 'produto_id': l.produto_id,
                     'fornecedor': l.fornecedor.nome, 'saldo': l.quantidade_atual,
                     'custo_centavos': l.custo_unitario_centavos}
                    for l in db.session.query(Lote).order_by(Lote.id).all()])


@api.post('/produtos')
def cadastrar_produto():
    data = json_body()
    nome, categoria, preco = data.get('nome'), data.get('categoria'), data.get('preco_centavos')
    if not isinstance(nome, str) or not nome.strip() or not isinstance(categoria, str) or not categoria.strip() or type(preco) is not int or preco < 0:
        raise RegraEstoqueError('Nome, categoria e preço válido são obrigatórios.')
    item = Produto(nome=nome.strip(), categoria=categoria.strip(), preco_venda_centavos=preco)
    db.session.add(item)
    db.session.commit()
    return jsonify({'id': item.id}), 201


@api.post('/fornecedores')
def cadastrar_fornecedor():
    data = json_body()
    nome = data.get('nome')
    if not isinstance(nome, str) or not nome.strip():
        raise RegraEstoqueError('Nome do fornecedor é obrigatório.')
    normalized = nome.strip()
    if db.session.query(Fornecedor).filter(db.func.lower(Fornecedor.nome) == normalized.lower()).first():
        raise RegraEstoqueError('Fornecedor já cadastrado.')
    item = Fornecedor(nome=normalized)
    db.session.add(item)
    db.session.commit()
    return jsonify({'id': item.id}), 201


@api.post('/entradas')
def registrar_entrada():
    data = json_body()
    lote = entrada(data.get('produto_id'), data.get('fornecedor_id'), data.get('quantidade'), data.get('custo_centavos'))
    return jsonify({'lote_id': lote.id, 'saldo': lote.quantidade_atual}), 201


@api.post('/saidas')
def registrar_saida():
    data = json_body()
    lote = saida(data.get('lote_id'), data.get('quantidade'))
    return jsonify({'lote_id': lote.id, 'saldo': lote.quantidade_atual})
