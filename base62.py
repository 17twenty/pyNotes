#!/usr/bin/env python

""" Base62 conversion library - Alphanumeric only """

import string
alphabet = string.letters + string.digits
max = 11

def fromInt(num):
    if num == 0:
        return alphabet[0]

    arr = []
    radix = len(alphabet)
    while num:
        arr.append(alphabet[num%radix])
        num /= radix
    arr.reverse()
    return (alphabet[0] * (max - len(arr))) + ''.join(arr)

def toInt(stri):
    radix = len(alphabet)
    power = len(stri) - 1
    num = 0
    for char in stri:
        num += alphabet.index(char) * (radix ** power)
        power -= 1
    return num
