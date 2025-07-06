
(function () {
  // 1. Restaurar aba ativa salva (sem scroll com replaceState)
  const savedHash = sessionStorage.getItem('abaAtiva');
  if (savedHash && document.querySelector(savedHash)) {
    history.replaceState(null, null, savedHash);
    sessionStorage.removeItem('abaAtiva');
  }

  // 2. Espera o DOM carregar
  document.addEventListener('DOMContentLoaded', () => {
    const tabLinks = Array.from(document.querySelectorAll('.tab-link'));
    const tabContents = Array.from(document.querySelectorAll('.tab-content'));

    function ativarAba(tabId, updateHash = false) {
      tabLinks.forEach(btn => btn.classList.toggle('active', btn.dataset.tab === tabId));
      tabContents.forEach(content =>
        content.classList.toggle('active', content.id === 'tab-' + tabId)
      );
      if (updateHash) history.replaceState(null, null, '#tab-' + tabId);
    }

    // 3. Clique nas abas atualiza hash
    tabLinks.forEach(btn => {
      btn.addEventListener('click', () => {
        ativarAba(btn.dataset.tab, true);
      });
    });

    // 4. Ativar aba via hash da URL ou padrão
    let currentTab = window.location.hash.replace('#tab-', '');
    if (!currentTab || !document.getElementById('tab-' + currentTab)) {
      currentTab = tabLinks[0]?.dataset.tab;
    }
    ativarAba(currentTab, false);

    // 5. Salva aba ativa antes de submit
    document.querySelectorAll('form').forEach(form => {
      form.addEventListener('submit', () => {
        sessionStorage.setItem('abaAtiva', window.location.hash);
      });
    });
  });
})();