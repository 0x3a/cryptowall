#!/usr/bin/python

"""
    CryptoWall C2 communication decoder by Yonathan Klijnsma (@ydklijnsma)

    Works for:
        - Unnamed cryptlocker clone (2013)
        - CryptoDefense (2014)
        - CryptoWall 1.0 (2014)
        - CryptoWall 2.0 (2014)
        - CryptoWall 3.0 (2015)
        - CryptoWall "4" (2015)
"""

import re
import sys

def rc4(data, key):
    x = 0
    box = range(256)
    for i in range(256):
        x = (x + box[i] + ord(key[i % len(key)])) % 256
        box[i], box[x] = box[x], box[i]
    
    x = y = 0
    out = []
    for char in data:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        out.append(chr(ord(char) ^ box[(box[x] + box[y]) % 256]))    
    return ''.join(out)
    
def decrypt_data(scrambled_key, data):
    key = ''.join(sorted(list(scrambled_key)))

    if not len(data) % 2:
        encr_data = data.decode('hex')
        decr_data = rc4(encr_data, key)

        if decr_data[:1] == '{' and decr_data[-1:] == '}':
            return decr_data

    pd_offset = sum([ int(i) for i in re.findall(r'\d', key)])
    encr_data = data[pd_offset:].decode('hex')
    decr_data = rc4(encr_data, key)

    if decr_data[:1] == '{' and decr_data[-1:] == '}':
        return decr_data

    return ''

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: %s <post url param/location> <post data>' % sys.argv[0]
        exit()
    else:
        print decrypt_data(sys.argv[1], sys.argv[2])
