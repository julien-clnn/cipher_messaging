import os

def clear_console():
    """
    Clear the console depending on the OS used.

    Returns:
        None
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')