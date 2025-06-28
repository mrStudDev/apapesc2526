document.addEventListener('DOMContentLoaded', () => {
  let uploadIndex = 1;

  // Aplica listener ao input inicial
  setupFileInput(document.querySelector('#file-input-0'));

  // Função global para adicionar um novo bloco
  window.addForm = function () {
    const container = document.getElementById('form-container');
    const selectBase = document.getElementById('id_tipo_base');
    const currentIndex = uploadIndex++;

    const block = document.createElement('div');
    block.className = 'upload-block';

    block.innerHTML = `
      <div class="form-group">
        <label>Tipo de Documento:</label>
        <select name="tipo" class="tipo-select">
          ${Array.from(selectBase.options).map(o => `<option value="${o.value}">${o.text}</option>`).join('')}
        </select>
      </div>
      <div class="form-group">
        <label>Ou/Nomear Doc:</label>
        <input type="text" name="tipo_custom">
      </div>
      <div class="form-group file-group">
        <label id="arquivo-label-${currentIndex}">Arquivo:</label>
        <input type="file" name="arquivo" id="file-input-${currentIndex}" required>
      </div>
      <button type="button" class="remove-btn" onclick="removeBlock(this)">🗑️ Remover</button>
    `;

    container.appendChild(block);
    setupFileInput(block.querySelector(`#file-input-${currentIndex}`));
  };

  // Função global para remover um bloco
  window.removeBlock = function (button) {
    const container = document.getElementById('form-container');
    const blocks = container.querySelectorAll('.upload-block');
    if (blocks.length > 1) {
      button.closest('.upload-block').remove();
    }
  };

  // Setup dinâmico para atualizar label do input file
  function setupFileInput(input) {
    if (!input) return;
    const label = input.previousElementSibling;
    input.addEventListener('change', () => {
      const count = input.files.length;
      label.textContent = count > 1
        ? `${count} arquivos selecionados`
        : count === 1
        ? input.files[0].name
        : 'Nenhum arquivo selecionado';
    });
  }
});
