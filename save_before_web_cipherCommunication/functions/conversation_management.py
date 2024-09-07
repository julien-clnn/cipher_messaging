import json
from functions.user_management import get_public_key_from_user
from functions.rsa_management import cipher_with_rsa
from datetime import datetime

def load_all_conversations(filename='data/conversations.json'):
    """
    Load all conversations from a JSON file.

    Args:
        filename (str): The path to the JSON file where conversations are stored. Defaults to 'data/conversations.json'.

    Returns:
        list: A list of conversations loaded from the JSON file. If the file does not exist, returns an empty list.
    """
    try:
        with open(filename, 'r') as file:
            conversations = json.load(file)
    except FileNotFoundError:
        conversations = []
    return conversations
    
def load_conversations_from_user(user, filename='data/conversations.json'):
    """
    Load and organize conversations for a specific user from a JSON file.

    Args:
        user (str): The username of the user whose conversations are to be loaded.
        filename (str): The path to the JSON file where conversations are stored. Defaults to 'data/conversations.json'.

    Returns:
        dict: A dictionary containing organized conversations for the specified user. The dictionary has two keys:
            - "users_interactions": A list of usernames with whom the user has conversations.
            - "conversations": A list of dictionaries, each representing a conversation with a specific user. Each conversation dictionary contains:
                - "conversation_with": The username of the other participant in the conversation.
                - "messages": A list of messages exchanged with that user.
    """

    conversations = load_all_conversations(filename)
    
    user_conversations = [
        message for message in conversations
        if message['sender'] == user or message['recipient'] == user
    ]

    user_conversations_sorted = {
        "users_interactions" : [],
        "conversations" : []
    }

    for message in user_conversations:

        if message['sender'] != user:
            other_user = message['sender']
        else:
            other_user = message['recipient']

        if other_user != user and other_user not in user_conversations_sorted['users_interactions']:
            conv_data = {
                "conversation_with": other_user,
                "messages" : [message]
            }
            user_conversations_sorted['conversations'].append(conv_data)
            user_conversations_sorted['users_interactions'].append(other_user)
        else:
            for conversation in user_conversations_sorted['conversations']:
                if conversation['conversation_with'] == other_user:
                    conversation['messages'].append(message)
                    break

    return user_conversations_sorted

def store_message(sender, recipient, cipher_message_for_sender, cipher_message_for_recipient, filename='data/conversations.json'):
    """
    Store a message in a JSON file.

    Args:
        sender (str): The username of the sender.
        recipient (str): The username of the recipient.
        content (str): The content of the message.
        filename (str): The path to the JSON file where messages are stored. Defaults to 'data/conversations.json'.

    Returns:
        bool: True if the message is successfully stored, False otherwise.
    """

    new_message = {
        "id": None,
        "sender": sender,
        "recipient": recipient,
        "timestamp": datetime.now().isoformat(),
        "cipher_message_for_sender": cipher_message_for_sender,
        "cipher_message_for_recipient": cipher_message_for_recipient
    }

    conversations = load_all_conversations()

    if conversations != []:
        new_message['id'] = conversations[-1]['id'] + 1
    else:
        new_message['id'] = 1

    conversations.append(new_message)

    try:
        with open(filename, 'w') as file:
            json.dump(conversations, file, indent=4)
        return True
    except IOError:
        print("Failed to write to file.")
        return False

def send_message(user, other_user, message_content):
    """Send a message from user to another user and save it to the JSON file.
    
    Args:
        user (str): The username of the sender.
        other_user (str): The username of the recipient.
        message_content (str): The content of the message.
    """
    sender_public_key = get_public_key_from_user(user)
    recipient_public_key = get_public_key_from_user(other_user)

    cipher_message_for_sender = cipher_with_rsa(message_content,sender_public_key)
    cipher_message_for_recipient = cipher_with_rsa(message_content,recipient_public_key)

    store_message(user,other_user,cipher_message_for_sender,cipher_message_for_recipient)

def load_conversation_between_two_users(user, other_user):
    """
    Load conversations between two specific users from a JSON file.

    Args:
        user (str): The username of the first user.
        other_user (str): The username of the second user.

    Returns:
        list: A list of messages exchanged between the two specified users. Each message is represented as a dictionary.
    """
    
    conversations = load_all_conversations()

    filtered_conversations = [
        conversation for conversation in conversations 
        if (conversation['sender'] == user and conversation['recipient'] == other_user) or 
           (conversation['sender'] == other_user and conversation['recipient'] == user)
    ]
    
    return filtered_conversations




