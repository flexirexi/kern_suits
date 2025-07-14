document.addEventListener("DOMContentLoaded", () => {
    const filterForm = document.getElementById("filterForm");
    const filterElements = filterForm.querySelectorAll('input, select');

    filterElements.forEach(el => {
        el.addEventListener('change', () => {
            alert("funzt");
            filterForm.submit();
        });
    });

});