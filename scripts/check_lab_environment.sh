#!/usr/bin/env bash

set -u

required_commands=(
    ip ping ss tcpdump nc ethtool traceroute mtr socat lsof dig iperf3
    nft tshark wireshark python3 gcc gdb make cmake pkg-config ninja
    strace valgrind bluetoothctl btmon rfkill picocom minicom lsusb lspci
    jq curl git
)

missing=0

echo "== 命令检查 =="
for command_name in "${required_commands[@]}"; do
    if command -v "${command_name}" >/dev/null 2>&1; then
        printf 'OK      %s\n' "${command_name}"
    else
        printf 'MISSING %s\n' "${command_name}"
        missing=1
    fi
done

echo
echo "== 用户组检查 =="
if id -nG | tr ' ' '\n' | grep -qx wireshark; then
    echo "OK      当前会话已加入 wireshark 组"
else
    echo "PENDING 当前会话尚未加入 wireshark 组；请注销并重新登录"
    missing=1
fi

echo
echo "== 内核与蓝牙检查 =="
kernel_release=$(uname -r)
if [[ -d /usr/src/linux-headers-${kernel_release} ]]; then
    echo "OK      linux-headers-${kernel_release}"
else
    echo "MISSING linux-headers-${kernel_release}"
    missing=1
fi

if systemctl is-active --quiet bluetooth; then
    echo "OK      bluetooth.service active"
else
    echo "MISSING bluetooth.service not active"
    missing=1
fi

echo
if [[ ${missing} -eq 0 ]]; then
    echo "ENVIRONMENT_OK"
else
    echo "ENVIRONMENT_INCOMPLETE"
fi

exit "${missing}"

