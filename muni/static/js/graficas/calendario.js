document.addEventListener("DOMContentLoaded", function () {
    var currentDate = new Date(); // Obtiene la fecha actual
    var defaultDate = currentDate.toISOString().slice(0, 10); // Formatea la fecha actual en formato "YYYY-MM-DD"
    var config = {
        inline: true,
        prevArrow: "<span title=\"Previous month\">&laquo;</span>",
        nextArrow: "<span title=\"Next month\">&raquo;</span>",
        defaultDate: defaultDate,
        onChange: function(selectedDates, dateStr, instance) {
            // Your logic to handle date change
            // For example, add CSS class to highlight weekends
            var calendar = instance.calendarContainer;
            selectedDates.forEach(function(date) {
                if (date.getDay() === 0 || date.getDay() === 6) {
                    calendar.querySelector('.flatpickr-day:not(.prevMonthDay):not(.nextMonthDay)[aria-label="' + date.toDateString() + '"]').classList.add('weekend');
                }
            });
        }
    };
    document.getElementById("datetimepicker-dashboard").flatpickr(config);

    // Pinta el día actual al cargar la página
    var calendar = document.querySelector(".flatpickr-calendar");
    calendar.querySelector('.flatpickr-day.today').classList.add('current-day');
});
