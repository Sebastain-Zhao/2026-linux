#!/usr/bin/env python3
import argparse
import socket


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("message")
    parser.add_argument("--port", type=int, default=8888)
    args = parser.parse_args()

    payload = args.message.encode()
    with socket.create_connection((args.host, args.port), timeout=5) as sock:
        sock.sendall(payload)
        reply = sock.recv(4096)
    print(reply.decode(errors="replace"))


if __name__ == "__main__":
    main()

