# List of club names
club_names = [
    'AeroModeling Club',
    'Animal Welfare Club',
    'Anti Drug Club',
    'Artificial Intelligence & Robotics',
    'Association of Serious Quizzers',
    'Astronomy Club',
    'Book Readers Club',
    'CAP Nature Club',
    'Cyber Security Club',
    'Dramatix Club',
    'English Literary Society',
    'Entrepreneurs Club',
    'Fine Arts Club',
    'Finverse Club',
    'Global Leaders Forum',
    'Higher Education Forum',
    'Industry Interaction Forum',
    'Martial Arts Club',
    'PSG Tech Chronicle Club',
    'Paathshala Club',
    'Radio Hub',
    'Rotaract Club',
    'SPIC-MACAY Heritage Club',
    'Student Research Council',
    'Tech Music',
    'Women Development Cell',
    'Youth Outreach Club',
    'Youth Red Cross Society',
    'Yuva Tourism Club'
]

def generate_insert_query(club_names):
    """
    Generate an SQL INSERT query for inserting club names into a club_list table.

    Args:
        club_names (list): List of club names to be inserted.

    Returns:
        str: The complete SQL INSERT query.
    """
    query = 'INSERT INTO club_list (club_id, club_name) VALUES\n'
    values = [f"({i}, '{club}')" for i, club in enumerate(club_names, start=1)]
    query += ',\n'.join(values) + ';'
    return query

file_name = 'insert_club_list.sql'
query = generate_insert_query(club_names)

with open(file_name, 'w') as file:
    file.write(query + '\n')

print(f"SQL script has been created and saved as '{file_name}'.")
