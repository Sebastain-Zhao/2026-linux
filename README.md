# Linux 网络与嵌入式学习记录

## 当前阶段

第一阶段 / Project 01：认识我的 Linux 网络

当前微实验：01 —— 识别 Ubuntu 主机的网络接口与 IP 地址（待验收）

环境准备：审计及脚本已完成，等待执行安装脚本并验收。

最近进度记录：[`notes/2026-09-19_10-53-57-进度.md`](notes/2026-09-19_10-53-57-进度.md)

## 已完成实验

- 暂无
- 已完成 Ubuntu 网络、内核、BLE 与嵌入式基础环境审计；安装待验收
- 已完成 GitHub SSH、全局 Git 身份和 Codex 文档同步规则配置

## 使用过的命令

- 导师远程诊断使用：`ip addr`、`ip route`、`ip rule`、`ip route get`、`ping`、`ss`、`curl`
- 学员实验仍待执行：`ip addr`

## 重要知识点

- 浏览器代理通常代理 HTTP/HTTPS；`ping` 使用 ICMP，不能据此判断网页是否可访问。
- Linux 可能通过策略路由把流量送入代理软件创建的 TUN 虚拟接口。
- 排障时应分别验证局域网、DNS、IP 层 ICMP、TCP/HTTPS 和代理链路。

## 我遇到的问题

- Codex 沙箱不能代替学员完成需要观察和解释的网络实验，真实实验由学员在 Ubuntu 终端执行。
- 基础软件安装需要本人在终端输入 sudo 密码，Codex 不读取或保存密码。
- Ubuntu 主机浏览器可访问 Google，但 `ping google.com` 无响应；诊断记录见 `notes/00_proxy_ping_diagnosis.md`。
- Codex CLI 联网与 Linux sandbox 均已验证成功；Ubuntu 24.04 已加载 bubblewrap 专用 AppArmor profile，见 `notes/00_codex_cli_diagnosis.md`。

## 我的理解

- 待用户完成实验后填写

## 尚未理解的问题

- 如何从 `ip addr` 输出识别接口、IPv4 地址、前缀长度和 localhost？

## 下一步

- 执行并验收 `scripts/setup_ubuntu_lab.sh`
- 注销并重新登录，确认 `wireshark` 与 `dialout` 用户组生效
- 在 Ubuntu 主机执行 `ip addr`，观察并解释输出。
