function autoGrow(element) {
    element.style.height = 'auto';
    element.style.height = (element.scrollHeight) + "px";
}

// Se já tiver conteúdo, ajusta ao carregar:
document.addEventListener('DOMContentLoaded', function() {
    var ta = document.getElementById('content-textarea');
    if (ta) {
        autoGrow(ta);
    }
});