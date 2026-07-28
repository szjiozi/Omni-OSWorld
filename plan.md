# OSWorld Video Learning 任务开发计划

## 1. 项目目标

本项目基于 OSWorld 和 Daytona，开发一组“从视频中学习桌面任务”的数据、环境与评测工具，研究两个相互关联的问题：

1. **从视频理解难以用语言完整描述的任务目标**
   - 输入不再只是自然语言，而是一个演示视频、一个待编辑文件和一条很短的指令。
   - Agent 需要从视频中识别目标状态、关键编辑操作、可迁移的风格或规则，再在一个不同但同构的文件上完成任务。
   - 任务从网页/动画复现扩展到 PPT、表格、图片和视频编辑。

2. **从人类轨迹学习更高效且不损失准确率的执行方式**
   - 收集带时间戳的人类 GUI 操作、截图、录屏和最终产物。
   - 将人类轨迹和成功的 Agent 轨迹对齐、去冗余、组合成可执行的高效轨迹。
   - 同时优化成功率、决策步数、原子动作数、端到端时延和模型调用成本。

建议将项目暂命名为 **OSWorld-VideoLearn**。第一版不追求覆盖全部 OSWorld 应用，而是先在 evaluator 最稳定的 LibreOffice Impress 和 Calc 上建立闭环。

## 2. 关键设计决策

### 2.1 两条研究线共用一种中间表示

引入可执行的 **SkillIR**，作为视频、人类轨迹和 Agent 执行之间的统一表示：

```text
演示视频 ──> 目标/操作解析 ──> SkillIR ──> OSWorld 执行 ──> 最终状态 evaluator
人类轨迹 ──> 对齐/剪枝/组合 ──┘                  └──> 效率 evaluator
```

SkillIR 不应只是自然语言摘要，也不应绑定某个视频里的绝对坐标。它至少包含：

- `name`：技能名称，例如“将标题统一为参考页的字体与颜色”。
- `preconditions`：应用、文件类型、对象是否存在、当前选择状态等。
- `goal_spec`：最终状态约束，区分必须满足与允许变化的属性。
- `parameters`：颜色、字体、布局、公式范围等可迁移参数。
- `steps`：语义动作或可执行动作块，而非单纯逐帧复述。
- `observations_needed`：每个动作块之后是否必须重新观察。
- `verification`：完成后如何检查结果。
- `fallbacks`：菜单、快捷键或对象定位失败时的恢复策略。

### 2.2 主评测看最终状态，不要求复刻演示路径

同一个目标通常存在多条有效轨迹。主要分数必须来自 OSWorld 的最终状态 evaluator；轨迹相似度只用于诊断，不作为正确性的必要条件。

### 2.3 先做 Office，再扩展视觉编辑

首个 MVP 选择 Impress 和 Calc，原因是仓库已经具有 `compare_pptx_files`、`compare_table` 及多种细粒度规则，可进行结构化、可重复的目标验证。

第二阶段再加入：

- GIMP：调色、裁剪、蒙版、排版、局部替换和风格迁移。
- VLC/视频工具：字幕、裁剪、转码、拼接、播放设置等可验证编辑。
- 多应用任务：从视频提取规则，在 PPT、表格或图片应用中完成迁移。

### 2.4 OSWorld-Human 只作为评测参照

OSWorld-Human 提供单动作和分组动作的人类参考轨迹及 WES 指标，但其官方仓库明确说明不应将公开解答用于训练。项目应采用以下隔离策略：

- OSWorld-Human 原始任务和轨迹只进入锁定的评测集。
- 训练轨迹来自本项目新建的任务、公开许可的视频或重新采集的人类示范。
- 训练集和测试集按“目标变换族”划分，而不只是按文件或视频 ID 随机划分。
- 任何从评测轨迹生成的 SkillIR 都不得进入训练、检索库或 prompt 示例。

## 3. 研究问题与可检验假设

### RQ1：视频是否比长自然语言更适合表达复杂编辑目标？

对同一批任务比较四种条件：

1. 仅短文本。
2. 详细文本。
3. 短文本 + 演示视频。
4. 短文本 + 从视频编译出的 SkillIR。

主要假设：视频在风格、空间布局和多步操作目标上提高最终状态得分；SkillIR 能保留这种增益，同时降低执行阶段的上下文长度与推理时延。

### RQ2：视频中学到的是轨迹，还是可迁移的目标？

对演示文件和执行文件进行内容替换，保持编辑规则相同。例如演示视频编辑销售 PPT，而测试文件是课程 PPT。若 Agent 只复刻坐标或文本会失败，只有正确提取变换规则才能成功。

### RQ3：人类轨迹能否提高效率而不降低准确率？

比较：

- 原始 Agent。
- 检索人类 SkillIR 的 Agent。
- 经过成功轨迹蒸馏/SFT 的 Agent。
- 使用动作分组和验证策略的 Agent。

主要假设：语义动作块、快捷键和减少不必要观察可以降低模型调用次数；保留关键验证点能够避免单纯压缩步数造成成功率下降。

### RQ4：组合多条高效轨迹是否优于模仿单条“最短”轨迹？

单条最短轨迹可能脆弱。应将多条成功轨迹合成一个带分支的技能图，比较它与单轨迹模仿在不同分辨率、窗口状态和轻微界面变化下的鲁棒性。

## 4. 任务定义

### 4.1 每个任务的输入

每个 episode 包含：

- 初始桌面 snapshot。
- 待编辑的目标文件。
- 演示视频。
- 简短指令，例如“参照演示视频，把当前演示文稿改成同样风格”。
- 可选的源文件，用于区分视频中的原始状态和编辑后状态。
- 仅供 evaluator 使用的目标文件或目标属性规则。

建议同时支持三种视频交付方式：

| 模式 | 说明 | 用途 |
|---|---|---|
| `context` | Runner 将视频采样帧、时间信息或视频路径交给支持视频的 Agent adapter | 主研究设置，减少“操作播放器”造成的干扰 |
| `ui` | 视频文件放在桌面并用 VLC 播放，Agent 必须像用户一样观看、暂停和拖动 | 纯 CUA / UI-only 设置 |
| `compiled` | 直接提供离线生成的 SkillIR | 隔离执行能力，作为诊断上界 |

MVP 先实现 `context` 和 `compiled`，`ui` 模式在 VLC snapshot 稳定后加入。

### 4.2 任务类型

#### A. 目标复现

演示与测试文件结构接近，Agent 需要复现最终状态。适合验证最小闭环，但不应成为主要难度来源。

示例：

- 将 PPT 中特定文本统一为演示中的字体、字号和颜色。
- 将表格中的某列设置为演示中的数字格式和条件格式。

#### B. 风格迁移

内容不同，风格规则相同。重点评测参数抽取、对象匹配和泛化。

示例：

- 将参考视频中的标题、正文和背景风格迁移到另一套幻灯片。
- 将演示中的表格主题、边框和交替行样式迁移到不同数据表。

#### C. 编辑意图迁移

演示具体操作，但测试文件需要根据语义选择不同对象。

示例：

- 演示把最大值高亮为绿色；测试表格的最大值位于其他单元格。
- 演示统一所有章节页版式；测试 PPT 的章节页数量和位置不同。

#### D. 多技能组合

一段视频包含多个可分离目标，Agent 需要确定顺序和依赖。

示例：

- 清理表格数据、添加公式、生成图表并统一图表样式。
- 修改 PPT 主题、重排对象、添加页码并保存为指定文件名。

#### E. 视觉编辑

第二阶段加入，目标主要依赖视觉而非明确属性。

示例：

- 将图片调成演示中的色调与对比度。
- 复现蒙版、裁剪和文本叠加风格。
- 将视频做成演示中的画幅、字幕和转场样式。

## 5. 数据与轨迹格式

### 5.1 扩展 OSWorld task JSON

保留现有 `id`、`snapshot`、`instruction`、`config`、`related_apps` 和 `evaluator`，增加一个向后兼容的 `video_learning` 字段。以下路径和字段均为本项目拟新增内容：

```json
{
  "id": "uuid",
  "snapshot": "libreoffice_impress",
  "instruction": "参考演示视频，把当前演示文稿改成同样的标题风格。",
  "config": [],
  "related_apps": ["libreoffice_impress"],
  "video_learning": {
    "demo_video": {
      "type": "cloud_file",
      "path": "<dataset URL>",
      "dest": "demo.mp4",
      "sha256": "<content hash>"
    },
    "delivery_mode": "context",
    "transfer_family": "ppt_title_style",
    "source_artifact": "demo_before.pptx",
    "demo_result_artifact": "demo_after.pptx",
    "skill_ir": "skill.json",
    "split_group": "ppt_title_style_family_03"
  },
  "evaluator": {}
}
```

数据 loader 对不认识的字段应保持忽略，以免破坏现有 OSWorld 任务。

### 5.2 统一轨迹事件 schema

当前 `lib_run_single.py` 的不同 runner 写入不同字段，且多数只有字符串时间戳，无法准确拆分模型推理、动作执行和等待时间。应新增统一版本化 schema：

```json
{
  "schema_version": "1.0",
  "episode_id": "uuid",
  "task_id": "uuid",
  "actor": "human|agent",
  "event_id": 17,
  "group_id": 6,
  "event_type": "observation|plan|action|verification|result",
  "semantic_action": {
    "verb": "set_font",
    "target": "slide.title",
    "args": {"font": "Aptos Display"}
  },
  "raw_action": "pyautogui.hotkey(...)",
  "timestamps_ns": {
    "started": 0,
    "finished": 0
  },
  "latency_ms": {
    "model": 0,
    "grounding": 0,
    "environment": 0,
    "settle": 0
  },
  "observation_ref": "frames/000017.png",
  "a11y_ref": "a11y/000017.xml",
  "window": {"app": "libreoffice_impress", "title": "..."},
  "outcome": "ok",
  "error": null
}
```

原始数据不可丢弃。标准化脚本生成统一轨迹，原 runner 的 `traj.jsonl` 继续作为 raw artifact 保存。

### 5.3 人类示范采集

Daytona 的 noVNC 适合远程操作，但仅录屏不足以学习精确动作。采集器需要同步记录：

- OSWorld controller 的 `recording.mp4`。
- 初始截图和动作后截图。
- 客户端或 guest X11 层面的键盘、鼠标事件与单调时钟时间戳。
- 活动窗口、屏幕分辨率和缩放。
- 可用时的 accessibility tree。
- 最终文件、evaluator 得分和任务完成确认。
- 示范者 ID 的匿名哈希、熟练度和重试次数，不收集个人内容。

建议先验证两种实现，再选择更稳定的一种：

1. 在 noVNC/RFB 客户端层记录输入事件。
2. 在 Daytona guest 中用 X11 输入事件监听器记录事件。

每个任务至少采集 3 条成功轨迹，其中至少 1 条来自熟练用户。轨迹必须在干净 snapshot 上重放或人工复核，并通过最终状态 evaluator。

## 6. Video → SkillIR 流水线

### 6.1 视频预处理

- 使用视频时间戳而不是仅按固定帧率抽帧。
- 结合画面差分、鼠标/键盘事件和窗口变化识别关键帧。
- OCR 提取菜单、对象和属性面板文本。
- 将连续输入、拖拽、快捷键组合成候选动作段。
- 对 Office 任务读取演示前后文件的结构差异，作为弱监督目标；模型不可在测试时访问 gold diff。

### 6.2 目标解析

将观察到的变化分成：

- 内容变化：文本、数值、公式、媒体。
- 样式变化：字体、颜色、边框、背景、主题。
- 布局变化：位置、尺寸、对齐、层级、合并。
- 文档级变化：页数、sheet、保存路径、格式。
- 过程约束：必须使用某应用或功能。
- 不变量：视频中未改变、迁移时也不应破坏的属性。

目标解析阶段输出带置信度的 `goal_spec`。低置信度属性不应默认为硬约束，而应记录为可选目标或触发补充观察。

### 6.3 轨迹抽象与参数化

- 将绝对坐标转换为 UI 元素、文档对象或相对位置。
- 将演示中的具体内容转换为参数，例如“最大值所在单元格”。
- 将连续且无需新观察的动作分成一个 grouped action。
- 标注每个步骤的前置状态、后置状态和失败恢复点。
- 删除等待、重复点击、无效菜单探索等冗余动作，但保留对准确率有帮助的验证步骤。

### 6.4 SkillIR 验证

每个生成的 SkillIR 必须经过：

1. schema 校验。
2. 在演示初始状态上的 replay 或执行验证。
3. 在至少一个内容不同的同族任务上的迁移验证。
4. 最终状态 evaluator 校验。
5. 重置环境后至少 3 次重复执行，记录成功率和方差。

## 7. 高效轨迹学习

### 7.1 先建立准确的时延分解

端到端时延应从“首个可操作 observation 就绪”计到“最后一个有效动作完成”，并单独报告：

- 环境创建和 snapshot reset。
- 演示视频预处理。
- 模型规划。
- UI grounding。
- 动作执行。
- 动作后等待。
- 验证和恢复。
- evaluator 运行。

仓库目前 `lib_run_single.py` 存在固定的 60 秒启动等待和 20/30 秒结束等待。这些时间不能混进 Agent 执行时延；后续应改为 readiness/settled 条件或至少单独计量。

### 7.2 构建高效轨迹

对同一任务的多条成功轨迹进行：

1. 按 UI 状态和语义动作对齐。
2. 标出重复观察、无效点击、反向操作和错误恢复。
3. 将可交换步骤合并为局部 DAG。
4. 从多条轨迹选择低成本且高成功率的边。
5. 把稳定快捷键和批量操作优先加入候选轨迹。
6. 在干净环境中自动 replay，只有 evaluator 通过的组合轨迹才进入训练集。

不要把“最少原子事件”直接当作最优。更合理的优化目标是：

```text
cost =
  λ_step * decision_steps
  + λ_action * atomic_actions
  + λ_time * wall_clock
  + λ_model * model_calls
  + λ_error * recoveries
```

并附加 `task_success >= baseline_success - δ` 的准确率非劣约束。

### 7.3 训练路线

按实现成本从低到高推进：

1. **Skill 检索基线**：根据当前任务检索相似 SkillIR，Agent 在线适配参数。
2. **Prompt/Context 蒸馏**：将高效动作块作为少量示例，减少每步长历史输入。
3. **行为克隆/SFT**：用标准化成功轨迹学习语义动作与 grouped action。
4. **偏好优化**：同一状态下，以“成功且低成本”的动作块优于冗余或失败轨迹。
5. **带约束的在线优化**：奖励成功和效率，同时对文件损坏、错误退出和低 evaluator 分数施加高惩罚。

第一版优先完成 1 和 2；只有数据量和 replay 质量达到门槛后再做 SFT。

### 7.4 保持准确率的机制

- 每个 SkillIR 明确关键验证点，而不是每步都反思。
- 对高风险操作保留一次 observation，例如删除、覆盖或批量格式化之后。
- 低风险、确定性动作允许 action chunking。
- 执行前检查 preconditions，执行后检查 goal predicates。
- 快捷路径失败时回退到更慢但稳健的菜单路径。
- 报告准确率—效率 Pareto 曲线，不只报告单一加权分数。

## 8. 评测体系

### 8.1 核心指标

| 维度 | 指标 |
|---|---|
| 正确性 | OSWorld evaluator score、严格成功率、部分完成得分 |
| 目标理解 | goal predicate precision/recall、目标参数误差、未要求属性的破坏率 |
| 决策效率 | Agent decision steps、grouped action 数、模型调用数 |
| 操作效率 | 原子动作数、冗余动作率、恢复次数 |
| 时间效率 | 执行总时延及 planning/grounding/action/settle 分解 |
| 成本 | 输入/输出 token、模型费用、Daytona sandbox-minutes |
| 鲁棒性 | 3 次重复成功率、不同分辨率/窗口状态下成功率 |

### 8.2 OSWorld-Human 兼容指标

保留：

- Single-Action WES+。
- Grouped-Action WES+。
- WES-。
- Agent steps / human reference steps。

另外增加不依赖单条人类最短路径的指标：

- `Success@HumanBudget`：在人类 grouped step 预算内的成功率。
- `NormalizedExcessSteps`：相对人类参考多出的步骤比例。
- `LatencySlowdown`：Agent 有效执行时延 / 人类有效执行时延。
- `AccuracyAtEfficiency`：满足指定效率阈值时的成功率。

### 8.3 对照与消融

至少包含：

- Text-only Agent。
- Video end-to-end Agent。
- Video → SkillIR → Agent。
- Oracle SkillIR。
- 原始 Agent 与 human-skill retrieval Agent。
- 单动作与 grouped-action。
- 有/无 post-action verification。
- 有/无轨迹剪枝。

所有模型在相同 Daytona snapshot、分辨率、最大步数、等待策略和 evaluator 版本下运行。

## 9. Daytona 开发与运行方案

### 9.1 基本原则

本项目不依赖服务器 Docker 权限。Daytona sandbox 本身就是桌面，不在 sandbox 内启动嵌套 VM，也不使用上游 qcow2/KVM 路径。

按 `DEVELOPMENT.md` 的开发方式：

1. 本地完成小步修改和测试。
2. 提交并推送当前分支到 `omni`。
3. 在计算节点 `git fetch/switch/pull`。
4. 激活 `osworld_env`。
5. 用 Daytona provider 运行集成测试。

凭据只通过环境变量提供，绝不写入 task JSON、snapshot、日志或仓库。

### 9.2 Snapshot 分层

建议维护两个不可变 snapshot：

- `osworld-video-office-v1`：LibreOffice、字体、录屏与 Office evaluator 依赖。
- `osworld-video-media-v1`：在 Office 基础上增加 VLC、GIMP、ffmpeg/ffprobe 和媒体依赖。

每个 snapshot 记录：

- 构建脚本 commit SHA。
- 包版本与字体清单。
- 屏幕分辨率、locale 和时区。
- OSWorld server 版本。
- smoke test 结果。
- snapshot 名称和创建时间。

Daytona 基线 snapshot 不保证 GIMP、VLC、Chrome 等应用齐全，因此媒体任务不能在未扩展的基线上直接宣称通过。

### 9.3 Daytona 验证命令

以下命令均在计算节点仓库根目录、`conda activate osworld_env` 后运行。API key 由环境变量预先注入，不在命令历史里写明文：

```bash
python -m desktop_env.providers.daytona.build_snapshot \
  --name osworld-video-office-v1

export DAYTONA_OSWORLD_SNAPSHOT=osworld-video-office-v1

python -m desktop_env.providers.daytona.smoke_test

python scripts/python/manual_explore.py \
  --provider-name daytona \
  --headless \
  --ssh-host hkust-compute

python scripts/python/run_multienv.py \
  --provider_name daytona \
  --headless \
  --observation_type screenshot \
  --max_steps 30 \
  --num_envs 1 \
  --result_dir ./results/video_learning_smoke
```

注意事项：

- Daytona Tier 1/2 可能限制任意网络访问。任务资源应预下载、缓存并带 SHA-256，避免 episode 运行时依赖不稳定外网。
- reset 会先创建替代 sandbox，再后台删除旧 sandbox，短时间内一个 environment 会占用两个 sandbox。并发数必须给配额留出至少一倍 reset 余量。
- 开发阶段始终从 `--num_envs 1` 开始，通过 10 个连续 episode 无泄漏后再增加并发。
- 每次异常退出后检查带 `osworld.managed` / `osworld.alloc` 标签的残留 sandbox。
- smoke test、Office task smoke 和媒体 task smoke 应分开，避免“控制面正常”被误认为“所有应用任务可用”。

## 10. 拟议代码与数据结构

以下是后续实现阶段拟新增或修改的范围，不代表这些文件当前已经存在：

```text
evaluation_examples/
└── video_learning/
    ├── test_mvp.json
    ├── examples/
    │   ├── libreoffice_impress/
    │   └── libreoffice_calc/
    ├── skills/
    └── schemas/

scripts/python/
├── collect_human_trajectory.py
├── normalize_trajectory.py
├── compile_video_skill.py
├── validate_video_task.py
└── score_video_learning.py

desktop_env/
└── trajectory/
    ├── recorder.py
    ├── schema.py
    └── grouping.py
```

预计修改：

- `scripts/python/manual_explore.py`
  - 支持加载具体 task JSON。
  - 启动/停止录屏和输入事件采集。
  - 结束后运行 evaluator 并保存 manifest。
- `lib_run_single.py`
  - 接入统一 trajectory recorder。
  - 使用单调时钟记录各阶段时延。
  - 保留原 runner 输出，逐步迁移，避免一次性重构所有 agent 分支。
- `scripts/python/run_multienv.py`
  - 增加 video context adapter、schema 版本和计时配置。
- `desktop_env/evaluators/metrics/slides.py`
  - 优先复用现有规则，只对缺失的风格/布局属性增加小型 evaluator。
- `desktop_env/evaluators/metrics/table.py`
  - 增加 MVP 任务确实需要、现有 `compare_table` 无法表达的规则。
- `desktop_env/providers/daytona/build_snapshot.py`
  - 分层安装 Office/媒体依赖，并输出可审计 manifest。

每项行为变更都应带单元测试；snapshot 和完整 GUI 流程则通过 Daytona smoke/integration test 验证。

## 11. 分阶段里程碑

### Phase 0：环境与契约冻结（第 1 周）

实现状态（2026-07-28）：

- [x] Task extension、SkillIR、trajectory event 三个 v1 JSON Schema。
- [x] 默认 runner 的统一事件、单调计时和原子 episode manifest。
- [x] `manual_explore.py` 的任务加载、录屏、周期截图、X11 输入事件和 evaluator。
- [x] Daytona Office snapshot manifest、Office smoke 和 10-reset soak 工具。
- [x] 2 个 Impress + 2 个 Calc 任务、确定性 fixture 和本地验证报告。
- [x] 本地定向测试：`5 passed, 1 skipped`；四任务验证均满足 initial=0、gold=1。
- [ ] 在计算节点使用真实 Daytona 凭据执行 snapshot build、10-reset soak 和四任务 `--daytona` 验收。当前本地进程未设置 `DAYTONA_API_KEY` / `DAYTONA_OSWORLD_SNAPSHOT`，因此不能伪造此项结果。

交付物：

- Daytona Office snapshot 可以稳定 reset。
- 修复或替代失效的 `manual_examine.py` 文档路径。
- Task JSON、SkillIR 和 trajectory schema v1。
- 统一计时定义和结果 manifest。
- 2 个 Impress + 2 个 Calc 手工任务端到端通过。

退出条件：

- 连续 10 次 reset/episode 无残留 sandbox。
- 同一 gold 文件的 evaluator 结果稳定。
- 录屏、动作、截图和单调时间戳可对齐。

### Phase 1：MVP 数据集（第 2–3 周）

规模：

- Impress 12 个任务。
- Calc 12 个任务。
- 6 个目标变换族，每族至少 4 个不同内容文件。
- 每个任务 3 条成功人类示范。

交付物：

- 24 个 task JSON、演示视频、初始文件、gold 文件和 SkillIR。
- 数据校验器与 replay 验证报告。
- Text-only、Video、Compiled SkillIR 三个基线。

退出条件：

- 100% task 配置可从干净 snapshot 初始化。
- 100% gold artifact evaluator 通过。
- 至少 90% 人类轨迹 replay 或人工复核通过。
- train/dev/test 不共享目标变换实例或源文件。

### Phase 2：效率学习基线（第 4–5 周）

交付物：

- 统一人类/Agent trajectory normalizer。
- 单动作和 grouped-action 统计。
- Skill 检索、动作分组和关键点验证基线。
- 准确率—效率 Pareto 报告。

退出条件：

- 相对原始 Agent，成功率下降不超过 2 个百分点。
- 成功 episode 的 decision steps 中位数下降至少 20%。
- 时延分解覆盖至少 95% 的有效执行时间。

### Phase 3：轨迹蒸馏与组合（第 6–7 周）

交付物：

- 多轨迹对齐、剪枝和技能图生成。
- 组合轨迹自动 replay gate。
- SFT 或偏好优化的小规模实验。
- 对窗口位置、分辨率和轻微 UI 扰动的鲁棒性测试。

退出条件：

- 组合轨迹全部通过 clean-snapshot evaluator。
- 相比单条最短轨迹，组合技能图的重复执行成功率更高或持平。
- 训练过程不访问锁定评测轨迹。

### Phase 4：视觉编辑扩展（第 8 周及以后）

交付物：

- Daytona media snapshot。
- GIMP/VLC 各 10–20 个可复现任务。
- 结构化属性 + 感知指标 + 人工抽检的混合 evaluator。
- Office 与视觉编辑的统一榜单和分域结果。

退出条件：

- 媒体依赖和字体被固定在 snapshot manifest。
- 感知 evaluator 与双人盲评的一致性达到预设阈值。
- 不以单一像素相似度误判内容正确但编码不同的结果。

## 12. 测试与发布门槛

### 12.1 单元测试

- Task/SkillIR/trajectory schema 校验。
- 时间戳单调性和事件排序。
- 单动作到 grouped-action 的转换。
- 轨迹成本与 WES 计算。
- 数据 split 去重与内容 hash 检查。
- PPT/Calc 新 evaluator 的正例、反例和无关属性扰动。

### 12.2 集成测试

- Daytona snapshot 创建、启动、reset、关闭。
- 演示视频下载或缓存校验。
- task config 初始化。
- 人类采集完成后 artifact 落盘。
- Agent runner 读取视频 context。
- 最终文件提取和 evaluator 运行。
- 中断后清理 sandbox。

### 12.3 数据质量

每个任务必须通过自动校验：

- 所有资源 URL 或缓存路径可解析。
- SHA-256 与 manifest 一致。
- 初始文件不已满足目标。
- gold 文件满足全部目标谓词。
- evaluator 对至少一个故意错误的输出给出低分。
- 视频能解码、时长合理、无隐私信息和未授权内容。
- 人类轨迹最终得分达标。

## 13. 主要风险与缓解

| 风险 | 影响 | 缓解 |
|---|---|---|
| 视频只是泄露具体答案，不能测迁移 | 结果虚高 | 使用不同内容的执行文件，按变换族拆分 |
| 最终状态 evaluator 过拟合 gold 文件 | 合法解法被误判 | 使用属性规则、容差和多 gold；人工抽检 |
| 轨迹越短但越脆弱 | 效率提升、准确率下降 | 准确率非劣约束、关键验证点、重复执行 |
| OSWorld-Human 评测泄漏 | 研究结论无效 | 锁定评测集，不训练、不检索其解答 |
| noVNC 只有视频没有动作 | 无法做精确轨迹学习 | 增加客户端或 X11 输入事件 recorder |
| Daytona snapshot 与上游 qcow2 不一致 | 大量任务初始化失败 | 分层 snapshot、应用级 smoke、版本 manifest |
| Daytona reset 短暂双倍占用配额 | 并发失败或资源泄漏 | 单环境起步，按两倍峰值规划并发 |
| 固定 sleep 污染时延 | 效率结论错误 | readiness 条件和分阶段计时 |
| 字体、locale、分辨率差异 | Office/视觉得分波动 | 固定 snapshot 配置并记录 manifest |
| 视频版权与隐私 | 数据无法发布 | 使用自录或明确许可素材，自动隐私检查 |

## 14. 第一轮实施清单

建议下一轮开发只完成下面这些小而可验收的事项：

1. 定义三个 JSON Schema：task extension、SkillIR、trajectory event。
2. 扩展 `manual_explore.py`，使其能加载指定 task、录屏并在退出时运行 evaluator。
3. 为 Daytona Office snapshot 增加 manifest 和应用级 smoke test。
4. 制作 2 个 Impress 和 2 个 Calc 的 video-learning task。
5. 给 `lib_run_single.py` 的默认 runner 增加单调计时和统一 recorder；暂不改全部 agent-specific runner。
6. 实现一个不训练模型的 Video → SkillIR 基线，以及一个 Oracle SkillIR 上界。
7. 输出首份报告：四个任务的正确性、步数、分组步数和时延分解。

完成这 7 项后，再决定是优先扩大数据量，还是先投入人类轨迹的 SFT/偏好优化。

## 15. 参考资料

- [OSWorld 仓库与任务格式](https://github.com/xlang-ai/OSWorld)
- [OSWorld-Human 论文](https://arxiv.org/abs/2506.16042)
- [OSWorld-Human 官方实现与 WES 评分](https://github.com/WukLab/osworld-human)
- 本仓库 `DEVELOPMENT.md`
- 本仓库 `desktop_env/providers/daytona/DAYTONA_GUIDELINE.md`
- 本仓库 `evaluation_examples/README.md`
- 本仓库 `desktop_env/evaluators/README.md`
