#!/usr/bin/env python3
import argparse
import socket

from binary_protocol import encode_frame, recv_frame


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8890)
    parser.add_argument("--frames", type=int, default=0)
    args = parser.parse_args()
    handled = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((args.host, args.port))
        listener.listen(5)
        connection, _peer = listener.accept()
        with connection:
            while not args.frames or handled < args.frames:
                command, data = recv_frame(connection)
                handled += 1
                connection.sendall(encode_frame(command | 0x80, b"OK:" + data))


if __name__ == "__main__":
    main()

