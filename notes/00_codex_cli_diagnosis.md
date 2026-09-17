# 真实案例：Codex CLI 无法正常运行

## 状态

诊断与修复验证完成；Codex 模型请求及 Linux sandbox 均正常。

## 关键结果

- Codex 路径：`/home/seb/.local/bin/codex`
- Codex 版本：`codex-cli 0.154.0`
- 登录状态：使用 ChatGPT 登录
- 实际最小请求成功返回 `OK`
- 非交互 SSH 默认找不到 `codex`，交互式 zsh 可以找到
- `bubblewrap 0.9.0` 已安装
- `kernel.apparmor_restrict_unprivileged_userns = 1`
- user namespace 测试失败：`Operation not permitted`
- `apparmor-profiles` / `apparmor-utils` 及 `bwrap-userns-restrict` profile 缺失

## 结论

当前不是 Codex 到 OpenAI 的网络或代理故障。模型请求能够成功。剩余问题位于本机 Linux sandbox 前置条件：Ubuntu AppArmor 阻止了 bubblewrap 所需的 user namespace。

## 推荐修复方向

按照 OpenAI 官方 Codex sandbox 文档，为 Ubuntu 24.04 安装 AppArmor profiles，并加载专用于 bubblewrap 的 profile。优先采用专用 profile，不全局关闭 user namespace 限制。

## 修复与验收

- 已安装 `apparmor-profiles` 和 `apparmor-utils`。
- 已安装 `/etc/apparmor.d/bwrap-userns-restrict` 并加载 profile。
- 保持 `kernel.apparmor_restrict_unprivileged_userns = 1`，未全局降低安全限制。
- 普通用户 bubblewrap 冒烟测试返回 `BWRAP_OK`。
- Codex 以 `read-only` sandbox 启动，无先前的 user namespace warning。
- Codex 成功调用 shell 执行 `pwd`，结果为 `/tmp`。
