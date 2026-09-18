# 待办清单

更新时间：2026-09-17

## 当前优先事项

- [ ] 在 Ubuntu 主机执行 `ip addr`
- [ ] 保存完整输出到 `notes/01_ip_addr.md`
- [ ] 回答实验 01 的五道思考题
- [ ] 完成实验 01 验收后，再进入 `ip link` 与 `ip route` 实验

## Project 01：认识我的 Linux 网络

- [ ] 识别 loopback 接口
- [ ] 识别实际联网接口
- [ ] 解释 IPv4 地址与前缀长度
- [ ] 观察接口的 UP/DOWN 状态
- [ ] 使用 `ip link` 观察 MAC 地址
- [ ] 使用 `ip route` 理解 destination、gateway、dev、src
- [ ] 使用 `ping` 验证 localhost、局域网网关和另一台设备
- [ ] 故意制造一次错误网段配置并分层排查
- [ ] 能解释 Linux 收到目标 IP 后如何决定下一跳和出接口

## 第一阶段后续项目

- [ ] Project 02：ARP + ICMP 抓包
- [ ] Project 03：Netcat TCP 实验
- [ ] Project 04：使用 `ss` 观察 Socket
- [ ] Project 05：Python TCP Client / Server
- [ ] Project 06：TCP 三次握手抓包
- [ ] Project 07：远程控制嵌入式设备
- [ ] Project 08：UDP 版本
- [ ] Project 09：设计简单嵌入式二进制协议

## 环境与工具

- [x] 建立课程总记录 `README.md`
- [x] 建立实验笔记目录 `notes/`
- [x] 审计 Ubuntu 网络、内核、BLE、编译与串口基础环境
- [ ] 执行 `scripts/setup_ubuntu_lab.sh` 并重新登录
- [ ] 运行 `scripts/check_lab_environment.sh`，得到 `ENVIRONMENT_OK`
- [x] 通过 SSH 连接 Ubuntu 主机 `seb@192.168.31.195`
- [x] 排查“浏览器可访问 Google，但 ping 无响应”
- [x] 验证 FlClash HTTP 代理与 Meta TUN 路由
- [x] 验证 Codex CLI 登录及 OpenAI 网络链路
- [x] 修复 Ubuntu 24.04 上 Codex bubblewrap/AppArmor sandbox
- [x] 验证 Codex 可在只读沙箱内调用 shell

## GitHub

- [x] 在 `E:\2026-linux` 初始化本地 Git 仓库
- [x] 创建首次提交：`3ad1724 Add Linux networking study notes`
- [x] 创建 GitHub public 仓库 `2026-linux`
- [x] 添加 GitHub remote `origin`
- [x] 推送 `main` 分支
- [x] 验证 GitHub 上的 README 和 notes 文件完整
- [x] 今后课程新增或更新文档时，在当次任务完成后提交并推送

## 每个实验的固定验收问题

- [ ] 我刚才做了什么？
- [ ] Linux 内部发生了什么？
- [ ] `tcpdump` 能看到什么？
- [ ] 如果失败，我应该从哪里开始排查？
- [ ] 这个知识与 Linux Driver、BLE、Digital Key 有什么关系？
