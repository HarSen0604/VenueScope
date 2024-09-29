#!/bin/bash

DATABASE_NAME="VenueScope"

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    echo "MySQL is not installed. Please install MySQL to proceed."
    exit 1
fi

# Execute Python files
/usr/local/bin/python3 ClubList.py
/usr/local/bin/python3 ClubHeadDetails.py
/usr/local/bin/python3 ClubHead.py
/usr/local/bin/python3 VenueList.py

# Run SQL files in the correct order
mysql -u root -p <<EOF
CREATE DATABASE IF NOT EXISTS $DATABASE_NAME;
USE $DATABASE_NAME;

-- Run the table creation and initial data insertion
SOURCE create_table.sql;
SOURCE insert_club_head_details.sql;
SOURCE insert_club_list.sql;
SOURCE insert_venue_list.sql;
SOURCE insert_club_head.sql;
EOF

# Remove the .sql files created
rm -f insert_club_list.sql
rm -f insert_club_head_details.sql
rm -f insert_club_head.sql
rm -f insert_venue_list.sql

echo "Database setup and data insertion completed successfully."