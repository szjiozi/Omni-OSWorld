# OSWorld 专家轨迹技能学习 Benchmark 与历史项目 Handoff

## 2026-08-12 香港标注与 Deferred Aliyun 迁移

用户决定当前 reference annotation 继续使用 AWS 香港 `ap-east-1`。交互性能诊断证明 guest
内部服务健康，但当前大陆 ISP 到香港 EC2 线路只有约 `6.6 KiB/s`（SSM）或
`12–15 KiB/s`（公网 443 SSH）；关闭代理或升级实例不能解决。阿里云迁移已作为 deferred
下一步写入 `plan.md`：目标 `cn-shenzhen`、x86 4 vCPU/16 GiB、10 Mbps 按流量，先跑最小
A/B smoke，确认亚秒级交互后再扩展现有 Aliyun provider 和 AWS-only annotation runner。

同日发现一台香港 smoke instance 超过 180 分钟仍运行：EventBridge schedule 时间正确但执行
失败，当前 PowerUser 无权检查 execution role inline policy。遗留实例、schedule、手工隧道和
临时 443 ingress 已清理。Runner 新增 guest systemd 180 分钟 poweroff backstop；由于实例启动
行为为 terminate，它与 Scheduler、`finally env.close()` 共同构成三层回收。后续仍需用更高
IAM 权限审核 `osworld-scheduler-ec2-terminate` 实际 policy。

noVNC recurrent-loading 根因也已固化：SSM+SSH 功能正常，但香港跨境链路首次静态资源和首帧
需要约 10–30 秒，公网 5910 则直接 timeout。Runner 下次优先固定 localhost `15000/15910`
以复用浏览器缓存，并在交付链接前硬性验证 HTML 200、WebSocket 101 与 RFB banner；不再用
“端口已监听”作为成功条件。Runner URL 还固定附加
`autoconnect=true&resize=scale&quality=0&compression=9`，只降低 noVNC 交互预览的带宽；
guest geometry 与正式 MP4 仍保持 OSWorld 要求的 1920×1080，不能通过降低 guest 分辨率
换取速度。2026-08-12 的 task 1 mouse-overlay smoke 已完成并终止实例。

## 2026-08-05 C4b Setup Config 与 C5 AWS Annotation Runner

C4b 已完成。`generate_reference_task_configs.py` 让 construction LLM 只生成受 schema 约束的
setup blueprint；可信本地 assembler 再校验 initial XLSX SHA256，注入固定
`upload_file → open` actions。LLM 不接触 host path/hash，也不能生成 shell command、下载、
额外文件或 evaluator。冻结输出为 `pilot/annotation_setup_blueprints.json`、
`pilot/task_configs/*.json` 和 `pilot/task_config_manifest.json`。最终 4 calls 使用 6712/678
input/output tokens，估算 `$0.021560`。四个 config 均无 evaluator。

C5 runner `record_reference_task.py` 已实现 approved-only gate，并保留 `--allow-pending` 供
工程 smoke；revision/rejected 不能绕过。它固定使用 `osworld-dev`，默认
annotation region 已切换为香港 `ap-east-1`。由于官方香港公共 AMI 已失效，香港使用从
`us-east-1` 官方干净 AMI 复制得到的私有加密副本，并通过 `AWS_AP_EAST_1_*` 隔离 subnet、
security group 和 AMI；`--aws-region us-east-1` 保留为 fallback。香港默认通过 SSM 注入
一次性 SSH 公钥，以单 SSH 连接复用本地动态 API/noVNC 端口，不依赖公网 ingress 或本机代理；
美国 public fallback 才把专用 SG 的 5000/5910 ingress 更新为当前 IPv4 `/32`。Artifact
打开后第一次 Enter 才启动 timestamped
XInput/MP4，第二次 Enter 停止。Reference annotation 默认关闭周期 PNG 截图以免占满与 noVNC
共享的 SSM+SSH 隧道，但仍保留 initial/start/final 三张关键截图；通用 OSWorld 实验与
`manual_explore.py` 保持原设定。默认会把快捷键和特殊键规范化到
`key_events.jsonl`，把左键、双击、右键和滚轮规范化到 `pointer_events.jsonl`；拖拽不显示
额外提示。`input_timing.json` 保存视频/XInput monotonic 对齐点，`key_overlay.ass` 使用 guest
ffmpeg burn-in 为正式 `recording.mp4`，同时保留无提示的 `recording_raw.mp4`；普通文字输入
不会逐键显示。随后 runner 保存并回收 final XLSX、写完整 bundle，并在 `finally`
terminate。Operator guide
只显示在本地终端。`--no-key-overlay` 仅供工程调试；正式录制对 capture/burn-in fail closed。

2026-08-12 发现官方 `/start_recording` 的 FFmpeg stderr PIPE 无消费者，约 4:38 后会阻塞；task 3
的 5:55 操作窗口因此只产生 4:37.8 视频。Reference runner 已改用独立 guest recorder：stderr
落文件、`ultrafast` 实时编码、第二次 Enter 先停视频、MP4 duration 对 guest monotonic 窗口
做 5 秒容差校验。截断 run 会标记 failed；通用 OSWorld server/正式实验路径未改。

新增本地测试覆盖 schema、prompt trust boundary、artifact hash、标准 actions、review gate、
SG `/32` 更新、evaluator 拒绝、final workbook 回收，以及 shortcut privacy filter、XInput
时间对齐、ASS 渲染和 guest overlay lifecycle。2026-08-11 已用 pending
`reference-task-r01-001` 完成一次付费 AWS 单实例 smoke（run
`20260811T130617Z`）：真实 XInput 捕获并过滤为 11 个可公开事件，`Ctrl+A`、
`Ctrl+Shift+V`、Tab、方向键和 Enter 均正确，普通文字未进入事件文件；guest ffmpeg 成功
烧录 1920×1080 overlay，抽帧确认提示位于底部中央。结果包、raw/overlay MP4、最终 XLSX 和
manifest 均完整，EC2 最终为 `terminated`，EBS、ENI、TTL schedule 均无残留。当前四个
packages 仍是 pending，正式标注前仍需完成人工 review。Annotator 操作见
`evaluation_examples/expert_skill_learning/annotator.md`。

## 2026-08-05 Reference Package、Review Loop 与 Artifact Generation

C2 已从 task-only 输出升级为可直接支持人工 reference-video 标注的 package：每个候选包含
`task_instruction`、`artifact_spec`、非强制逐步照抄的 `operator_guide` 和显式
`expected_incidental_operations`。只有 sampled 2–5 skills 是 mandatory coverage；有限的
task-specific、prerequisite 和重复操作可以存在，以免任务不自然。

当前冻结数据：

- `pilot/reference_packages.json`：4 个英文 Calc packages，candidate-level 覆盖 12/12；
- `pilot/reference_package_generation_run.json`：4 calls、6400/8485 tokens，generation
  `$0.114620`；
- `similarity_reference.semantic`：`text-embedding-3-small` cosine，不再是字符串近似；本轮
  337 tokens、`$0.00000674`；lexical sequence similarity 继续保留为辅助；
- `pilot/reference_package_reviews.json`：已有 4 条预填 task ID 的空白 review forms；空白
  decision 按 pending 处理，不会误判为 rejected；
- `pilot/coverage_state.json`：0/12 approved，证明 candidate coverage 没被误当 approved。

C3 软件闭环已经实现。Reviewer 可选择 `approved`、`revision_requested` 或 `rejected`。
全局 coverage 只合并 approved packages；revision 保持同一组 sampled skills 并携带反馈；
rejected exact combination 被 blocked，包含的 unresolved skills 会进入后续重新采样。只要还有
未 review 的 package，resume CLI 就会拒绝继续，防止生成状态分叉。

C4a artifact generation 也已实现：construction LLM 根据 package 的 `artifact_spec` 生成 strict
Calc blueprint，Node builder 使用 `@oai/artifact-tool` 生成真实 XLSX，应用初始 number format
和 AutoFilter，逐 sheet 渲染 PNG、扫描公式错误并记录 SHA256。冻结输出位于
`pilot/artifact_blueprints.json` 和 `pilot/artifacts/`，4 个 workbook 都是合成数据且
`manual_setup_required=false`。final blueprint run 为 4 calls、9167/3447 tokens、`$0.059698`。
一次早期 artifact iteration 花费 `$0.059986`。Enrollment artifact 首次有 9 个 Review rows，
developer QC 按 spec 修正为 8 个，调整已显式写入 `developer_qc_adjustments`。

下一步不是继续自动生成，而是由用户/annotator 人工 review 这 4 个 packages。review 完成后
重算 `coverage_state.json`；只有出现 rejected/revision/uncovered skills 时才运行 round 2。
之后进入 C4b setup-only OSWorld config 和 C5 Enter-controlled AWS recording runner。

## 2026-08-04 Reference Task Construction Pilot

研究目标仍是 inference-only benchmark：评测 omni-model 能否从专家 reference 操作中
归纳可迁移的高效技能，帮助下游 agent。但当前工程顺序已经收缩为先完成 task generation
和 human annotation 基础设施，不先实现 agent execution、训练或完整两阶段评测。

已确认的 Pilot contract：

- 选取 3 个明确的 `libreoffice_calc` OSWorld-Human tasks；
- LLM 输入严格只有 instruction 和 `human-ground-truth.single-action`；
- 只生成英文 app-operation skills，procedure 必须具体并含例子；
- 持久化 `app/name/procedure/efficiency_tip/source(task_id, action_ids)`，暂不去重；
- 同 app 随机采样 2–5 skills 生成自然的新任务，不自然时允许拒绝；
- 新任务不复用原 artifact、关键内容或完整有序解法，source contribution 只人工判断；
- Pilot coverage 为每个 skill 至少进入一个 approved task；
- LLM 默认生成 initial artifact，expert 负责检查、修订或替换；skill guide 可以按实际界面调整；
- deliverable 是 setup-only OSWorld config、artifact、skill cards、recording 和 review；
- AWS/noVNC 用于标注，终端 Enter 开始/停止录制；
- 第二位标注者在本地看 MP4，只在需要时启动 AWS 检查/复现 artifact；
- 暂用 GitHub remote；大视频不适合普通 Git 时再切 Git LFS/S3；
- construction LLM 使用 async OpenAI-compatible Python client、独立 `.txt` prompts、
  schema validation 和逐 attempt token/cost log，默认 `gpt-5.6-terra`。

2026-08-04 已开始 C0/C1：新增 `benchmark_construction/`、
`evaluation_examples/expert_skill_learning/` 和
`scripts/python/extract_reference_skills.py`。当前工具要求显式传入 3 个 task IDs，不会任意
替用户挑选。经用户授权，已在 OSWorld-Human commit
`deff1a7cd8940f6040a895593097fc3c5511f36b` 冻结 `035f41ba-...`、`8b1ce5f2-...` 和
`1954cced-...`，分别覆盖 formula/autofill/cross-sheet、conditional formatting 和 Pivot
Table。三个 task 的 40 个 `single_actions`、raw relative path 和 SHA256 已复制到
`pilot/source_tasks.json`，不再依赖 `/private/tmp` 才能复现 prompt；传入 upstream clone 时
会额外核验 hash 和内容。

聚焦测试已在 `osworld-aws-dev` 环境通过，atomic extraction 也已完成开发者 QC：
`pilot/skill_pool.json` 包含 12 个英文 app-operation skills。它们覆盖 38 个 substantive
source actions；普通 header 输入的 2 个 actions 作为 scaffolding 保留但不提升为 skill；
所有已分配 action 均无重复归属。`pilot/extraction_run.json` 记录最终 3 calls 的 prompt
hash、3690/2249 input/output tokens 和 `$0.034368` 估算成本。包含此前所有 prompt 迭代，
截至 C1 atomic skill extraction，开发 API 成本约 `$0.209436`。

2026-08-04 C2 已继续完成：新增 `benchmark_construction/reference_generation.py` 和
`scripts/python/generate_reference_tasks.py`。sampler 使用真正跨进程可复现的 seeded RNG，
按同 app 随机组合 2–5 skills；模型可以 reject，失败组合返回 uncovered pool；本地严格检查
candidate IDs 等于 sampled set。prompt 会列出未采样 pool skills，防止模型为了让组合自然
而偷偷增加未计入 coverage 的 substantive 操作；缺少前置技能时只能依赖明确 initial state
或 reject。

冻结的 `pilot/reference_tasks.json` 有 3 个英文 Calc candidates，candidate coverage 覆盖
全部 12 skills，但全都保持 `review_status=pending`。`pilot/reference_task_generation_run.json`
记录最终 3 calls、5274/2286 tokens、`$0.037980`。包含一次早期付费 generation iteration，
C2 开发调用合计 `$0.072294`；两次 schema 400 在推理前失败，成本为 0。Task 001 的空布局
Pivot 要求偏演示型，Task 003 包含某个 source task 的完整两-skill set，均已明确留给 C3
human review，而不是自动批准。该 task-only 输出现作为历史记录保留；当前 C3 软件闭环与
package/artifact 输出见上方 2026-08-05 更新。

旧的完整专家轨迹拆分、reference video bank、Qwen Stage 1/Stage 2、效率 evaluator 和
PowerPoint/AWS 历史内容继续保留；若与本节冲突，以本节、最新 `plan.md` 和
`developer.md` 顶部为准。

## 2026-08-03 研究方向转向

当前优先方向已从 PowerPoint `video-to-design/video-to-animation` 转为一个纯推理
benchmark：

> 在原始 OSWorld task 上，评测 omni-model 能否从拆分重组的专家 reference videos 中
> 归纳高效操作技能，并通过冻结 skill artifact 帮助固定 omni-agent 提升
> accuracy-constrained efficiency。

本项目不进行 SFT、RL、微调或任何模型训练，也不更新 omni-model 或下游 agent 的参数。
“学习”只指 omni-model 在推理阶段从专家轨迹生成 text playbook 或 SkillIR。完整协议是：

```text
OSWorld-Human 标注或人工录制的完整专家轨迹
→ action-group/subskill 拆分并跨轨迹重组
→ 非 1:1 reference video bank
→ Stage 1 omni-model inference
→ frozen skill artifact
→ Stage 2 fixed omni-agent on original OSWorld target
→ final-state + efficiency evaluator
→ paired uplift vs the same agent without skill
```

旧 Phase 0、AWS PowerPoint Web W0/W1、PPTX animation evaluator、登录态私有 AMI
和相关 fixture 全部保留；它们是可复用基础设施，不再是近期研究主线。原 PowerPoint
W2-W5 暂停，新的阶段编号为 E0-E4，详见根目录 `plan.md`。

### 外部数据状态

截至 2026-08-03，OSWorld-Human 已在
`https://github.com/WukLab/osworld-human` 公开。每个 OSWorld task JSON 包含：

- `human-ground-truth.single-action`：人工确定并在 VM 中验证的必要动作；
- `human-ground-truth.grouped-action`：可从同一 observation 连续执行的动作组；
- 官方 `score.py`：从 OSWorld result directory 计算 single/grouped WES。

它不是人类真实 GUI episode 数据集：没有逐帧 screenshot、录屏、坐标、输入事件、
timestamp、latency 或 recovery trace。用户此前“human trajectory 还没放出来”的判断，
如果指 raw state-action/video trajectory，仍然成立；如果指最短步骤标注，则已经公开。

OSWorld-Human README 明确说明这些文件包含 benchmark evaluation solution，不应被用于
训练；本项目没有训练环节。对于选定的 OSWorld pilot task，优先复用其 golden
`single-action` / `grouped-action` 操作语义和边界，再在 OSWorld 环境人工 replay 并录制；
缺失或粒度不足时自行标注。未拆分的完整 expert video 和 ordered solution 只进入 hidden
provenance/evaluator。参评模型只能看到拆成 action group/subskill、分散在多个上下文并
重排后的 reference videos。

这不是 task-level source/target 隔离 benchmark。目标任务仍是原始 OSWorld task；防泄漏
依赖 reference construction：任何单个视频不能包含完整解法，视频顺序不能编码 target
顺序，完整 golden video 仅作为不计入主分数的 diagnostic upper bound。

论文版本也要固定：2026-05-18 的 arXiv v2 报告领先 agent 需要约 `2.7-4.3x` 的必要
步骤，而仓库 README 仍显示较早的 `1.4-2.7x`。报告数字时必须注明 paper/repo version，
不得混用。

### 当前代码库对新方向的支持

可直接复用：

- `desktop_env/trajectory/recorder.py`：human/agent episode、纳秒时间、manifest；
- trajectory-event v1：`group_id`、plan/action/observation/result 和分项 latency；
- `lib_run_single.py`：默认 runner 的 normalized events、raw `traj.jsonl`、MP4 和结果；
- `scripts/python/manual_explore.py`：人工操作、周期截图、录屏、A11y、guest `xinput`；
- OSWorld task setup/final-state evaluator：accuracy gate；
- AWS/Daytona 生命周期与录屏基础设施；
- 旧 Office/PowerPoint task：可作为未来内部 pilot domain。

尚未完成：

- 多数 agent-specific runner 的统一 normalized trajectory；
- `xinput` 到 click/drag/scroll/type/hotkey 的 normalizer；
- OSWorld-Human golden annotation/WES importer 与官方 scorer parity test；
- action、decision group、observation、model-call、latency/token/cost 的统一 report；
- Stage 1 expert-trajectory-to-skill 的 inference harness、schema validation、hash 和 provenance；
- Stage 2 固定下游 agent 的 paired execution 与 C0-C7 controls；
- 3 个 OSWorld task 的 expert replay/人工标注与 evaluator-success 轨迹；
- action-group fragment cutter、跨轨迹 video recomposer 和 reference leakage report；
- mismatched/length/golden-upper-bound controls；
- text/structured/video/long-video 模型输入 adapter 与 paired modality ablation；
- WES、重复 grounding、loop、backtrack、recovery 和 Pareto 分析。

结论是“基础设施支持，但两阶段 benchmark orchestration 与因果评测尚未实现”。不需要
重写 OSWorld、recorder 或 AWS provider；新增重点是 inference-only skill induction、冻结
artifact、配对执行和 evaluator，而不是训练系统。

### 推荐接手顺序

1. 从现有 OSWorld 选择 3 个 pilot task，冻结其 instruction、snapshot、setup 和 evaluator。
2. 核对 OSWorld-Human 标注；有则 replay，无或不足则人工完成专家轨迹。
3. 对齐输入事件、截图、视频、semantic action、action group 和 evaluator result。
4. 将完整轨迹拆成 fragments，并确定性重组为 R2 reference video bank。
5. 冻结 video-capable Qwen omni-model 与 Qwen-based omni-agent 的版本、prompt 和预算。
6. 实现 Stage 1 inference harness，输出带 hash 的冻结 text playbook/SkillIR。
7. 对 no-reference、R2 recomposed、mismatched 和 R0 golden upper-bound 做 paired runs。
8. 输出 3-task accuracy、WES、step/call/time/token/cost、Pareto 和 reference leakage 报告。

多任务长视频只是待评测的输入模态，不是训练语料或默认最优方案；必须带
task/timeline/group 索引，并与更便宜、更可诊断的 text 和 structured trajectory baseline
在等 source 信息量、上下文预算和 target 条件下对照。

以下 2026-07-30 及更早内容作为已完成工程和历史计划保留；若与本节冲突，以本节和
最新 `plan.md` 为准。

## 2026-07-30 AWS PowerPoint Web W1 更新

当前主路径已从原 Daytona/LibreOffice Phase 0 切换为
`OSWorld 官方 Ubuntu AMI + Chrome + PowerPoint Web`。下文的 Phase 0 内容仍用于
理解已有 video-learning 数据契约和 evaluator，不代表当前云部署状态。

W1 已验证：

- AWS `us-east-1` 基础设施 preflight：13 pass、0 warning、0 blocked；
- 官方 `t3.xlarge`、30 GiB gp3、180 分钟 TTL、`/32` security group 和
  项目专属 `$20/月` Budget 配置；
- SSM diagnostics、OSWorld API、GNOME/X11、noVNC、Chrome/CDP、截图；
- 当前单实例完成 Microsoft 登录；
- 单页 PPTX upload/open/edit/slideshow/record/download；
- 标题 `Fade / On Click / 0.50 s` 在放映前隐藏、单击后出现；
- 下载稿通过 ZIP 和 `python-pptx` 检查，并在 OOXML 中保存
  `clickEffect`、`filter="fade"` 和 500 ms timing；
- OSWorld 录屏输出为 H.264、1920×1080、30 fps；
- provider 默认创建加密 gp3，实际新卷验证 `Encrypted=true`；
- 私有 AMI `ami-0c68ad8829df7c05e`
  （`osworld-ppt-web-auth-20260730`）及加密 snapshot
  `snap-0832dc22794c270f2` 已创建；
- AMI 和 snapshot permissions 为空，未公开或共享；
- 从 AMI 启动全新实例后，PowerPoint Web 登录态自动恢复；
- 制镜源实例、验证实例、EBS 和 TTL schedules 已清理；
- `AWS_AMI_ID` 已写入 `osworld-aws-dev` Conda 环境；
- 正式 PowerPoint Web task ID
  `5f24d8c2-4779-4f6d-9b8c-6e3bc97ed441` 已接入；
- static-content gate 保持文字、颜色、版式、master 和 theme，animation gate
  比较目标对象、效果、trigger、duration 和顺序；
- initial 的 static/animation 分数为 `1/0`，gold 为 `1/1`；
- SSM 复现 `osworld.service` 在 X11 前启动并耗尽
  `StartLimitBurst=4`；由于认证 AMI 不保证重跑 cloud-init UserData，
  launch/reset 现在通过 SSM 主动安装并验证等待 `xdpyinfo` 的 drop-in，
  UserData 仅作干净 AMI 后备；
- 当前代码修复后 10/10 create/reset/close 通过，readiness
  `98.143–186.995 s`，总墙钟约 38 分 47 秒；
- soak 结束后 EC2/EBS/ENI/TTL schedule 均为 0；
- W1 相关本地测试 40/40 通过。

Budget 状态：

- 原 `osworld-ppt-web-monthly` 没有 cost filter，因此 `$198.63 actual /
  $218.75 forecast` 邮件反映的是整个 AWS 账户，而非 W1 项目；
- 该账户级 Budget 的 actual 80% 和 forecast 100% 通知已于 2026-07-30 删除并
  验证为空，Budget 对象仍保留但不再发信；
- `scripts/python/setup_aws_project_budget.py` 已准备
  `Project=OSWorld-PPT-Web` 过滤、`$20/月`、actual 80% 和 forecast 100%
  的项目配置；
- Billing 尚未发现 `Project` 成本分配标签，因此项目 Budget 尚未应用；
- 标签出现后按 `developer.md` 的命令激活，并通过
  `AWS_BUDGET_EMAIL` + `--apply` 创建；不要把邮箱硬编码进仓库。

W1 已完成。2026-07-30 AWS Pricing API 折算当前配置约 `$0.6884/3h`；最终 10 次
soak 墙钟约 38 分 47 秒，估算低于 `$0.20`。Cost Explorer 尚未入账并标记
`Estimated=true`，后续需复核实际账单。Billing 仍未发现 `Project` 成本分配标签，
所以项目 Budget 配置尚未应用；这不影响 terminate、TTL 和资源审计。
最终 soak 完成后的本地 SSO token 已过期；下一次 AWS 操作前先运行
`aws sso login --profile osworld-dev`。soak 报告已在凭据有效时完成终态审计，
记录 EC2/EBS/ENI/TTL schedule 全为 0。

继续工作前先阅读根目录的 `plan.md` 和 `developer.md`。这里原定的 Phase W2
（Layout、Coverage、Order、Detail、rendered temporal evaluator 和 fancy demo）已于
2026-08-03 暂停；当前下一步是 E0 3-task pilot contract。W1 单页 Fade
task 继续作为诊断 fixture，不代表最终任务难度。

该 AMI 包含敏感 Microsoft 登录 Cookie/令牌。不得公开、跨账户共享或导出 Chrome
profile；session 过期后应使用新的加密实例重新登录并替换 AMI。删除时必须先
deregister AMI，再显式删除其 snapshot。

## 1. 文档目的

本文档用于把 Phase 0 的代码、数据、Daytona 环境和验收状态交接给下一位
开发者。它回答以下问题：

- 当前已经完成了什么。
- 每个新增或修改文件负责什么。
- 数据如何在 Task、视频、SkillIR、trajectory 和 evaluator 之间流动。
- 如何在本地和计算节点复现验证。
- 哪些能力只是接口或占位，尚未形成完整的 video-learning 系统。
- 下一阶段建议先做什么，以及每项工作的完成标准。

本文档对应以下版本：

- 分支：`codex/phase0-video-learning`
- Phase 0 验收提交：`2b8043fac9145b697d3fedaac34039e868a6cf12`
- Daytona Office snapshot：`osworld-video-office-v1`
- 计算节点 Conda 环境：`osworld_env`
- 计算节点 Python：3.10.20

`handoff.md` 本身创建于上述验收提交之后，因此后续若提交本文档，需要记录新的
commit SHA。

## 2. Phase 0 完成范围

Phase 0 已经打通以下基础闭环：

```mermaid
flowchart LR
    A["Task JSON"] --> B["OSWorld setup"]
    V["演示视频"] --> A
    S["SkillIR"] --> A
    B --> C["Daytona Office desktop"]
    C --> D["人工或 Agent 操作"]
    D --> E["TrajectoryRecorder"]
    E --> F["events.jsonl"]
    E --> G["episode_manifest.json"]
    C --> H["OSWorld evaluator"]
    H --> I["initial / gold score"]
```

已经完成：

- Video-learning Task、SkillIR 和统一 trajectory event 的 v1 JSON Schema。
- Agent 默认 runner 的统一事件记录、单调计时和原子 manifest。
- 人类演示采集入口，支持录屏、周期截图、X11 输入事件和 evaluator。
- 可复现的 Daytona Office snapshot 构建、smoke 和 10-reset soak。
- 两个 Impress、两个 Calc 的确定性 Phase 0 任务与 fixtures。
- 本地结构验证和真实 Daytona setup/evaluator 验收。

尚未完成：

- Agent adapter 还不会把 `delivery_mode=context` 的视频帧真正发送给视频模型。
- 当前视频是合成的 before/after 卡片，不是真实 GUI 操作视频。
- 四份 SkillIR 是手工编写的，还没有 video/trajectory-to-SkillIR compiler。
- SkillIR 还没有通用执行器。
- Daytona 四任务验收只证明 setup 和 evaluator 正确，没有证明 Agent 从视频中学会
  并完成任务。
- 人类 X11 事件仍是原始日志，没有转换成统一的语义 action event。

## 3. 总体数据流

一个 Phase 0 task 包含：

1. 初始 Office 文件。
2. 演示视频。
3. 演示前文件和演示后文件。
4. 与演示规则对应的 SkillIR。
5. OSWorld setup 配置。
6. 目标 Gold 文件和 evaluator 规则。

执行时：

1. OSWorld 将初始 Office 文件和 `demo.mp4` 上传到 Daytona guest。
2. 打开 Office 文件。
3. 人类或 Agent 修改文件。
4. runner/采集器记录截图、动作、时间和 MP4。
5. evaluator 先触发保存，再从 guest 取回结果文件。
6. Calc 使用 `compare_table`，Impress 使用 `compare_pptx_files`。
7. `TrajectoryRecorder` 输出统一 JSONL 和 episode manifest。

验证脚本使用一个额外的诊断流程：

- 将初始文件上传并 evaluate，要求分数小于 1。
- 将 Gold 文件当作输入上传并 evaluate，要求分数等于 1。
- 该流程用于验证 task/evaluator 正确性，不是 Agent 能力评测。

## 4. 数据契约

### 4.1 `evaluation_examples/video_learning/schemas/task-extension.schema.json`

用途：

- 定义 video-learning task 是一个合法 OSWorld task 的扩展。
- 要求存在 `id`、`snapshot`、`instruction`、`config`、`related_apps`、
  `evaluator` 和 `video_learning`。
- 冻结视频位置、交付模式、迁移族、演示前后文件、SkillIR 和 split group 的表示。

关键字段：

- `video_learning.schema_version`：当前固定为 `1.0`。
- `demo_video`：本地视频路径和 guest 目标文件名。
- `delivery_mode`：计划支持 `context`、`ui`、`compiled`。
- `transfer_family`：同一种可迁移编辑规则的标识。
- `source_artifact`：演示操作前的 Office 文件。
- `demo_result_artifact`：演示操作后的 Office 文件。
- `skill_ir`：对应 SkillIR JSON。
- `split_group`：防止同一模板或规则跨 benchmark source/target 泄漏。

注意：

- Schema 已允许表达三种 delivery mode，但当前 runner 尚未实现通用 video context
  adapter。
- 当前 task 同时把 `demo.mp4` 上传到 guest，主要用于保持数据自包含；Daytona
  evaluator 验收不会观看该视频。

### 4.2 `evaluation_examples/video_learning/schemas/skill-ir.schema.json`

用途：

- 表示从视频或人类轨迹抽取出的、可迁移的任务目标和操作方法。
- 将“具体坐标动作”提升为“语义对象 + 参数 + 验证条件”。

顶层字段：

- `schema_version`
- `name`
- `description`
- `preconditions`
- `goal_spec`
- `parameters`
- `steps`
- `verification`
- `fallbacks`

设计原则：

- `goal_spec.required` 表示必须满足的最终状态。
- `goal_spec.optional` 表示允许存在但不影响通过的属性。
- `goal_spec.invariants` 表示编辑过程中不能改变的内容，例如单元格值或正文文本。
- `parameters` 保存从视频抽取出的风格参数。
- `steps` 使用语义 target，例如 `slide.title`、`sheet.header_row`，避免绑定坐标。
- `verification` 用于定义关键检查点。
- `fallbacks` 为将来的失败恢复和分支技能图预留接口。

当前限制：

- 没有 compiler 自动生成该结构。
- 没有 executor 将任意 SkillIR 转成 pyautogui/UI 动作。
- 当前默认 runner 的 normalized action 主要保存 `raw_action`，尚未填充完整
  `semantic_action`。

### 4.3 `evaluation_examples/video_learning/schemas/trajectory-event.schema.json`

用途：

- 让人类轨迹和 Agent 轨迹共享一个事件格式。
- 支持之后计算成功率、动作数、观察数、模型时延和环境时延。

事件类型：

- `observation`
- `plan`
- `action`
- `verification`
- `result`

重要字段：

- `episode_id`、`task_id`、`actor`
- `event_id`、`group_id`
- `semantic_action`、`raw_action`
- `timestamps_ns.started/finished`
- `latency_ms.model/grounding/environment/settle`
- `observation_ref`、`a11y_ref`
- `window`
- `outcome`、`error`
- `metadata`

时间戳使用单调时钟纳秒，不使用 wall clock 计算持续时间，避免系统时间跳变。

### 4.4 `desktop_env/trajectory/schema.py`

用途：

- 将短名称 `task`、`skill`、`trajectory_event` 映射到三个 Schema 文件。
- 缓存已加载 Schema。
- 使用 JSON Schema Draft 2020-12 和 `FormatChecker` 校验文档。

公开接口：

- `SCHEMA_VERSION`
- `load_schema(name)`
- `validate_document(document, schema_name)`

`jsonschema>=4.21` 因此被加入 `pyproject.toml` 和 `requirements.txt`。

### 4.5 `desktop_env/trajectory/__init__.py`

用途：

- 对外统一导出 `SCHEMA_VERSION`、`TrajectoryRecorder` 和
  `validate_document`。
- 其他模块不需要知道 Schema 的具体磁盘路径。

## 5. 统一轨迹记录

### 5.1 `desktop_env/trajectory/recorder.py`

核心类：`TrajectoryRecorder`

初始化参数：

- `output_dir`
- `task_id`
- `actor`：只能是 `human` 或 `agent`
- 可选 `episode_id`
- 可选 `validate_events`

主要输出：

- `events.jsonl`：append-only 的 normalized events。
- `episode_manifest.json`：episode 结束时原子写入的汇总。

主要方法：

- `now_ns()`：获取 `time.monotonic_ns()`。
- `add_timing(name, elapsed_ns)`：累加阶段耗时。
- `record_event(...)`：写入单个事件。
- `finalize(...)`：写 manifest，只允许 completed/failed/interrupted。

关键实现：

- 使用线程锁保护 event id、timing 和文件追加。
- 每个事件包含完整的四类 latency 字段，未提供的字段写 0。
- 未知 latency 字段会直接报错，避免悄悄产生不可比较指标。
- `finalize()` 先写 `.json.tmp`，再通过 `os.replace` 原子替换。
- 重复调用 `finalize()` 会读取已有 manifest，不会重复覆盖。
- finalize 后禁止追加事件。

Manifest 中的 timing policy 明确规定：

- execution 从首个可行动 observation 开始，到最后一次环境 action 结束。
- environment setup、initial settle、post-action settle、evaluation 和录屏收尾不计入
  execution。
- wall clock 仍单独保留，可用于端到端成本分析。

已知限制：

- JSONL 目前每个 event 单独 open/write，没有 fsync；进程被强制 kill 时最后一行仍有
  小概率丢失。
- 没有对截图文件是否真实存在进行 finalize-time 校验。
- 尚未实现计划中的 `grouping.py`，`group_id` 由调用方提供。

## 6. Agent runner 接入

### 6.1 `lib_run_single.py`

改动范围：

- 只改造默认 `run_single_example()`。
- Kimi、AGI、OpenAI CUA 等专用 runner 暂未迁移。
- 原来的 `traj.jsonl`、截图、`result.txt` 和 `recording.mp4` 继续保留。

新增记录：

- environment reset 耗时。
- 60 秒 initial settle。
- 初始截图和可选 accessibility tree。
- 每次 `agent.predict()` 的 model latency 和 plan event。
- 每个 `env.step()` 的 environment latency、raw action、截图和 a11y。
- execution 总耗时。
- 20 秒 post-action settle。
- evaluator 耗时和 result event。
- 录屏 finalize 耗时。
- completed 或 failed manifest。

兼容性选择：

- 原始 `traj.jsonl` 没有删除，避免破坏已有分析工具。
- 原有 60 秒和 20 秒 sleep 暂时保留，防止改变 benchmark 行为。
- 两段 sleep 不计入 execution，但计入 wall clock。
- agent reset 先尝试传 `runtime_logger`，失败后兼容旧签名。
- 异常会生成 failed manifest，然后重新抛出，不吞掉原始错误。

下一步接手时要注意：

- 其他 agent-specific runner 仍使用旧格式。
- 默认 runner test 在 Python <3.12 时模块级 skip。
- 如果要正式比较 agent efficiency，应先统一所有 runner，再决定是否移除固定 sleep。

## 7. 人类轨迹采集

### 7.1 `scripts/python/manual_explore.py`

用途：

- 启动一个可人工操作的 OSWorld 环境。
- 可加载具体 task，采集人类演示，并在结束后 evaluate。
- 替代文档中已经失效的 `manual_examine.py` 入口。

主要参数：

- `--provider-name/--provider_name`
- `--path-to-vm/--path_to_vm`
- `--os-type`
- `--headless`
- `--ssh-host`
- `--local-vnc-port`
- `--task-config/--task_config`
- `--result-dir/--result_dir`
- `--sample-interval`
- `--no-recording`
- `--no-input-events`
- `--require-a11y-tree`

主要流程：

1. 解析 task JSON。
2. 把 host 端 `upload_file.local_path` 和 evaluator `local_file.path` 转为仓库绝对路径。
3. 创建 `results_human_examine/<task-id>/<UTC timestamp>/`。
4. 创建 actor=`human` 的 `TrajectoryRecorder`。
5. 创建并 reset `DesktopEnv`。
6. 保存 initial screenshot/a11y。
7. 启动 MP4 录屏。
8. 在 guest 中启动 `xinput test-xi2 --root`。
9. 后台按固定间隔抓取截图。
10. 提示 noVNC 或本地 GUI 访问方式，等待 Enter/Ctrl-C/SIGTERM。
11. 停止输入采集和截图线程。
12. 保存 final screenshot/a11y。
13. 若有 task，运行 evaluator。
14. 停止录屏，写 completed/interrupted/failed manifest，关闭环境。

输出示例：

```text
results_human_examine/
└── <task-id>/
    └── <UTC timestamp>/
        ├── events.jsonl
        ├── episode_manifest.json
        ├── initial_state.png
        ├── final_state.png
        ├── recording.mp4
        ├── input_events.xinput.log
        ├── result.txt
        └── frames/
            └── 000000_<monotonic-ns>.png
```

容错策略：

- xinput 不可用时继续录屏和截图。
- 周期截图失败不会立即终止人工 session，错误写入 manifest metadata。
- Ctrl-C 被记录为 interrupted，而不是 failed。
- finally 中再次尝试停止截图线程、xinput、录屏和环境。

已知限制：

- 只支持 X11 `xinput`，不支持 Wayland input event。
- `input_events.xinput.log` 还是原始文本，没有统一 timestamp/event normalization。
- 周期截图和 xinput 使用不同数据源，需要后续离线对齐。
- 目前没有记录窗口焦点变化和语义对象。
- 人工 session 尚未批量采集真实 Phase 1 demonstrations。

### 7.2 文档入口修复

以下文件由失效的 `manual_examine.py` 改为当前入口：

- `README.md`
- `scripts/README.md`
- `scripts/bash/run_manual_examine.sh`

`run_manual_examine.sh` 仍是便捷包装；需要复杂参数时直接调用
`scripts/python/manual_explore.py`。

## 8. Daytona Office 环境

### 8.1 `desktop_env/providers/daytona/build_snapshot.py`

用途：

- 从 Daytona base snapshot 构建适合 Phase 0 的不可变 Office snapshot。
- 不依赖服务器 Docker、KVM 或 qcow2 权限。

默认 base：

- `daytonaio/sandbox:0.8.0`

新增/确认的 apt 包：

- OSWorld server 基础依赖。
- `xinput`
- `fonts-liberation`
- `fonts-dejavu-core`
- `libreoffice`
- `libreoffice-calc`
- `libreoffice-impress`

十个构建阶段：

1. 创建 build sandbox。
2. 启动 computer-use desktop。
3. 上传 OSWorld guest server。
4. 安装 wrapper。
5. 安装 apt/Office 依赖。
6. 安装 guest Python 依赖。
7. 写 snapshot manifest。
8. 验证 server、截图、accessibility、LibreOffice 和 xinput。
9. 创建命名 snapshot。
10. 删除 build sandbox。

Manifest：

- Guest 路径：`/etc/osworld/snapshot-manifest.json`
- 可选 host 副本：`--manifest-out <path>`
- 字段包括 snapshot/base 名称、构建时间、OSWorld commit、构建脚本 SHA-256、
  LibreOffice 版本、包版本和 capabilities。

本次验收 snapshot：

- 名称：`osworld-video-office-v1`
- LibreOffice：25.2.3.2
- Manifest：`results/osworld-video-office-v1-manifest.json`

### 8.2 `desktop_env/providers/daytona/smoke_test.py`

用途：

- 独立于完整 ML stack 验证 Daytona provider 生命周期。

检查项：

- sandbox allocate/start。
- SSH tunnel。
- `/platform`。
- `/screenshot`。
- `/accessibility`。
- LibreOffice、Calc、Impress、xinput 和 snapshot manifest。
- 可选 snapshot/revert。
- restore 后再次检查 platform 和 Office。
- sandbox teardown。

环境变量：

- `DAYTONA_SMOKE_REQUIRE_A11Y=1`：accessibility 必须成功。
- `DAYTONA_SMOKE_SKIP_SNAPSHOT=1`：跳过一次性 snapshot/revert。

在真实计算节点测试中，截图首帧曾超过原来的 10 秒 read timeout，因此截图专用
read timeout 调整为 30 秒；轻量 HTTP 探针仍保持 10 秒。

注意：

- 当前 Daytona 凭据允许创建 snapshot，但删除 snapshot 返回 HTTP 403。
- 完整 smoke 留下了 `osworld-smoke-4cb8902168`，需要在 Dashboard 手工删除。
- 日常一键验收默认 skip 临时 snapshot，由 10-reset soak 覆盖 restore。

### 8.3 `desktop_env/providers/daytona/soak_test.py`

用途：

- 验证从同一个不可变 snapshot 连续 replacement reset 是否稳定。
- 检查旧 sandbox 是否进入 destroying/destroyed。
- 生成机器可读 JSON 报告。

每轮检查：

- platform。
- screenshot。
- LibreOffice Calc/Impress。
- xinput。
- snapshot manifest。

参数：

- `--iterations`，默认 10。
- `--report`，默认 `results/daytona_phase0_soak.json`。

报告包含：

- snapshot 名称。
- 初次 launch。
- 每轮 old/new sandbox id。
- 旧 sandbox 状态。
- 各轮耗时和端口。
- passed/failed 状态和 teardown error。

本次真实结果：

- 10/10 reset 通过。
- 本次测试创建的 sandbox 已全部清理。
- 账号中另有一个早于本次测试约 7 小时创建的 managed sandbox，因不属于本次运行
  而保留未动。

### 8.4 `desktop_env/providers/daytona/tunnel.py`

改动：

- `TUNNEL_START_TIMEOUT_SEC` 从 10 秒调整为 30 秒。

原因：

- `DesktopEnv` 四任务验证中，SSH 进程仍存活但 listener 未在 10 秒内出现。
- smoke/soak 已观察到 15–22 秒的真实冷启动波动。
- 增加 listener 等待不会掩盖 SSH 进程退出、端口冲突或 forward 拒绝，这些情况仍会
  提前失败。

### 8.5 `scripts/bash/validate_phase0_daytona.sh`

用途：

- 在 snapshot 已构建、两个 Daytona 环境变量已设置后执行完整 Phase 0 验收。

顺序：

1. 检查 `DAYTONA_API_KEY`。
2. 检查 `DAYTONA_OSWORLD_SNAPSHOT`。
3. 重新生成 fixtures。
4. 执行 skip-temp-snapshot 的 Office smoke。
5. 执行 10-reset soak。
6. 执行四任务原生 Daytona validator。

为什么 smoke 默认 skip snapshot：

- 后面的 soak 已经覆盖从配置 snapshot 恢复。
- 当前账号不能 API 删除临时 snapshot。
- 避免每次 CI/人工运行都积累 `osworld-smoke-*`。

### 8.6 `desktop_env/providers/daytona/DAYTONA_GUIDELINE.md`

用途：

- 记录 snapshot build、manifest、smoke、soak、任务验证和环境变量。
- 特别说明 reset 会短暂同时存在新旧两个 sandbox，需要为 quota 留余量。
- 记录 snapshot delete 403 的处理方式。

## 9. Phase 0 Fixtures

### 9.1 `scripts/python/generate_phase0_fixtures.py`

用途：

- 程序化生成四个任务的演示视频、initial、demo-before、demo-after 和 gold 文件。
- 输出 SHA-256/size manifest。

生成内容：

- 4 个 MP4。
- 8 个 Impress PPTX。
- 8 个 Calc XLSX。
- 合计 20 个被 manifest 跟踪的文件。

视频规格：

- 960×540。
- 10 FPS。
- 30 帧。
- 3 秒。
- before 1.2 秒、transition 0.6 秒、after 1.2 秒。

确定性处理：

- Office ZIP member 按名称排序。
- ZIP entry 时间固定为 1980-01-01。
- `docProps/core.xml` 的 created/modified 固定为
  `2000-01-01T00:00:00Z`。
- ZIP 使用固定压缩级别。
- 生成 `fixture_manifest.json`，记录每个文件的 SHA-256 和字节数。

为什么需要 core property 修复：

- OpenPyXL 会写当前创建/修改时间。
- 本地快速连续生成可能落在同一秒，无法发现问题。
- 计算节点两次生成相差一秒，确定性测试因此失败。
- 修复后跨机器重复生成已经通过测试。

当前视频的定位：

- 它们是基础管道 fixtures，不是最终研究视频。
- 视频展示 before/after 属性，不包含真实菜单、快捷键和鼠标轨迹。
- Phase 1 应替换或补充真实操作录屏。

### 9.2 `evaluation_examples/video_learning/fixtures/generated/`

每个任务族都有：

- `<family>_initial.<office-ext>`
- `<family>_gold.<office-ext>`
- `<family>_demo_before.<office-ext>`
- `<family>_demo_after.<office-ext>`
- `<family>_demo.mp4`

任务族：

- `impress_title`
- `impress_background`
- `calc_currency`
- `calc_header`

`fixture_manifest.json` 是验证入口，不要手工修改二进制文件后忘记重新生成 manifest。

## 10. 四个 Phase 0 任务

### 10.1 Impress title style

Task：

- `evaluation_examples/video_learning/examples/libreoffice_impress/`
  `0f4e50c1-0c2c-4f83-9ea9-48f7b67e1001.json`

目标：

- 标题字体：Liberation Serif。
- 标题字号：32 pt。
- 标题颜色：`#1F4E78`。
- 标题文字和正文内容不变。

Evaluator：

- `compare_pptx_files`

SkillIR：

- `evaluation_examples/video_learning/skills/impress_title_style.json`

### 10.2 Impress background treatment

Task：

- `evaluation_examples/video_learning/examples/libreoffice_impress/`
  `0f4e50c1-0c2c-4f83-9ea9-48f7b67e1002.json`

目标：

- Slide background：`#1F4E78`。
- 标题和正文颜色：`#FFFFFF`。
- 文字内容不变。

Evaluator：

- `compare_pptx_files`

SkillIR：

- `evaluation_examples/video_learning/skills/impress_background_style.json`

### 10.3 Calc currency format

Task：

- `evaluation_examples/video_learning/examples/libreoffice_calc/`
  `0f4e50c1-0c2c-4f83-9ea9-48f7b67e1003.json`

目标：

- Amount cells number format：`$#,##0.00`。
- 所有单元格值不变。

Evaluator：

- `compare_table`
- `sheet_data` 规则确保值不变。
- `style[number_format]` 检查格式。

SkillIR：

- `evaluation_examples/video_learning/skills/calc_currency_format.json`

### 10.4 Calc header style

Task：

- `evaluation_examples/video_learning/examples/libreoffice_calc/`
  `0f4e50c1-0c2c-4f83-9ea9-48f7b67e1004.json`

目标：

- Header bold。
- 字体颜色 `#FFFFFF`。
- 背景颜色 `#1F4E78`。
- 所有单元格值不变。

Evaluator：

- `compare_table`
- `sheet_data`。
- `style[font_bold,font_color,bgcolor]`。

SkillIR：

- `evaluation_examples/video_learning/skills/calc_header_style.json`

### 10.5 `evaluation_examples/video_learning/test_phase0.json`

用途：

- 四个 task JSON 的索引列表。
- 可作为后续 runner 加载 Phase 0 suite 的入口。

### 10.6 `evaluation_examples/video_learning/README.md`

用途：

- 提供 fixture 生成、本地验证、Daytona 验收和人工采集的最短命令。
- 明确本地 fallback 不能替代 Daytona 原生 evaluator 验收。

## 11. Task Validator

### 11.1 `scripts/python/validate_phase0_tasks.py`

本地验证：

- 必须正好找到四个 task。
- 校验 Task Schema。
- 校验对应 SkillIR Schema。
- 检查 demo-before/demo-after 存在。
- 验证 fixture manifest 的 SHA-256 和 size。
- 用 OpenCV 验证视频可解码、帧数和 FPS。
- 计算 initial 和 gold 分数。
- 要求 initial `<1`、gold `>=1`。

本地 metric engine：

- 优先导入 OSWorld 原生 `compare_pptx_files` / `compare_table`。
- 如果仅缺少 `formulas` 或 `rapidfuzz`，使用
  `phase0_compatible` 结构比较。
- Fallback 只实现四个 Phase 0 task 使用的规则，不是通用 evaluator。
- 报告会写 `metric_engine`，不能把 fallback 结果宣称为 Daytona 通过。

`--daytona` 验证：

- 创建真实 `DesktopEnv(provider_name="daytona")`。
- 对每个 task 上传 initial 并 evaluate。
- 再把 task 输入替换为 Gold，reset 后 evaluate。
- 要求四个任务全部 initial=0、gold=1。
- finally 中关闭环境。

输出：

- 默认：`results/phase0_task_validation.json`
- Daytona：通常指定 `results/phase0_daytona_tasks.json`
- 使用临时文件 + `os.replace` 原子写报告。

已知限制：

- Daytona 路径没有真正执行编辑动作。
- `compare_pptx_files` 对整个演示文稿结构较严格，扩展到真实任务时可能需要更细粒度
  evaluator。
- Fallback 的 PPTX shape 顺序、几何和文本 run 比较不适用于复杂 deck。

## 12. 测试文件

### 12.1 `tests/test_trajectory_recorder.py`

验证：

- 事件符合 Schema。
- event JSONL 被正确写入。
- timing 从纳秒转换为毫秒。
- manifest 原子写入后不存在 `.tmp`。
- finalize 后继续写 event 会报错。

### 12.2 `tests/test_default_runner_trajectory.py`

使用 fake env/agent/controller 验证：

- 保留原始 `traj.jsonl`。
- normalized event 顺序为 observation/plan/action/result。
- 生成 recording。
- manifest status/result/timing 正确。
- agent 异常时写 failed manifest。

限制：

- Python <3.12 时整个模块 skip。
- 计算节点 `osworld_env` 为 Python 3.10.20，因此本次验收跳过该文件。

### 12.3 `tests/test_manual_explore_phase0.py`

验证：

- task 中 host local upload paths 被转换为绝对路径。
- evaluator expected local path 被转换为绝对路径。

### 12.4 `tests/test_phase0_video_learning.py`

验证：

- 在两个目录重复生成的 20 个文件 hash/size 完全相同。
- 每个 PPTX/XLSX core properties 包含固定时间。
- 四 task 本地验证通过。
- 全部 initial=0、gold=1。

## 13. 依赖与忽略规则

### 13.1 `pyproject.toml`

新增：

- `jsonschema>=4.21`

当前声明：

- `requires-python = ">=3.12"`

### 13.2 `requirements.txt`

新增：

- `jsonschema>=4.21`

### 13.3 `.gitignore`

新增：

- `daytona_key.sh`

目的：

- 防止计算节点或本地的 Daytona 凭据脚本被误提交。

`results/**` 原本已被忽略，因此验收报告不会自动进入 Git。

### 13.4 开发与使用文档

- `plan.md`
  - 保存完整研究目标、实验问题、指标、Daytona 策略和 Phase 0–4 路线图。
  - Phase 0 的真实验收状态已经勾选。
- `DEVELOPMENT.md`
  - 保存本地修改、Git fork 同步、Slurm allocation、`osworld_env` 和
    `daytona_key.sh` 的标准流程。
- `README.md`
  - 修复根目录人工探索命令，使其指向现有的 `manual_explore.py`。
- `scripts/README.md`
  - 更新脚本级人工探索说明和参数。
- `evaluation_examples/video_learning/README.md`
  - Video-learning 数据目录的最短使用说明。
- `desktop_env/providers/daytona/DAYTONA_GUIDELINE.md`
  - Daytona snapshot、smoke、soak、任务验收、quota 和清理限制的详细说明。

## 14. 开发和计算节点流程

完整说明见 `DEVELOPMENT.md`，关键流程如下。

本地提交：

```bash
git add <files>
git commit -m "<message>"
git push omni HEAD
```

申请计算节点：

```bash
ssh hkust-hpc2
module load slurm
srun -p i64m512u -n 4 --mem=8G --time=07:00:00 --pty bash
```

若 `srun` 不在 PATH：

```bash
/opt/slurm/bin/srun \
  -p i64m512u \
  -n 4 \
  --mem=8G \
  --time=07:00:00 \
  --pty bash
```

进入计算节点后：

```bash
cd "$HOME/Omni-OSWorld"
git remote -v
git fetch origin
git switch codex/phase0-video-learning
git pull --ff-only origin codex/phase0-video-learning

source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate osworld_env
source daytona_key.sh

test "${CONDA_DEFAULT_ENV}" = "osworld_env"
test -n "${DAYTONA_API_KEY:-}"
test -n "${DAYTONA_OSWORLD_SNAPSHOT:-}"
```

安全要求：

- 不要 `cat daytona_key.sh`。
- 不要打印 API key。
- 不要把 key 写入 task、manifest、日志或 Git。
- 每个新的 shell 都要重新 activate/source。
- `ssh hkust-compute` 只有在 active Slurm allocation 存在时才可用。

计算节点最初缺少 pytest，本次已在 `osworld_env` 安装：

```text
pytest 8.4.2
```

## 15. 常用命令

本地 fixture 与任务验证：

```bash
python scripts/python/generate_phase0_fixtures.py
python scripts/python/validate_phase0_tasks.py
```

定向测试：

```bash
python -m pytest \
  tests/test_trajectory_recorder.py \
  tests/test_default_runner_trajectory.py \
  tests/test_phase0_video_learning.py \
  tests/test_manual_explore_phase0.py \
  -q -rs
```

构建 Daytona Office snapshot：

```bash
python -m desktop_env.providers.daytona.build_snapshot \
  --name osworld-video-office-v1 \
  --manifest-out results/osworld-video-office-v1-manifest.json

export DAYTONA_OSWORLD_SNAPSHOT=osworld-video-office-v1
```

日常完整验收：

```bash
bash scripts/bash/validate_phase0_daytona.sh
```

单独运行 soak：

```bash
python -m desktop_env.providers.daytona.soak_test \
  --iterations 10 \
  --report results/daytona_phase0_soak.json
```

单独运行原生 evaluator 验收：

```bash
python scripts/python/validate_phase0_tasks.py \
  --daytona \
  --report results/phase0_daytona_tasks.json
```

采集人工演示：

```bash
python scripts/python/manual_explore.py \
  --provider_name daytona \
  --headless \
  --task-config \
  evaluation_examples/video_learning/examples/libreoffice_impress/\
0f4e50c1-0c2c-4f83-9ea9-48f7b67e1001.json
```

## 16. 已完成验收

本地及计算节点定向测试：

```text
5 passed, 1 skipped
```

Skip：

- `tests/test_default_runner_trajectory.py`
- 原因：`osworld_env` Python 3.10.20，而项目声明 Python >=3.12。

Daytona：

- Office snapshot build：通过。
- Office smoke：通过。
- Replacement reset soak：10/10 通过。
- 四 task 原生 evaluator：全部通过。
- 每个 task：initial=0、gold=1。
- 本次创建的 sandbox：全部清理。
- Slurm job：已释放。

本地保存的验收证据：

- `results/daytona_phase0_soak.json`
- `results/phase0_daytona_tasks.json`
- `results/osworld-video-office-v1-manifest.json`
- `results/phase0_task_validation.json`

这些文件位于被 `.gitignore` 忽略的 `results/`，如果需要长期归档，应复制到正式
artifact store，而不是强制提交带运行时信息的报告。

## 17. 已知问题与操作注意事项

### 17.1 Python 版本不一致

- `pyproject.toml` 要求 Python >=3.12。
- 服务器 `osworld_env` 是 Python 3.10.20。
- 默认 runner 测试因此没有在服务器真正执行。

建议尽快选择：

1. 升级/重建 `osworld_env` 到 Python 3.12；或
2. 如果代码实际支持 3.10，修改项目声明并移除 3.12-only 语法。

在决策前不要简单删除 test skip。

### 17.2 Daytona snapshot 删除权限

- 当前 key 能创建 snapshot。
- 当前 key 删除 snapshot 返回 HTTP 403。
- 临时 `osworld-smoke-4cb8902168` 仍需 Dashboard 手工删除。
- 一键验收已避免继续创建临时 smoke snapshot。

### 17.3 Video context 尚未接入 Agent

- `delivery_mode=context` 目前是 task contract。
- 没有统一的 frame sampling/token budget/model adapter。
- 不能据此声称 Agent 已完成 video learning。

### 17.4 SkillIR 尚未自动化

- 当前四个 SkillIR 是人工 gold representation。
- 没有从视频、字幕、轨迹或 before/after 文件自动生成。
- 没有通用 SkillIR executor。

### 17.5 人类轨迹还不能直接作为 Stage 1 benchmark 输入

- X11 输入为 raw log。
- 没有窗口坐标归一化、键盘组合解析、click/drag 聚合或语义 target grounding。
- 截图、MP4 和 input log 尚未统一成可供 omni-model 推理消费、可审计的 trajectory
  artifact。

### 17.6 Recorder 覆盖范围不完整

- 只有默认 runner 使用统一 recorder。
- Agent-specific runner 仍需迁移。
- `semantic_action`、`verification` 和 `window` 字段多数尚未填充。

### 17.7 Phase 0 视频不是实际操作视频

- 当前 MP4 是合成的 before/after 说明卡。
- 适合验证视频文件流和任务 contract。
- 不适合研究 shortcut、鼠标效率或 GUI grounding。

## 18. 建议的下一步（历史计划，已被 2026-08-03 转向取代）

### P0：解决运行环境与测试覆盖

工作：

- 将计算节点 `osworld_env` 升级到 Python 3.12，或明确支持 Python 3.10。
- 在最终选定环境中运行默认 runner 测试。
- 为 Daytona tunnel、screenshot timeout 和 soak report 增加独立单元测试。

完成标准：

- 不再出现 Python 版本导致的 test skip。
- Phase 0 定向测试全部通过。
- CI/计算节点使用同一个 Python minor version。

### P0：实现 video context adapter

工作：

- 在 `run_multienv.py` 或 agent adapter 层读取
  `task["video_learning"]["demo_video"]`。
- 实现固定 FPS/关键帧/变化点采样。
- 定义视频帧、时间戳和 task instruction 的模型输入格式。
- 记录视频预处理时间和 token/frame budget。

完成标准：

- 支持视频模型的 Agent 能在不操作 VLC 的情况下收到演示帧。
- 日志能证明实际发送了哪些帧。
- 同一个 task 可运行 `no-video` 和 `video-context` 两种条件。

### P0：把人工轨迹归一化

工作：

- 解析 `xinput test-xi2`。
- 统一键盘 press/release 和 modifier。
- 将连续 pointer motion 聚合为 drag。
- 将 click 与最近截图/窗口状态对齐。
- 输出 trajectory-event Schema 的 action events。

完成标准：

- 一个 manual episode 可转换为完整的 observation/action/result JSONL。
- 原始日志和 normalized event 可以双向追踪。
- 时间对齐误差有可测量上限。

### P1：实现 SkillIR compiler

建议先拆为两个可诊断阶段：

1. Video/before-after/trajectory → candidate goal and parameters。
2. Candidate representation → validated SkillIR。

工作：

- 从 before/after Office 文件提取属性 diff，建立精确 supervision。
- 从视频和轨迹提取操作顺序与对象匹配。
- 将多个演示合并成带 fallback 的技能图。
- 使用 Schema 校验和 evaluator 反向验证候选 SkillIR。

完成标准：

- 四个 Phase 0 task 的自动编译 SkillIR 与人工 gold 在关键参数和 invariants 上一致。
- 对内容替换后的文件仍能表达正确 transfer rule。

### P1：实现 SkillIR executor

工作：

- 将语义 target 映射到当前 Office UI 对象。
- 支持 select、format、save、verify。
- 增加观察点和失败恢复。
- 同时记录 semantic action 和 raw pyautogui action。

完成标准：

- `compiled` delivery mode 能执行四个 Phase 0 SkillIR。
- 四个 task 均通过 evaluator。
- 执行轨迹包含 verification 和 recovery 信息。

### P1：扩展到真实 MVP 数据集

建议规模：

- Impress 12 个任务。
- Calc 12 个任务。
- 每个 transfer family 至少包含不同内容、不同对象位置和轻微布局变化。

数据要求：

- 真实 GUI 操作视频。
- demo-before/demo-after。
- test initial/gold。
- task JSON。
- SkillIR gold。
- 至少一条成功人类轨迹。

Split 要求：

- 按模板、内容来源和 transfer family 分组。
- 同源模板不能跨 train/test。
- 增加内容替换任务，防止坐标或文字记忆。

### P1：统一效率评测

从 normalized trajectory 计算：

- success rate。
- executable action count。
- observation count。
- model call count。
- model/grounding/environment/settle latency。
- active execution time。
- wall clock。
- 相对人类动作数和时间的倍率。

建议同时报告 Pareto frontier：

- 准确率。
- 动作数。
- 时间。
- 成本。

不要只报告最短轨迹；需要保留关键 verification，评估效率提升是否牺牲鲁棒性。

### P2：研究实验

建议最小对照组：

- Instruction only。
- Instruction + raw video。
- Instruction + sampled frames。
- Instruction + gold SkillIR。
- Instruction + compiled SkillIR。
- Instruction + retrieved human trajectory。

核心研究问题：

- 视频是否提高最终状态复现。
- SkillIR 是否保留视频增益并降低推理成本。
- 人类轨迹是否能减少动作数而保持准确率。
- 多条成功轨迹组合是否比单条最短轨迹更鲁棒。

## 19. 推荐的接手顺序

1. 阅读 `plan.md` 的研究目标和 Phase 1。
2. 运行本地 fixture/validator。
3. 复查本地 `results/` 中三个 Daytona 报告。
4. 手工删除遗留的 `osworld-smoke-4cb8902168`。
5. 解决 Python 版本不一致。
6. 实现 video context adapter。
7. 用 `manual_explore.py` 采集第一条真实 GUI 演示。
8. 实现 xinput normalization。
9. 实现 Phase 0 SkillIR compiler/executor。
10. 再扩展 Phase 1 数据规模。

## 20. 不应误删或误改的内容

- 不要提交 `daytona_key.sh`。
- 不要删除 `osworld-video-office-v1`，除非已经构建并验证替代 snapshot。
- 不要把本地 fallback 当作 Daytona 原生 evaluator 结果。
- 不要在没有重新生成 manifest 的情况下手工修改 Office fixture。
- 不要在没有迁移 agent-specific runner 前假设所有 Agent 都产生统一 trajectory。
- 不要删除原始 `traj.jsonl`，现有 OSWorld 工具仍可能依赖它。
- 不要删除固定 60/20 秒 sleep，除非同时做兼容性实验并更新 timing policy。

## 21. 交接结论（历史）

Phase 0 已经完成“契约、可复现环境、轨迹记录、四个种子任务和 evaluator 验收”。
这段历史结论原本建议把演示视频直接接入 Agent；当前方向已由文首的两阶段纯推理
benchmark 取代。后续复用 Phase 0 时，应把真实人类 GUI trajectory 规范化为 Stage 1
输入，并把 SkillIR 视为冻结的推理产物，不增加任何训练路径。
