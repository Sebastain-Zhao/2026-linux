#!/usr/bin/env bash
set -euo pipefail

if [[ ${EUID} -ne 0 ]]; then
  echo "Run with sudo: sudo bash scripts/run_packet_capture_preflight.sh" >&2
  exit 1
fi

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
CAPTURE_DIR="${ROOT_DIR}/captures"
REPORT="${ROOT_DIR}/notes/00_packet_capture_preflight.md"
mkdir -p "${CAPTURE_DIR}"

INTERFACE="$(ip -4 route show default | awk 'NR == 1 {print $5}')"
GATEWAY="$(ip -4 route show default | awk 'NR == 1 {print $3}')"
if [[ -z ${INTERFACE} || -z ${GATEWAY} ]]; then
  echo "No IPv4 default route found" >&2
  exit 1
fi

ARP_PCAP="${CAPTURE_DIR}/arp_icmp_gateway.pcap"
TCP_PCAP="${CAPTURE_DIR}/tcp_8888_loopback.pcap"
ARP_TEXT="$(mktemp)"
TCP_TEXT="$(mktemp)"
cleanup() {
  rm -f "${ARP_TEXT}" "${TCP_TEXT}"
}
trap cleanup EXIT

ip neigh del "${GATEWAY}" dev "${INTERFACE}" 2>/dev/null || true
timeout 6 tcpdump -U -i "${INTERFACE}" -nn -e \
  "arp or (icmp and host ${GATEWAY})" -w "${ARP_PCAP}" >/dev/null 2>&1 &
ARP_CAPTURE_PID=$!
sleep 0.5
ping -c 1 -W 2 "${GATEWAY}" >/dev/null
wait "${ARP_CAPTURE_PID}" || [[ $? -eq 124 ]]
tcpdump -nn -e -r "${ARP_PCAP}" >"${ARP_TEXT}" 2>/dev/null

grep -F "ARP, Request" "${ARP_TEXT}" >/dev/null
grep -F "ARP, Reply" "${ARP_TEXT}" >/dev/null
grep -F "ICMP echo request" "${ARP_TEXT}" >/dev/null
grep -F "ICMP echo reply" "${ARP_TEXT}" >/dev/null

timeout 6 tcpdump -U -i lo -nn "tcp port 8888" -w "${TCP_PCAP}" >/dev/null 2>&1 &
TCP_CAPTURE_PID=$!
sleep 0.5
python3 "${ROOT_DIR}/labs/tcp_echo_server.py" --host 127.0.0.1 --port 8888 --once &
SERVER_PID=$!
sleep 0.3
python3 "${ROOT_DIR}/labs/tcp_echo_client.py" 127.0.0.1 TCP_CAPTURE_OK --port 8888 >/dev/null
wait "${SERVER_PID}"
wait "${TCP_CAPTURE_PID}" || [[ $? -eq 124 ]]
tcpdump -nn -r "${TCP_PCAP}" >"${TCP_TEXT}" 2>/dev/null

grep -F "Flags [S]" "${TCP_TEXT}" >/dev/null
grep -F "Flags [S.]" "${TCP_TEXT}" >/dev/null
grep -F "Flags [.]" "${TCP_TEXT}" >/dev/null
grep -F "Flags [P.]" "${TCP_TEXT}" >/dev/null
grep -F "Flags [F.]" "${TCP_TEXT}" >/dev/null

{
  echo "# 特权抓包预验收"
  echo
  echo "- 接口：\`${INTERFACE}\`"
  echo "- 默认网关：\`${GATEWAY}\`"
  echo "- ARP/ICMP pcap：\`captures/$(basename "${ARP_PCAP}")\`"
  echo "- TCP pcap：\`captures/$(basename "${TCP_PCAP}")\`"
  echo
  echo "## ARP + ICMP"
  echo
  echo '```text'
  cat "${ARP_TEXT}"
  echo '```'
  echo
  echo "## TCP 连接、数据与关闭"
  echo
  echo '```text'
  cat "${TCP_TEXT}"
  echo '```'
  echo
  echo "## 验收"
  echo
  echo "- [x] ARP Request"
  echo "- [x] ARP Reply"
  echo "- [x] ICMP Echo Request"
  echo "- [x] ICMP Echo Reply"
  echo "- [x] TCP SYN"
  echo "- [x] TCP SYN-ACK"
  echo "- [x] TCP ACK"
  echo "- [x] TCP PSH/数据"
  echo "- [x] TCP FIN/关闭"
} >"${REPORT}"

if [[ -n ${SUDO_UID:-} && -n ${SUDO_GID:-} ]]; then
  chown "${SUDO_UID}:${SUDO_GID}" "${ARP_PCAP}" "${TCP_PCAP}" "${REPORT}"
fi

echo "PACKET_CAPTURE_PREFLIGHT_PASSED"
echo "Report: ${REPORT}"

