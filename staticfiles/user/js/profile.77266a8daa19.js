document.addEventListener("DOMContentLoaded", function() {

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
});