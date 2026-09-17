# 真实案例：浏览器可访问 Google，但 ping 无响应

## 状态

只读诊断完成，未修改系统配置。

## 环境

- Ubuntu 24.04.4 LTS
- 物理接口：`enx6c1ff768ace6`，地址 `192.168.31.195/24`
- 默认网关：`192.168.31.1`
- 代理核心：`FlClashCore`
- 本地代理监听：`127.0.0.1:7890`
- TUN 接口：`Meta`，地址 `198.18.0.1/30`

## 关键证据

1. `ping 192.168.31.1` 成功：本机接口、局域网链路和网关可达。
2. `ping 8.8.8.8` 成功：ICMP 外网访问并非整体故障。
3. `getent ahostsv4 google.com` 成功：DNS 可以解析 Google。
4. `ping google.com` 无回复：只说明该 ICMP Echo 链路没有得到响应。
5. 显式使用 `127.0.0.1:7890` 的 HTTPS 请求返回 HTTP 200：HTTP 代理工作正常。
6. `ip rule` 和 table 2022 将普通用户流量导向 `Meta`：FlClash TUN 模式正在接管流量。

## 结论

浏览器访问与 `ping` 测试的不是同一种协议。浏览器使用 TCP + TLS + HTTP，经本地代理或 TUN 转发；`ping` 使用 ICMP。HTTP/SOCKS 代理本身不提供通用 ICMP 代理语义，TUN 模式对 ICMP 的处理也取决于代理核心、规则和出口节点。因此“网页可访问但 ping 没回复”并不矛盾，也不能单凭该现象认定网络或 Google 不通。

## 分层定位方法

- 网关 ping：检查本机到局域网网关。
- 公网 IP ping：检查 ICMP 是否整体可出网。
- DNS 查询：检查名字能否转换为 IP。
- `curl`/浏览器：检查 TCP、TLS、HTTP 和代理链路。
- `ip rule`、`ip route get`：检查内核最终选择的路由表和出接口。

