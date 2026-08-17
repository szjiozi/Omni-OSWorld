# OSWorld 专家轨迹技能学习 Benchmark 开发注意事项

更新日期：2026-08-05

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

C2 的旧 task-only 入口仍保留用于历史复现，但当前开发入口已经升级为 reference package：

```bash
python scripts/python/generate_reference_packages.py \
  --skill-pool \
    evaluation_examples/expert_skill_learning/pilot/skill_pool.json \
  --source-manifest \
    evaluation_examples/expert_skill_learning/pilot/source_tasks.json \
  --seed 20260805
```

sampler 对所有候选 ID 排序后再用 seeded RNG shuffle，保证不同 Python 进程结果一致；
每组 2–5 个同 app skills。模型必须把 sampled skills 全部作为主要演示要求，但允许少量
task-specific、substantive prerequisite 和重复操作来保持任务自然；它们必须单独写入
`expected_incidental_operations`，不算 coverage。输出不再只有 instruction，而是：

- outcome-oriented `task_instruction`；
- 可由 LLM/人工制作的 `artifact_spec`；
- 给 expert 参考、但不强制逐步照抄的 `operator_guide`；
- incidental operations 明细。

本地代码要求 candidate IDs 与 sampled set 完全一致且无重复；model rejection 返回 pool。
相似度同时记录 `difflib` sequence ratio 和真实 embedding cosine。semantic backend 批量调用
`text-embedding-3-small`；两个分数都只供 reviewer 参考，不能自动拒绝。

旧冻结输出 `pilot/reference_tasks.json` 与
`pilot/reference_task_generation_run.json` 保留。当前冻结输出：

- `pilot/reference_packages.json`：4 个 `pending` packages、source contribution、lexical 与
  semantic similarity；
- `pilot/reference_package_generation_run.json`：seed/model/prompt hashes/token/cost/attempts；
- `pilot/reference_package_reviews.json`：每个 package 一条预填 task ID 的 review form；
  `decision/reviewer/notes` 初始留空，空白记录按 pending 处理；
- `pilot/coverage_state.json`：由 review CLI 重算，当前 0/12 approved。

当前 package run 为 4 calls、6400 input、8485 output、估算 `$0.114620`；semantic
embedding 为 337 input tokens、`$0.00000674`，合计 `$0.11462674`。当前 12 skills 只是
candidate coverage 全覆盖，四个 packages 仍需 human review，不能写成 approved coverage。

review 文件中的空字符串只表示尚未填写；完成 review 后 decision 只能是 `approved`、
`revision_requested` 或 `rejected`。运行：

`generate_reference_packages.py` 会通过 `--reviews-output` 创建或扩展 review form，只补充
缺失的 package IDs，不覆盖已经填写的记录。

```bash
python scripts/python/review_reference_packages.py \
  --skill-pool evaluation_examples/expert_skill_learning/pilot/skill_pool.json \
  --packages evaluation_examples/expert_skill_learning/pilot/reference_packages.json \
  --reviews evaluation_examples/expert_skill_learning/pilot/reference_package_reviews.json \
  --output evaluation_examples/expert_skill_learning/pilot/coverage_state.json
```

有 unresolved skills 时 exit code 为 2，这是预期状态。只有 previous packages 全部 review 后
才允许 resume；`revision_requested` 会保留原 sampled skill set 并把 reviewer instructions
发给 LLM，`rejected` 的 exact combination 被 blocked，其他 uncovered skills 重新采样。

Reviewer 页面分三步生成，不能在 packet export 中临时调用 LLM：

```bash
python scripts/python/manage_reference_review_packets.py details
python scripts/python/generate_reference_reviewer_guides.py
python scripts/python/manage_reference_review_packets.py export
```

第一步把原完整 `TASK.md` 确定性保留为
`pilot/task_details/<reference-task-id>/TASK_DETAIL.md`；第二步只基于该 Markdown 生成结构化中文
新手参考 guide，并记录输入 SHA256、prompt/model/token/cost；第三步确定性生成精简的 user-facing
`TASK.md`，同时把 `TASK_DETAIL.md` 复制进 packet。最终页面不展示 artifact 规格、incidental
operations 或 annotation command，但保留 initial preview、完整 required skill provenance、原
operator guide、中文 guide、完整 source single actions 与明确 review checklist。guide 与 detail
SHA256 不一致时 export/collect 必须 fail closed。

当前 4 份 frozen reviewer guides 已使用 `gpt-5.6-terra` 生成，合计 12374 input、7606 output
tokens，估算 `$0.116020`。输出在 `pilot/reviewer_guides.json`，逐 attempt 日志在
`results/expert_skill_learning/reviewer_guide_llm_calls.jsonl`。第一次真实 API 尝试因 strict
Structured Outputs 的 `language.const` 缺少显式 string type 在推理前返回 400；schema 修正后
四次 generation 全部成功。

C4a artifact generation 入口：

```bash
python scripts/python/generate_reference_artifacts.py \
  --packages evaluation_examples/expert_skill_learning/pilot/reference_packages.json \
  --build-output-dir results/expert_skill_learning/artifacts \
  --node <bundled-node> \
  --node-modules <directory-containing-@oai/artifact-tool>
```

LLM 只生成 strict Calc blueprint；builder 负责真实 XLSX、number formats、必要 AutoFilter、
列宽/冻结表头、逐 sheet PNG、formula error scan 和 manifest SHA256。native Pivot Table 不会
预建，因为当前四个任务都要求 expert 在录制中创建。已冻结的 blueprint 可零 API 成本重建：

```bash
python scripts/python/generate_reference_artifacts.py \
  --blueprints-input \
    evaluation_examples/expert_skill_learning/pilot/artifact_blueprints.json \
  --build-output-dir evaluation_examples/expert_skill_learning/pilot/artifacts \
  --node <bundled-node> \
  --node-modules <directory-containing-@oai/artifact-tool>
```

最终 frozen artifact run 为 4 calls、9167/3447 tokens、`$0.059698`。四个 workbooks 均
`manual_setup_required=false`，公式错误扫描为 0。此前为完善 number-format/AutoFilter
contract 做过一次 4-call artifact iteration，成本 `$0.059986`；不要把它误算为 frozen run。
LLM 首次把 Enrollment Log 生成成 9 个 Review rows，developer QC 改为 spec 要求的 8 个；
调整记录在 `pilot/artifact_blueprints.json` 的 `developer_qc_adjustments`。

LLM 只收到原 instruction 和带零开始索引的 single steps。task ID、app 和最终 source
字段由本地代码注入；prompt 中不得新增 artifact、evaluator、grouped actions 或原 task
其他内容。默认模型 `gpt-5.6-terra`，可通过 `--model` 和 `--base-url` 切换 compatible
provider。未知模型仍记录 token usage，但 estimated cost 必须为 `null`。

当前 Chat Completions construction backend 只发送 text。`MediaInput(video, ...)` 已作为
未来接口保留，但 backend 必须明确拒绝不支持的视频，不能静默丢弃。现用 Terra、Luna、
GPT-4.1 均不能按 native video 输入处理。

C4b/C5 已新增：

```bash
# LLM 生成 constrained setup blueprint，再由本地代码注入可信 actions
conda run -n osworld-aws-dev python \
  scripts/python/generate_reference_task_configs.py

# 已有 frozen blueprint 时零 API 成本重建 configs
conda run -n osworld-aws-dev python \
  scripts/python/generate_reference_task_configs.py \
  --blueprints-input \
    evaluation_examples/expert_skill_learning/pilot/annotation_setup_blueprints.json

# 正式标注；pending 工程 smoke 额外添加 --allow-pending
python scripts/python/record_reference_task.py \
  --reference-task-id reference-task-r01-001
```

LLM blueprint 不包含 host path、SHA256 或任意 command。本地 assembler 校验 artifact hash，
只注入 `upload_file → open`，config 不含 evaluator。当前 frozen run 为 4 calls、6712/678
tokens、`$0.021560`。

Runner 不改变通用 `manual_explore.py` 的行为，而是复用其 observation、xinput 和 screenshot
helpers：reset/upload/open 完成后等待第一次 Enter 才开始 MP4/input，第二次 Enter 立即停止，
随后 `Ctrl+S`、回收最终 XLSX、写 bundle，并在 `finally` 调用 `env.close()`。Reference
annotation 的 `--sample-interval` 默认是 `0`，不启动周期 PNG sampler；initial、recording-start、
final 三张关键截图仍保留。只有工程诊断显式传正数才启用周期截图，通用 OSWorld 实验配置不变。

Reference annotation 不再调用 AMI 内官方 `/start_recording`。2026-08-12 发现官方 server 将
FFmpeg stderr 接到 `subprocess.PIPE` 却不在录制期间读取，约 278–283 秒后 pipe 填满并阻塞，
导致 task 3 的 355.4 秒窗口只录到 277.8 秒。专用 guest recorder 现在使用
`libx264 -preset ultrafast -crf 23`，把 warning stderr 写到
`recording_capture.ffmpeg.log`；第二次 Enter 后先停止视频，再回收 XInput。Raw MP4 duration
必须与 guest monotonic start/stop 相差不超过 5 秒，否则 fail closed。该修复不修改通用
OSWorld server 或正式实验录制设定。
正式运行只接受 approved package；pending 仅能用 `--allow-pending`，revision/rejected 不能
绕过。Guide 显示在本地终端，不进入 noVNC 录制画面；cross-validator 本地看 MP4。

默认 input overlay 从同一份 timestamped XI2 日志生成：快捷键和特殊键写入
`key_events.jsonl`；左键、双击、右键和滚轮写入 `pointer_events.jsonl`。鼠标提示显示在实际
坐标附近；按下/释放位移超过 10 px 视为拖拽，不显示额外提示。`input_timing.json` 保存 guest
monotonic 时间轴。FFmpeg process start 只能作为 provisional 起点；停止后必须以
`video_stop_monotonic_ns - actual_mp4_duration` 计算第一帧的 calibrated 起点，再将输入事件
对齐到视频 PTS。`key_overlay.ass` 由 guest ffmpeg burn-in 为正式 `recording.mp4`，无提示的
`recording_raw.mp4` 永久保留。

2026-08-18 对 Portal run `1ce7dffe47cb4df79d7bbe6c3e89af24` 的诊断发现：guest 窗口为
112.925 秒，但 MP4 为 111.000 秒；旧实现因此把全部 overlay 延后 1925.202 ms。旧 direct-noVNC
样本也有同类 303–324 ms 偏移，只是不明显。共享 recorder 现统一执行 stop-minus-duration
校准；`input_timing.json` 和 manifest 的 `recording_timeline` 必须保留 provisional/calibrated
起点、stop time、correction ms 和 method，不能再直接用 `/proc` process start 生成 overlay。
修复后 75 项 annotation/recording 回归测试通过，真实样本中的 `Ctrl+A` 从 109.275 秒校准为
107.350 秒；gateway source bundle `375eedb4965b...` 已部署，CloudFront `/healthz` 返回 200。

该 bundle 部署后的首次 relaunch 返回 500：workspace admission 的 transaction 包含
`ConditionCheck` maintenance gate，但 gateway role 只有 `TransactWriteItems`，缺少独立的
`dynamodb:ConditionCheckItem` 权限。DynamoDB 明确返回 `AccessDeniedException`，因此没有创建
workspace、lock 或 worker。Gateway IAM policy 必须同时保留这两个 action；权限缺失时 store
应返回可读的 portal administration error，不能再把原始 ClientError 暴露为无说明的 500。
修复后 76 项相关测试通过，source bundle `b3ad0003a18d...` 部署成功。Portal launch 返回 200，
workspace `5e39b69c4b644f2c867e42803c55cae9` 创建 worker `i-05bc936b519f2c274` 并进入 `ready`。

同一 workspace 首次 stop 时又暴露了两个独立问题。Portal 的 `renderWorkspace()` 在
ready → recording 时重写整个 `innerHTML`，销毁已认证的 noVNC iframe，迫使 annotator 再次连接
并输入 VNC 密码；状态轮询还会再重写一次。现在同一 session 且仍为 ready/recording 时只原地
更新 status/message/buttons，必须保留原 iframe browsing context。

该 run 的 provisional process start 为 433.600 秒，MP4 为 78.334 秒，而 stop window 为
85.799 秒；第一帧启动空档 7.465 秒被旧完整性 gate 误判为截断。首个实际 click 在 446.984 秒，
晚于估算第一帧约 5.9 秒，因此这次没有丢 substantive 操作，但 failed bundle 不可作为正式结果。
Guest recorder 现在通过 FFmpeg `-progress` 等待 `frame > 0`，写入
`first_frame_monotonic_ns` 后 Start API 才返回；`guest_recording_start_monotonic_ns()` 读取该 marker，
不再扫描 `/proc/<pid>/stat`。duration integrity 和 post-hoc stop-minus-duration residual 校准继续
保留，用真实第一帧起点即可区分 encoder startup 与录制中途截断。
修复后 79 项回归测试与 Node syntax check 通过，source bundle `b6b3010a0a68...` 已部署；
CloudFront `app.js` 已确认包含 iframe-preserving 分支。新 workspace
`11a0857bdae646279f26230db8897348` 创建 worker `i-0d28821dc73739e37` 并进入 `ready`。

Portal workspace 控制补充三个明确入口：ready/recording 的 noVNC iframe 可用浏览器 Fullscreen
API 原地全屏；仅 `ready` 可以执行 `Close without submitting`，同步终止 worker 后转为
`terminated` 并释放 user/task/global locks；`failed`、`expired`、`terminated` 页面可以按原 task
发起全新 workspace。不要把 retry 实现成复用旧 DesktopEnv。Pilot 暂不允许取消
`provisioning`，因为尚未取得 concrete instance/runtime 时直接释放 lock 可能留下 orphan EC2；如需
支持必须先在 controller 增加可持久化、幂等的 cancellation/reconciliation。
上述 workspace controls 加入后，Portal/infra/recording 共 83 项回归测试及 Node syntax check
通过。2026-08-18 部署前检查发现 active count 为 1、worker `i-093f715ded4956dc1` 仍在运行，
因此最初未重启 gateway。用户确认该环境只用于探索后，管理员安全终止 session
`111fe17aff4745fa850344d0e234b1b7`：worker 转为 `terminated`、对应 TTL schedule 删除，Portal
事务释放 locks 并把 active count 归零。随后 source bundle `562c8192e271...` 已部署；CloudFront
`/healthz` 返回 ok，线上 `app.js` 已确认包含 Fullscreen、Close without submitting 和 Retry
workspace，部署后 active count 仍为 0。

Portal task card 的任务说明必须只渲染当前 immutable pilot snapshot 中的 review packet
`TASK.md`；不要再在前端额外拼接 `reference_packages.json` 的 instruction、operator guide 或
skill list，避免 human-edited TASK 与生成期字段出现两个版本。Fullscreen 必须请求包住 iframe
的 `.desktop-shell`，并在该容器内显示 `Exit fullscreen`；直接让 iframe fullscreen 会使父页面
按钮不可见，用户只能依赖不明显的浏览器 Escape 行为。
该调整通过 43 项 Portal/publisher/review-packet 回归测试，source bundle
`b2738c5a6f08...` 已部署。随后使用 batch publisher 原子切换到 catalog
`00320cb6e158733d48dbf9c91d09fad1b3c893f7b82b3bacf10ad90a5339364f`，包含 4 个任务和
4 条 assignment，gateway 未重启。SSM 核验 `live-pilot` 已指向该 snapshot，四份远端
`TASK.md` SHA256 与本地逐一一致；CloudFront source 已包含 `Task instructions (TASK.md)`、
`Exit fullscreen` 与 `document.exitFullscreen`，且不再包含旧 quick-guide label。

AWS runner 固定 `osworld-dev`，默认 annotation region 由
`AWS_ANNOTATION_REGION` 决定，当前主路径为香港 `ap-east-1`。香港官方公共 AMI ID 已失效，
因此 `AWS_AP_EAST_1_AMI_ID` 指向从 `us-east-1` 官方干净 AMI 跨区复制的私有加密副本；
`AWS_AP_EAST_1_SUBNET_ID/AWS_AP_EAST_1_SECURITY_GROUP_ID` 也必须是香港资源。显式传入
`--aws-region us-east-1` 时仍回退原有通用 subnet/SG 和官方公共 AMI。解析器禁止把通用
美国资源静默用于香港。

所有实例继续标记为 `Project=OSWorld-Expert-Skill-Learning`。香港默认使用 SSM+SSH：SSM
只承载一条到 guest SSH 的连接，SSH 在其上复用本地动态 API/noVNC 端口；因此不查询
`checkip.amazonaws.com`，也不更新 5000/5910 公网 ingress。一次性 Ed25519 公钥通过
`AWS-RunShellScript` 注入临时实例，私钥只保存在本机 temporary directory，runner 退出时
清理。美国 public fallback 才把专用 SG 的 5000/5910 规则更新为当前出口 `/32`；两种模式
都不能传共享 security group。完整 annotator 操作见
`evaluation_examples/expert_skill_learning/annotator.md`。香港 private AMI 对应的 EBS
snapshot 是持续计费资源；当前标准 snapshot 单价为 `$0.055/GB-month`，删除前应保留在项目
成本审计中。

2026-08-12 的香港交互诊断确认：guest 内 noVNC HTML 约 `0.01s`、screenshot 约 `0.13s`，
实例 load average 约 `0.14`；本地经 SSM 仅约 `6.6 KiB/s`，公网 443 SSH 也只有约
`12–15 KiB/s`。瓶颈是当前大陆 ISP 到 AWS 香港 EC2 的线路，不是 CPU、内存、noVNC、代理或
实例规格。当前标注按用户决定继续使用香港，未来 migration next step 见 `plan.md` 的
Alibaba Cloud Shenzhen deferred smoke。

同次诊断发现 EventBridge TTL schedule 虽在正确 UTC 时间创建并保持 `ENABLED`，却未执行
terminate；当前 SSO PowerUser 无权读取/修复 execution role inline policy。Runner 因此在
SSM Online 后额外 arm guest systemd poweroff backstop；EC2 launch config 的
`InstanceInitiatedShutdownBehavior=terminate` 会把该 poweroff 转为实例终止。Scheduler 仍保留
为第一层保护，guest timer 为第二层，`finally env.close()` 为正常退出路径。后续获得 IAM
权限后必须审核 `osworld-scheduler-ec2-terminate-inline`，不能把“schedule 已创建”视为已验证。

阿里云迁移目前仅记录、不实施。代码库已有 `desktop_env/providers/aliyun`，但正式复用前必须
处理 `ALIYUN_USE_PRIVATE_IP=0`、x86 QCOW2 导入、专用 `/32` SG、SSH tunnel、AWS-only runner、
镜像 provenance、终态资源审计与异常回收；目标 region 为 `cn-shenzhen`，先做单实例延迟
A/B smoke，再决定是否迁移 annotation pipeline。

本地 reference annotation 相关测试和 2026-08-11 付费单实例 AWS smoke 均已通过。该 smoke
使用 pending `reference-task-r01-001 --allow-pending`，run ID 为 `20260811T130617Z`；
正式 `recording.mp4` 和 raw MP4、11 个隐私过滤后的按键事件、最终 XLSX 与 completed manifest
均已回收。抽取 `Ctrl+A` 时间点的帧确认 overlay 实际烧录在视频底部中央；普通文字未进入
`key_events.jsonl`。结束后 EC2 为 `terminated`，EBS、ENI 和 TTL schedule 均无残留。

这次从 OSWorld HTTP API 回传约 5.8 MiB raw MP4 和 6.3 MiB overlay MP4 明显偏慢，但 TCP
持续前进且结果完整。正式批量标注前应把大文件回收改成可观测的 streaming download，避免
长时间无终端输出被误判为死锁；在此之前不要因等待而手动终止仍有接收字节增长的 runner。

GitHub 暂作 Pilot remote。提交前必须检查 MP4/artifact 是否包含个人信息或凭据，并做文件
大小预检；普通 Git 失败后再决定 Git LFS/S3，不在当前代码中自动上传外部服务。

### Multi-annotator Annotation Portal（2026-08-17）

四位协作者的主入口改为 Annotation Portal；单人 terminal runner 保留。门户代码位于
`benchmark_construction/annotation_portal/`，启动入口为
`scripts/python/run_annotation_portal.py`。本地模式必须显式指定 `--mode local` 和一个未跟踪
的 credentials JSON；AWS 模式必须显式指定 `--mode aws`，缺少任一 Cognito、DynamoDB、S3
或 worker network 配置都会 fail closed。

状态机固定为：

```text
assigned → provisioning → ready → recording → finalizing → uploading → submitted
                                 ↘ failed / expired / terminated
                                                                         ↕
                                                                   discarded → deleted
```

`MemoryPortalStore` 只用于本地测试。生产使用 single-table `DynamoPortalStore`：创建 workspace
时在同一个 `TransactWriteItems` 中写 workspace、user lock、task lock 并递增 global active
counter；因此同一 annotator、同一 task 只能各有一个 active workspace，总数最多 4。活动态
退出时在事务中释放两把锁并递减 counter。`WorkspaceJanitor` 对 ready-idle 45 分钟和全部活动
workspace 180 分钟 hard TTL 执行清理；worker 本身仍应保留独立的 termination backstop，不能
只依赖 gateway 进程。

Cognito User Pool 关闭 self-registration。管理员通过
`scripts/python/create_annotation_portal_users.py` 创建固定账户；脚本用 `MessageAction=SUPPRESS`
生成一次性临时密码，只写到用户指定的本地 `0600` 文件，不在 stdout、Git 或日志展示密码。
首次登录的 `NEW_PASSWORD_REQUIRED` Cognito session 留在 gateway 内存，浏览器只收到短期 opaque
challenge ID；正式 portal cookie 同样是 opaque random token，DynamoDB 只存 SHA256，cookie
使用 `HttpOnly + Secure + SameSite=Lax`，不把 Cognito token 放进 localStorage。

noVNC 的 HTML/JS 和 WebSocket 都通过已认证的 gateway 路由：

```text
/api/workspaces/<session>/vnc/<asset>
/api/workspaces/<session>/vnc/websockify
```

每次请求都校验 session owner/admin，然后 gateway 通过 worker private IP 的 5910 连接；HTTP
client 显式 `trust_env=False`，不会再次受本机/实例 proxy 影响。worker SG 的 5000/5910 只接受
gateway SG，不对 annotator 公网开放。CloudFront 必须转发所有 cookies、query strings 和除
Host 外的 viewer headers，尤其是 `Sec-WebSocket-*`；缓存策略使用 CachingDisabled。预览继续
固定 `quality=0&compression=9&resize=scale`，不改变 guest 1920×1080 录制清晰度。

生产入口使用 CloudFront 默认 `*.cloudfront.net` HTTPS，不要求自有域名。IaC 为
`infra/annotation_portal/template.yaml`：gateway EC2 位于 private subnet，并以 CloudFront VPC
Origin 作为唯一入口，不创建 ALB/NLB。CloudFront VPC Origin 官方要求 private subnet；香港默认
VPC 原本只有 public subnets，因此模板会创建一个自动选择且不与现有 subnet 重叠的 private
`/24`，并使用 public subnet 中的 `t4g.nano` NAT instance 出站。不要把 gateway 改回 public
subnet，也不要为了省事换成约 USD 0.045/hour 的 managed NAT Gateway。

gateway 使用 Canonical Ubuntu 24.04 `t3.micro`，启动时建立 2 GiB swap，并从 stack 的 private
S3 bucket 下载 content-addressed source tarball、校验 SHA256、建立 `.venv` 后启动 systemd。
`scripts/python/deploy_annotation_portal.py` 先创建无 compute 的 control plane，再上传 deterministic
bundle，最后启用 NAT/gateway/CloudFront；bundle 包含完整 `benchmark_construction` Python package、
portal 所需的最小 AWS DesktopEnv 路径、pilot configs/artifacts 和 requirements，不包含 `.git`、
results、`secret_keys.sh` 或 credentials。重复部署时 bundle 使用 content hash key，CloudFormation
稳定后通过 SSM 下载、校验并原地刷新 gateway service；annotation S3 bucket 继续保留。gateway
role 保留最小 SSM agent channel 权限，便于诊断 private instance，不开放 SSH 或公网 IP。

当前香港按需成本基线约 USD 24/month：`t3.micro` gateway、`t4g.nano` NAT、1 个 public IPv4 和
48 GiB gp3。每个 live `t3.xlarge` worker 约 USD 0.24/hour 加少量 IPv4/gp3，hard TTL 180 分钟。
portal 显式设置 `AWS_EBS_IOPS=3000`、`AWS_EBS_THROUGHPUT_MIBPS=125`，不得继承通用 runner 的
4000/1000 高性能默认值造成额外存储费用。实际创建这些持续计费资源必须再次获得用户明确授权。

Portal 的 AWS controller 直接持有每个 live `DesktopEnv`，网页按钮分别调用 start/stop API，
不使用 PTY 或向旧 CLI 伪造 Enter。reference annotation 仍禁用周期截图，并复用现有 XInput、
guest FFmpeg、duration integrity、key/pointer overlay、最终 XLSX 和 manifest 逻辑。AWS manager
仅在主线程安装 SIGINT/SIGTERM handler，使最多四个后台 provisioning thread 可以并发分配实例；
原单人 CLI 的信号清理行为不变。

停止录制后先在 gateway 本地完成 bundle。`S3BundlePublisher` 对每个文件计算 SHA256，上传时写
object metadata，并用 `HeadObject` 核对；所有文件成功后最后写
`reference-annotations/<user>/<task>/<run>/COMPLETE.json`。上传或校验失败时不写 complete marker、
不删除本地 bundle，但仍请求终止 worker，避免为重试上传继续支付 EC2 费用。

2026-08-17 的 portal operations v2 已实现并部署：task card 会安全渲染完整 `TASK.md`，packet
内相对图片/附件通过 owner-checked API 提供，绝对、带 scheme 或 `..` 链接会被禁用；停止后页面
按 capture、raw collection、overlay render、artifact、manifest、S3 verify、worker termination
显示真实阶段，不伪造百分比。`WorkspaceSession` 在 launch 时冻结 `catalog_version` 和不可变
`task_config_path`，因此动态批次切换不会改变已启动任务。

提交历史从 DynamoDB workspace 记录读取。`recording.mp4` 预览必须走 owner-checked 的同源
`/api/submissions/<session>/video`；gateway 将浏览器 `Range` 转发给 private S3，并以 200/206、
`Content-Length`、`Content-Range`、`Accept-Ranges` 流式返回。不要再把 presigned regional S3 URL
放进 `<video>`：大陆/代理网络可能能访问 CloudFront Portal 却不能访问第二个 S3 域名。网关还
必须对 `recording.mp4` 强制返回 `Content-Type: video/mp4`，不能信任历史 S3 对象的
`binary/octet-stream` 元数据；新上传 bundle 同时按扩展名写入正确 MIME 类型。
可将整次 run 标成 `discarded` 并在 7 天内恢复。后台 janitor 到期后删除该精确 S3 prefix
的全部 object versions，再置为 `deleted`。不要用 S3 `Expiration Days=7` 代替：它按 object
创建时间而不是 discard 时间计算，无法保证七天恢复窗口。gateway role 因此需要
`Get/PutObjectTagging`、`DeleteObjectVersion` 和 `ListBucketVersions`。

新增任务使用 `scripts/python/publish_annotation_batch.py`，不得运行 full deploy：publisher 把
完整 pilot 打成 content-addressed immutable snapshot，经 SSM 安装到
`/opt/osworld/published-pilots/<hash>/pilot`，校验后用 `ln -sfnT` 原子切换 `live-pilot`，再 upsert
assignments；portal 的 `ReloadingTaskCatalog` 按 symlink target 热加载，不重启 systemd。完整代码
部署则原子取得 Dynamo maintenance lock：同一事务要求 active count 为 0，lock 存在时新的
workspace admission fail closed；30 分钟 TTL 防止部署进程异常退出后永久锁死。

结果回收使用 `scripts/python/download_annotation_results.py`。它只下载存在 `COMPLETE.json` 的
run，默认跳过 discarded，检查 manifest 路径边界，并在 size/SHA256 全部通过后原子 rename；
不要用未经校验的 `aws s3 sync` 作为正式 benchmark ingestion。

operations v2 首次部署尝试在任何资源变更前失败：DynamoDB 将 `ttl` 识别为 condition expression
保留字。maintenance-lock 的 Put 和 workspace admission ConditionCheck 现在统一使用
`ExpressionAttributeNames={"#ttl": "ttl"}` 与 `#ttl < :now`；对应回归测试必须保留。修复后 source
bundle `52431107632c...` 部署成功。线上复核为 CloudFront health 200、未认证 tasks 401、systemd
active、`live-pilot` 4 个 `TASK.md`、maintenance lock released、active workspace 0、live
`Role=AnnotationWorker` 0。额外一次 SSM Python 诊断因本地构造的嵌套 shell quoting 丢失路径引号
而失败，但同一 invocation 已先输出 systemd active 和正确 symlink；随后无嵌套引号的 packet
检查成功，不能把这类诊断命令语法错误误判为 portal 服务故障。

四人默认 assignment 文件示例在
`evaluation_examples/expert_skill_learning/annotation_portal/assignments.example.json`。当前四个
packages 都是 pending，所以正式 portal 默认显示 0 个任务；工程 smoke 必须显式
`--allow-pending`。部署/付费 smoke 前先运行：

```bash
PYTHONPATH=. conda run -n osworld-aws-dev pytest -q \
  tests/test_annotation_portal.py \
  tests/test_annotation_portal_infra.py \
  tests/test_aws_launch_config.py \
  tests/test_reference_recording.py \
  tests/test_reference_annotation.py
```

CloudFront VPC Origin 以及 WebSocket 的约束以 AWS 官方文档为准：香港 region 已支持 VPC
origin，且 CloudFront 支持 RFC 6455 WebSocket；变更模板时不得退回 public gateway/worker
端口方案。

2026-08-17 已完成真实部署：stack `osworld-annotation-portal` 为 `UPDATE_COMPLETE`，入口为
`https://d3iwl4nu2200t4.cloudfront.net/`。公网 `/healthz` 返回 200，首页返回 200，未认证
`/api/tasks` 返回 401；四个 Cognito 用户均 enabled 且处于首次改密状态，active annotation
worker 为 0。CloudFront VPC Origin 创建后必须允许 AWS service-managed
`CloudFront-VPCOrigins-Service-SG` 到 gateway 8080；部署脚本会自动补该规则。

首次验收的 504 根因不是 CloudFront 或 proxy，而是精简 source bundle 缺少
`benchmark_construction/models.py`：Python 加载 package `__init__.py` 时即退出，gateway 8080
因此未监听。SSM `systemctl status`/`journalctl` 定位后，bundle 改为包含完整 package，并新增
bundle 内容测试和 SSM 原地刷新。遇到同类 504 时依次检查 CloudFront/VPC Origin 状态、gateway
SG service-managed source、EC2 status、SSM journal 和实例内 `curl 127.0.0.1:8080/healthz`；不要
通过开放公网端口来绕过诊断。

同日首个真实 worker smoke 到达 `ready` 后，noVNC 静态资源均为 200，但 WebSocket 403。gateway
journal 显示浏览器请求被重复拼成
`/api/.../vnc/api/.../vnc/websockify`；原因是前端传给 noVNC 的 `path` 没有前导 `/`，浏览器按
iframe 当前目录解析成相对 WebSocket URL。`app.js` 现固定传
`/api/workspaces/<session>/vnc/websockify` 的绝对 path，并有回归测试。诊断时若 HTML/JS 200 但
noVNC 显示 `Failed to connect to server`，先看 gateway journal 中实际 WebSocket path；出现重复
`/vnc/api/` 时不是本机 proxy、worker readiness 或 security group 问题。活动 workspace 期间只
热更新静态文件，不重启 portal service，否则会丢失 gateway 进程内持有的 DesktopEnv runtime。

修复 WebSocket 后，`annotator-hk-1` 于 2026-08-17 完成首个真实 portal annotation，session
`1ce7dffe47cb4df79d7bbe6c3e89af24`。后台成功生成 overlay MP4、raw MP4、最终 XLSX、输入事件、
截图和 manifest，共 20 个 S3 objects，最后写入 `COMPLETE.json`；worker 于提交后 terminate，
对应 TTL schedule、EBS 和 ENI 均为 0。页面一度看似卡住不是 finalization 失败：后端已异步处理
且浏览器每 2 秒读到了 `submitted`，但前端 terminal branch 只停止 polling，没有清除 completed
workspace 或重新启用任务卡。现在 `submitted` 会显示明确成功消息并执行 dashboard refresh；不要
因旧页面未复位而重复录制，先核对 DynamoDB status、S3 complete marker 和 EC2 终态。

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

香港主路径必须使用 runner 输出的
`http://127.0.0.1:<dynamic-port>/vnc.html`。不要单独运行
`AWS-StartPortForwardingSession` 把本机端口直接映射到 guest 5910：2026-08-11 smoke 中，
HTML 和 WebSocket 在实例内均正常，但 Chrome 的多个并发连接会占住该原生 SSM forward，
页面持续 loading。当前 runner 使用 SSM 转发 guest 22，再由一条 SSH 连接复用 5000/5910；
实测本地 HTML 返回 200、WebSocket 返回 101。

香港故障先检查 runner、Session Manager plugin 与 SSH 三层进程，以及 localhost URL：

```bash
ps -ax -o pid,ppid,stat,command | \
  rg 'record_reference_task|session-manager-plugin|ssh -N'
lsof -nP -iTCP:<dynamic-port>
curl --noproxy '*' -sS -I --connect-timeout 8 --max-time 12 \
  'http://127.0.0.1:<dynamic-port>/vnc.html'
```

不要把 localhost URL 改成实例公网 IP，也不要为此开放公网 SSH/5910。若要绕过日常 Chrome
profile 的代理扩展，可用 runner URL 启动临时直连窗口。

Runner 现在优先固定本地 API/noVNC 为 `15000/15910`，端口冲突时才使用 ephemeral ports，
以便浏览器缓存跨实例复用同一 localhost origin。链接交付前的 readiness 不再只检查 listener：
必须依次取得 noVNC HTML 200、WebSocket 101 和 `RFB 003.008` banner。香港链路实测首次完整
加载仍可能需要 10–30 秒；通过 readiness 后持续 loading 应先等待首帧，不要反复刷新或同时
打开多个 profile。Runner URL 固定附加
`autoconnect=true&resize=scale&quality=0&compression=9`，只降低 noVNC JPEG 交互预览带宽；
guest geometry 和正式录屏仍保持 OSWorld 要求的 1920×1080。不要通过 `xrandr` 降低 guest
分辨率，也不要在 noVNC 设置面板中把 quality 调回默认 6。公网 5910 从当前大陆出口实测
timeout，不是可靠 fallback。

以下公网 IP/白名单/WebSocket 流程仅适用于显式的美国 public fallback。若终端 smoke 已
通过，但日常 Chrome 中 noVNC 无法打开或一直加载，先区分 AWS 白名单问题和浏览器代理对
WebSocket 的影响。

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
