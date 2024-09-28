import bcrypt

def generate_phone_number():
    """
    Generate a random phone number.

    Returns:
        str: A phone number in string format.
    """
    return '9876543210'

def encrypt_password(password):
    """
    Encrypt a password using bcrypt.

    Args:
        password (str): The plain text password to be encrypted.

    Returns:
        str: The encrypted password.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

club_heads = [
    "John Doe", "Jane Smith", "Sam Johnson", "Emily Davis", "Chris Brown", "Anna Lee", 
    "Michael White", "Emma Wilson", "David Harris", "Sophia Thompson", "James Martin", 
    "Olivia Taylor", "Benjamin Walker", "Ava Scott", "Liam Adams", "Isabella Nelson", 
    "Noah Young", "Mia Allen", "Lucas Hall", "Charlotte King", "Mason Wright", 
    "Amelia Moore", "Ethan Green", "Harper Lewis", "Alexander Clark", "Abigail Turner", 
    "Elijah Baker", "Evelyn Phillips", "Logan Mitchell"
]

password = "PSG_Tech@123"

try:
    encrypted_password = encrypt_password(password)
except ValueError as e:
    print(e)
    encrypted_password = None

if encrypted_password:
    query = "INSERT INTO club_head_details (head_id, club_head, phone_number, password, email) VALUES\n"

    values = [
        f"({idx}, '{head}', '{generate_phone_number()}', '{encrypted_password}', '{head.replace(' ', '_')}@random.com')"
        for idx, head in enumerate(club_heads, start=1)
    ]

    query += ',\n'.join(values) + ';'

    with open('insert_club_head_details.sql', 'w') as file:
        file.write(query)

    print("SQL query has been written to 'insert_club_head_details.sql'")
