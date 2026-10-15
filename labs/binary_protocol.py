#!/usr/bin/env python3
import struct

MAGIC = 0xAA55
VERSION = 1
HEADER = struct.Struct("!HBBH")
CRC = struct.Struct("!H")


def crc16_ccitt(data: bytes) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc


def encode_frame(command: int, data: bytes) -> bytes:
    body = HEADER.pack(MAGIC, VERSION, command, len(data)) + data
    return body + CRC.pack(crc16_ccitt(body))


def recv_exact(sock, length: int) -> bytes:
    chunks = bytearray()
    while len(chunks) < length:
        chunk = sock.recv(length - len(chunks))
        if not chunk:
            raise EOFError("connection closed during frame")
        chunks.extend(chunk)
    return bytes(chunks)


def recv_frame(sock) -> tuple[int, bytes]:
    header = recv_exact(sock, HEADER.size)
    magic, version, command, length = HEADER.unpack(header)
    if magic != MAGIC or version != VERSION:
        raise ValueError("invalid frame header")
    data = recv_exact(sock, length)
    received_crc = CRC.unpack(recv_exact(sock, CRC.size))[0]
    expected_crc = crc16_ccitt(header + data)
    if received_crc != expected_crc:
        raise ValueError("CRC mismatch")
    return command, data

