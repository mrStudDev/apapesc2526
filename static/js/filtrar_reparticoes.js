document.addEventListener('DOMContentLoaded', function() {
    const associacaoSelect = document.getElementById('id_associacao');
    const reparticaoSelect = document.getElementById('id_reparticao');

    if (associacaoSelect && reparticaoSelect) {
        associacaoSelect.addEventListener('change', function() {
            const associacaoId = this.value;

            // Limpa as opções anteriores SEM EXCEÇÃO
            reparticaoSelect.innerHTML = '<option value="">---------</option>';

            if (!associacaoId) return;

            // Realiza a requisição para carregar as repartições da associação selecionada
            fetch(`/associacao/ajax/reparticoes-por-associacao/?associacao_id=${associacaoId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.reparticoes && data.reparticoes.length > 0) {
                        // Preenche as novas opções de repartição
                        data.reparticoes.forEach(rep => {
                            const option = document.createElement('option');
                            option.value = rep.id;
                            option.textContent = rep.nome;

                            // Verifica se a opção já foi adicionada
                            const optionExists = [...reparticaoSelect.options].some(opt => opt.value === option.value);

                            if (!optionExists) {
                                reparticaoSelect.appendChild(option);
                            }
                        });
                    }
                })
                .catch(error => {
                    console.error('Erro ao buscar repartições:', error);
                });
        });
    }
});
