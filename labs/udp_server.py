#!/usr/bin/env python3
import argparse
import socket


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9999)
    parser.add_argument("--count", type=int, default=0)
    args = parser.parse_args()
    received = 0

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((args.host, args.port))
        while not args.count or received < args.count:
            payload, peer = sock.recvfrom(65535)
            received += 1
            sock.sendto(b"ACK " + payload, peer)


if __name__ == "__main__":
    main()

