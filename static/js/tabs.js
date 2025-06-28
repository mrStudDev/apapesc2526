// tabs.js
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.tab-link').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-link').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      btn.classList.add('active');
      const target = document.getElementById('tab-' + btn.dataset.tab);
      if (target) target.classList.add('active');
    });
  });
});
document.addEventListener('DOMContentLoaded', () => {
  const hash = window.location.hash;

  if (hash && document.querySelector(hash)) {
    document.querySelectorAll('.tab-link').forEach(btn =>
      btn.classList.remove('active')
    );
    document.querySelectorAll('.tab-content').forEach(c =>
      c.classList.remove('active')
    );

    const tabBtn = document.querySelector(`.tab-link[data-tab="${hash.replace('#tab-', '')}"]`);
    if (tabBtn) tabBtn.classList.add('active');
    document.querySelector(hash).classList.add('active');
  }

  document.querySelectorAll('.tab-link').forEach(btn =>
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-link').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
    })
  );
});
