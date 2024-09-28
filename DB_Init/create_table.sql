-- Contains details about the club heads
CREATE TABLE club_head_details (
    head_id INT PRIMARY KEY,
    club_head VARCHAR(100) NOT NULL,
    phone_number VARCHAR(10) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    CONSTRAINT check_phone_number CHECK (phone_number REGEXP '^[0-9]{10}$')
);

-- Contains the list of clubs from the website (https://su.psgtech.ac.in/clubs.php)
CREATE TABLE club_list (
    club_id INT PRIMARY KEY,
    club_name VARCHAR(100) NOT NULL
);

-- Contains the list of venues
CREATE TABLE venue_list (
    venue_id INT PRIMARY KEY,
    venue_name VARCHAR(100)
);

-- Connects clubs to their heads
CREATE TABLE club_head (
    club_id INT,
    head_id INT,
    PRIMARY KEY (club_id, head_id),
    FOREIGN KEY (club_id) REFERENCES club_list(club_id),
    FOREIGN KEY (head_id) REFERENCES club_head_details(head_id)
);

-- Stores the booking details for venue
CREATE TABLE booked_venue (
    venue_id INT NOT NULL,
    club_id INT NOT NULL,
    date DATE NOT NULL,
    from_time TIME NOT NULL,
    end_time TIME NOT NULL,
    venue_link TEXT NOT NULL,
    FOREIGN KEY (venue_id) REFERENCES venue_list(venue_id),
    FOREIGN KEY (club_id) REFERENCES club_list(club_id)
);