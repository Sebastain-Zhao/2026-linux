#!/usr/bin/env python3
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def check(name: str, condition: bool, detail: str = "") -> None:
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {name}{': ' + detail if detail else ''}")
    if not condition:
        raise RuntimeError(name)


def wait_port(port: int, socktype: int = socket.SOCK_STREAM) -> None:
    if socktype == socket.SOCK_DGRAM:
        time.sleep(0.15)
        return
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.1):
                return
        except OSError:
            time.sleep(0.05)
    raise TimeoutError(f"port {port} did not open")


def start(script: str, *args: str) -> subprocess.Popen:
    return subprocess.Popen(
        [sys.executable, str(ROOT / script), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def stop(process: subprocess.Popen) -> None:
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()


def main() -> None:
    check("required command ip", shutil.which("ip") is not None)
    check("required command ss", shutil.which("ss") is not None)
    check("required command nc", shutil.which("nc") is not None)

    addresses = subprocess.check_output(["ip", "-brief", "-4", "addr"], text=True)
    routes = subprocess.check_output(["ip", "-4", "route"], text=True)
    check("IPv4 interface present", "127.0.0.1/8" in addresses)
    check("default route present", "default via" in routes)

    nc_server = subprocess.Popen(["nc", "-l", "-s", "127.0.0.1", "-p", "8877"], stdout=subprocess.PIPE, text=True)
    try:
        time.sleep(0.15)
        subprocess.run(["nc", "-N", "127.0.0.1", "8877"], input="NC_OK\n", text=True, timeout=3, check=True)
        output, _ = nc_server.communicate(timeout=3)
        check("Netcat TCP", output.strip() == "NC_OK", output.strip())
    finally:
        stop(nc_server)

    echo = start("tcp_echo_server.py", "--port", "8888")
    try:
        wait_port(8888)
        with socket.create_connection(("127.0.0.1", 8888), timeout=3) as client:
            listening = subprocess.check_output(["ss", "-lnt"], text=True)
            established = subprocess.check_output(["ss", "-nt"], text=True)
            check("ss LISTEN", ":8888" in listening)
            check("ss ESTABLISHED", ":8888" in established)
            client.sendall(b"TCP_OK")
            check("Python TCP echo", client.recv(64) == b"TCP_OK")
    finally:
        stop(echo)

    device = start("device_server.py", "--port", "8889")
    try:
        wait_port(8889)
        result = subprocess.check_output(
            [sys.executable, str(ROOT / "device_client.py"), "127.0.0.1", "LED_ON", "STATUS", "LED_OFF", "STATUS", "--port", "8889"],
            text=True,
            timeout=5,
        )
        expected = ["OK LED=ON", "OK LED=ON", "OK LED=OFF", "OK LED=OFF"]
        check("simulated device protocol", result.splitlines() == expected, result.replace("\n", "; ").strip())
    finally:
        stop(device)

    udp = start("udp_server.py", "--port", "9999", "--count", "1")
    try:
        wait_port(9999, socket.SOCK_DGRAM)
        result = subprocess.check_output(
            [sys.executable, str(ROOT / "udp_client.py"), "127.0.0.1", "UDP_OK", "--port", "9999"],
            text=True,
            timeout=5,
        )
        check("UDP request/reply", result.rstrip().endswith("ACK UDP_OK"), result.strip())
    finally:
        stop(udp)

    binary = start("binary_server.py", "--port", "8890", "--frames", "3")
    try:
        time.sleep(0.15)
        result = subprocess.check_output(
            [sys.executable, str(ROOT / "binary_client.py"), "127.0.0.1", "--port", "8890"],
            text=True,
            timeout=5,
        )
        expected = ["cmd=0x81 data=OK:A", "cmd=0x82 data=OK:B", "cmd=0x83 data=OK:FRAGMENTED"]
        check("binary framing, fragmentation and CRC", result.splitlines() == expected, result.replace("\n", "; ").strip())
    finally:
        stop(binary)

    print("ALL_NON_PRIVILEGED_TESTS_PASSED")


if __name__ == "__main__":
    main()

