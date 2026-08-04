# OSWorld 专家轨迹技能学习 Benchmark 开发计划

更新日期：2026-08-04

## 2026-08-04 当前实施主线：Reference Task Construction Pilot

当前第一阶段不执行 downstream agent，也不实现完整的 Stage 1/Stage 2 benchmark
实验。近期目标是先验证 reference task 的构建与人工标注流程：

```text
3 个 LibreOffice Calc OSWorld-Human task
→ instruction + single-action
→ LLM 提取英文 app-operation skills
→ 同 app 随机组合 2–5 个 skills
→ LLM 生成非 1:1 reference task
→ 人工审核与 Pilot coverage
→ 人工寻找/制作 artifact
→ setup-only OSWorld config
→ AWS 专家标注与录屏
→ 第二位标注者本地看视频并交叉验证
```

本阶段不训练模型，不测试 agent 执行，也不要求 reference task 有自动 evaluator。旧的完整
reference-video-to-skill-to-agent 协议继续作为后续 benchmark 目标保留，但在本 Pilot 完成前
不是实施优先级。

### P0. 已冻结的 Pilot 决策

- 源任务固定为 3 个 `libreoffice_calc` OSWorld task；具体 task IDs 必须显式指定，工具不
  随机替用户挑选；
- construction LLM 只接收原 instruction 与 `human-ground-truth.single-action`；task ID、
  app 和 action provenance 由本地可信代码附加；
- 只提取 `app_operation` skills，排除业务计算、事实、任务目标和完整 end-to-end 解法；
- skill 粒度小于完整任务、大于单一 click/type；procedure 必须包含具体操作和例子；
- skill 持久化字段为 `app/name/procedure/efficiency_tip/source(task_id, action_ids)`；
- Pilot 不做 semantic deduplication；
- reference task 只能组合同一 app 的 2–5 个 skills，组合不自然时允许拒绝生成；
- 不复用原 artifact、关键 literals 或完整有序源解法；单一源任务占比只作人工审核参考，
  不作自动 hard reject；
- Pilot coverage 只要求每个 skill 至少进入一个人工批准的 reference task；
- skill、procedure、efficiency tip 和 reference instruction 统一使用英文；
- artifact 由 expert 在 Pilot 中人工寻找或制作，skill guide 只作参考，允许按实际 UI 调整；
- 标注脚本一键启动 AWS/noVNC 和 artifact，由终端 Enter 明确开始、停止录屏；
- 第二位标注者在本地观看 `recording.mp4`；只有检查或复现 artifact 时才启动 AWS 环境；
- metadata、task config、artifact 和 MP4 先推送 GitHub remote；若普通 Git 不适合视频大小，
  再切换 Git LFS 或对象存储；
- construction client 使用 Python OpenAI-compatible API、async 并发、独立 `.txt` prompts、
  schema validation、逐次调用 token/cost 日志，并预留但不启用 video input；
- 默认 construction model 为 `gpt-5.6-terra`，`gpt-4.1` 和其他 compatible model 通过
  配置切换。模型价格必须使用有日期的独立配置，未知模型不得猜价。

### P1. 实施阶段

1. **C0 数据契约与 prompts**
   - Skill、LLM extraction response、reference candidate 和 review JSON Schema；
   - 独立 `prompts/*.txt`；
   - dated pricing table、prompt/version provenance 和最小测试。
2. **C1 OSWorld-Human importer 与 skill extraction**
   - 显式加载 3 个 Calc task；
   - 严格构造 `instruction + indexed single steps` 输入；
   - OpenAI-compatible `AsyncOpenAI`、concurrency semaphore、retry、structured JSON；
   - 本地注入 source task/action IDs，输出 Pilot skill pool 和逐 attempt cost log。
3. **C2 Reference task generation**
   - seeded same-app 2–5 skill sampler；
   - natural-task generation/rejection；
   - literals、ordered sequence 等自动提示与人工 similarity checklist；
   - rejected skills 返回 pool，达到 max attempts 时输出 unresolved list。
4. **C3 Human review 与 coverage loop**
   - approve/reject、review notes、covered skill IDs；
   - 每个 skill 至少一次 approved coverage；
   - 不在 Pilot 引入多次覆盖或复杂 balance 指标。
5. **C4 Artifact intake 与 setup-only task package**
   - expert 人工指定 artifact；
   - SHA256、敏感信息检查和 Git 文件大小预检；
   - 生成只含 snapshot/instruction/config/related_apps/reference metadata 的 OSWorld config，
     不含 evaluator。
6. **C5 AWS annotation runner**
   - 复用 `manual_explore.py`、AWS provider、noVNC 与 controller recording；
   - reset 后等待专家 Enter 才开始视频、截图和 input-event 采集；
   - 再次 Enter 后停止、下载 artifacts、写 manifest 并关闭实例/保留 TTL 兜底。
7. **C6 Cross-validation**
   - reviewer 本地观看视频和 skill cards；
   - 可选一键启动相同 initial artifact 环境进行检查/复现；
   - 输出 approved/rejected、covered、missing/incorrect skills 与 notes。
8. **C7 Pilot 验收**
   - 3 个 Calc task 可重复导入；
   - 所有 skill 均有可信 provenance 且至少一次 approved coverage；
   - reference bundle 可从 GitHub 拉取；
   - 两位标注者可以完成录制和交叉验证；
   - 每个 LLM attempt 有 prompt/model/token/cost/status 记录。

### P2. 当前开发状态

- [x] C0 的代码目录、Skill/source models、JSON Schema、英文 prompt 和 dated pricing table；
- [x] C1 的 OSWorld-Human importer、严格 prompt boundary、异步 compatible client、逐 attempt
  cost log 与显式 3-task CLI 基础；
- [x] 选择并冻结 3 个具体 Calc source task IDs：`035f41ba-...`（formula/autofill/
  cross-sheet）、`8b1ce5f2-...`（conditional formatting）、`1954cced-...`（Pivot Table）；
- [x] 将 3 个 source tasks 的 40 个 `single_actions`、原文件路径和 SHA256 复制进自包含
  manifest，并支持与 pinned OSWorld-Human clone 核验；
- [x] 使用真实 OpenAI API 完成 atomic skill extraction 和开发者质量检查：12 skills、38
  substantive source actions、2 scaffolding actions、0 duplicate assignments；最终 accepted
  run `$0.034368`，含此前 prompt 迭代的总开发成本 `$0.209436`；
- [ ] C2 reference task sampler/generator；
- [ ] C3 review/coverage loop；
- [ ] C4-C6 annotation package、AWS runner 和本地 cross-validation；
- [ ] C7 Pilot 验收。

## A. Benchmark 定位

当前首要方向从 PowerPoint `video-to-design/video-to-animation` 转为：

> 评测 omni-model 能否从专家操作轨迹中归纳高效、可迁移的 computer-use skill，
> 并通过该 skill 帮助固定 downstream agent 更准确、更高效地完成原始 OSWorld 任务。

本项目只构建 benchmark、数据、推理协议、baseline 和 evaluator，不进行 SFT、RL、
微调或任何模型训练。参评 omni-model 在 inference 阶段读取专家轨迹并生成 skill；
downstream agent 在 inference 阶段消费该 skill。模型如何获得能力不属于本项目范围。

PowerPoint Web、AWS 环境、动画 evaluator 和旧 video-learning Phase 0 不删除，继续
作为已完成基础设施和未来可复用 task domain；原 W2-W5 暂停。

本项目直接扩展 OSWorld，不另造一套替代任务。目标 task、instruction、initial state、setup
和 final-state evaluator 均沿用 OSWorld；新增的是专家轨迹标注、拆分重组后的 reference
video bank、skill induction 和效率评测。

## B. 两阶段评测协议

```text
OSWorld-Human 标注或人工录制的完整专家轨迹
        ↓ 拆分为 action group / subskill，并跨轨迹重组
reference video bank（不含 1:1 完整解法）
        ↓
omni-model skill induction（inference only）
        ↓
frozen skill artifact
        ↓
fixed omni-agent + 原始 OSWorld target task
        ↓
OSWorld task evaluator + efficiency evaluator
        ↓
相对同一 agent/no-skill baseline 的 accuracy 与 efficiency uplift
```

### B.1 Stage 1：Skill induction

Omni-model 接收为 target 构建的若干 reference videos。每个视频只展示一个或多个操作
片段，这些片段分散来自不同专家轨迹或不同上下文；任何单个视频都不能构成 target 的
完整、有序 golden solution。第一阶段可同时提供 target instruction，帮助模型从 reference
bank 中选择相关操作，但不提供 target 的 hidden evaluator state 或完整操作顺序。

Reference bank 的源信息可包含：

- raw/per-task/multi-task video；
- 对齐截图或采样帧；
- normalized semantic actions 和 action groups；
- 片段所在原始 task 的局部上下文、成功结果和必要的时间边界。

模型必须输出冻结、可审计的 skill artifact。第一版支持：

- bounded text playbook；
- schema-validated structured SkillIR。

Skill induction 在 target episode 开始前完成。模型不得看到未拆分的 target expert video、
完整 ordered action list、gold artifact 或 evaluator state。Skill artifact 一经生成，在同一
benchmark cell 中不得针对单次 rollout 手工修改。

### B.2 Stage 2：Downstream execution

固定 downstream agent 接收 target instruction、正常 observation 和 Stage 1 的 skill
artifact，在原始 OSWorld target task 上执行。Benchmark 比较同一个 agent、同一个 target、
同一环境与预算下的 paired rollout：

- without skill；
- with learned skill；
- with control/oracle skill。

核心被测对象是 omni-model 产生的 skill utility，而不是 downstream agent 的绝对能力。
报告必须分离 skill induction 的 token/latency/cost 与 downstream execution 的
token/latency/cost；可额外报告 skill 被多个 target 复用后的 amortized cost。

## C. 数据与 contamination 边界

截至 2026-08-03，`WukLab/osworld-human` 已公开原 OSWorld 369 个任务的人工
`single-action`、`grouped-action` 标注和 WES scorer，但没有公开真实逐帧视频、坐标、
输入事件、时间戳或完整 state-action episode。

官方仓库明确说明这些标注不应被用于训练；本项目没有训练环节。对 pilot 中选定的
OSWorld task，标注按以下优先级使用：

1. 若 OSWorld-Human 提供可用的 `single-action` / `grouped-action` golden 标注，则复用其
   操作语义、最短步骤与分组边界；由于仓库没有原始视频、坐标和完整 state-action event，
   仍需在 OSWorld 环境中人工 replay 并录制；
2. 若没有对应标注或粒度不足，则人工完成并标注该 OSWorld task 的专家轨迹；
3. 完整轨迹只保存在 hidden provenance/evaluator 区，不直接提供给参评模型；模型只能看到
   由 action group/subskill 拆分、跨轨迹重排后生成的 reference videos。

主 benchmark 条件必须满足：

- reference 和 target 不是一条完整轨迹对一个任务的 1:1 replay；
- 任何单个 reference video 都不包含 target 的完整 ordered solution；
- target 所需操作被拆散到至少两个 reference videos，并混合不同上下文或无关片段；
- reference video 顺序不编码 target action 顺序，不显示 hidden gold artifact；
- manifest 记录每个片段来自哪条专家轨迹、原 action group、剪辑边界和重组方式；
- 报告 `operation coverage`、最长有序公共子序列和 task-specific visual overlap，量化泄漏风险。

完整 golden video 只可作为 diagnostic upper bound，必须单独标记，不能计入主 benchmark
结果。项目不建立训练集，所有轨迹和视频仅用于 inference-time benchmark context 与评测。

任何 OSWorld-Human 数字都必须标明 single-action 或 grouped-action WES 以及所用版本。

## D. Benchmark 任务单元

每个 benchmark task 继续对应一个原始 OSWorld task，并至少包含：

- `osworld_task`：原 task ID、instruction、snapshot、setup 和 evaluator；
- `expert_trajectories`：OSWorld-Human 标注或人工录制的完整专家轨迹，仅构建/evaluator 可见；
- `skill_fragments`：按 action group/subskill 拆出的带 provenance 片段；
- `reference_videos`：跨轨迹、跨上下文重组后的多个可学习视频；
- `hidden_target_expert`：仅 efficiency evaluator 可见的完整高效参考；
- `skill_contract`：允许的 text/SkillIR 长度、schema 和禁止信息；
- `downstream_agent_config`：固定 agent、模型、action space 和预算；
- `evaluator`：最终状态 accuracy + trajectory efficiency；
- `provenance`：轨迹来源、采集者、环境、时间、OSWorld-Human 版本、片段映射和重组 seed。

Reference 难度分层：

- R0 `golden_replay`：完整 1:1 golden video，仅用于检查视频理解/执行上界；
- R1 `ordered_fragments`：拆成多个视频但仍按 target 顺序排列，作为弱诊断；
- R2 `recomposed`：操作片段分散、乱序并处于不同上下文，作为第一阶段主条件；
- R3 `recomposed+distractors`：加入相似但无关操作、恢复片段或 UI 变化，测试选择与组合。

正式主分数不包含 R0；第一阶段以 R2 对 C0 no-reference 的增益为核心。

## E. 现有代码支持度

### E.1 可直接复用

| 能力 | 位置 | Benchmark 用途 |
| --- | --- | --- |
| Task setup 与最终状态 evaluator | `desktop_env`、`evaluation_examples` | accuracy gate |
| 统一 episode/event recorder | `desktop_env/trajectory/recorder.py` | expert/agent 同构记录 |
| actor、`group_id`、纳秒时间 | trajectory-event v1 | action group 与时延对齐 |
| plan/action/observation/result events | `lib_run_single.py` | downstream 执行记录 |
| 视频、截图、A11y、raw trajectory | runner/controller | expert context modalities |
| 人工演示和 guest input capture | `scripts/python/manual_explore.py` | expert trajectory 采集 |
| SkillIR schema | `evaluation_examples/video_learning/schemas` | skill artifact contract |
| AWS/Daytona 环境与录屏 | providers | 可复现实机 benchmark |
| Office/PowerPoint tasks | Phase 0、W1 | pilot family 候选 |

### E.2 部分支持与缺口

- 人工采集能得到 MP4、周期截图和 `xinput`，但还不能输出完整 semantic action groups。
- 默认 runner 写 normalized events，多数 agent-specific runner 尚未统一。
- `group_id` 已存在，但还没有 frozen skill artifact、skill provenance 和 condition ID。
- 缺少 benchmark orchestrator：Stage 1 生成一次 skill，Stage 2 在多个 target/seed 复用。
- 缺少 no-skill/learned/raw/oracle/mismatched 条件的 paired result aggregator。
- 缺少 expert trajectory replay、fragment cutter/recomposer 和 reference leakage report。
- 缺少统一 efficiency report 与 OSWorld-Human scorer parity。
- 缺少 text/SkillIR/video/long-video 的统一 context-budget adapter。

结论：现有代码库足以支撑 expert capture、downstream execution 和 accuracy gate；需要
新增的是 benchmark orchestration 与 evaluator，而不是模型训练系统。

## F. 指标与因果归因

每个 condition 至少报告：

- task success / 原 OSWorld evaluator score；
- raw executable action、decision/action-group、observation、model-call 数；
- planning、grounding、verification、environment latency；
- active execution time、wall time、token 和成本；
- 相对 hidden expert single/grouped step 的倍率；
- WES+、WES-、总 WES；
- 重复动作、无状态变化动作、回退和恢复数量。

Omni-model skill 的核心效果使用 paired uplift：

- `ΔSuccess = Success(with_skill) - Success(no_skill)`；
- `ΔWES = WES(with_skill) - WES(no_skill)`；
- decision/model-call/action/time/cost 的相对变化；
- 相对 oracle skill 的剩余 gap；
- mismatched skill 相对 learned skill 的下降，用于排除“只是多了一段提示词”。

Accuracy 与 efficiency 必须分别报告，并展示 Pareto frontier。效率提升只有在 success
non-inferiority 成立时才可作为正面结论。关键 condition 对同一 target 做 paired seeds；
不得通过缩短 `max_steps`、跳过保存/验证/evaluator 或修改 downstream agent 来制造 uplift。

## G. 必要对照组

- C0 `no_skill`：downstream agent 只接收 target instruction；
- C1 `golden_video_upper_bound`：完整 1:1 golden video，仅作 diagnostic，不进入主分数；
- C2 `recomposed_video_direct`：重组 reference videos 直接给 omni-agent；
- C3 `learned_text_skill`：omni-model 输出 bounded text playbook；
- C4 `learned_structured_skill`：omni-model 输出 schema-valid SkillIR；
- C5 `oracle_skill`：人工编写但不泄露 target-specific 解法的可迁移 skill；
- C6 `mismatched_skill`：来自其他 family 的同长度 skill；
- C7 `empty/length_control`：与 learned skill 等长度但无操作信息的文本。

专家 context modality 另做正交 ablation：structured events、sampled frames、per-task video、
多任务 long video。这样才能区分“omni-model 学到了 skill”与“downstream agent 直接模仿
raw demo”或“只是获得了更多 token”。

多任务长视频必须包含 task/time/action-group index；同时限制总 frame/token budget，
并与等预算的分段视频、采样帧和 structured trajectory 比较。

## H. 分阶段实施

### Phase E0：3-task pilot contract

- 从现有 OSWorld 中人工选择 3 个任务，不修改其 instruction、setup 和 evaluator；
- 冻结 expert/fragment/reference-video/skill-artifact contract；
- 定义 action、decision group、model call 和 active/wall time 口径；
- 定义 R0-R3、C0-C7、provenance、reference leakage audit 和 result schema；
- 冻结一个 video-capable Qwen omni-model 与一个 Qwen-based omni-agent 的具体版本、prompt、
  decoding 和执行预算。

退出条件：metric contract、skill schema、paired condition 和 leakage rules 都有测试；
3 个 task 的原始 OSWorld evaluator 可重复运行。

### Phase E1：3-task expert trajectory annotation

- 检查 3 个 task 是否有 OSWorld-Human golden action/group 标注；
- 有则人工 replay 并录制，无或粒度不足则自行完成专家操作并标注；
- 每个 task 至少得到一条 evaluator 成功的完整专家轨迹；
- 将 `xinput`、截图、MP4、semantic actions 和 evaluator result 对齐；
- 标注 action group、state boundary、shortcut、verification 和 recovery。

退出条件：3 条专家轨迹均通过原始 task evaluator；每个 action group 可追溯到视频时间、
输入事件和 OSWorld-Human 标注或人工标注来源。

### Phase E2：Fragment/recompose reference videos

- 将每条完整专家轨迹按 action group/subskill 拆分；
- 把 target 所需操作分散到多个视频，跨 task/trajectory 重排并加入必要上下文；
- 生成 R0-R3 reference set 和 machine-readable fragment manifest；
- 自动检查完整 ordered solution、视频顺序、视觉状态和 action overlap。

退出条件：R2 中无单个视频含完整解法，target 操作覆盖分散到至少两个视频，重组可由
manifest 确定性复现。

### Phase E3：Qwen inference pilot

- 固定 omni-model inference interface 和 context budget；
- 实现 text playbook 与 SkillIR 两种 frozen artifact；
- 记录 reference video/fragment IDs、prompt/model/version、token/latency/cost 和 artifact hash；
- 由选定 Qwen omni-model 读取 reference videos 生成 skill；
- 由固定 Qwen omni-agent 在 3 个原始 OSWorld task 上执行 C0-C6 paired runs。

退出条件：得到 no-reference、R2 recomposed、mismatched 和 R0 golden upper-bound 的首份
accuracy/efficiency 对照结果；无论是否提升都保存可诊断 artifacts。

### Phase E4：Downstream paired evaluation and scale-up

- 固定至少一个 downstream agent；
- 对 C0-C7 做 paired task/seed 执行；
- 汇总 accuracy/efficiency uplift、oracle gap 和 mismatched control；
- 比较 structured、frames、per-task video 和 long-video source context。

退出条件：至少一个 learned-skill condition 在 success 不下降的前提下减少 decision step、
model call 或 active time；若无提升，也能定位是 induction、skill contract 还是 agent use
失败。

- 扩展 OSWorld task、application、reference 难度和 downstream agents；
- 校准 expert efficiency、人工 skill oracle 和 evaluator 可靠性；
- 做 contamination audit、重复运行、bootstrap confidence interval 和人工 error review；
- 发布 benchmark card、数据 provenance、baseline 和复现命令。

退出条件：benchmark 能稳定区分 no-skill、learned、mismatched 和 oracle；结论跨多个
downstream agent 不完全反转；所有模型交互均为 inference-only。

## I. 近期执行清单

1. [ ] 从现有 OSWorld 选择 3 个 pilot task 并冻结原 task/evaluator 版本。
2. [ ] 核对这 3 个 task 的 OSWorld-Human golden action/group 标注覆盖。
3. [ ] 人工 replay/标注并录制 3 条 evaluator-success 专家轨迹。
4. [ ] 实现 action-group fragment manifest 与 R2 reference video recomposer。
5. [ ] 冻结 Qwen omni-model、Qwen omni-agent、prompt 和 budget。
6. [ ] 跑 C0 no-reference、R2 recomposed、mismatched 和 R0 golden upper-bound。
7. [ ] 输出 3-task accuracy、WES、action/group/model-call/time/cost 与泄漏诊断报告。

---

# 历史计划：PowerPoint Web Video-to-Animation（已暂停，内容保留）

以下 W0/W1 结果仍有效；W2-W5 暂停，未来可作为高效轨迹学习的 PowerPoint 应用域。

## 1. 项目目标

项目暂时只研究一个场景：

> 在 AWS Ubuntu 环境的 PowerPoint for the web 中，根据参考视频复刻较复杂的排版和
> 动画效果，同时保持初始 PPT 的内容、颜色和素材，输出可继续编辑的 `.pptx`。

开发链路：

```text
initial.pptx + reference.mp4 + short instruction
        ↓
OSWorld 官方 Ubuntu AMI + Chrome + PowerPoint Web
        ↓
上传、编辑、播放、录制、下载
        ↓
PPTX 结构评测 + 浏览器渲染视频评测 + 内容保持 gate
```

原 Windows Server + Office LTSC 路线因固定成本过高而取消。LibreOffice Impress
继续作为离线开发和兼容性诊断工具，不作为主执行应用。旧 HKUST HPC + Daytona 流程
归档在 `hkust_hpc developer.md`，历史状态见 `handoff.md`。

## 2. 范围

### 2.1 当前包含

- AWS EC2 Ubuntu，优先复用 OSWorld 官方 AMI。
- Chrome 中的 PowerPoint for the web。
- 输入：初始 PPT、参考视频、短指令。
- 输出：从 PowerPoint Web 下载的原生 `.pptx`。
- 从视频理解对象角色、布局、进入/强调/退出方式、顺序和节奏。
- 保持初始 PPT 的文本、颜色、图片和其他素材。
- OOXML 动画结构、静态布局和浏览器播放视频的混合评测。

### 2.2 第一版动画边界

允许：

- Appear、Fade、Fly、Wipe、Split、Zoom 等网页端可添加效果；
- On Click、With Previous、After Previous；
- Duration、Delay、顺序和单对象多效果；
- 网页端可编辑的 slide transition。

暂不包含：

- animation trigger；
- 桌面 PowerPoint 专有效果；
- Morph；
- VBA、add-in、ActiveX；
- 音频同步、复杂媒体控制；
- Calc、Excel、GIMP、VLC；
- 大规模轨迹训练或 SFT。

任务必须匹配 PowerPoint Web 实际能力，不能把桌面端效果当作 Agent 必须完成的目标。

## 3. 当前基础与缺口

### 3.1 可复用

- Video-learning task、SkillIR 和 trajectory event v1 schema。
- `TrajectoryRecorder`、统一计时和 episode manifest。
- `manual_explore.py` 的任务加载、截图、录屏与 evaluator 入口。
- OSWorld AWS manager/provider、TTL 和官方 Ubuntu AMI。
- Chrome、文件上传/下载和现有 browser automation 能力。
- `compare_pptx_files` 的文本、形状和静态几何比较。
- Phase 0 的 initial/gold 双向 evaluator 验证方法。

### 3.2 关键缺口

1. 还没有最小正式 PowerPoint Web task/config。
2. 还没有正式 OOXML animation timeline parser 和 rendered evaluator。
3. 还没有 session 过期检测、AMI 轮换和敏感镜像删除工具。
4. PowerPoint Web 会持续更新，不能像桌面 Office 一样固定 build。
5. `compare_pptx_files` 和 `check_transition` 不足以评测 animation timeline。
6. 已验证的浏览器播放、点击、录制和下载流程还没有固化为 runner 协议。

下一优先级是把已验证的低成本单实例闭环固化为 task、runner 和 evaluator。

## 4. 系统设计

### 4.1 本地控制面

本地负责代码、task/evaluator、AWS API、结果回收和离线评测。只安装最小 Conda
开发环境，不安装完整 OSWorld GUI 或模型依赖。

本地不得保存明文 AWS 密钥、Microsoft 密码、cookie 或 session token。AWS 使用
IAM Identity Center profile `osworld-dev`。

### 4.2 AWS 执行面

每个 environment 从 OSWorld 官方 Ubuntu 1920×1080 AMI 启动，包含：

- OSWorld server/controller；
- Chrome；
- screenshot、输入、文件传输和录屏；
- benchmark 字体和媒体工具；
- 1920×1080、固定 locale/timezone；
- 受控的 PowerPoint Web authenticated browser profile。

PowerPoint Web 是在线服务，无法固定后端 build。每个 run 必须记录浏览器版本、运行
日期和可见 UI 版本；gold 与 candidate 尽量在同一时间窗口和相同执行镜像中播放。

### 4.3 Microsoft 测试账户

- 新建专用免费 Microsoft 账户，不使用用户个人主账户。
- 账户无私人文件、邮件、联系人和付款信息。
- OneDrive 只保存当前 benchmark 的临时输入与输出。
- authenticated profile 视为 secret，只存在于私有镜像或受控存储。
- 密码、MFA、cookie 和 token 不进入代码、task、日志或公开 artifact。
- Session 失效必须显式失败并人工更新，不能静默使用匿名或错误账户。

### 4.4 生命周期与网络

- 开发期 `num_envs=1`。
- default VPC + public subnet；专用 security group 仅允许当前出口 IP `/32`。
- 不使用 `0.0.0.0/0` 暴露管理或 OSWorld 端口。
- 正常退出主动 terminate；180 分钟 TTL 处理异常退出。
- 每次运行后审计 EC2、EBS、ENI、Elastic IP 和 scheduler。
- 每个 task 下载结果后删除 OneDrive 临时文件。

## 5. AWS 成本基线

冻结配置：

- region：`us-east-1`；
- instance：OSWorld 仓库官方默认 `t3.xlarge`；
- root volume：30 GiB gp3，4000 IOPS / 1000 MiB/s；
- TTL：180 分钟；
- 项目 Budget 警戒线：`USD 20/月`，仅统计
  `Project=OSWorld-PPT-Web`；
- 不创建 Managed AD、Office LTSC 或 RDS SAL。

粗略成本：

| 配置 | 3 小时单次 | 20 次/月 |
|---|---:|---:|
| 官方 `t3.xlarge` + 官方 gp3 性能 + public IPv4 | 约 `$0.75–0.80` | 约 `$15–16` |

manager/provider 已通过统一的 `launch_config.py` 读取实例和磁盘配置；EC2 DryRun
已验证启动参数有效。2026-07-29 的实测表明降到 `t3.large` 和基线 gp3 不能解决
readiness 问题，因此恢复官方规格并通过实际 EC2/EBS describe 验证。

2026-07-30 发现原 `osworld-ppt-web-monthly` 没有 cost filter，邮件中的
`$198.63 actual / $218.75 forecast` 是整个 AWS 账户的费用，不是本项目 W1
费用。其 actual/forecast 通知已关闭。项目专属配置已由
`scripts/python/setup_aws_project_budget.py` 准备；待 Billing 发现并激活
`Project` 成本分配标签后才应用，避免创建一个暂时统计不到费用的 Budget。

## 6. PowerPoint Web 任务定义

### 6.1 任务语义

参考视频表达动画与排版规则，而不是要复制的文字和颜色。Agent 必须：

- 识别参考中的标题、正文、图片、装饰形状等对象角色；
- 推断空间关系、z-order、进入/退出方式、并行关系和节奏；
- 将这些规则映射到初始 PPT 的不同内容；
- 保持初始 PPT 的文字、颜色和媒体；
- 使用原生可编辑对象和动画，不得用整页图片、GIF 或视频作弊；
- 从 PowerPoint Web 下载到指定 `.pptx`。

### 6.2 Hidden gold

```text
Agent 可见：
  initial.pptx + reference.mp4 + short instruction

Evaluator 可见：
  gold.pptx + gold browser render + structural rubric
```

Gold 由人工在同一 PowerPoint Web 能力边界内制作。每个动画族映射到至少两个不同内容
的 initial，验证迁移而不是像素复制。

### 6.3 难度

1. Tier A1：单页、自动播放、4–7 个对象、基础 entrance/exit。
2. Tier A2：单页、多个效果、并行/串行、Duration/Delay。
3. Tier B：多个 click group 和网页端 transition。
4. Tier C：多页动画一致性。

Morph、trigger、motion path 等桌面专用或网页端不可编辑能力不进入当前 benchmark。

## 7. 混合评测

### 7.1 Gate 0：有效性

- 下载的 `.pptx` 可打开且不要求修复；
- 浏览器 slideshow 能完整播放；
- 文件保存到正确位置；
- 输出不是整页栅格、视频或 GIF；
- task 云端副本和输出 artifact 可对应。

### 7.2 Gate 1：内容保持

- 文本 token 保持；
- 图片/媒体 hash 保持；
- 主题色和对象颜色在容差内保持；
- slide 数量和顺序保持；
- 非目标对象没有额外变化；
- 目标对象仍可编辑。

Gate 失败时不得进入高分区间。

### 7.3 Layout

按文本 hash、图片 hash、对象类型和角色匹配候选与 gold，比较：

- 中心点、宽高、旋转和裁剪；
- z-order、grouping、对齐和间距；
- 最终关键帧；
- 文本越界、遮挡和可读性。

### 7.4 Animation structure

解析 `.pptx` OOXML `<p:timing>` 与 `<p:transition>`：

- target object；
- effect family；
- On Click / With Previous / After Previous；
- click group、顺序和并行关系；
- duration、delay、repeat；
- transition。

结构报告拆成 Coverage、Order 和 Detail。第一版不依赖 PowerPoint COM。

### 7.5 Rendered behavior

Gold 和 candidate 在同一 Ubuntu AMI、Chrome 配置、分辨率和录制协议中播放：

- 只比较 animated region；
- appearance 使用感知特征和受约束 DTW；
- temporal 使用方向、速度、可见面积和对象 mask 时间序列；
- click group 分段，不允许 DTW 跨组匹配；
- 同时报告原始总时长误差，防止 DTW 掩盖错误节奏。

主报告保留 Preservation、Layout、Animation Coverage、Order、Detail、Rendered
Appearance、Rendered Temporal 和 Robustness，不用单一像素分数替代诊断。

## 8. 分阶段实施

### Phase W0：路径与成本决策

状态：已完成。

- [x] 主路径切换为 Ubuntu + PowerPoint Web。
- [x] Windows/Office license-included 路线取消。
- [x] `osworld-dev` SSO 和 `us-east-1` 确认。
- [x] 官方 OSWorld Ubuntu AMI 确认。
- [x] 官方 `t3.xlarge`、4000 IOPS / 1000 MiB/s gp3、180 分钟 TTL、
  `$20/月`警戒线冻结。
- [x] 专用 Microsoft 测试账户和安全边界冻结。
- [x] `scripts/python/preflight_aws_ppt_web_w0.py --stage w0 --strict` 通过。

### Phase W1：PowerPoint Web 单实例闭环

状态：已完成。2026-07-30 已通过核心闭环、私有加密 AMI session 恢复、正式诊断
task/evaluator 和 10 次 lifecycle soak。

交付物：

- [x] 关闭无 cost filter 的账户级 Budget 误报通知；
- [x] 准备按 `Project=OSWorld-PPT-Web` 过滤的项目 Budget 配置；
- [ ] Billing 激活 `Project` 成本分配标签并应用项目 Budget；
- [x] subnet 选择和 `/32` security group；
- [x] provider 可配置 instance type、连接模式和默认加密的基线 gp3；
- [x] reset 路径只创建一个 TTL schedule；
- [x] EC2 DryRun 验证官方 AMI 和启动参数；
- [x] TTL scheduler role、180 分钟 schedule 创建与失败清理；
- [x] 单实例 smoke 验证 EC2、EBS、TTL、noVNC 和 `/32` 网络；
- [x] 创建 SSM diagnostic instance profile，读取 `osworld.service` journal；
- [x] 当前实例完成 Microsoft 登录并确认 PowerPoint Web authenticated session；
- [x] 私有加密 AMI 持久化 authenticated Chrome profile；
- [x] upload/open/edit/slideshow/record/download smoke；
- [x] 最小 PowerPoint Web task；
- [x] 修复 `osworld.service` 在 X11 前启动并耗尽 systemd start limit 的竞争；
- [x] reset/close/失败路径删除对应 TTL schedule。

退出条件：

- [x] 一台全新实例无需个人账户介入即可恢复受控测试 session；
- [x] initial 上传并下载 round-trip 成功；
- [x] 添加一个动画后播放、录制、下载成功；
- [x] 下载的 `.pptx` 可通过 ZIP、`python-pptx` 和 OOXML timing 检查；
- [x] 正式 evaluator 可读取并评分；
- [x] 10 次 create/reset/close 无云资源残留；
- [x] Pricing API 当前配置折算 3 小时约 `$0.6884`，低于 `$0.80`。

2026-07-30 smoke 使用单页自制 fixture。标题对象成功写入并播放
`Fade / On Click / 0.50 s`；下载稿保留原始文字，OOXML 中存在
`clickEffect`、`animEffect filter="fade"` 和 500 ms timing。OSWorld 录屏生成
H.264、1920×1080、30 fps MP4。这验证了 Ubuntu + PowerPoint Web 主路径对
对象动画任务的技术可行性。

正式 W1 task ID 为 `5f24d8c2-4779-4f6d-9b8c-6e3bc97ed441`。initial 的
static-content/animation 分数为 `1/0`，gold 为 `1/1`。认证 AMI 不保证重跑
cloud-init UserData，因此 launch/reset 现在通过 SSM 主动安装、重启并验证 X11
等待 drop-in，UserData 仅作干净 AMI 后备。当前代码的 10 次 soak readiness 为
`98.143–186.995 s`，总墙钟约 38 分 47 秒；每轮均通过
TTL/API/GNOME-X11/drop-in/截图 gate，结束后 EC2/EBS/ENI/TTL schedule 全为 0。
Cost Explorer 对本次运行仍显示 `Estimated=true` 且尚未入账；实际账单值待延迟后
复核，不能用价格估算冒充。

这个单页 Fade task 是 W1 诊断 fixture，不是最终 fancy benchmark demo。复杂排版与
多对象动画仍由 W2/W3 实现和评测。

登录态 AMI 为 `ami-0c68ad8829df7c05e`
（`osworld-ppt-web-auth-20260730`），backing snapshot 为
`snap-0832dc22794c270f2`。AMI 与 snapshot 均加密、私有且未共享。从该 AMI 启动
全新实例并按 OSWorld 标准方式启动 Chrome 后，PowerPoint Web 直接恢复登录首页。
Conda 环境已设置 `AWS_AMI_ID`，provider 和主 runner 在该变量存在时优先使用私有
AMI，未设置时仍回退官方 `IMAGE_ID_MAP`。

### Phase W2：Evaluator v0

交付物：

- PowerPoint Web 标准播放/录制/下载协议；
- OOXML animation timeline parser；
- 内容/颜色保持 gate；
- Layout、Coverage、Order、Detail evaluator；
- rendered appearance + temporal evaluator 原型。

退出条件：

- 同一 gold 连续渲染 5 次方差低于阈值；
- 删除、换序、改时长、改颜色和栅格化反例均被检出；
- 合法但实现细节不同的结果不过度受罚。

### Phase W3：首批 demo

- 3 个公开许可或自制动画族；
- 每族 2 个不同内容 initial；
- 共 6 个 Tier A 任务；
- 每个任务包含 initial、reference、hidden gold、rubric 和来源 manifest；
- text-only、video、oracle rubric/SkillIR 三个基线。

### Phase W4：click group 与复杂网页动画

- Tier B 任务；
- 标准化点击协议；
- 分段录制和分段 DTW；
- click 数量、组间顺序和组内节奏的独立诊断；
- 自动评测与人工 pairwise judgment 校准。

### Phase W5：Agent 基线与规模化

- video context adapter；
- PowerPoint Web agent baseline；
- 单环境 soak 后受控并发；
- 成本、成功率和多维指标报告；
- 每个任务至少 3 次独立运行；
- 每次批量运行后云资源和 OneDrive 清理审计。

Desktop PowerPoint 只作为未来可选 validation backend，重新立项前不创建任何相关
AWS 许可资源。

## 9. 测试门槛

### 本地

- task/SkillIR/trajectory schema；
- AWS 配置和成本参数；
- OOXML timing parser fixtures；
- 内容、颜色、Layout、Coverage、Order、Detail 正反例；
- 不相关属性变化的容忍。

### AWS smoke

- EC2 创建/readiness/Chrome/截图；
- PowerPoint Web session health；
- 上传、打开、保存、下载；
- slideshow 和录屏；
- evaluator artifact 回收；
- SIGINT、异常、超时后的 terminate。

### AWS soak

- 10 次顺序 reset；
- 5 次相同 gold 渲染一致性；
- session 过期可诊断；
- 启动、episode、下载时间和费用；
- EC2/EBS/ENI/scheduler/OneDrive 清理。

## 10. 近期执行清单

1. [x] 修改 AWS provider：读取实例、连接和基线 gp3 配置。
2. [x] 配置 TTL scheduler IAM role。
3. [x] 关闭账户级 Budget 误报，准备 `$20` 项目专属 Budget，并创建 `/32`
   security group。
4. [ ] Billing 发现后激活 `Project` 成本分配标签，应用项目 Budget。
5. [x] 验证官方 OSWorld Ubuntu AMI、Chrome 和 PowerPoint Web 可访问。
6. [x] 使用当前 Microsoft 账户建立私有 encrypted authenticated AMI；
   批量运行前再评估迁移到专用测试账户。
7. [x] 跑通 `.pptx` upload/download round-trip。
8. [x] 跑通单动画 edit/slideshow/record/download。
9. [x] 跑通 10-reset 和异常清理。
10. [x] 实现 W1 所需的语义 OOXML animation timeline parser 和静态内容保持
    gate。
11. [ ] 扩展为 W2 Layout、Coverage、Order、Detail evaluator。
12. [ ] 制作第一个真正需要视频描述的 Tier A fancy hidden gold demo。
11. [ ] 实现 Animation2Code 风格 rendered evaluator 原型并用反例校准。

第 8 项完成前不批量制作任务；第 11 项完成前不运行大规模 Agent benchmark。

## 11. 主要风险

| 风险 | 缓解 |
|---|---|
| PowerPoint Web UI 持续更新 | 记录浏览器/日期/UI，gold 与 candidate 同窗口重渲染 |
| Microsoft session 过期或触发 MFA | 专用账户、session health check、显式失败、人工续期 |
| Agent 接触个人云数据 | 不使用个人账户；测试账户无私人数据 |
| 网页版能力不足以复刻参考 | 数据生成时做 capability gate，超范围参考不入库 |
| OneDrive 自动保存但下载失败 | 下载 artifact hash/存在性作为完成条件 |
| PPTX 动画 OOXML 与网页播放不一致 | 结构 + 浏览器 render 双评测 |
| gp3 或实例过度配置 | provider 参数化并用 Budget/manifest 记录实际成本 |
| 公网端口暴露 | `/32` security group，后续评估私网/SSM |
| EC2 异常退出持续计费 | 主动 terminate + TTL + 资源审计 |
| fancy 示例版权不清 | 官方/许可素材或自制 reference |

## 12. 参考

- `handoff.md`
- `hkust_hpc developer.md`
- `desktop_env/providers/aws/AWS_GUIDELINE.md`
- `desktop_env/providers/aws/AWS_PPT_WEB_W0_DECISIONS.md`
- [PowerPoint for the web 入门](https://support.microsoft.com/en-us/powerpoint/get-started-with-powerpoint-for-the-web)
- [PowerPoint Web 动画效果](https://support.microsoft.com/en-US/PowerPoint/animation-effects-available-in-powerpoint-for-the-web)
- [PowerPoint 平台功能比较](https://support.microsoft.com/en-us/powerpoint/compare-powerpoint-features-on-different-platforms)
- [PowerPoint Web animation timing](https://support.microsoft.com/en-US/PowerPoint/set-the-start-time-and-speed-of-an-animation-effect)
- [Animation2Code](https://arxiv.org/html/2606.28593)
- [PPT-Eval](https://arxiv.org/html/2606.31154)
- [Animation Needs Attention](https://arxiv.org/html/2507.03916)
