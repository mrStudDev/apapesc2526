document.addEventListener('DOMContentLoaded', () => {
  let deleteDocId = null;

  window.openDeleteModal = function(docId) {
    deleteDocId = docId;
    document.getElementById('deleteModal').style.display = 'flex';
  }

  window.closeDeleteModal = function() {
    deleteDocId = null;
    document.getElementById('deleteModal').style.display = 'none';
  }

  const confirmBtn = document.getElementById('confirmDeleteBtn');
  if (confirmBtn) {
    confirmBtn.addEventListener('click', () => {
      if (!deleteDocId) return;

      fetch(`/uploads/delete/${deleteDocId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
        }
      })
      .then(resp => {
        if (resp.ok) {
          closeDeleteModal();
          window.location.reload();
        } else alert('Erro ao excluir.');
      })
      .catch(() => alert('Erro na conexão.'));
    });
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      document.cookie.split(';').forEach(c => {
        const cookie = c.trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        }
      });
    }
    return cookieValue;
  }
});
