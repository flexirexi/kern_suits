// CSRF
function getCookie(name) { const m = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)')); return m ? decodeURIComponent(m[1]) : null; }
const csrftoken = getCookie('csrftoken');
let firstLoad = true;

// Category render helper
function renderCategory(el) {
    if (!el) return;
    const isActive = el.getAttribute('data-active') === '1';
    const isStaff = el.getAttribute('data-staff') === '1';
    const isSuper = el.getAttribute('data-super') === '1';

    let text = 'customer';
    let classes = 'fw-normal text-body';

    if (isSuper) { text = 'admin'; classes = 'fw-bold'; el.style.color = '#7e0a0a'; }      // dark red
    else if (isStaff) { text = 'staff'; classes = 'fw-bold'; el.style.color = '#0a3d7e'; } // dark blue
    else { el.style.removeProperty('color'); }

    if (!isActive) text += ' (deactivated)';

    el.className = 'user-cat ' + classes;
    el.textContent = text;
}

// initial category render
document.querySelectorAll('.user-cat').forEach(renderCategory);

// Toast
function showToast(msg) {
    const el = document.getElementById('rightsToast');
    const body = document.getElementById('rightsToastBody');
    if (!el || !body) return;
    body.textContent = msg || 'Saved';
    if (window.bootstrap?.Toast) new bootstrap.Toast(el, { delay: 1800 }).show();
}

// Toggle handler (only enabled for superusers)
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.rights-toggle').forEach(function (cb) {
        cb.addEventListener('change', function (e) {
            const row = e.target.closest('.pm-row');
            const url = row?.dataset.endpoint;
            const field = e.target.dataset.field;
            const value = e.target.checked ? '1' : '0';
            if (!url || !field) { return; }
    
            fetch(url, {
                method: 'POST',
                headers: { 'X-CSRFToken': csrftoken },
                body: new URLSearchParams({ field, value })
            }).then(function (res) {
                if (!res.ok) return res.text().then(t => { throw new Error(t || 'Request failed') });
                return res.json();
            }).then(function (data) {
                // update category dataset based on server truth
                alert("firstload?");
                if (!firstLoad) {
                    const cat = row.querySelector('.user-cat');
                    if (cat) {
                        cat.setAttribute('data-active', data.is_active ? '1' : '0');
                        cat.setAttribute('data-staff', data.is_staff ? '1' : '0');
                        cat.setAttribute('data-super', data.is_superuser ? '1' : '0');
                        renderCategory(cat);
                    }
                    showToast('Saved.');
                }
                firstLoad = false;
            }).catch(function (err) {
                // revert UI on error
                e.target.checked = !e.target.checked;
                showToast('Error saving.');
                console.error(err);
                firstLoad = false;
            });
        });
    });
    
});