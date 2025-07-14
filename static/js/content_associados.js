
document.getElementById('notas-form').addEventListener('submit', function(e){
    e.preventDefault();
    const content = document.getElementById('content-textarea').value;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const msgSpan = document.getElementById('notas-msg');

    fetch(window.location.href, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: new URLSearchParams({ content })
    })
    .then(resp => resp.json())
    .then(data => {
        if(data.success){
            msgSpan.textContent = data.message;
            msgSpan.style.display = 'inline';
            msgSpan.style.color = 'green';
            setTimeout(()=>msgSpan.style.display='none', 2500);
        } else {
            msgSpan.textContent = "Falha ao salvar!";
            msgSpan.style.display = 'inline';
            msgSpan.style.color = 'red';
        }
    })
    .catch(()=>{
        msgSpan.textContent = "Erro na requisição!";
        msgSpan.style.display = 'inline';
        msgSpan.style.color = 'red';
    });
});

