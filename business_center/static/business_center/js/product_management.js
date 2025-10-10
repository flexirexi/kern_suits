

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
const csrftoken = getCookie('csrftoken');

// Selection handling
let selectedRow = null;
function setSelected(row) {
    if (selectedRow) selectedRow.classList.remove('selected');
    selectedRow = row;
    if (selectedRow) selectedRow.classList.add('selected');
    const disabled = !selectedRow;
    document.getElementById('btn-edit').disabled = disabled;
    document.getElementById('btn-duplicate').disabled = disabled;
    document.getElementById('btn-plus').disabled = disabled;
    document.getElementById('btn-minus').disabled = disabled;
    document.getElementById('btn-remove').disabled = disabled;
}

document.querySelectorAll('.pm-row').forEach(row => {
    row.addEventListener('click', () => setSelected(row));
    row.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {e.preventDefault(); setSelected(row); }
    if (e.key === 'Enter') handleEdit(); 
    });
    row.addEventListener('dblclick', () => handleEdit());
});


function showToast(msg) {
    const el = document.getElementById('pmToast');
    document.getElementById('pmToastBody').textContent = msg;
    if (window.bootstrap?.Toast) {
        new bootstrap.Toast(el, { delay: 2200 }).show();
    } else {
        el.classList.add('show');
        setTimeout(() => el.classList.remove('show'), 2200);
    }
}

// Fetch helper
async function postJSON(url, body) {
    const res = await fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
        body: JSON.stringify(body || { })
    });
    if (!res.ok) throw new Error(await res.text());
    return await res.json();
}

// Button handlers
function requireSelection() {
    if (!selectedRow) {showToast('Please select a variant first.'); return null; }
    return selectedRow;
}

async function handlePlus() {
    const row = requireSelection(); if (!row) return;
    try {
        const data = await postJSON(row.dataset.endpointPlus);

    row.querySelector('[data-field="qty"]').textContent = data.stock;
    showToast(data.message || 'Increased quantity.');
    } catch (e) {showToast('Error increasing quantity.'); }
}

async function handleMinus() {
    const row = requireSelection(); if (!row) return;
    try {
        const data = await postJSON(row.dataset.endpointMinus);
    row.querySelector('[data-field="qty"]').textContent = data.stock;
    showToast(data.message || 'Reduced quantity.');
    } catch (e) {showToast('Error reducing quantity.'); }
}

async function handleDuplicate() {
    const row = requireSelection(); if (!row) return;
    try {
        const data = await postJSON(row.dataset.endpointDuplicate);
    showToast(data.message || 'Variant duplicated.');

    } catch (e) {showToast('Error duplicating variant.'); }
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

async function handleRemoveDo() {
    if (!removeVariantEndpoint || !selectedRow) return;
    try {
        const data = await postJSON(removeVariantEndpoint);
    selectedRow.remove();
    setSelected(null);
    showToast(data.message || 'Variant removed.');
    } catch (e) {showToast('Error removing variant.'); }
    finally {removeVariantEndpoint = null; }
}

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