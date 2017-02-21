#!/usr/bin/env python3


def bytes_to_int(value, signed=False):
    """Return integer given bytes."""
    return int.from_bytes(bytes(value), byteorder='big', signed=signed)


def int_to_bytes(value, length=1, signed=False):
    """Return bytes given integer"""
    return int(value).to_bytes(length, byteorder='big', signed=signed)


def ber_decode(length):
    """Return decoded BER length as integer given bytes."""
    if bytes_to_int(length) < 128:
        # BER Short Form
        return bytes_to_int(length)
    else:
        # BER Long Form
        return bytes_to_int(length[1:])


def ber_encode(length):
    """Return encoded BER length as bytes given integer."""
    if length < 128:
        # BER Short Form
        return int_to_bytes(length)
    else:
        # BER Long Form
        byte_length = ((length.bit_length() - 1) // 8) + 1

        return int_to_bytes(byte_length + 128) + int_to_bytes(length, length=byte_length)
