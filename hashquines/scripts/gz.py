#!/usr/bin/env python3

DESCRIPTION = "Set rendered hex value in Ange's GZIP hashquine."

# Ange Albertini 2023

import hashlib
import random

from argparse import ArgumentParser
from collisions import *

HEX_BASE = 16
MD5_LEN = 32

HEADER_S = 85760
HEADER_MD5 = 'de4a4312a137a2b95c3dfaa3dceb6520'

# 192 Unicolls, evenly spaced
block_indexes = [1 + 7 * i for i in range(192)]


def main():
    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-v',
                        '--value',
                        type=str,
                        nargs='?',
                        const=random,
                        help='Hex value to encode (random if not specified)')

    parser.add_argument("filename")
    args = parser.parse_args()

    fn = args.filename
    with open(fn, "rb") as f:
        data = bytearray(f.read())

    assert hashlib.md5(data[:HEADER_S]).hexdigest() == HEADER_MD5
    if args.value is not None:
        if args.value == random:
            hex_value = "".join(
                [random.choice("0123456789abcdef") for _ in range(MD5_LEN)])
            print("Encoding random value: %s" % hex_value)
        else:
            hex_value = "%032x" % int(args.value, HEX_BASE)
            hex_value = hex_value[:MD5_LEN]
            print("Encoding requested value: `%s` (len:%i)" %
                  (hex_value, len(hex_value)))
    else:
        hex_value = hashlib.md5(data).hexdigest()
        print("Encoding file MD5: `%s` (len:%i)" % (hex_value, len(hex_value)))

    collcount = len(block_indexes)
    HEXRANGE = "0123456789abcdef"
    VALUES = HEXRANGE * (collcount // 16) + \
        HEXRANGE[:collcount % 16]
    assert len(VALUES) == collcount

    targetidx = 0
    output = ""
    for i, index in enumerate(block_indexes):
        if (targetidx < len(hex_value)) and (hex_value[targetidx]
                                             == VALUES[i]):
            output += VALUES[i]
            data, _ = setUniColl(data, index, True)
            targetidx += 1
        else:
            data, _ = setUniColl(data, index, False)

    print("Output value: '%s' (length:%i)" % (output, len(output)))
    with open("output.gz", "wb") as f:
        f.write(data)


if __name__ == '__main__':
    main()
