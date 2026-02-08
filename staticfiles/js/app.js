document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-confirm]").forEach(function (btn) {
        btn.addEventListener("click", function (e) {
            if (!confirm(btn.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });
});
