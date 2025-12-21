document.addEventListener("DOMContentLoaded", function () {
    const datePicker = document.getElementById("datePicker");
    const timeSelect = document.getElementById("timeSelect");
    const hiddenInput = document.getElementById("startDatetimeInput");
    const meta = document.getElementById("editApptMeta");
    
    const currentDate = meta?.dataset.currentDate || "";
    const currentHour = Number(meta?.dataset.currentHour || "");
    
    const bookedSlotsEl = document.getElementById("booked-slots");
    const bookedSlots = bookedSlotsEl
        ? JSON.parse(bookedSlotsEl.textContent || "{}") || {}
        : {};

    const openingHours = {
        monday: [10, 21],
        tuesday: [10, 21],
        wednesday: [10, 21],
        thursday: [10, 21],
        friday: [10, 21],
        saturday: [9, 20],
        sunday: [9, 20],
    };

    function getWeekdayName(dateString) {
        const d = new Date(dateString);
        return d.toLocaleDateString("en-US", { weekday: "long" }).toLowerCase();
    }

    function populateTimeSlots(dateString, preferredHour = null) {
        if (!dateString) return;

        const weekday = getWeekdayName(dateString);
        const hours = openingHours[weekday];
        if (!hours) return;

        const [startHour, endHour] = hours;

        const bookedHours = (bookedSlots[dateString] || []).map(Number);

        timeSelect.innerHTML = '<option value="">Please choose a time slot</option>';

        for (let h = startHour; h < endHour; h++) {
            if (bookedHours.includes(h)) continue; // skip booked hour

            const option = document.createElement("option");
            option.value = String(h);
            option.textContent = String(h).padStart(2, "0") + ":00";
            timeSelect.appendChild(option);
        }

        timeSelect.disabled = false;

        // Select default hour if available
        if (preferredHour !== null) {
            const match = [...timeSelect.options].find(
                (opt) => Number(opt.value) === Number(preferredHour)
            );
            if (match) timeSelect.value = String(preferredHour);
        }
    }

    function syncHiddenInput() {
        const selectedDate = datePicker.value;
        const selectedHour = timeSelect.value;
        if (selectedDate && selectedHour) {
            hiddenInput.value =
                selectedDate + "T" + selectedHour.padStart(2, "0") + ":00";
        } else {
            hiddenInput.value = "";
        }
    }

    // Init with current appointment date/time
    if (currentDate) {
        datePicker.value = currentDate;
        populateTimeSlots(currentDate, currentHour);
        syncHiddenInput(); // keeps current slot even if user only edits comment
    }

    datePicker.addEventListener("change", function () {
        populateTimeSlots(datePicker.value, null);
        hiddenInput.value = "";
    });

    timeSelect.addEventListener("change", function () {
        syncHiddenInput();
    });
});
