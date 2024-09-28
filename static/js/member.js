document.addEventListener('DOMContentLoaded', () => {
    VANTA.FOG({
        el: "#vanta-bg", // The background element
        highlightColor: 0xffc300, // Yellow highlight
        midtoneColor: 0xff1f00, // Red midtone
        lowlightColor: 0x2d00ff, // Blue lowlight
        baseColor: 0xffebeb, // Light pink base
        blurFactor: 0.6, // Set blur factor
        zoom: 1.0, // Default zoom level
        speed: 1.0, // Default speed
        mouseControls: true,
        touchControls: true,
        gyroControls: false,
        minHeight: 200.00,
        minWidth: 200.00
    });
});

document.getElementById("venueForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent form submission until validation is complete

    const currentDateTime = new Date();
    const selectedDate = new Date(document.getElementById("date").value);
    const fromTime = document.getElementById("from_time").value;
    const endTime = document.getElementById("end_time").value;
    const venueName = document.getElementById("venue_name").value;
    const venueLink = document.getElementById("link").value;

    // Prevent booking in the past
    if (selectedDate < currentDateTime) {
        alert("You cannot book a venue in the past.");
        return;
    }

    // Ensure end time is after the start time
    if (fromTime >= endTime) {
        alert("End time must be later than the start time.");
        return;
    }

    // Make a fetch request to the server for validation
    fetch('/book_venue', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            date: document.getElementById("date").value,
            from_time: fromTime,
            end_time: endTime,
            venue_name: venueName,
            link: venueLink
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'error') {
            // Show an alert if there's an error
            alert(data.message);
        } else {
            // Redirect to the main page after successful booking
            window.location.href = "/mainMember";
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while booking the venue.');
    });
});
