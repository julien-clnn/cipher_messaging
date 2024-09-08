import os

from functions.user_management import create_user, connexion_user, load_users, get_private_key_from_user
from functions.conversation_management import load_conversations_from_user, send_message, load_conversation_between_two_users
from functions.rsa_management import decipher_with_rsa
from functions.colors import *
from functions.clear_console import clear_console

def display_connexion_menu_in_console():
    """
    Display the connection menu in the console for user login or account creation.

    This function displays a menu with options to create a new user or sign in. It uses colored text to enhance the visual appeal.
    After displaying the menu, it waits for the user's choice and processes the input to either create a new user, sign in, or redisplay the menu in case of invalid input.

    Returns:
        None
    """

    clear_console()

    print(f"{GREEN}****************************************{RESET}")
    print(f"{GREEN}*      {CYAN}Welcome to Ciphered Messaging   {GREEN}*{RESET}")
    print(f"{GREEN}****************************************{RESET}")
    print(f"{PURPLE}╔═══════════════════════════════════════╗{RESET}")
    print(f"{PURPLE}║                 {YELLOW}Menu{PURPLE}                  ║{RESET}")
    print(f"{PURPLE}╠═══════════════════════════════════════╣{RESET}")
    print(f"{PURPLE}║   {CYAN}1. Create user{PURPLE}                      ║{RESET}")
    print(f"{PURPLE}║   {CYAN}2. Sign in{PURPLE}                          ║{RESET}")
    print(f"{PURPLE}╚═══════════════════════════════════════╝{RESET}")
    print()
    choice = input(f"{YELLOW}Enter the desired option : \n{RESET}-> ")

    if choice == "1" :
        connexion, user, password = create_user()
        if connexion == True:
            display_message_menu_in_console(user, password)
        else:
            display_connexion_menu_in_console()
    
    elif choice == "2" :
        connexion, user, password = connexion_user()
        if connexion == True:
            display_message_menu_in_console(user, password)
        else:
            display_connexion_menu_in_console()

    else:
        display_connexion_menu_in_console()

def display_message_menu_in_console(user, password):
    """
    Display the message menu in the console after a successful connection.

    Args:
        user (str): The username of the connected user.
        password (str): The password of the connected user. (Note: Not used in the function directly, but may be required for future functionality.)

    This function displays a menu with options for the connected user to either view their conversations or exit. It uses colored text for better visual appeal. Based on the user's choice, it either displays the user's conversations or returns to the connection menu.

    Returns:
        None
    """
    clear_console()

    print(f"{GREEN}╔═══════════════════════════════════════╗{RESET}")
    print(f"{GREEN}║       ✅ {CYAN}Successfully connected!      {GREEN}║{RESET}")
    print(f"{GREEN}╚═══════════════════════════════════════╝{RESET}\n")

    print(f"{PURPLE}What do you want to do ?{RESET}")
    print(f"{PURPLE}╔═══════════════════════════════════════╗{RESET}")
    print(f"{PURPLE}║     {CYAN}1. {YELLOW}See my conversations           {PURPLE}║{RESET}")
    print(f"{PURPLE}║     {CYAN}2. {YELLOW}Exit                           {PURPLE}║{RESET}")
    print(f"{PURPLE}╚═══════════════════════════════════════╝{RESET}\n")
    choice = input("-> ")

    if choice == "1":
        display_user_conversations(user, password)
    elif choice == "2":
        display_connexion_menu_in_console()
    else:
        display_message_menu_in_console(user, password)

def display_user_specific_conversation(user, other_user, conversation, password):
    """
    Display a specific conversation between the user and another user, and handle message interactions.

    Args:
        user (str): The username of the connected user.
        other_user (str): The username of the other participant in the conversation.
        conversation (list): A list of messages exchanged between the user and the other user. Each message is a dictionary with details.
        password (str): The password of the connected user, used to retrieve the user's private key.

    This function displays a formatted conversation between the connected user and another specified user. It includes a prompt for the user to enter their password to confirm access and displays each message with its timestamp and sender. After displaying the conversation, it offers options to send a new message or go back to the conversation list.

    Returns:
        None
    """
    rectangle_width = 45 
    border_char = '═'
    padding = 0  

    text_width = rectangle_width - 2 
    text_with_padding = text_width - 2 * padding 

    padded_name = f" Conversation with {user}".center(text_with_padding)

    border_line = f"╔{border_char * (rectangle_width - 2)}╗"
    content_line = f"║{CYAN}{border_char * padding}{padded_name}{border_char * padding}{GREEN}║"
    bottom_line = f"╚{border_char * (rectangle_width - 2)}╝"

    print(f"{GREEN}{border_line}{RESET}")
    print(f"{GREEN}{content_line}{RESET}")
    print(f"{GREEN}{bottom_line}{RESET}")
    print()
    print(f"{GREEN}╔═══════════════════════════════════════════╗{RESET}")
    print(f"{GREEN}║ {YELLOW}Please enter your password to confirm :{RESET}   {GREEN}║{RESET}")
    print(f"{GREEN}╚═══════════════════════════════════════════╝{RESET}\n")
    
    user_private_key = get_private_key_from_user(user, password)

    print(f"{GREEN}╔═══════════════════════════════════════════╗{RESET}")
    print(f"{GREEN}║ {CYAN}Conversation with {other_user}{RESET}                     {GREEN}║{RESET}")
    print(f"{GREEN}╚═══════════════════════════════════════════╝{RESET}\n")

    for message in conversation:
        sender = message['sender']
        timestamp = message['timestamp']
        if sender == user :
            content = decipher_with_rsa(encrypted_message=message['cipher_message_for_sender'], private_key=user_private_key)
        else:
            content = decipher_with_rsa(encrypted_message=message['cipher_message_for_recipient'], private_key=user_private_key)
        
        print(f"{YELLOW}[{timestamp}] {CYAN}{sender}:{RESET} {content}")

    print()
    print(f"{PURPLE}╔═══════════════════════════════════════════╗{RESET}")
    print(f"{PURPLE}║   {CYAN}1. {YELLOW}Send a message                       {PURPLE}║{RESET}")
    print(f"{PURPLE}║   {CYAN}2. {YELLOW}Go back                              {PURPLE}║{RESET}")
    print(f"{PURPLE}╚═══════════════════════════════════════════╝{RESET}")
    print()
    choice = input("-> ")

    if choice == "1":
        display_message_writing(user=user, other_user=other_user, conversation=conversation, password=password)
    elif choice == "2":
        display_user_conversations(user, password)
    else:
        display_user_specific_conversation(user, other_user, conversation, password)

def display_user_conversations(user, password):
    """
    Display a menu of conversations for the connected user and handle user interactions.

    Args:
        user (str): The username of the connected user.
        password (str): The password of the connected user, used to retrieve the user's private key.

    This function displays a list of conversations for the connected user, including an option to create a new conversation, open an existing conversation, or go back to the previous menu. It uses colored text for better visual appeal. The user is prompted to select an option, and the corresponding action is performed based on the choice.

    Returns:
        None
    """
    clear_console()

    i = 1
    conversations = load_conversations_from_user(user)

    print(f"{GREEN}╔═══════════════════════════════════════╗{RESET}")
    print(f"{GREEN}║ {CYAN}Your conversations{RESET}                    {GREEN}║{RESET}")
    print(f"{GREEN}╚═══════════════════════════════════════╝{RESET}")
    print(f"{GREEN}   {CYAN}{i}. {YELLOW}Create a conversation with another user{GREEN}  {RESET}")

    for other_user in conversations['users_interactions']:
        i += 1
        print(f"{GREEN}   {CYAN}{i}. {YELLOW}Open conversation with {other_user}")
    print(f"{GREEN}   {CYAN}{i+1}. {YELLOW}Go back{RESET}")
    
    try:
        choice = int(input("\n-> "))
    except ValueError:
        display_user_conversations(user=user,password=password)

    clear_console()

    if choice == 1:
        display_message_writing(user=user, password=password, conversation=conversations)
    elif choice == i+1:
        display_message_menu_in_console(user, password)
    elif 1 < choice <= i:
        other_user = conversations['users_interactions'][choice-2]
        conversation = load_conversation_between_two_users(user=user, other_user=other_user)
        display_user_specific_conversation(user=user, other_user=other_user, conversation=conversation, password=password)
    else : 
        display_user_conversations(user)

def display_message_writing(user, conversation, password, other_user=None,):
    """
    Display a prompt to either create a conversation with another user or send a message in an existing conversation.

    Args:
        user (str): The username of the connected user.
        conversation (list): The list of messages in the current conversation.
        password (str): The password of the connected user, used to retrieve the user's private key.
        other_user (str, optional): The username of the recipient for the message. If None, allows the user to select a recipient from available users.

    This function allows the connected user to either select an existing user to start a new conversation or send a message to an existing conversation. If no recipient is specified (`other_user` is `None`), the function displays a list of available users to choose from. Once a recipient is selected or specified, the function prompts the user to enter a message and sends it.

    Returns:
        None
    """
    if other_user is None:
        users = load_users()
        available_users = [u['username'] for u in users if u['username'] != user]
        if not available_users:
            print("No other users available for creating a conversation.")
            display_user_specific_conversation(user, None, conversation, password)
            return
        
        print(f"{GREEN}╔═══════════════════════════════════════╗{RESET}")
        print(f"{GREEN}║     {CYAN}Users available{RESET}                   {GREEN}║{RESET}")
        print(f"{GREEN}╚═══════════════════════════════════════╝{RESET}\n")
        for i, username in enumerate(available_users, start=1):
            print(f"    {CYAN}{i}. {YELLOW}{username}{RESET}")

        user_found = False
        while not user_found:
            try:
                user_choice = int(input(f"\n{YELLOW}Enter the number of the user you want to message : {RESET}\n-> "))
                if 1 <= user_choice <= len(available_users):
                    other_user = available_users[user_choice - 1]
                    user_found = True
                else:
                    print(f"{CYAN}Invalid choice. Please select a valid number.{RESET}")
            except ValueError:
                print(f"{CYAN}Invalid input. Please enter a number.{CYAN}")

    message = input(f"\n{YELLOW}What is the message that you want to send to {CYAN}{other_user}{YELLOW} ? {RESET}\n-> ")
      
    send_message(user, other_user, message)
    clear_console()
    print(f"✅ {GREEN}Message has been sent")
    conversation = load_conversation_between_two_users(user=user, other_user=other_user)
    display_user_specific_conversation(user=user, other_user=other_user, conversation=conversation, password=password)

    
    