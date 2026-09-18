#!/usr/bin/env bash

set -Eeuo pipefail

if [[ ${EUID} -ne 0 ]]; then
    echo "请使用 sudo 运行：sudo ./scripts/setup_ubuntu_lab.sh" >&2
    exit 1
fi

lab_user=${SUDO_USER:-}
if [[ -z ${lab_user} || ${lab_user} == root ]]; then
    echo "无法确定实验用户。请以普通用户通过 sudo 运行本脚本。" >&2
    exit 1
fi

echo "将为用户 ${lab_user} 配置 Linux 网络、内核、BLE 和嵌入式基础环境。"

# Allow members of the wireshark group to capture through dumpcap. Keep
# tcpdump unchanged so it still requires sudo for live packet capture.
printf '%s\n' 'wireshark-common wireshark-common/install-setuid boolean true' \
    | debconf-set-selections

export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get install -y \
    iproute2 \
    iputils-ping \
    tcpdump \
    netcat-openbsd \
    ethtool \
    traceroute \
    mtr-tiny \
    socat \
    lsof \
    dnsutils \
    iperf3 \
    nftables \
    tshark \
    wireshark \
    python3 \
    python3-venv \
    build-essential \
    gcc \
    gdb \
    make \
    cmake \
    pkg-config \
    ninja-build \
    strace \
    valgrind \
    "linux-headers-$(uname -r)" \
    bc \
    bison \
    flex \
    libssl-dev \
    libelf-dev \
    dwarves \
    cpio \
    bluez \
    rfkill \
    libbluetooth-dev \
    picocom \
    minicom \
    usbutils \
    pciutils \
    jq \
    curl \
    git

usermod -aG wireshark "${lab_user}"
systemctl enable --now bluetooth

echo
echo "基础环境安装完成。"
echo "请注销并重新登录，使 wireshark 用户组立即生效。"
echo "重新登录后运行：./scripts/check_lab_environment.sh"

