(function () {
    const list = document.querySelector(".om-list");
    if (!list) return;

    const bulkEndpoint = list.dataset.endpointBulk;
    const csrfInput = list.querySelector('input[name="csrfmiddlewaretoken"]');
    const csrfToken = csrfInput ? csrfInput.value : "";

    const btnConfirm = document.getElementById("btn-confirm");
    const btnDeny = document.getElementById("btn-deny");
    const btnSent = document.getElementById("btn-sent");
    const btnReturned = document.getElementById("btn-returned");
    const btnLost = document.getElementById("btn-lost");

    const rows = Array.from(document.querySelectorAll(".om-row"));

    function getSelectedRows() {
        return rows.filter(r => r.classList.contains("om-selected"));
    }

    function getStatuses(rowsSel) {
        return rowsSel.map(r => ({
            status: r.dataset.status,
            effective: r.dataset.effectiveStatus,
        }));
    }

    function setButtonState(btn, enabled) {
        if (!btn) return;
        btn.disabled = !enabled;
    }

    function updateButtons() {
        const selected = getSelectedRows();
        const any = selected.length > 0;

        if (!any) {
            setButtonState(btnConfirm, false);
            setButtonState(btnDeny, false);
            setButtonState(btnSent, false);
            setButtonState(btnReturned, false);
            setButtonState(btnLost, false);
            return;
        }

        const st = getStatuses(selected);

        // confirm only if ALL selected are created/denied
        const canConfirm = st.every(x => ["created", "denied"].includes(x.status));
        console.log("Selection Started ----------------------- ");
        console.log("STATUSES", st);
        console.log("canConfirm?", canConfirm);
        setButtonState(btnConfirm, canConfirm);

        // deny only if NONE are sent/delivered (package already on the way)
        const canDeny = st.every(x => !["sent", "delivered"].includes(x.effective));
        setButtonState(btnDeny, canDeny);

        // sent only if ALL are confirmed
        const canSent = st.every(x => x.status === "confirmed");
        setButtonState(btnSent, canSent);

        // returned always allowed (info flag only) -> implementing the feature is more effort than benefit
        // pure information is
        setButtonState(btnReturned, true);

        // mark lost only if ALL are sent/delivered 
        const canLost = st.every(x => ["sent", "delivered"].includes(x.effective));
        setButtonState(btnLost, canLost);
    }

    function toggleRow(row) {
        row.classList.toggle("om-selected");
        updateButtons();
    }

    // Click on row selects but clicking the expand button should NOT select
    rows.forEach(row => {
        row.addEventListener("click", (e) => {
            const isToggle = e.target.closest(".om-toggle");
            if (isToggle) return;
            toggleRow(row);
        });

        row.addEventListener("keydown", (e) => {
            if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                toggleRow(row);
            }
        });
    });

    async function postBulkAction(action) {
        const selected = getSelectedRows();
        if (selected.length === 0) return;

        const ids = selected.map(r => r.dataset.orderId);

        const form = new FormData();
        form.append("action", action);
        ids.forEach(id => form.append("order_ids[]", id));
        if (csrfToken) form.append("csrfmiddlewaretoken", csrfToken);

        const res = await fetch(bulkEndpoint, {
            method: "POST",
            body: form,
            headers: { "X-Requested-With": "XMLHttpRequest" },
        });

        const data = await res.json();
        if (!res.ok || !data.ok) {
            alert(data.error || "Action failed.");
            return;
        }

        // Simple refresh -> easiest 
        window.location.reload();
    }

    btnConfirm?.addEventListener("click", () => postBulkAction("confirm"));
    btnDeny?.addEventListener("click", () => postBulkAction("deny"));
    btnSent?.addEventListener("click", () => postBulkAction("sent"));
    btnReturned?.addEventListener("click", () => postBulkAction("returned"));
    btnLost?.addEventListener("click", () => {
        const ok = confirm("Mark selected order(s) as LOST? This should be used only when shipment is confirmed missing.");
        if (ok) postBulkAction("mark_lost");
    });

    updateButtons();
})();
