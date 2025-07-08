document.addEventListener("DOMContentLoaded", function() {
    const messages = document.querySelectorAll(".message, .toast");
    messages.forEach(function(msg) {
        setTimeout(function() {
            msg.style.transition = "opacity 0.5s ease-out";
            msg.style.opacity = "0";
            setTimeout(function() {
                msg.remove();
            }, 600);
        }, 3000);
    });
});
