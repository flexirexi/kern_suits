document.addEventListener('DOMContentLoaded', function () {
    const datePicker = document.getElementById('datePicker');
    const timeSelect = document.getElementById('timeSelect');
    const hiddenInput = document.getElementById('startDatetimeInput');

    const bookedSlots = JSON.parse(
        document.getElementById('booked-slots').textContent
    );

    const openingHours = {
        monday: [10, 21],
        tuesday: [10, 21],
        wednesday: [10, 21],
        thursday: [10, 21],
        friday: [10, 21],
        saturday: [9, 20],
        sunday: [9, 20]
    };

    function getWeekdayName(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { weekday: 'long' }).toLowerCase();
    }

    function populateTimeSlots(dateString) {

        if (!dateString) return;

        const weekday = getWeekdayName(dateString);
        const hours = openingHours[weekday];
        if (!hours) return;

        const [startHour, endHour] = hours;

        // Alle gebuchten Stunden an dem Tag
        const bookedHours = bookedSlots[dateString] || [];

        timeSelect.innerHTML = '<option value="">Bitte Uhrzeit wählen</option>';

        for (let h = startHour; h < endHour; h++) {
            if (bookedHours.includes(h)) continue; // skippe gebuchte Stunde

            const hourString = String(h).padStart(2, '0') + ":00";
            const option = document.createElement('option');
            option.value = h;
            option.textContent = hourString;
            timeSelect.appendChild(option);
        }

        timeSelect.disabled = false;
    }

    datePicker.addEventListener('change', function () {
        const selectedDate = datePicker.value;
        populateTimeSlots(selectedDate);
        hiddenInput.value = '';
    });

    timeSelect.addEventListener('change', function () {
        const selectedDate = datePicker.value;
        const selectedHour = timeSelect.value;
        if (selectedDate && selectedHour) {
            const datetimeString = selectedDate + 'T' + selectedHour.padStart(2, '0') + ':00';
            hiddenInput.value = datetimeString;
            console.log("CALCULATED DATE: " + datetimeString + "-------------------->");
        }
    });
});