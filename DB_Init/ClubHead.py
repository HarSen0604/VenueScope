import random

numClubs = 29
numHeads = 29

headIds = list(range(1, numHeads + 1))

def generateClubHeadAssociations(numClubs, headIds):
    """
    Generate random associations between clubs and club heads.

    Args:
        num_clubs (int): The number of clubs.
        head_ids (list): List of head IDs.

    Returns:
        list: A list of tuples where each tuple contains a club ID and a head ID.
    """
    random.shuffle(headIds)
    associations = []
    for club_id in range(1, numClubs + 1):
        head_id = headIds[club_id - 1]
        associations.append((club_id, head_id))
    return associations

associations = generateClubHeadAssociations(numClubs, headIds)

query = "INSERT INTO club_head (club_id, head_id) VALUES\n"
values = [f"({club_id}, {head_id})" for club_id, head_id in associations]
query += ',\n'.join(values) + ';'

with open('insert_club_head.sql', 'w') as file:
    file.write(query)

print("SQL query for club-head associations has been written to 'insert_club_head.sql'")
