const sections = ['menu','saida','resultado'];
const select = document.getElementById('lote');
let lotes = [];
function screen(name) {
  for (const id of sections) document.getElementById(id).hidden = id !== name;
  document.getElementById('content').focus();
  if (name === 'saida') loadLotes();
}
document.querySelectorAll('[data-screen]').forEach(b => b.addEventListener('click', () => screen(b.dataset.screen)));
async function loadLotes() {
  try {
    const response = await fetch('/api/lotes');
    if (!response.ok) throw new Error('Falha ao consultar lotes.');
    lotes = await response.json();
    select.replaceChildren();
    for (const lote of lotes) {
      const option = document.createElement('option');
      option.value = lote.id;
      option.textContent = `Lote ${lote.id} — produto ${lote.produto_id} — ${lote.saldo} unidades`;
      select.append(option);
    }
    updateDetails();
  } catch (e) { document.getElementById('detalhes').textContent = e.message; }
}
function updateDetails() {
  const lote = lotes.find(x => String(x.id) === select.value);
  document.getElementById('detalhes').textContent = lote
    ? `Fornecedor: ${lote.fornecedor} | Custo unitário: R$ ${(lote.custo_centavos/100).toFixed(2)} | Saldo disponível: ${lote.saldo}`
    : 'Nenhum lote cadastrado. Cadastre um produto, fornecedor e entrada pela API.';
}
select.addEventListener('change', updateDetails);
document.getElementById('saida-form').addEventListener('submit', async event => {
  event.preventDefault();
  const lote = lotes.find(x => String(x.id) === select.value);
  const quantidade = Number(document.getElementById('quantidade').value);
  const mensagem = document.getElementById('mensagem');
  const saldo = document.getElementById('saldo');
  if (!lote || !Number.isInteger(quantidade) || quantidade <= 0) {
    mensagem.textContent = 'Não foi possível registrar: selecione um lote e uma quantidade válida.';
    saldo.textContent = '';
    screen('resultado'); return;
  }
  try {
    const response = await fetch('/api/saidas', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({lote_id:lote.id,quantidade})});
    const result = await response.json();
    mensagem.textContent = response.ok ? '✓ Saída registrada com sucesso!' : `Atenção: ${result.erro || 'Operação rejeitada.'}`;
    saldo.textContent = response.ok ? `Saldo anterior: ${lote.saldo} | Quantidade retirada: ${quantidade} | Saldo atualizado: ${result.saldo}` : 'O estoque não foi alterado.';
  } catch (e) { mensagem.textContent = 'Não foi possível conectar ao servidor.'; saldo.textContent = ''; }
  screen('resultado');
});
