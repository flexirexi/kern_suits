document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("profile-form");
    const inputs = form.querySelectorAll("input, select, textarea");
    const editButton = document.getElementById("editButton");
    const saveButton = document.getElementById("saveButton");

    // Alle Felder deaktivieren
    inputs.forEach(input => input.disabled = true);

    editButton.addEventListener("click", () => {
        // Alle Felder aktivieren
        inputs.forEach(input => input.disabled = false);

        // Buttons umschalten
        editButton.style.display = "none";
        saveButton.style.display = "inline-block";
    });

    const postal = document.querySelector("#id_postcode");
    const phone = document.querySelector("#id_phone_number");
    console.log("funzt");

    if (postal) {
        postal.addEventListener("input", () => {
            postal.value = postal.value.replace(/\D/g, "").slice(0, 5);
        });
    }

    if (phone) {
        phone.addEventListener("input", () => {
            // erlaubt: + 0-9 space () -
            phone.value = phone.value.replace(/[^0-9+()\-\s]/g, "").slice(0, 20);
        });
    }
});