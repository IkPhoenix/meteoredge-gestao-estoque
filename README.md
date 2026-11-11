# MeteorEdge — Gestão de Estoque (MVP acadêmico)

Projeto educacional para controle de produtos, fornecedores, lotes de compra e saídas de estoque com custo real por lote.

## Tecnologias
Python 3.12, Flask, Flask-SQLAlchemy, SQLAlchemy, SQLite, HTML, CSS, JavaScript e Pytest.

## Execução local
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python run.py
```
Abra `http://127.0.0.1:5000`.

## Testes
```bash
python -m pytest -q
```

## Dados de demonstração (PowerShell)
O MVP não tem formulário visual de cadastro. Use a API local para cadastrar um produto, um fornecedor e uma entrada antes de testar a saída na interface.

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/api/produtos -Method Post -ContentType 'application/json' -Body '{"nome":"Blister Quádruplo Pokémon - Coleção Exemplo","categoria":"TCG","preco_centavos":5990}'
Invoke-RestMethod -Uri http://127.0.0.1:5000/api/fornecedores -Method Post -ContentType 'application/json' -Body '{"nome":"Distribuidora Exemplo"}'
Invoke-RestMethod -Uri http://127.0.0.1:5000/api/entradas -Method Post -ContentType 'application/json' -Body '{"produto_id":1,"fornecedor_id":1,"quantidade":10,"custo_centavos":3650}'
```

## Aviso de segurança
**Protótipo local para estudo; não publicar na internet nem usar com dados reais.** Esta versão ainda não implementa login, autorização, CSRF, rate limiting, migrações de banco nem configuração de produção. O RNF01 e partes do RNF02 permanecem pendentes. O `.gitignore` deve excluir o banco SQLite, `.env` e outros segredos. A chave de desenvolvimento é apenas temporária.

## Versionamento
Os cinco pacotes de alterações representam etapas reais e devem ser publicados separadamente, com mensagens semânticas `feat:` e `test:`. Nunca invente SHAs ou datas.
## Critérios de validação do estoque

O sistema deverá verificar a quantidade disponível antes de registrar qualquer saída de mercadorias.

- Não permitir saídas com quantidade maior que o saldo disponível.
- Rejeitar quantidades negativas ou iguais a zero.
- Preservar o saldo quando uma operação for rejeitada.
- Registrar movimentações válidas vinculadas ao lote correspondente.
- Apresentar mensagens claras de confirmação ou erro.

Esses critérios orientarão os testes de integridade do estoque e a revisão técnica do MVP.
