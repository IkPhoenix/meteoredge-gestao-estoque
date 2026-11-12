from datetime import datetime, timezone
from sqlalchemy import update
from .models import db, Produto, Fornecedor, Lote, Movimentacao


class RegraEstoqueError(ValueError):
    pass


def entrada(produto_id, fornecedor_id, quantidade, custo_centavos):
    if type(quantidade) is not int or quantidade <= 0:
        raise RegraEstoqueError('Quantidade deve ser um inteiro positivo.')
    if type(custo_centavos) is not int or custo_centavos < 0:
        raise RegraEstoqueError('Custo deve ser um inteiro não negativo.')
    if not db.session.get(Produto, produto_id) or not db.session.get(Fornecedor, fornecedor_id):
        raise RegraEstoqueError('Produto ou fornecedor não encontrado.')
    lote = Lote(produto_id=produto_id, fornecedor_id=fornecedor_id,
                quantidade_inicial=quantidade, quantidade_atual=quantidade,
                custo_unitario_centavos=custo_centavos,
                data_entrada=datetime.now(timezone.utc))
    db.session.add(lote)
    db.session.flush()
    db.session.add(Movimentacao(lote_id=lote.id, tipo='ENTRADA', quantidade=quantidade,
                                data_movimentacao=datetime.now(timezone.utc)))
    db.session.commit()
    return lote


def saida(lote_id, quantidade):
    if type(quantidade) is not int or quantidade <= 0:
        raise RegraEstoqueError('Quantidade deve ser um inteiro positivo.')
    lote = db.session.get(Lote, lote_id)
    if lote is None:
        raise RegraEstoqueError('Lote não encontrado.')
    # Atomic conditional update avoids negative balance even with concurrent requests.
    result = db.session.execute(update(Lote).where(
        Lote.id == lote_id, Lote.quantidade_atual >= quantidade
    ).values(quantidade_atual=Lote.quantidade_atual - quantidade))
    if result.rowcount != 1:
        db.session.rollback()
        raise RegraEstoqueError('Saldo insuficiente no lote.')
    db.session.add(Movimentacao(lote_id=lote_id, tipo='SAIDA', quantidade=quantidade,
                                data_movimentacao=datetime.now(timezone.utc)))
    db.session.commit()
    db.session.refresh(lote)
    return lote
