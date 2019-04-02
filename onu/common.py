




def hexify(buffer):
    """
    Return a hexadecimal string encoding of input buffer
    """
    return ''.join('%02x' % ord(c) for c in buffer)