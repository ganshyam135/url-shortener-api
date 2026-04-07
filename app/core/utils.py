import string

BASE62 = string.ascii_letters + string.digits

def encode_base62(num: int) -> str:
    if num == 0:
        return BASE62[0]
    
    base = len(BASE62)
    result = []

    while num > 0:
        remainder = num % base
        result.append(BASE62[remainder])
        num = num // base

    return ''.join(reversed(result))
