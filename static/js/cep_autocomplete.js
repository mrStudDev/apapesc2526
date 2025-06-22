document.addEventListener('DOMContentLoaded', function() {
    var cepInput = document.querySelector('#id_cep');

    if (cepInput) {
        cepInput.addEventListener('change', function() {
            buscarCep(cepInput);
        });
    }
});

function buscarCep(cepInput) {
    var cep = cepInput.value.replace(/\D/g, '');

    if (cep.length === 8) {
        fetch(`https://viacep.com.br/ws/${cep}/json/`)
            .then(response => response.json())
            .then(data => {
                if (!data.erro) {
                    var logradouro = document.querySelector('#id_logradouro');
                    var bairro = document.querySelector('#id_bairro');
                    var municipio = document.querySelector('#id_municipio');
                    var uf = document.querySelector('#id_uf');

                    if (logradouro) logradouro.value = data.logradouro;
                    if (bairro) bairro.value = data.bairro;
                    if (municipio) municipio.value = data.localidade;
                    if (uf) uf.value = data.uf;
                } else {
                    alert('CEP não encontrado.');
                    cepInput.value = '';
                    cepInput.focus();
                }
            })
            .catch(() => {
                alert('Erro ao consultar o CEP.');
            });
    } else if (cep.length > 0) {
        alert('CEP inválido! Deve conter exatamente 8 números.');
        cepInput.focus();
    }
}
