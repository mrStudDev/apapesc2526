function copySenhas(elementId, triggerBtn = null) {
  const el = document.getElementById(elementId);
  if (!el) return;

  const text = Array.from(el.childNodes)
    .filter(n => n.nodeType === Node.TEXT_NODE)
    .map(n => n.textContent.trim())
    .join(' ');

  const textArea = document.createElement("textarea");
  textArea.value = text;
  textArea.style.position = "fixed";
  textArea.style.left = "-9999px";
  document.body.appendChild(textArea);
  textArea.select();

  try {
    if (document.execCommand("copy") && triggerBtn) {
      showCheckIcon(triggerBtn);
    }
  } catch (err) {
    console.error("Erro ao copiar senha:", err);
  }

  document.body.removeChild(textArea);
}



function showCheckIcon(triggerElement) {
  // Já existe o ícone?
  if (triggerElement.querySelector(".copy-check")) return;

  const icon = document.createElement("span");
  icon.textContent = "✔️";
  icon.className = "copy-check";
  icon.style.color = "green";
  icon.style.marginLeft = "1px";
  icon.style.fontSize = "9px";
  icon.style.opacity = "0.85";
  icon.style.transition = "opacity 0.3s ease";

  triggerElement.appendChild(icon);

  setTimeout(() => {
    icon.style.opacity = "0";
    setTimeout(() => {
      triggerElement.removeChild(icon);
    }, 300);
  }, 1200);
}
