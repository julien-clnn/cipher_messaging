import random

from functions.generate_prime_number import generatePrimeNumber, pgcd, modularInverse

def generate_rsa_keys(key_length=1024, seed=None, only_public_key=False, only_private_key=False):
    """
    Asymetric Cryptography, generate a pair of keys (one public and private key for users)
    
    Args:
        key_length (int): length of the keys
    Returns:
        str: giving the 2 keys (public key and private key)
    """

    # Generation of 2 prime numbers with 2 different seeds
    if seed is not None:
        random.seed(seed)

    seed_p = seed
    seed_q = seed + "1" if seed is not None else None

    p = generatePrimeNumber(key_length, seed=seed_p)
    q = generatePrimeNumber(key_length, seed=seed_q)

    # Define the module (n), and phi (Euler indicator function)
    n = p * q
    phi = (p - 1) * (q - 1)

    # Taking a public exponent (e must be prime with phi)
    # We are doing this until we find a good random value
    e = random.randrange(2, phi)
    while pgcd(e, phi) != 1:
        e = random.randrange(2, phi)

    # Processing a private exponent
    d = modularInverse(e, phi)

    # Creating the two keys
    public_key = (e, n)
    private_key = (d, n)

    # Returning the keys
    if only_public_key:
        return public_key
    elif only_private_key:
        return private_key
    else:
        return public_key, private_key
    
def cipher_with_rsa(message, public_key):
    """
    Encrypt a message using RSA encryption with a public key.
    
    Args:
        message (str): The message to encrypt.
        public_key (tuple): The RSA public key (e, n).
    
    Returns:
        list: The encrypted message as a list of integers.
    """
    e, n = public_key
    # Convert the message to a list of characters and encrypt each character
    encrypted_message = [pow(ord(char), e, n) for char in message]
    return encrypted_message

def decipher_with_rsa(encrypted_message, private_key):
    """
    Decrypt a message using RSA encryption with a private key.
    
    Args:
        encrypted_message (list): The encrypted message as a list of integers.
        private_key (tuple): The RSA private key (d, n).
    
    Returns:
        str: The decrypted message.
    """
    d, n = private_key
    # Decrypt each character and convert back to string
    decrypted_message = ''.join(chr(pow(char, d, n)) for char in encrypted_message)
    return decrypted_message