#!/usr/bin/env python3
import argparse
import socket


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("commands", nargs="+")
    parser.add_argument("--port", type=int, default=8889)
    args = parser.parse_args()

    with socket.create_connection((args.host, args.port), timeout=5) as sock:
        stream = sock.makefile("rwb")
        for command in args.commands:
            stream.write((command + "\n").encode())
        stream.flush()
        for _ in args.commands:
            print(stream.readline().decode(errors="replace").rstrip())


if __name__ == "__main__":
    main()

