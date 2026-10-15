# Ubuntu 实验环境配置

## 状态

基础环境已审计；等待执行安装脚本与重新登录后的验收。

## 已确认环境

- Ubuntu 24.04.4 LTS，x86_64
- 当前内核对应的 Linux headers 已安装
- 物理有线接口、Wi-Fi 接口和代理 TUN 接口可见
- BlueZ 已安装，蓝牙服务已启用且控制器可见
- Python 3.12、GCC、GDB、Make、Git 和 OpenBSD netcat 已安装
- 根文件系统约有 427 GiB 可用空间

## 本次补充范围

- 网络诊断：`traceroute`、`socat`、`iperf3`、`nftables`
- 抓包分析：Wireshark、TShark，以及普通用户 `dumpcap` 权限
- Python/C 构建：CMake、pkg-config、Ninja、strace、Valgrind
- 内核构建依赖：Bison、Flex、OpenSSL/ELF 开发库、pahole
- BLE 开发：BlueZ 开发库
- 嵌入式串口：picocom、minicom
- 硬件枚举：usbutils、pciutils

## 权限策略

- `tcpdump` 不授予系统范围 capability，实时抓包时仍使用 `sudo tcpdump`。
- Wireshark/TShark 通过受限的 `dumpcap` 和 `wireshark` 用户组支持普通用户抓包。
- 串口设备通过 `dialout` 用户组授权，不为串口工具使用 root 身份。
- SSH 私钥、令牌和其他凭据不得写入项目或 Git。

## 操作

在项目根目录运行：

```bash
sudo ./scripts/setup_ubuntu_lab.sh
```

安装后注销并重新登录，再运行：

```bash
./scripts/check_lab_environment.sh
```

## 暂缓项

以下配置依赖具体开发板，确定型号、CPU 架构和烧录方式后再安装：

- ARM/AArch64/RISC-V 交叉编译器
- 厂商 SDK、BSP 与烧录工具
- USB 转串口设备的实际权限验证
- GPIO 库、设备树与内核模块实验配置

## 验收标准

- 验收脚本最终输出 `ENVIRONMENT_OK`
- 当前登录会话属于 `wireshark` 用户组
- 当前登录会话属于 `dialout` 用户组
- `bluetooth.service` 为 active
- 当前内核版本对应的 headers 存在
