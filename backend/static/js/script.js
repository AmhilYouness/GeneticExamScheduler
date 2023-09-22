document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: '/get_calendar_data',
        eventClick: function(info) {
            var event = info.event;
            var popupContent = `
                <p><strong>Room Name:</strong> ${event.title}</p>
                <p><strong>Morning Investigator:</strong> ${event.extendedProps.invig_morning}</p>
                <p><strong>Noon Investigator:</strong> ${event.extendedProps.invig_noon}</p>
            `;

            // Create the modal
            var modal = document.createElement('div');
            modal.className = 'modal';
            modal.innerHTML = `
                <div class="modal-content">
                    <span class="close" onclick="closeModal()">&times;</span>
                    <h2>Event Details</h2>
                    ${popupContent}
                </div>
            `;
            document.body.appendChild(modal);

            // Display the modal
            modal.style.display = 'block';
        }
    });
    calendar.render();
});

function closeModal() {
    var modal = document.querySelector('.modal');
    if (modal) {
      modal.parentNode.removeChild(modal); 
    }
}