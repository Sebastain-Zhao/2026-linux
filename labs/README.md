# 第一阶段参考实验

这里保存导师用于预验收网络环境的最小参考实现。学习阶段仍需按 Project 01 到 Project 09 的顺序亲自执行、观察和解释。

## 文件

- `tcp_echo_server.py` / `tcp_echo_client.py`：TCP echo 与 socket 基本调用
- `device_server.py` / `device_client.py`：文本设备控制协议，使用内存模拟 LED
- `udp_server.py` / `udp_client.py`：UDP 请求/响应
- `binary_protocol.py`：二进制帧、网络字节序与 CRC16
- `binary_server.py` / `binary_client.py`：TCP 字节流上的组帧、粘包和拆包
- `smoke_test.py`：自动启动各端并执行预验收

## 自动预验收

```bash
python3 labs/smoke_test.py
```

自动预验收只证明环境和参考实现能够运行，不能代替手动抓包、现象观察和口头解释。

