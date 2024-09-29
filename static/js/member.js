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

    const dateInput = document.getElementById("date").value;
    const fromTimeInput = document.getElementById("from_time").value;
    const endTimeInput = document.getElementById("end_time").value;
    const venueName = document.getElementById("venue_name").value;
    const venueLink = document.getElementById("link").value;

    // Regular expression to validate date format (YYYY-MM-DD)
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
    if (!dateRegex.test(dateInput)) {
        alert("Invalid date format. Please enter the date in YYYY-MM-DD format.");
        return;
    }

    // Regular expression to validate time format (HH:MM in 24-hour format)
    const timeRegex = /^([01]\d|2[0-3]):([0-5]\d)$/;
    if (!timeRegex.test(fromTimeInput) || !timeRegex.test(endTimeInput)) {
        alert("Invalid time format. Please enter time in HH:MM 24-hour format.");
        return;
    }

    const currentDateTime = new Date();
    const selectedDate = new Date(dateInput + "T00:00:00"); // Date object based on selected date

    // Adjust for IST (+5:30 hours)
    const offsetInMinutes = currentDateTime.getTimezoneOffset() + 330; // 330 minutes for IST
    const adjustedCurrentDate = new Date(currentDateTime.getTime() + offsetInMinutes * 60 * 1000);

    const currentDateString = adjustedCurrentDate.toISOString().split('T')[0]; // Get the adjusted date

    // Check if booking is in the past date
    if (selectedDate < new Date(adjustedCurrentDate.toDateString())) {
        alert("You cannot book a venue in the past.");
        return;
    }

    // Parse from_time and end_time with the actual selected date
    const fromTime = new Date(`${dateInput}T${fromTimeInput}:00`);
    const endTime = new Date(`${dateInput}T${endTimeInput}:00`);

    // If booking is for today, check if from_time is in the past
    if (selectedDate.toDateString() === adjustedCurrentDate.toDateString() && fromTime <= adjustedCurrentDate) {
        alert("You cannot book a venue in the past time.");
        return;
    }

    // Ensure end time is after the start time
    if (fromTime >= endTime) {
        alert("End time must be later than the start time.");
        return;
    }

    // All validations passed, proceed with the fetch request
    fetch('/book_venue', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            date: dateInput,
            from_time: fromTimeInput,
            end_time: endTimeInput,
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