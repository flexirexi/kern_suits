const removeModalEl = document.getElementById('removeModal');
const removeModal = removeModalEl ? new bootstrap.Modal(removeModalEl) : null;

function getCookie(name) {
    const m = document.cookie.match(new RegExp('(?:^|; )' + name + '=([^;]*)'));
    return m ? decodeURIComponent(m[1]) : null;
}
const csrftoken = getCookie('csrftoken');


let selectedRow = null;
let removeEndpoint = null;

function setSelected(row) {
    if (selectedRow) selectedRow.classList.remove('selected');
    selectedRow = row || null;
    if (selectedRow) selectedRow.classList.add('selected');
    const disabled = !selectedRow;
    ['btn-edit', 'btn-duplicate', 'btn-plus', 'btn-minus', 'btn-remove']
        .forEach(id => { const el = document.getElementById(id); if (el) el.disabled = disabled; });
}

document.querySelectorAll('.pm-row').forEach(row => {
    row.addEventListener('click', () => setSelected(row));
    row.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); setSelected(row); }
    });
});



// Toast
function showToast(msg) {
    const el = document.getElementById('pmToast');
    const body = document.getElementById('pmToastBody');
    if (!el || !body) return alert(msg);
    body.textContent = msg;
    if (window.bootstrap?.Toast) new bootstrap.Toast(el, { delay: 2200 }).show();
}


// POST helper -> returns JSON already
async function postJSON(url, body) {
    const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
        body: JSON.stringify(body || {})
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
}

// REMOVE: open modal
document.getElementById('btn-remove')?.addEventListener('click', () => {
    if (!selectedRow) { showToast('Please select a variant first.'); return; }
    removeEndpoint = selectedRow.dataset.endpointRemove;
    if (!removeEndpoint) { showToast('Remove endpoint missing.'); return; }
    removeModal?.show();
});

// REMOVE: confirm
document.getElementById('confirmRemove')?.addEventListener('click', async () => {
    if (!removeEndpoint || !selectedRow) return;
    const modalEl = document.getElementById('removeModal');
    try {
        const data = await postJSON(removeEndpoint); // <-- JSON direct
        // remove row + reset UI
        const row = selectedRow;
        const next = row.nextElementSibling || row.previousElementSibling;
        row.remove();
        selectedRow = null;
        ['btn-duplicate', 'btn-plus', 'btn-minus', 'btn-remove'].forEach(id => {
            const el = document.getElementById(id); if (el) el.disabled = true;
        });
        const editLink = document.getElementById('link-edit');
        if (editLink) { editLink.href = '#'; editLink.classList.add('is-disabled'); editLink.setAttribute('aria-disabled', 'true'); }
        if (next && next.classList.contains('pm-row')) next.focus();

        showToast((data && data.message) || 'Variant removed.');
        bootstrap.Modal.getInstance(modalEl)?.hide();
        removeModal?.hide();
    } catch (e) {
        console.error(e);
        showToast('Error removing variant.');
    } finally {
        removeEndpoint = null;
    }
});

// Button handlers
function requireSelection() {
    if (!selectedRow) { showToast('Please select a variant first.'); return null; }
    return selectedRow;
}

async function handlePlus() {
    const row = requireSelection(); if (!row) return;
    try {
        const data = await postJSON(row.dataset.endpointPlus);

        row.querySelector('[data-field="qty"]').textContent = data.stock;
        showToast(data.message || 'Increased quantity.');
    } catch (e) { showToast('Error increasing quantity.'); }
}

async function handleMinus() {
    const row = requireSelection(); if (!row) return;
    try {
        const data = await postJSON(row.dataset.endpointMinus);
        row.querySelector('[data-field="qty"]').textContent = data.stock;
        showToast(data.message || 'Reduced quantity.');
    } catch (e) { showToast('Error reducing quantity.'); }
}

async function handleDuplicate() {
    const row = requireSelection(); if (!row) return;
    try {
        const data = await postJSON(row.dataset.endpointDuplicate);
        showToast(data.message || 'Variant duplicated.');

    } catch (e) { showToast('Error duplicating variant.'); }
}

function handleEdit() {
    const row = requireSelection(); if (!row) return;

    window.location.href = row.dataset.endpointEdit;
}

let removeVariantEndpoint = null;
function handleRemoveAsk() {
    const row = requireSelection(); if (!row) return;
    removeVariantEndpoint = row.dataset.endpointRemove;
    const modal = new bootstrap.Modal('#removeModal');
    modal.show();
}


// --- Remove: ask ---
document.getElementById('btn-remove')?.addEventListener('click', function () {
    if (!selectedRow) { showToast('Please select a variant first.'); return; }
    removeEndpoint = selectedRow.dataset.endpointRemove;
    if (!removeEndpoint) { showToast('Remove endpoint missing.'); return; }
    var modal = new bootstrap.Modal(document.getElementById('removeModal'));
    modal.show();
});

// --- Remove: do ---
function handleRemoveDo() {
    if (!removeEndpoint || !selectedRow) return;

    postJSON(removeEndpoint).then(function (res) {
        if (!res.ok) { return res.text().then(function (t) { throw new Error(t || 'Request failed'); }); }
        return res.json();
    }).then(function (data) {
        // remove row from DOM
        var toRemove = selectedRow;
        // try to pick a sensible next focus candidate
        var next = toRemove.nextElementSibling || toRemove.previousElementSibling;
        toRemove.remove();
        selectedRow = null;

        // disable action buttons
        ['btn-duplicate', 'btn-plus', 'btn-minus', 'btn-remove'].forEach(function (id) {
            var el = document.getElementById(id); if (el) el.disabled = true;
        });
        // also disable edit link if you use it
        var editLink = document.getElementById('link-edit');
        if (editLink) { editLink.href = '#'; editLink.classList.add('is-disabled'); editLink.setAttribute('aria-disabled', 'true'); }

        // focus next row (optional)
        if (next && next.classList.contains('pm-row')) next.focus();

        // success toast
        showToast((data && data.message) || 'Variant removed.');
        // hide modal
        bootstrap.Modal.getInstance(document.getElementById('removeModal'))?.hide();
    }).catch(function (err) {
        showToast('Error removing variant.');
        console.error(err);
    }).finally(function () {
        removeEndpoint = null;
    });
}

removeModalEl?.addEventListener('hidden.bs.modal', () => {
    document.body.classList.remove('modal-open');           // falls hängen geblieben
    document.body.style.removeProperty('padding-right');    // falls hinzugefügt
    document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
});


function handleCreate() {
    window.location.href = "{% url 'bc_variant_create' %}";
}

document.getElementById('btn-plus').addEventListener('click', handlePlus);
document.getElementById('btn-minus').addEventListener('click', handleMinus);
document.getElementById('btn-duplicate').addEventListener('click', handleDuplicate);
document.getElementById('btn-edit').addEventListener('click', handleEdit);
document.getElementById('btn-remove').addEventListener('click', handleRemoveAsk);
document.getElementById('btn-create').addEventListener('click', handleCreate);
document.getElementById('confirmRemove').addEventListener('click', handleRemoveDo);