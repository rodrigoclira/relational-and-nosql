// static/core/main.js — pequenos aprimoramentos de interface, sem chamadas ao backend

document.addEventListener('DOMContentLoaded', function () {
    // Destaca o link do menu correspondente à página atual
    document.querySelectorAll('.sgc-navbar [data-nav-link]').forEach(function (link) {
        if (link.getAttribute('href') === window.location.pathname) {
            link.classList.add('active');
        }
    });

    // Envia o filtro de busca automaticamente ao trocar o tipo, sem esperar o clique no botão
    var tipoSelect = document.getElementById('tipo');
    if (tipoSelect) {
        tipoSelect.addEventListener('change', function () {
            tipoSelect.form.submit();
        });
    }

    // Botão "voltar ao topo": aparece após rolar a página
    var backToTop = document.getElementById('sgc-back-to-top');
    if (backToTop) {
        window.addEventListener('scroll', function () {
            backToTop.style.display = window.scrollY > 300 ? 'block' : 'none';
        });
        backToTop.addEventListener('click', function () {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
});
