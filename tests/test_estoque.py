import pytest
from app import create_app
from app.models import db, Produto, Fornecedor, Lote, Movimentacao
from app.services import entrada, saida, RegraEstoqueError


@pytest.fixture()
def contexto(tmp_path):
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': f'sqlite:///{tmp_path / "teste.db"}'})
    with app.app_context():
        produto = Produto(nome='Produto fictício', categoria='TCG', preco_venda_centavos=5000)
        fornecedor = Fornecedor(nome='Fornecedor fictício')
        db.session.add_all([produto, fornecedor])
        db.session.commit()
        yield produto.id, fornecedor.id
        db.session.remove()


def test_entrada_e_saida_por_lote(contexto):
    produto_id, fornecedor_id = contexto
    lote = entrada(produto_id, fornecedor_id, 10, 3650)
    assert lote.quantidade_atual == 10
    assert lote.custo_unitario_centavos == 3650
    lote = saida(lote.id, 3)
    assert lote.quantidade_atual == 7
    assert db.session.query(Movimentacao).count() == 2


def test_saida_maior_que_saldo_nao_altera_estoque(contexto):
    produto_id, fornecedor_id = contexto
    lote = entrada(produto_id, fornecedor_id, 10, 3650)
    with pytest.raises(RegraEstoqueError, match='Saldo insuficiente'):
        saida(lote.id, 11)
    db.session.refresh(lote)
    assert lote.quantidade_atual == 10
    assert db.session.query(Movimentacao).count() == 1


def test_lotes_preservam_custos_distintos(contexto):
    produto_id, fornecedor_id = contexto
    lote_a = entrada(produto_id, fornecedor_id, 5, 3000)
    lote_b = entrada(produto_id, fornecedor_id, 8, 4000)
    assert lote_a.custo_unitario_centavos == 3000
    assert lote_b.custo_unitario_centavos == 4000
    assert lote_a.quantidade_atual + lote_b.quantidade_atual == 13


def test_quantidade_invalida(contexto):
    produto_id, fornecedor_id = contexto
    with pytest.raises(RegraEstoqueError):
        entrada(produto_id, fornecedor_id, 0, 3650)
