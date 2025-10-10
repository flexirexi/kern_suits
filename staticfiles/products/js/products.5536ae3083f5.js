document.addEventListener("DOMContentLoaded", () => {
    const filterForm = document.getElementById('filterForm');
    const filterElements = filterForm.querySelectorAll('input, select');

    if(filterForm) {
        filterElements.forEach(el => {
            el.addEventListener('change', () => {
                filterForm.submit();
            });
        });
    } else {
        console.warn("No filter form found");
    }

});