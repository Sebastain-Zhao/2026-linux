# Project 01：最小网络闭环（导师演示）

## 状态

- 演示时间：2026-09-25 19:42 CST
- 导师闭环：已跑通
- 学员复现实验：待执行、待验收

## 目标

验证并观察下面这条最短路径：

```text
ping
  → 内核查询路由
  → 选择源 IPv4 和出接口
  → 查询邻居缓存中的下一跳 MAC
  → Ethernet 帧经驱动和物理网卡发出
  → 网关返回 ICMP Echo Reply
```

## 环境

- 实际出接口：`enx6c1ff768ace6`
- 本机 IPv4：`192.168.31.195/24`
- 默认网关：`192.168.31.1`
- Wi-Fi 接口：DOWN
- `Meta`：代理软件创建的 TUN 虚拟接口，不是本次局域网闭环的物理出口

## 操作与证据

### 1. 查询内核的路由决策

```bash
ip route get 192.168.31.1
```

关键输出：

```text
192.168.31.1 dev enx6c1ff768ace6 src 192.168.31.195
```

含义：

- destination：`192.168.31.1`，本次要到达的目标。
- `dev enx6c1ff768ace6`：内核选择的出接口。
- `src 192.168.31.195`：内核选择放入 IP 包头的源 IPv4 地址。
- 输出中没有 `via`：网关自身与本机位于直连网段，到它不需要再经过另一个网关。

### 2. 查看邻居缓存

```bash
ip neigh show 192.168.31.1
```

结果显示网关已有 MAC 地址，状态为 `REACHABLE`。因此本次发送 ICMP 前无需重新进行 ARP 查询。

### 3. 抓包并发送 ICMP

抓包过滤器只保留本机与网关之间的 ICMP：

```text
icmp and host 192.168.31.1
```

随后执行：

```bash
ping -c 2 -W 2 192.168.31.1
```

结果：

```text
2 packets transmitted, 2 received, 0% packet loss
```

抓包得到四个 Ethernet 帧：

```text
<PC_MAC>      > <GATEWAY_MAC>: 192.168.31.195 > 192.168.31.1: ICMP echo request, seq 1
<GATEWAY_MAC> > <PC_MAC>:      192.168.31.1 > 192.168.31.195: ICMP echo reply, seq 1
<PC_MAC>      > <GATEWAY_MAC>: 192.168.31.195 > 192.168.31.1: ICMP echo request, seq 2
<GATEWAY_MAC> > <PC_MAC>:      192.168.31.1 > 192.168.31.195: ICMP echo reply, seq 2
```

抓包统计为 4 个包，接口丢包为 0。

## Linux 内部发生了什么

1. `ping` 请求内核发送 ICMP Echo Request。
2. 内核查询路由表，确认目标属于 `192.168.31.0/24` 直连网段。
3. 内核选择 `enx6c1ff768ace6` 和源地址 `192.168.31.195`。
4. 内核在邻居缓存中找到 `192.168.31.1` 对应的 MAC 地址。
5. IP 包被封装进 Ethernet 帧，交给网卡驱动和 NIC 发出。
6. 网关收到请求并返回 ICMP Echo Reply。
7. 本机 NIC、驱动和内核网络栈接收回复，`ping` 显示时延和统计结果。

## 为什么没有看到 ARP

实验开始前，网关邻居项已经为 `REACHABLE`。内核已知道目标 IPv4 对应的下一跳 MAC，因此可以直接发送 Ethernet 帧。

Project 02 会在受控条件下清除邻居缓存，再观察：

```text
ARP Request → ARP Reply → ICMP Request → ICMP Reply
```

## 一次抓包竞态

第一次尝试让抓包器和 `ping` 同时启动，只捕获到第二次请求与回复。原因是第一包可能早于抓包器完全就绪。这不是网络丢包。

第二次实验先让抓包器就绪，再执行 `ping`，成功捕获全部四包。以后做抓包实验时，应先确认抓包已经开始，再触发被观察的网络行为。

## 与后续学习的联系

- `ping` 发起请求：以后对应 socket API 和 system call。
- 路由与 IP：以后进入 Linux 内核网络栈和策略路由。
- Ethernet 源/目的 MAC：以后对应驱动准备的二层帧。
- 物理接口：以后对应 network driver、NIC 和 PHY。
- 先抓包再触发事件：同样适用于 BLE HCI snoop 和数字钥匙协议分析。

## 验收结论

导师最小闭环已跑通，但这不代表学员完成实验。下一步由学员亲自执行相同的观察流程，并用自己的话解释结果。

