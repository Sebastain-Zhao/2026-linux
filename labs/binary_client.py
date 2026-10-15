#!/usr/bin/env python3
import argparse
import socket
import time

from binary_protocol import encode_frame, recv_frame


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("--port", type=int, default=8890)
    args = parser.parse_args()

    first = encode_frame(1, b"A")
    second = encode_frame(2, b"B")
    third = encode_frame(3, b"FRAGMENTED")
    with socket.create_connection((args.host, args.port), timeout=5) as sock:
        # 两个应用帧一次写入，接收端不能依赖 recv() 边界。
        sock.sendall(first + second)
        # 一个应用帧拆成三次写入，接收端必须按长度重组。
        sock.sendall(third[:2])
        time.sleep(0.02)
        sock.sendall(third[2:7])
        time.sleep(0.02)
        sock.sendall(third[7:])
        for _ in range(3):
            command, data = recv_frame(sock)
            print(f"cmd=0x{command:02x} data={data.decode()}")


if __name__ == "__main__":
    main()

