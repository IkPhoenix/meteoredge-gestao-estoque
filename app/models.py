from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

db = SQLAlchemy()


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(160), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    preco_venda_centavos = db.Column(db.Integer, nullable=False, default=0)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    __table_args__ = (CheckConstraint('preco_venda_centavos >= 0'),)


class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(160), nullable=False, unique=True)
    ativo = db.Column(db.Boolean, nullable=False, default=True)


class Lote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'), nullable=False)
    quantidade_inicial = db.Column(db.Integer, nullable=False)
    quantidade_atual = db.Column(db.Integer, nullable=False)
    custo_unitario_centavos = db.Column(db.Integer, nullable=False)
    data_entrada = db.Column(db.DateTime, nullable=False)
    produto = db.relationship('Produto')
    fornecedor = db.relationship('Fornecedor')
    __table_args__ = (
        CheckConstraint('quantidade_inicial > 0'),
        CheckConstraint('quantidade_atual >= 0 AND quantidade_atual <= quantidade_inicial'),
        CheckConstraint('custo_unitario_centavos >= 0'),
    )


class Movimentacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lote_id = db.Column(db.Integer, db.ForeignKey('lote.id'), nullable=False)
    tipo = db.Column(db.String(7), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data_movimentacao = db.Column(db.DateTime, nullable=False)
    observacao = db.Column(db.String(300))
    __table_args__ = (
        CheckConstraint("tipo IN ('ENTRADA', 'SAIDA')"),
        CheckConstraint('quantidade > 0'),
    )
