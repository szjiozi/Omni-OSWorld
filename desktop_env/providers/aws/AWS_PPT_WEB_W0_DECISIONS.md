# AWS Ubuntu PowerPoint Web Phase W0 决策记录

更新日期：2026-07-29

状态：W0 已完成；W1 控制面资源已创建，所有 smoke 实例均已清理。

本文档冻结 Phase W1 所依赖的部署决策。它不记录 AWS 密钥、Microsoft 密码、浏览器
cookie、session token 或个人账户信息。

## 1. 部署基线

| 项目 | 决策 |
|---|---|
| 本地开发环境 | Conda `osworld-aws-dev`，Python 3.12 |
| AWS 身份 | IAM Identity Center profile `osworld-dev` |
| Identity Center region | `us-east-2` |
| EC2 deployment region | `us-east-1` |
| 执行系统 | OSWorld 官方 Ubuntu 1920×1080 AMI |
| 目标应用 | Chrome 中的 PowerPoint for the web |
| 输出 | 下载后的原生 `.pptx` |
| 并发 | 1 个 environment |
| 默认 TTL | 180 分钟 |
| 首批动画 | Tier A：单页、自动播放、无 trigger |

仓库当前 `desktop_env/providers/aws/manager.py` 已包含 `us-east-1` 的官方 OSWorld
Ubuntu AMI 映射，不需要构建 Windows/Office AMI。

## 2. Microsoft 账户与产品边界

- 不使用用户的 Microsoft 365 Personal 主账户，避免 Agent 接触私人 OneDrive、
  邮件、付款信息或其他文件。
- W1 新建一个无私人数据、无付款信息的专用 Microsoft 测试账户。
- PowerPoint for the web 本身可由普通 Microsoft 账户使用，不需要 AWS Office、
  Managed Microsoft AD 或 RDS SAL。
- 浏览器登录 session 视同凭据：只保存在私有测试镜像或受控 profile 中，不进入
  Git、日志、task JSON 或公开数据。
- Session 过期、MFA 或风控提示必须显式报错，不得把密码写入自动化脚本绕过。

首批任务只使用 PowerPoint Web 可编辑的能力：

- Appear、Fade、Fly、Wipe、Split、Zoom 等网页端可用效果；
- On Click、With Previous、After Previous；
- Duration、Delay、顺序和单对象多效果。

首批任务不使用 animation trigger、桌面端专有效果或依赖桌面 PowerPoint 才能编辑的
动画。Morph 暂不进入个人/免费账户基线。

## 3. AWS 网络

- 复用 `us-east-1` default VPC 和一个 public default subnet。
- W1 创建项目专用 security group。
- 入站只允许创建时探测到的开发者公网出口 IP `/32`。
- 不把 SSH、VNC、5000、5910、8006、8080、8081 或 9222 暴露给
  `0.0.0.0/0`。
- 不创建长期 Elastic IP。

这是对上游 OSWorld AWS 示例的安全收紧，不改变其 Ubuntu AMI 和 provider 主路径。

## 4. 实例、磁盘与成本

- instance type：恢复 OSWorld 仓库官方默认 `t3.xlarge`。
- Root volume：30 GiB `gp3`，使用官方 4000 IOPS / 1000 MiB/s。
- provider 已在 W1 改为统一读取并验证官方实例、磁盘和可选 instance profile。
- 默认 TTL：180 分钟。
- 月度预算警戒线：`USD 20`。
- 不创建 Office、AD 或 RDS 固定月费资源。

按 `us-east-1` on-demand 粗略估算：

| 配置 | 3 小时单次 | 20 次/月 |
|---|---:|---:|
| `t3.xlarge` + 30 GiB 官方 gp3 性能 + public IPv4 | 约 `$0.75–0.80` | 约 `$15–16` |

数据传输、快照、失败后未清理的资源和价格调整会产生额外费用。这是预算估算，不是
账单保证；W1 仍需启用 AWS Budget 告警、TTL 和运行后资源审计。

## 5. W0 技术检查

本地运行：

```bash
python3 scripts/python/preflight_aws_ppt_web_w0.py
python3 scripts/python/preflight_aws_ppt_web_w0.py --stage w0 --strict
```

检查器不调用 AWS API、不打印配置值，也不读取 Microsoft 登录信息。W0 中 subnet 和
security group 尚未选择或创建，因此显示 warning；W1 使用默认
`--stage w1 --strict`，届时这些资源 ID 必须存在。

## 6. W0 退出检查表

- [x] 主路径切换为 AWS Ubuntu + PowerPoint Web。
- [x] Windows Server、Office LTSC、Managed AD 和 RDS SAL 路线已取消。
- [x] IAM Identity Center、`osworld-dev` profile 和 `us-east-1` 已验证。
- [x] 官方 OSWorld Ubuntu AMI 路径已确认。
- [x] 官方 `t3.xlarge`、4000 IOPS / 1000 MiB/s gp3、180 分钟 TTL 和
  `$20/月`警戒线已冻结。
- [x] default VPC/public subnet + `/32` 安全组方案已冻结。
- [x] 专用免费 Microsoft 测试账户方案已冻结。
- [x] W0 strict preflight 和单元测试通过。
- [x] W1 provider 成本/连接配置和 EC2 DryRun 已通过。
- [x] W1 关闭无过滤条件的账户级 Budget 误报，并准备项目专属 Budget 配置。
- [x] W1 配置 TTL scheduler IAM role，并实测 schedule 与失败清理。
- [x] W1 创建 SSM diagnostic instance profile，诊断并修复 5000 API/X11
  readiness race；launch/reset 通过 SSM 主动安装并验证 X11 wait drop-in，
  UserData 仅作干净 AMI 后备。
- [x] W1 建立私有 encrypted authenticated browser AMI。
- [x] W1 完成 upload/edit/slideshow/download/record smoke。
- [x] W1 接入最小正式 task、static/animation evaluator，并完成 10 次
  create/reset/close soak；每轮通过 TTL/API/GNOME-X11/drop-in/截图 gate，
  最终 EC2/EBS/ENI/TTL schedule 全为 0。

Phase W0 和 W1 已完成；项目 Budget 等 Billing 发现 `Project` 标签后应用。

## 7. 参考

- [OSWorld AWS guideline](./AWS_GUIDELINE.md)
- [PowerPoint for the web 入门](https://support.microsoft.com/en-us/powerpoint/get-started-with-powerpoint-for-the-web)
- [PowerPoint Web 动画效果](https://support.microsoft.com/en-US/PowerPoint/animation-effects-available-in-powerpoint-for-the-web)
- [PowerPoint Web 与桌面功能比较](https://support.microsoft.com/en-us/powerpoint/compare-powerpoint-features-on-different-platforms)
- [免费 Microsoft 365 Web Apps](https://support.microsoft.com/en-US/accounts-billing/subscriptions/what-s-the-difference-between-a-microsoft-365-subscription-and-free-web-apps)
