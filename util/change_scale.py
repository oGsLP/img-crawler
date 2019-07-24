def baseN(num, b):
    return ((num == 0) and "0") or \
        (baseN(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])
def encode_b64(n):
    table = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ#$'
    result = []
    temp = n
    if 0 == temp:
      result.append('0')
    else:
      while 0 < temp:
        result.append(table[temp % 64])
        temp //= 64
    return ''.join([x for x in reversed(result)])