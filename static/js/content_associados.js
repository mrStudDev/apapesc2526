document.addEventListener('DOMContentLoaded', function() {
    // --- AutoGrow no carregamento
    var ta = document.getElementById('content-textarea');
    if (ta) {
        autoGrow(ta);
    }

    // --- Submit AJAX do form
    var notasForm = document.getElementById('notas-form');
    if (notasForm) {
        notasForm.addEventListener('submit', function(e){
            e.preventDefault();
            const content = ta.value;
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
    }

    // ---- Funções do Editor
    window.wrapSelection = function(tag, cssClass) {
        var ta = document.getElementById('content-textarea');
        if (!ta) return;
        var start = ta.selectionStart;
        var end = ta.selectionEnd;
        var selected = ta.value.substring(start, end);

        let openTag = `<${tag}${cssClass ? ` class="${cssClass}"` : ''}>`;
        let closeTag = `</${tag}>`;

        if (tag === 'ul') {
            let items = selected.split('\n').map(line => `<li>${line.trim()}</li>`).join('');
            ta.value = ta.value.substring(0, start) + `<ul>${items}</ul>` + ta.value.substring(end);
            ta.setSelectionRange(start, start + (`<ul>${items}</ul>`).length);
            ta.focus();
            window.autoGrow(ta);
            return;
        }

        ta.value = ta.value.substring(0, start) + openTag + selected + closeTag + ta.value.substring(end);
        ta.setSelectionRange(start + openTag.length, start + openTag.length + selected.length);
        ta.focus();
        window.autoGrow(ta);
    };

    window.insertComment = function() {
        var ta = document.getElementById('content-textarea');
        if (!ta) return;
        var start = ta.selectionStart;
        var end = ta.selectionEnd;
        var selected = ta.value.substring(start, end) || 'Comentário';
        let html = `<span class="comentario">${selected}</span>`;
        ta.value = ta.value.substring(0, start) + html + ta.value.substring(end);
        ta.setSelectionRange(start + html.length, start + html.length);
        ta.focus();
        window.autoGrow(ta);
    };

    window.autoGrow = function(element) {
        element.style.height = 'auto';
        element.style.height = (element.scrollHeight) + "px";
    };

});
