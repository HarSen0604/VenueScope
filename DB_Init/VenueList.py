def generate_venue_insert_query(venues):
    """
    Generate an SQL INSERT query for inserting venue names into a table.

    Args:
        venues (list): List of venue names to be inserted.

    Returns:
        str: The complete SQL INSERT query.
    """
    query = 'INSERT INTO venue_list (venue_id, venue_name) VALUES\n'
    values = [f"({i}, '{venue}')" for i, venue in enumerate(venues, start=1)]
    query += ',\n'.join(values) + ';'
    return query

venues = [
    "D - Block Ground Floor",
    "D - Block 1st Floor",
    "F - Block 1st Floor",
    "F - Block 2nd Floor",
    "G - 301",
    "G - 302",
    "G - 303",
    "G - 304",
    "G - 305",
    "J - 410",
    "J - 411",
    "J - 412",
    "J - 413"
]

file_name = "insert_venue_list.sql"
query = generate_venue_insert_query(venues)

with open(file_name, "w") as file:
    file.write(query + '\n')

print(f"SQL script has been created and saved as '{file_name}'.")