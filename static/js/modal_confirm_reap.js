// modal_confirm_reap.js

// Abrir modal ao clicar no botão
document.getElementById('btn-gerar-reap').addEventListener('click', function() {
    document.getElementById('modal_confirm').style.display = 'flex';
});

// Função para fechar o modal
function closeModalConfirm() {
    document.getElementById('modal_confirm').style.display = 'none';
}

// Quando clica em "Sim"
document.getElementById('btn-modal-sim').addEventListener('click', function() {
    // Fecha modal
    closeModalConfirm();
    // Submete o formulário
    document.getElementById('form-gerar-reap').submit();
});

// Quando clica em "Não"
document.getElementById('btn-modal-nao').addEventListener('click', function() {
    closeModalConfirm();
});
