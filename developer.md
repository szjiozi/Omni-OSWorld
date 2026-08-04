# OSWorld 专家轨迹技能学习 Benchmark 开发注意事项

更新日期：2026-08-04

## 2026-08-04 当前开发入口

当前先实现 3-task LibreOffice Calc reference-task construction Pilot，不先跑 downstream
agent。下文原有 expert video bank、skill induction、Qwen agent 和效率 evaluator 内容是
后续 benchmark 设计；近期开发以根目录 `plan.md` 的 P0-P2 为准。

新增代码和数据契约：

```text
benchmark_construction/                         # construction Python primitives
scripts/python/extract_reference_skills.py      # 显式 3-task extraction CLI
evaluation_examples/expert_skill_learning/
├── prompts/                                    # 独立英文 .txt prompts
├── schemas/                                    # LLM/final/review JSON Schema
└── pricing/                                    # 有日期的 token 单价
```

本地环境需要 OpenAI Python SDK v1+ 的 `AsyncOpenAI`。更新最小开发环境：

```bash
conda env update -n osworld-aws-dev -f environment.aws-dev.yml --prune
conda activate osworld-aws-dev
python -c "from openai import AsyncOpenAI; print('AsyncOpenAI ready')"
```

API key 只能通过环境变量提供，不能写进 prompt、命令历史示例、JSON、日志或 Git：

```bash
export OPENAI_API_KEY=<provided-outside-the-repository>
```

冻结的 3 个 OSWorld-Human Calc task 记录在
`evaluation_examples/expert_skill_learning/pilot/source_tasks.json`。运行：

```bash
python scripts/python/extract_reference_skills.py \
  --source-manifest \
    evaluation_examples/expert_skill_learning/pilot/source_tasks.json
```

该 manifest 已复制全部 40 个 `single_actions`，可独立复现 prompt。需要核对上游时额外传
`--source-root /path/to/osworld-human`；工具将验证 pinned raw JSON 的 SHA256、instruction
和 actions。

默认输出：

- `results/expert_skill_learning/pilot_skill_pool.json`；
- `results/expert_skill_learning/llm_calls.jsonl`。

当前 accepted Pilot 输出已冻结在：

- `evaluation_examples/expert_skill_learning/pilot/skill_pool.json`；
- `evaluation_examples/expert_skill_learning/pilot/extraction_run.json`。

最终 atomic accepted run 为 3 calls、3690 input tokens、2249 output tokens，估算
`$0.034368`。包含此前所有 prompt QC 迭代，本次开发累计估算 `$0.209436`。第一次
Structured Outputs schema 的 10 个 400 attempts 在模型推理前被拒，usage/cost 均为 0；
client 已改为不重试永久 4xx。

当前 pool 有 12 个 skills。原子性定义是“一种可独立复用、值得单独录制的 application
technique”，而不是每个 click 一个 skill。相同 technique 在同一 task 多次出现时合并并
保留非连续 action IDs；每个 action ID 最多归属一个 skill；普通 header 输入和纯确认等
scaffolding 可以不入 skill pool。冻结结果为 38 substantive actions、2 scaffolding actions、
0 duplicate assignments。

LLM 只收到原 instruction 和带零开始索引的 single steps。task ID、app 和最终 source
字段由本地代码注入；prompt 中不得新增 artifact、evaluator、grouped actions 或原 task
其他内容。默认模型 `gpt-5.6-terra`，可通过 `--model` 和 `--base-url` 切换 compatible
provider。未知模型仍记录 token usage，但 estimated cost 必须为 `null`。

当前 Chat Completions construction backend 只发送 text。`MediaInput(video, ...)` 已作为
未来接口保留，但 backend 必须明确拒绝不支持的视频，不能静默丢弃。现用 Terra、Luna、
GPT-4.1 均不能按 native video 输入处理。

后续 annotation runner 必须改变 `manual_explore.py` 目前 reset 后立即开始 recording 的
行为：先完成环境启动和 artifact 检查，第一次 Enter 开始录制，第二次 Enter 停止。Review
时视频在 annotator 本地播放；AWS 只用于可选 artifact 检查/复现，不上传或播放视频。

GitHub 暂作 Pilot remote。提交前必须检查 MP4/artifact 是否包含个人信息或凭据，并做文件
大小预检；普通 Git 失败后再决定 Git LFS/S3，不在当前代码中自动上传外部服务。

本文档是当前默认开发流程。2026-08-03 起，主线转为在原始 OSWorld task 上评测
omni-model 能否从拆分重组的专家 reference videos 中归纳高效操作技能，并让固定的
omni-agent 更准确、更高效地完成任务。已经完成的 AWS Ubuntu + PowerPoint Web W0/W1
继续保留。原
HKUST HPC + Daytona 流程保存在 `hkust_hpc developer.md`。

## 0. 当前研究方向

这是一个纯推理 benchmark，不是 agent 训练项目。本项目不进行 SFT、RL、微调、
preference optimization 或任何其他模型训练，也不更新 omni-model 或下游 agent 的
参数。被评测系统分为两个隔离阶段：

1. 完整专家轨迹按 action group/subskill 拆分，并跨轨迹重组为不含 1:1 完整解法的
   reference video bank；
2. omni-model 在 Stage 1 读取 reference videos，并通过推理生成一个冻结的 text
   playbook 或 schema-valid SkillIR；
3. 固定版本的 omni-agent 在 Stage 2 获得该冻结 skill artifact，并在原始 OSWorld task
   上执行；benchmark 对照同一 agent 的 no-reference 和其他 control 条件。

评测目标不是单独压低耗时或动作数，而是在任务成功率不下降的条件下减少：

- decision/action-group 数；
- 大模型 planning、judging 和 reflection 调用；
- 冗余 GUI action、重复 grounding 和低效恢复；
- active execution time、wall time、token 和成本。

当前开发顺序是：

```text
从原始 OSWorld 选择 3 个 pilot task 并冻结 evaluator
→ 核对 OSWorld-Human golden action/group 标注
→ 人工 replay 或自行标注 3 条完整专家轨迹
→ 按 action group 拆分并重组 R2 reference video bank
→ Qwen omni-model inference 生成并冻结 skill artifact
→ 固定 Qwen omni-agent 做 no-reference / recomposed / mismatched / golden-upper-bound
→ accuracy/efficiency uplift、Pareto 与 reference leakage 报告
```

### 0.1 数据与 benchmark 边界

`WukLab/osworld-human` 已公开 369 个 OSWorld evaluation task 的人工
`single-action` 和 `grouped-action` 解法以及 WES scorer，但没有公开真实逐帧视频、
坐标或 state-action episode。官方明确说明该仓库不应被用于训练。

本项目不建立训练集。OSWorld-Human 标注和自采轨迹只用于构造 inference-time benchmark
context、效率参考与评测。开发时必须遵守：

- 有 OSWorld-Human `single-action` / `grouped-action` 标注时，复用其操作语义、最短步骤
  和分组边界，并在 OSWorld 环境人工 replay/录制；缺失或粒度不足时自行标注；
- 未拆分的完整 expert video、完整 ordered action list、gold artifact 和 evaluator state
  不得进入 Stage 1 或 Stage 2 的模型输入；
- target 所需操作可以进入 reference bank，但必须拆散到至少两个视频，跨轨迹或上下文
  重排；任何单个视频不得给出完整解法，视频顺序不得编码 target 操作顺序；
- 每个 benchmark artifact 必须记录 OSWorld task/version、标注来源、采集者、原 trajectory、
  action group、剪辑边界、重组 seed、模型版本、prompt hash、skill hash 和生成时间；
- 人类录屏、截图和输入日志在入库前必须检查账户、邮件、文件名、剪贴板和凭据泄漏；
- PowerPoint 登录态 AMI 和 Chrome profile 仍视为 secret，不能成为 benchmark artifact。

完整 golden video 只允许作为 R0 diagnostic upper bound，不能计入主 benchmark 分数。
Stage 1 在 target episode 开始前结束。生成的 skill artifact 一经写入 manifest 就必须冻结，
同一 target/condition 的所有 seed 复用相同内容；不得在看到 target observation、执行结果或
evaluator 分数后在线改写。skill induction 的 token、latency 和 cost 与下游执行分开报告，
需要时再给出按 target 数量摊销后的成本。

### 0.2 轨迹与效率计数约定

以下概念不能混用：

- **raw action**：实际执行的一次 click/type/scroll/hotkey 等动作；
- **action group / decision step**：一次 observation/model decision 后连续执行的一组动作；
- **model call**：planner、judge、reflection、grounder 或 verifier 的一次调用；
- **observation**：实际采集并交给 policy/verifier 的屏幕或结构化状态；
- **active time**：首个 actionable observation 到最后一个 environment action；
- **wall time**：包含 setup、settle、evaluation 和 artifact finalize 的总时间。

`TrajectoryRecorder` 继续使用 `time.monotonic_ns()`；同一个 model decision 产生的动作
共享 `group_id`。固定 setup/settle 可以从 active time 排除，但必须继续出现在 manifest
和 wall time 中。不得通过删除必要等待、验证或 evaluator 来制造效率提升。

每次对照实验至少同时输出：OSWorld success/evaluator score、single/grouped WES、raw
actions、groups、observations、各类 model calls、分项 latency、active/wall time、tokens、
cost、重复/回退/恢复数量。先检查 success non-inferiority，再比较效率。

## 1. PowerPoint/AWS 工作模式（已完成并保留）

代码在本地修改和测试；GUI 集成测试运行在 AWS Ubuntu EC2 的 Chrome 中，目标应用是
PowerPoint for the web。

```text
本地小步修改和单元测试
→ Git commit/push
→ AWS 单实例 smoke
→ PowerPoint Web upload/edit/slideshow/download
→ evaluator
→ terminate 并审计残留资源
```

不要在临时 EC2 中维护唯一代码副本，不要把 Microsoft 或 AWS 凭据提交到 Git。

## 2. 当前状态

Phase W0 已完成：

- AWS profile：`osworld-dev`；
- deployment region：`us-east-1`；
- OSWorld 官方 Ubuntu 1920×1080 AMI 已存在于 `IMAGE_ID_MAP`；
- 默认目标规格：OSWorld 官方 `t3.xlarge`、30 GiB gp3（4000 IOPS /
  1000 MiB/s）、180 分钟 TTL；
- 月度预算警戒线：`USD 20`；
- Windows Server、Office LTSC、Managed AD 和 RDS SAL 路线已取消。

Phase W1 已于 2026-07-30 完成：

- manager/provider 已统一读取可验证的实例、gp3 和连接模式配置；
- reset 路径重复创建 EventBridge Scheduler 的问题已修复；
- EC2 DryRun 和实际 describe 已确认官方 AMI、`t3.xlarge` 和官方 gp3 参数；
- default subnet 和仅允许当前公网 IP `/32` 的专用 security group 已配置；
- 原 `$20/月` 账户级 Budget 的 80% actual 和 100% forecast 通知已关闭；
- 项目专属 `$20/月` Budget 配置已准备，等待 `Project` 成本分配标签激活后应用；
- TTL scheduler role 和最小 SSM diagnostic instance profile 已创建；
- 严格 W1 preflight 达到 13 pass、0 warning、0 blocked；
- SSM journal 确认官方 AMI 的 `osworld.service` 在 X11 就绪前启动，并会在
  `StartLimitBurst=4` 后永久停止；
- 私有登录态 AMI 会保留 cloud-init 状态，不能假设克隆后 UserData 必然重跑；
  manager/provider 现在在每次 launch/reset 后通过 SSM 主动安装并验证 systemd
  drop-in，等待 `DISPLAY=:0 xdpyinfo` 成功、取消 4 次启动上限，再启动
  OSWorld API；无敏感 UserData 保留为官方干净 AMI 的后备路径；
- 单实例 smoke 已验证 TTL、OSWorld API、GNOME/X11、noVNC、Chrome/CDP、
  PowerPoint Web 页面和截图；
- 2026-07-30 人工登录后的 PowerPoint Web smoke 已验证
  upload/open/edit/slideshow/record/download；
- 下载稿保留原始两段文字，并包含 `clickEffect`、`filter="fade"` 和
  `dur="500"` 的 OOXML timing 节点；
- 录屏输出为 H.264、1920×1080、30 fps；
- provider 默认创建加密 gp3 根卷，EC2 DryRun 与实际新卷均确认
  `Encrypted=true`；
- 私有登录态 AMI `ami-0c68ad8829df7c05e`
  （`osworld-ppt-web-auth-20260730`）已创建；
- backing snapshot `snap-0832dc22794c270f2` 已加密，AMI 与 snapshot
  permissions 均为空，未向公众或其他账户共享；
- 从该 AMI 启动全新实例后，PowerPoint Web 无需重新输入凭据即可恢复账户头像、
  `My presentations` 和最近文件；
- 制镜源实例、验证实例、临时 EBS 和 TTL schedules 已全部清理；
- 正式诊断 task
  `evaluation_examples/powerpoint_web/examples/powerpoint_web/`
  `5f24d8c2-4779-4f6d-9b8c-6e3bc97ed441.json` 已接入；
- evaluator 将 OOXML timing 规范化为目标对象、效果、trigger、duration 和顺序，
  并以独立 static-content gate 保证文字、颜色、版式、master 和 theme 不变；
- initial 的 static/animation 分数为 `1/0`，gold 为 `1/1`；
- SSM 修复后的当前代码完成 10 次串行 create/reset/close，readiness 为
  `98.143–186.995 s`；每轮都验证 TTL、API、GNOME/X11、drop-in 和截图，
  最终 EC2/EBS/ENI/TTL schedule 均为 0；
- W1 相关本地测试 40/40 通过。

AWS Pricing API 在 2026-07-30 返回 `t3.xlarge=$0.1664/h`、gp3
`$0.08/GB-month`、`$0.005/IOPS-month`、`$0.04/MiBps-month` 和 public IPv4
`$0.005/h`。按 730 小时/月与当前 30 GiB / 4000 IOPS / 1000 MiB/s 配置，3 小时
约 `$0.6884`，低于 `$0.80` 门槛。最终 10 次 soak 墙钟约 38 分 47 秒，估算低于
`$0.20`。
Cost Explorer 尚未入账并返回 `Estimated=true`，后续账单复核不得把估算写成实际
费用。

原 W2 evaluator v0 和 fancy demo 数据方向已暂停。近期阶段改为 `plan.md` 中的 E0
3-task pilot contract；W1 单页 Fade task 继续作为基础设施诊断 fixture，未来也可作为
expert-trajectory skill benchmark 的一个应用域，但不得作为最终 benchmark 难度代表。

私有 AMI 保存 Microsoft Cookie/令牌，必须继续保持私有和加密，不得复制到其他
账户、公开共享、写入数据集或导出 Chrome profile。Microsoft 可正常使 session
过期；过期后应在新的加密实例重新登录并替换 AMI。

## 3. 本地环境

本地只安装 AWS/provider、文档和 evaluator 开发所需的最小依赖：

```bash
cd <OSWorld 仓库目录>
conda env create -f environment.aws-dev.yml
conda activate osworld-aws-dev
./scripts/bash/install_aws_cli_v2_macos.sh
python --version
aws --version
```

环境已存在时：

```bash
conda env update -n osworld-aws-dev -f environment.aws-dev.yml --prune
```

提交前：

```bash
git status --short
git diff --check
python -m pytest <相关测试文件> -q
```

只有公共 runner/provider/evaluator 受到影响时才扩大到：

```bash
python -m pytest tests -q
```

## 4. AWS 身份与配置

优先使用 IAM Identity Center/SSO 和短期凭据：

```bash
conda activate osworld-aws-dev
aws sso login --profile osworld-dev
aws sts get-caller-identity --profile osworld-dev
```

本地部署变量：

```bash
export AWS_PROFILE=osworld-dev
export AWS_REGION=us-east-1
export AWS_SUBNET_ID=<subnet-id>
export AWS_SECURITY_GROUP_ID=<security-group-id>
export AWS_AMI_ID=<private-authenticated-ami-id>
export AWS_INSTANCE_TYPE=t3.xlarge
export AWS_CONNECTION_MODE=public
export AWS_EBS_VOLUME_SIZE_GIB=30
export AWS_EBS_IOPS=4000
export AWS_EBS_THROUGHPUT_MIBPS=1000
export AWS_EBS_ENCRYPTED=true
export AWS_EC2_INSTANCE_PROFILE_NAME=osworld-ec2-ssm-diagnostics
export ENABLE_TTL=true
export DEFAULT_TTL_MINUTES=180
export AWS_SCHEDULER_ROLE_ARN=<role-arn>
```

`AWS_AMI_ID` 未设置时继续使用官方 `IMAGE_ID_MAP`；设置后，首次创建和 reset 都使用
该私有 AMI。AMI ID 会先进行格式验证。实例和 gp3 参数共用 `launch_config.py`，
环境变量会在 AWS API 调用前完成格式和范围验证。`AWS_EBS_ENCRYPTED` 默认是
`true`，不得为包含 Microsoft 登录态的实例关闭。`AWS_CONNECTION_MODE=public`
让本地 controller 使用实例公网地址；上游在 VPC 内运行 controller 时仍可使用默认的
`private`。

不得在命令、日志或仓库中写入 access key、secret key、Microsoft 密码、cookie 或
session token。

当前本地 Conda 环境已设置：

```text
AWS_AMI_ID=ami-0c68ad8829df7c05e
AWS_EBS_ENCRYPTED=true
```

AMI ID 不是凭据，可以记录；AMI 内的浏览器 profile 才是敏感数据。删除该登录态时，
先 deregister AMI，再删除 `snap-0832dc22794c270f2`，两步都需要显式确认。

## 5. W0/W1 preflight

W0：

```bash
python scripts/python/preflight_aws_ppt_web_w0.py
python scripts/python/preflight_aws_ppt_web_w0.py --stage w0 --strict
```

W1 创建 subnet 选择和 security group 后：

```bash
python scripts/python/preflight_aws_ppt_web_w0.py --stage w1 --strict
```

该脚本不调用 AWS API，也不打印环境变量值。W1 还必须额外进行只读 AWS API 检查：

- SSO 身份和 region 正确；
- 官方 OSWorld AMI 在账户中可见；
- subnet 有公网路由；
- security group 只允许当前出口 IP `/32`；
- `t3.xlarge` 配额和容量可用；
- TTL scheduler 权限可用。
- SSM diagnostic instance profile 已配置。

当前 `PowerUserAccess` 不包含 IAM role 管理。到 IAM Identity Center：

1. 打开 `Permission sets` → `PowerUserAccess`。
2. 打开 `Permissions` → `Inline policy` → `Edit`。
3. 粘贴
   `desktop_env/providers/aws/iam/osworld-w1-control-plane-policy.json`。
4. 保存并等待 permission set 重新 provision。
5. 重新执行 `aws sso login --profile osworld-dev`。

该策略只能管理项目的 scheduler role 和
`osworld-ec2-ssm-diagnostics` role/profile，并分别只能传给 Scheduler 与 EC2；
不需要授予 `IAMFullAccess` 或 `AdministratorAccess`。

更新 permission set 后创建 SSM profile：

```bash
python -m scripts.python.setup_aws_ssm_diagnostics_role
conda env config vars set -n osworld-aws-dev \
  AWS_EC2_INSTANCE_PROFILE_NAME=osworld-ec2-ssm-diagnostics
```

实例注册到 SSM 后，先用 `AWS-RunShellScript` 只读收集：

```text
systemctl status osworld --no-pager
journalctl -u osworld -b --no-pager -n 300
ss -ltnp
```

日志不得包含 Microsoft 登录信息；诊断完成后仍由 smoke/TTL 清理实例。

## 6. Microsoft 测试账户

PowerPoint Web 长期 benchmark 应使用专用免费 Microsoft 测试账户。2026-07-30
的 W1 实机 smoke 按用户指示临时使用个人 Microsoft 账户，因此必须遵守更严格的
隔离规则：

- 不读取或操作与 benchmark 无关的 OneDrive 内容；
- 不保存私人 OneDrive、邮件、联系人或付款信息；
- OneDrive 只放当前 benchmark 临时文件；
- 每次 task 下载输出后删除云端副本；
- authenticated Chrome profile/AMI 保持私有；
- session 过期时人工重新登录，不把密码写入 setup script；
- 不将登录 profile、cookie 或 AMI 分享到公开数据集。

PowerPoint Web 自动保存到 OneDrive。Evaluator 必须使用明确下载得到的 `.pptx`，
不能把“网页显示已保存”当作 artifact 已成功回收。

## 7. 动画能力边界

首批任务允许：

- 网页端可添加的 entrance/emphasis/exit 效果；
- On Click、With Previous、After Previous；
- Duration、Delay、顺序和多效果组合；
- 网页端可编辑的 slide transition。

首批任务禁止：

- animation trigger；
- 只能在桌面 PowerPoint 中编辑的效果；
- 依赖个人账户不可用能力的 Morph；
- VBA、add-in、ActiveX；
- 要求桌面 PowerPoint 才能正确保存的媒体工作流。

若参考视频含有超出边界的效果，任务必须降级、重制或移到未来 desktop validation
集合，不能要求 Agent 完成 UI 中不存在的操作。

## 8. AWS 网络和成本

开发期复用 default VPC/public subnet，但创建项目专用 security group：

- 只允许当前开发者公网出口 IP `/32`；
- 不对 `0.0.0.0/0` 开放 SSH、VNC、5000、5910、8006、8080、8081 或 9222；
- 不创建长期 Elastic IP；
- 正常退出主动 terminate，异常退出由 180 分钟 TTL 兜底。

### 8.1 noVNC 页面无法打开或一直加载

若终端 smoke 已通过，但日常 Chrome 中 noVNC 无法打开或一直加载，先区分 AWS
白名单问题和浏览器代理对 WebSocket 的影响。

```bash
export OSWORLD_HOST=<instance-public-ip>

# 直连与默认网络路径的出口 IP；应与 security group 的 /32 一致
curl --noproxy '*' -4 -sS https://checkip.amazonaws.com
curl -4 -sS https://checkip.amazonaws.com

# HTML 正常时应返回 HTTP 200
curl --noproxy "$OSWORLD_HOST" \
  -sS -I --connect-timeout 8 --max-time 12 \
  "http://${OSWORLD_HOST}:5910/vnc.html"

# WebSocket 正常时应返回 HTTP 101 Switching Protocols 和 RFB banner
curl --noproxy "$OSWORLD_HOST" \
  -sS -i --connect-timeout 8 --max-time 12 \
  -H 'Connection: Upgrade' \
  -H 'Upgrade: websocket' \
  -H 'Sec-WebSocket-Key: SGVsbG9Xb3JsZA==' \
  -H 'Sec-WebSocket-Version: 13' \
  "http://${OSWORLD_HOST}:5910/websockify"
```

如果 HTML 为 200、WebSocket 为 101，但 Chrome 仍失败，通常是 Chrome
代理扩展、VPN 或 PAC 规则代理了 `ws://`。不要为此把 security group 改成
`0.0.0.0/0`。优先把当前实例 IP 加入代理工具的 `DIRECT`/绕过列表；macOS
也可启动不影响日常 Chrome profile 的临时直连窗口：

```bash
open -na 'Google Chrome' --args \
  --user-data-dir="/private/tmp/osworld-novnc-direct-${OSWORLD_HOST}" \
  --proxy-server='direct://' \
  --proxy-bypass-list='*' \
  --no-first-run \
  --no-default-browser-check \
  "http://${OSWORLD_HOST}:5910/vnc.html?autoconnect=true&resize=scale"
```

AWS 官方 OSWorld AMI 的 noVNC 默认密码是
`osworld-public-evaluation`。实例重建后公网 IP 会变化，必须更新
`OSWORLD_HOST` 和代理绕过规则。演示结束后关闭临时 Chrome 窗口，并立即
terminate 实例；180 分钟 TTL 只是异常兜底。

目标磁盘配置恢复为 OSWorld 仓库官方 30 GiB gp3 的 4000 IOPS /
1000 MiB/s。降配 smoke 已复现同一 API readiness 失败，后续在修复服务启动前不要
继续用不同规格反复试错。

预算参考：

- 官方 `t3.xlarge` + 官方 gp3 性能 + public IPv4：按 2026-07-30 Pricing API
  约 `$0.6884/3 小时`；
- 月度 Budget 警戒线：`$20`。

原 `osworld-ppt-web-monthly` 的 `CostFilters` 为空，实际监控整个 AWS 账户；其
actual 和 forecast 邮件通知已于 2026-07-30 删除，Budget 对象保留但不再发信。
不要重新启用这两个账户级通知。

项目专属配置由 `scripts/python/setup_aws_project_budget.py` 管理：

- Budget：`osworld-ppt-web-project-monthly`；
- 过滤条件：`Project=OSWorld-PPT-Web`；
- 金额：`$20/月`；
- 通知：actual 超过 80%，forecast 超过 100%；
- tax、support 和 subscription 不计入项目运行成本；
- 默认命令仅打印配置，不调用 AWS 写 API；
- `--apply` 会先确认 Billing 中的 `Project` 成本分配标签状态为 `Active`，否则
  安全退出。

当前 `Project` 标签尚未被 Billing 发现。它出现后，先激活再应用：

```bash
conda activate osworld-aws-dev
aws ce list-cost-allocation-tags \
  --profile osworld-dev \
  --region us-east-1 \
  --tag-keys Project
aws ce update-cost-allocation-tags-status \
  --profile osworld-dev \
  --region us-east-1 \
  --cost-allocation-tags-status TagKey=Project,Status=Active
export AWS_BUDGET_EMAIL=<notification-email>
python -m scripts.python.setup_aws_project_budget --apply
```

成本分配标签不会回填激活前的历史项目费用；项目 Budget 是告警机制，不是硬消费
上限。每次云端运行仍须依靠 terminate、TTL 和资源审计控制费用。

## 9. W1 测试顺序

所有云端测试严格按以下顺序：

1. 只读身份、AMI、subnet、security group 和配额检查。
2. provider 成本配置单元测试。
3. 从 `AWS_AMI_ID` 指向的私有加密 AMI 启动一台带 SSM profile 的实例；
   重建镜像时才从官方 Ubuntu AMI 开始。
4. 验证 OSWorld server、Chrome 和录屏。
5. 验证 PowerPoint Web session health；过期时由用户人工重新登录并轮换 AMI。
6. 上传 initial `.pptx`，打开并下载未修改副本。
7. 添加一个网页端动画，播放、录制并下载结果。
8. 运行最小 evaluator。
9. 10 次 create/reset/close soak。
10. SIGINT、超时和失败后的资源清理。

前一步失败时不得增加并发。

### 9.1 2026-07-30 登录后实机 smoke 结果

使用无敏感内容的测试稿：

```text
evaluation_examples/video_learning/fixtures/generated/impress_title_initial.pptx
```

验证结果：

1. 上传到 `/home/user/Desktop/w1_title_roundtrip.pptx` 并由 PowerPoint Web
   正常打开。
2. 页面正确显示 `Quarterly Review` 和
   `Revenue, retention, and next steps`。
3. 标题对象添加 `Fade`、`On Click`、`0.50 s` 后，Animation Pane 显示
   对象级动画条目。
4. 放映开始时标题隐藏，单击后标题出现。
5. OSWorld `/start_recording` 和 `/end_recording` 成功生成 H.264、
   1920×1080、30 fps MP4。
6. `File → Create a copy → Download a copy` 生成 32,278-byte PPTX。
7. `unzip -t` 通过；`python-pptx` 可读取 1 页和原始文字；
   `ppt/slides/slide1.xml` 包含 `clickEffect`、`animEffect filter="fade"`
   和 500 ms timing。

可重复的 artifact 回收命令：

```bash
export OSWORLD_HOST=<instance-public-ip>

curl --noproxy "$OSWORLD_HOST" \
  -X POST \
  -F 'file_path=/home/user/Downloads/w1_title_roundtrip.pptx' \
  -o /tmp/w1_title_roundtrip_downloaded.pptx \
  "http://$OSWORLD_HOST:5000/file"

unzip -t /tmp/w1_title_roundtrip_downloaded.pptx
```

该 smoke 证明编辑闭环；私有 AMI 恢复与后续 10 次 lifecycle soak 又分别验证了
session 恢复和启动/清理稳定性。

### 9.2 W1 正式 task 与验证命令

```bash
python -m scripts.python.validate_aws_ppt_web_w1_task
python -m scripts.python.soak_aws_ppt_web_w1 \
  --iterations 10 \
  --report results/w1/aws_soak_10.json
```

正式 evaluator 同时要求：

- `compare_pptx_static_content == 1.0`；
- `compare_pptx_animation_timelines == 1.0`。

任一 gate 为 0 都失败。动画比较基于语义事件，不比较易变化的 OOXML timing node
ID。soak 每轮验证 TTL、OSWorld API、GNOME/X11 和截图，最终审计
EC2/EBS/ENI/scheduler。

## 10. Runner 命令

W1 完成后的单环境命令应基于当前真实 CLI：

```bash
python scripts/python/run_multienv.py \
  --provider_name aws \
  --region "$AWS_REGION" \
  --headless \
  --observation_type screenshot \
  --max_steps 30 \
  --num_envs 1 \
  --result_dir ./results/aws_ppt_web_smoke
```

当前 `run_multienv.py` 已使用 `os_type="Ubuntu"`。具体 task 配置和 Microsoft session
setup 在 W1 smoke 完成后补充；不要提前把示例命令写成已验证状态。

## 11. 运行后清理与故障记录

每次运行确认：

- 实例已 terminated；
- 无残留 EBS、ENI、Elastic IP 或 scheduler；
- OneDrive 中的 task 临时文件已删除；
- 输出目录包含 task/run ID、AMI ID、instance type、浏览器版本、录屏、下载的
  `.pptx`、trajectory 和 evaluator 报告；
- 日志不含 AWS/Microsoft 凭据或 hidden gold。

故障至少记录：

- commit SHA、task/run ID；
- region、AMI ID、instance type；
- Chrome 和 PowerPoint Web 可见版本/时间；
- allocate/readiness/login/upload/edit/slideshow/download 阶段；
- 错误、日志路径、截图和资源清理状态；
- 最小复现命令。

## 12. 完成标准

代码变更只有同时满足以下条件才算完成：

- diff 小而可审查；
- 有对应单元测试；
- 最快相关本地检查通过；
- AWS 行为变更完成单实例 smoke；
- 生命周期变更完成 reset/异常清理验证；
- PowerPoint Web 输出被下载并通过 evaluator；
- efficiency 变化同时报告 accuracy，不以短失败轨迹冒充优化；
- OSWorld-Human scorer parity、action/group/model-call 计数有边界测试；
- benchmark 数据 provenance、fragment mapping、reference leakage 和 artifact hash 可审计；
- 代码路径中不存在模型训练步骤，Stage 1 skill artifact 在 target 执行前冻结；
- `plan.md`、本文档和实际 CLI/环境变量一致；
- 所有云端和 OneDrive 临时资源已清理。
