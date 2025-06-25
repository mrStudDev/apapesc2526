if (!window.__filtrosReparticaoMunicipioLoaded) {
    window.__filtrosReparticaoMunicipioLoaded = true;

    document.addEventListener('DOMContentLoaded', function () {
        const associacaoSelect = document.getElementById('id_associacao');
        const reparticaoSelect = document.getElementById('id_reparticao');
        const municipioCircunscricaoSelect = document.getElementById('id_municipio_circunscricao');

        function limparSelect(selectElement) {
            while (selectElement.firstChild) {
                selectElement.removeChild(selectElement.firstChild);
            }
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = '---------';
            selectElement.appendChild(defaultOption);
        }

        if (associacaoSelect && reparticaoSelect) {
            associacaoSelect.addEventListener('change', function () {
                const associacaoId = this.value;

                limparSelect(reparticaoSelect);
                limparSelect(municipioCircunscricaoSelect);

                if (!associacaoId) return;

                fetch(`/associacao/ajax/reparticoes-por-associacao/?associacao_id=${associacaoId}`)
                    .then(response => response.json())
                    .then(data => {
                        const seen = new Set();

                        data.reparticoes.forEach(rep => {
                            if (!seen.has(rep.id)) {
                                const option = document.createElement('option');
                                option.value = rep.id;
                                option.textContent = rep.nome;
                                reparticaoSelect.appendChild(option);
                                seen.add(rep.id);
                            }
                        });
                    })
                    .catch(error => {
                        console.error('Erro ao carregar repartições:', error);
                    });
            });
        }

        if (reparticaoSelect && municipioCircunscricaoSelect) {
            reparticaoSelect.addEventListener('change', function () {
                const reparticaoId = this.value;

                limparSelect(municipioCircunscricaoSelect);

                if (!reparticaoId) return;

                fetch(`/associacao/ajax/municipios-por-reparticao/?reparticao_id=${reparticaoId}`)
                    .then(response => response.json())
                    .then(data => {
                        const seen = new Set();

                        data.municipios.forEach(mun => {
                            if (!seen.has(mun.id)) {
                                const option = document.createElement('option');
                                option.value = mun.id;
                                option.textContent = mun.nome;
                                municipioCircunscricaoSelect.appendChild(option);
                                seen.add(mun.id);
                            }
                        });
                    })
                    .catch(error => {
                        console.error('Erro ao carregar municípios:', error);
                    });
            });
        }
    });
}
