H = [
    0x6a09e667,
    0xbb67ae85,
    0x3c6ef372,
    0xa54ff53a,
    0x510e527f,
    0x9b05688c,
    0x1f83d9ab,
    0x5be0cd19
]

K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

def xorSha256(block1, block2):
    """
    Xor operation on two inputs from the same type. This function is used for SHA256 function

    Args:
        block1 (): object1
        block2 (): object2
    Returns:
        : give the xor of 2 objects from the same type
    """
    if type(block1) is int:
        return block1 ^ block2
    elif type(block1) is list:
        return [xorSha256(b1, b2) for b1, b2 in zip(block1, block2)]
    
def rotateLeft(block, shift):
    """
    Rotate left an input as the operation '<<<'

    Args:
        block (list): a binary list
        shift (int): an integer to give the number of rotates need to be done
    Returns:
        list: this returns back the list modfied according to the rotate given

    EXAMPLE: rotateLeft([1, 1, 1, 1, 0, 0, 0, 1], 2)
             -> [0, 1, 1, 1, 1, 1, 0, 0]
    """
    i = shift % 32
    return block[-i:] + block[:-i]

def rotateRight(block, shift):
    """
    Rotate right an input as the operation '>>>'

    Args:
        block (list): a binary list
        shift (int): an integer to give the number of rotates need to be done
    Returns:
        list: this returns back the list modfied according to the rotate given (cf rotateRight())
    """
    return rotateLeft(block, -shift)

def sha256(message):
    """
    Compute the SHA-256 hash of the given message.

    Args:
        message (str): The input message to be hashed.

    Returns:
        str: The SHA-256 hash of the input message as a hexadecimal string.
    """
    global H
    
    h0, h1, h2, h3, h4, h5, h6, h7 = H.copy()

    message = message.encode()

    message += b'\x80'
    while len(message) % 64 != 56:
        message += b'\x00'

    message_length_bits = 8 * (len(message) - 1)
    message += bytes([(message_length_bits >> (56 - i * 8)) & 0xFF for i in range(8)])

    for i in range(0, len(message), 64):
        block = message[i:i+64]
        w = [int.from_bytes(block[j:j+4], 'big') for j in range(0, 64, 4)]

        for j in range(16, 64):
            s0 = xorSha256(rotateRight([w[j-15]], 7), xorSha256(rotateRight([w[j-15]], 18), rotateRight([w[j-15]], 3)))
            s1 = xorSha256(rotateRight([w[j-2]], 17), xorSha256(rotateRight([w[j-2]], 19), rotateRight([w[j-2]], 10)))
            w.append((w[j-16] + s0[0] + w[j-7] + s1[0]) & 0xFFFFFFFF)

        a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7

        for j in range(64):
            s1 = xorSha256(rotateRight([e], 6), xorSha256(rotateRight([e], 11), rotateRight([e], 25)))
            ch = xorSha256([e & f], xorSha256([(~e) & g], [e & f]))
            temp1 = (h + s1[0] + ch[0] + K[j] + w[j]) & 0xFFFFFFFF
            s0 = xorSha256(rotateRight([a], 2), xorSha256(rotateRight([a], 13), rotateRight([a], 22)))
            maj = xorSha256([a & b], xorSha256([a & c], [b & c]))
            temp2 = (s0[0] + maj[0]) & 0xFFFFFFFF

            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF

        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF
        h5 = (h5 + f) & 0xFFFFFFFF
        h6 = (h6 + g) & 0xFFFFFFFF
        h7 = (h7 + h) & 0xFFFFFFFF

    return f'{h0:08x}{h1:08x}{h2:08x}{h3:08x}{h4:08x}{h5:08x}{h6:08x}{h7:08x}'