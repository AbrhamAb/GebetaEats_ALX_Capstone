// Simple scroll reveal helper using IntersectionObserver
document.addEventListener('DOMContentLoaded', function () {
    const els = document.querySelectorAll('[data-animate]');
    if (!els.length) return;
    const io = new IntersectionObserver((entries) => {
        entries.forEach((e) => {
            if (e.isIntersecting) {
                e.target.classList.add('in-view');
                io.unobserve(e.target);
            }
        });
    }, { threshold: 0.12 });
    els.forEach(el => io.observe(el));
    // update cart count
    function updateCartCount() {
        fetch('/cart/count/')
            .then(r => r.json())
            .then(data => {
                const el = document.getElementById('cart-count');
                if (el) el.textContent = data.count;
            }).catch(() => { });
    }
    updateCartCount();

    // handle AJAX add-to-cart forms
    function bindAddToCart() {
        document.querySelectorAll('form.ajax-add-to-cart').forEach(form => {
            if (form.dataset.bound) return; form.dataset.bound = '1';
            form.addEventListener('submit', function (e) {
                e.preventDefault();
                const fd = new FormData(form);
                fetch(form.action, { method: 'POST', body: fd, headers: { 'X-Requested-With': 'XMLHttpRequest' } })
                    .then(r => r.json())
                    .then(data => {
                        if (data && data.success) {
                            updateCartCount();
                            showToast(data.message || 'Added to cart');
                            // refresh preview if present
                            updateCartPreview();
                        } else {
                            showToast('Could not add to cart', 'error');
                        }
                    }).catch(() => showToast('Network error', 'error'));
            });
        });
    }
    bindAddToCart();

    // cart preview
    function updateCartPreview() {
        const preview = document.getElementById('cart-preview-body');
        if (!preview) return;
        fetch('/cart/preview/')
            .then(r => r.json())
            .then(data => {
                preview.innerHTML = '';
                if (!data.items || data.items.length === 0) {
                    preview.innerHTML = '<div class="p-3">Cart is empty</div>';
                    return;
                }
                data.items.forEach(it => {
                    const el = document.createElement('div');
                    el.className = 'd-flex justify-content-between align-items-center p-2 border-bottom';
                    el.innerHTML = `<div><a href="${it.url}">${it.name}</a><div class="text-muted small">Qty: ${it.quantity}</div></div><div>${it.line_total}</div>`;
                    preview.appendChild(el);
                });
                const foot = document.createElement('div');
                foot.className = 'p-2';
                foot.innerHTML = `<div class="d-flex justify-content-between"><strong>Total</strong><strong>${data.total}</strong></div><div class="mt-2 text-end"><a href="/cart/" class="btn btn-sm btn-primary">View Cart</a></div>`;
                preview.appendChild(foot);
            }).catch(() => { });
    }
    // update preview when clicking cart badge
    const cartLink = document.querySelector('a[href="/cart/"]');
    if (cartLink) {
        cartLink.addEventListener('mouseenter', updateCartPreview);
    }
    updateCartPreview();

    // show Django messages as toasts
    function showToast(message, level) {
        const containerId = 'toast-container';
        let container = document.getElementById(containerId);
        if (!container) {
            container = document.createElement('div');
            container.id = containerId;
            container.style.position = 'fixed';
            container.style.top = '16px';
            container.style.right = '16px';
            container.style.zIndex = 1200;
            document.body.appendChild(container);
        }
        const toast = document.createElement('div');
        toast.className = 'toast align-items-center text-white bg-success border-0 show';
        if (level && level.indexOf('error') !== -1) toast.className = 'toast align-items-center text-white bg-danger border-0 show';
        toast.style.minWidth = '220px';
        toast.style.marginTop = '8px';
        toast.innerHTML = `<div class="d-flex"><div class="toast-body">${message}</div><button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button></div>`;
        container.appendChild(toast);
        setTimeout(() => { toast.remove(); }, 5000);
    }

    const msgs = document.querySelectorAll('#django-messages .msg');
    msgs.forEach(m => showToast(m.textContent.trim(), m.dataset.level || ''));
});
