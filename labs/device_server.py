#!/usr/bin/env python3
import argparse
import socket
import time


class Device:
    def __init__(self) -> None:
        self.led_on = False
        self.started = time.monotonic()

    def execute(self, command: str) -> str:
        if command == "LED_ON":
            self.led_on = True
            return "OK LED=ON"
        if command == "LED_OFF":
            self.led_on = False
            return "OK LED=OFF"
        if command == "STATUS":
            return f"OK LED={'ON' if self.led_on else 'OFF'}"
        if command == "GET_UPTIME":
            return f"OK UPTIME={int(time.monotonic() - self.started)}"
        return "ERR UNKNOWN_COMMAND"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8889)
    parser.add_argument("--max-clients", type=int, default=0)
    args = parser.parse_args()
    device = Device()
    served = 0

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((args.host, args.port))
        listener.listen(5)
        while not args.max_clients or served < args.max_clients:
            connection, _peer = listener.accept()
            served += 1
            with connection:
                stream = connection.makefile("rwb")
                for raw_line in stream:
                    command = raw_line.decode(errors="replace").strip()
                    response = device.execute(command)
                    stream.write((response + "\n").encode())
                    stream.flush()


if __name__ == "__main__":
    main()

