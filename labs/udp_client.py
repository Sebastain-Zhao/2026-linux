#!/usr/bin/env python3
import argparse
import socket


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("message")
    parser.add_argument("--port", type=int, default=9999)
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(5)
        sock.sendto(args.message.encode(), (args.host, args.port))
        payload, peer = sock.recvfrom(65535)
    print(f"from={peer[0]}:{peer[1]} {payload.decode(errors='replace')}")


if __name__ == "__main__":
    main()

