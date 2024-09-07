import os, getpass, json, threading

from functions.hash_with_sha256 import sha256
from functions.rsa_management import generate_rsa_keys
from functions.colors import *
from functions.loading_message import display_loading_message
from functions.clear_console import clear_console

def load_users(filename='data/users.json'):
    """
    Load a list of users from a JSON file.

    Args:
        filename (str): The path to the JSON file where user data is stored. Defaults to 'data/users.json'.

    Returns:
        list: A list of user records loaded from the JSON file. Each record is expected to be a dictionary containing user details.

    Notes:
        - If the JSON file does not exist, an empty list is returned.
        - The function handles the FileNotFoundError to ensure that the application can continue to run even if the user file is missing.
    """
    try:
        with open(filename, 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []
    return users

def check_if_user_exists(username,users):
    """
    Check if a user with the given username exists in the list of users.

    Args:
        username (str): The username to check for existence.
        users (list): A list of user records, where each record is a dictionary containing user details.

    Returns:
        bool: True if a user with the given username exists in the list, False otherwise.
    """
    for user in users:
        if user['username'] == username :
            return True
    return False
            


def store_user(username, password, public_key, users, filename='data/users.json'):
    """
    Store a user's username and hashed password in a JSON file.
    
    Args:
        username (str): The user's username.
        password (str): The user's password.
        filename (str): The filename for the JSON file. Defaults to 'users.json'.
    """
    user_data = {
        "username": username,
        "password": password,
        "public_key": public_key
    }

    users.append(user_data)

    with open(filename, 'w') as file:
        json.dump(users, file, indent=4)
        
def username_creation_input(users):
    """
    Prompt the user to enter a username and check if it already exists in the list of users.

    Args:
        users (list): A list of user records, where each record is a dictionary containing user details.

    Returns:
        str: The username entered by the user, if it does not already exist in the list.

    Notes:
        - The function displays a prompt for the user to enter a username.
        - It checks if the entered username already exists in the list of users using `check_if_user_exists`.
        - If the username already exists, it informs the user and recursively prompts for a new username.
        - The process continues until a unique username is provided.
    """
    print(f"{CYAN}╔═══════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║       📝  {GREEN}Enter your username:        {CYAN}║{RESET}")
    print(f"{CYAN}╚═══════════════════════════════════════╝{RESET}")
    username = input("-> ")

    if check_if_user_exists(username, users) == True:
        print("User already exists")
        return username_creation_input(users)

    return username

def password_creation_input():
    """
    Prompt the user to enter and confirm a password.

    Returns:
        str: The password entered by the user, if the confirmation matches the initial entry.

    Notes:
        - The function first prompts the user to enter a password.
        - It then prompts the user to confirm the password by entering it again.
        - If the entered password and the confirmation do not match, the user is informed and asked to try again.
        - This process continues until the password confirmation matches the initial entry.
    """
    print(f"{CYAN}╔═══════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║      🔐  {GREEN}Enter your password:{RESET}         {CYAN}║{RESET}")
    print(f"{CYAN}╚═══════════════════════════════════════╝{RESET}")
    clear_password = getpass.getpass("-> ")

    print(f"{CYAN}╔═══════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║    🔐  {GREEN}Please confirm password:{RESET}       {CYAN}║{RESET}")
    print(f"{CYAN}╚═══════════════════════════════════════╝{RESET}")
    password_confirmation = getpass.getpass("-> ")

    if clear_password != password_confirmation:
        print("Password is not the same, please try again")
        return password_creation_input()
    else:
        return clear_password

def create_user():
    """
    Create a new user by collecting their username and password, generating RSA keys, 
    and storing the user's information.

    Steps:
        1. Clears the console.
        2. Loads the existing users from a JSON file.
        3. Prompts the user to input a username, ensuring it does not already exist.
        4. Prompts the user to create and confirm a password.
        5. Starts a loading animation while generating RSA keys and hashing the password.
        6. Stops the loading animation once the RSA keys are generated and the password is hashed.
        7. Stores the user's information (username, hashed password, and public key) in the JSON file.

    Returns:
        tuple: A tuple containing:
            - bool: True, indicating the user was successfully created.
            - str: The username of the newly created user.
            - str: The plaintext password used for creation (not usually recommended to return).
    """
    clear_console()

    users = load_users()

    username = username_creation_input(users)
    clear_password = password_creation_input()

    loading_done_event = threading.Event()
    loading_thread = display_loading_message(loading_done_event)

    public_key = generate_rsa_keys(seed=username+clear_password,only_public_key=True)
    hash_password = sha256(clear_password)

    loading_done_event.set()
    loading_thread.join()

    clear_console()

    store_user(username, hash_password, public_key, users)

    return True, username, clear_password

def connexion_user():
    """
    Authenticate a user by prompting for their username and password, and checking the credentials against stored data.

    Steps:
        1. Clears the console.
        2. Loads existing users from a JSON file.
        3. Prompts the user to enter their username.
        4. Checks if the entered username exists. If not, informs the user and returns `False`.
        5. If the username exists, repeatedly prompts for the password until the correct one is entered.
        6. Verifies the password by comparing the hashed input with the stored hashed password.
        7. Returns authentication status along with the username and password if successful.

    Returns:
        tuple: A tuple containing:
            - bool: True if the user is successfully authenticated, False otherwise.
            - str or None: The username of the authenticated user or None if authentication fails.
            - str or None: The plaintext password of the user or None if authentication fails.
    """
    clear_console()

    users = load_users()

    print(f"{CYAN}╔═══════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║       📝  {GREEN}Enter your username:        {CYAN}║{RESET}")
    print(f"{CYAN}╚═══════════════════════════════════════╝{RESET}")
    username = input("-> ")

    if check_if_user_exists(username, users) == False:
        print("This username does not exists, please create an account")
        return False, None, None
    else:
        connected = False
        while connected == False:
            print(f"{CYAN}╔═══════════════════════════════════════╗{RESET}")
            print(f"{CYAN}║      🔐  {GREEN}Enter your password:{RESET}         {CYAN}║{RESET}")
            print(f"{CYAN}╚═══════════════════════════════════════╝{RESET}")
            password = getpass.getpass("-> ")
            for user in users:
                if user['username'] == username:
                    if user['password'] == sha256(password):
                        return True, username, password
                    else :
                        print("\nWrong password, please try again")

def verif_password(username, password):
    """
    Verify if the provided password matches the stored password for the given username.

    Args:
        username (str): The username whose password is to be verified.
        password (str): The password to check against the stored password.

    Returns:
        bool: True if the provided password matches the stored password for the username, False otherwise.
    """
    users = load_users()
    for user in users:
        if user['username'] == username:
            if user['password'] == sha256(password):
                return True
            else:
                return False
            
def get_public_key_from_user(user, filename='data/users.json'):
    """
    Retrieve the public key of a specific user from a JSON file.
    
    Args:
        user (str): The username of the user whose public key is to be retrieved.
        filename (str): The path to the JSON file containing user data. Defaults to 'data/users.json'.
    
    Returns:
        list: The public key of the specified user.
        None: If the user is not found.
    """
    try:
        with open(filename, 'r') as file:

            users = json.load(file)
            
            for user_data in users:
                if user_data['username'] == user:
                    return user_data['public_key']
            
            return None
    
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return None
    
    except json.JSONDecodeError:
        print("Error decoding JSON file.")
        return None
    
def get_private_key_from_user(user, password):
    """
    Prompt the user to enter their password and verify it. If the password is correct, generate and return the private key.

    Args:
        user (str): The username for which the private key is to be generated.
        password (str): The password used to verify the user's identity.

    Returns:
        RSAKey: The generated RSA private key if the password is verified successfully.
    """
    verification_password = False

    while verification_password == False:
        password = getpass.getpass("-> ")
        bool_verif_password = verif_password(user,password)
        if bool_verif_password == True:
            verification_password = True
        else:
            print("Password inccorect, please try again...")

    loading_done_event = threading.Event()
    loading_thread = display_loading_message(loading_done_event)

    keys = generate_rsa_keys(key_length=1024, seed=user+password, only_private_key=True)

    loading_done_event.set()
    loading_thread.join()

    return keys


