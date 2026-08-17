# Reference Video Annotator Guide

本文档指导 human expert 在 AWS OSWorld Ubuntu 环境中启动一个 approved reference task，
手动决定何时开始和停止录制，并在本地得到完整的 annotation bundle。

## 0. 协作者默认流程：Annotation Portal

四人协作标注时，不要求 annotator 安装仓库、Conda、AWS CLI 或 SSO。管理员会分别提供：

- 一个 CloudFront HTTPS 链接；
- 一个固定 username；
- 一个一次性 temporary password；
- 已分配到该账户的 task。

打开网站后：

1. 用临时密码登录并由本人设置新密码；项目不开放自助注册；
2. 在 `Your tasks` 中展开 `Task instructions (TASK.md)`；它是网页上唯一的任务说明来源，内容
   直接来自当前发布批次对应 review packet 的 `TASK.md`，不再同时拼接旧 instruction、quick
   guide 或 skill list；
3. 点击 `Launch workspace`。状态为 `provisioning` 时等待，不重复点击；变为 `ready` 后 noVNC
   会嵌入同一网页；
4. 在 noVNC 中确认初始 workbook 正确，此时尚未录制；
   - 可点击 `Fullscreen desktop` 让当前 noVNC 进入全屏；使用右上角 `Exit fullscreen` 或浏览器
     `Esc` 返回网页，均不会重建连接或要求重新输入 VNC 密码；该退出按钮属于 Portal UI，不会
     被录进 guest desktop 视频；
   - 如果只是在探索环境、不准备保留视频，可在 `ready` 状态点击
     `Close without submitting`，系统会终止 EC2 并立即释放该账户和 task；录制开始后该按钮会
     消失，避免误删正在录制的工作；
5. 点击 `Start recording`，确认状态为 `recording` 后再开始需要展示的操作；
6. 完成 skill demonstration 后点击 `Stop & submit`。页面会显示真实阶段：停止 capture、回收
   raw video、渲染按键/鼠标 overlay、保存 artifact、验证 manifest、上传并核验 private S3、
   终止 worker；这是阶段指示器而不是虚假的百分比，可能需要数分钟；
7. `submitted` 表示最终 XLSX、raw/overlay MP4、输入日志和 manifest 已上传到 private S3，
   且 `COMPLETE.json` 已写入；在 `My submissions` 中可以通过 Portal 自身的认证流式接口预览
   `recording.mp4`。浏览器只连接当前 CloudFront 域名，不需要直接访问香港 S3；
8. 如果本次录制不需要，选择 `Discard this run`。它会立即从有效结果中隐藏，但 7 天内可由
   annotator 自己 `Restore`；7 天后后台才永久清除整次 run。不要把“discard”当成重新录制按钮，
   需要重录时再从对应 task 启动新 workspace。

一个 annotator 可以分配多个 task，页面会全部显示，并为每项标记 `not started`、`submitted`、
`discarded` 或 `deleted`；同一账户同时只允许一个 workspace，同一 task 也只能被一人同时占用，
系统全局最多 4 个。`ready` 后 45 分钟不开始
会自动释放；从创建起 180 分钟是硬上限。若页面意外刷新，重新登录后 `Active workspace` 会
恢复当前状态。遇到 `failed` 时先记录页面错误，再点击 `Retry workspace`；重试会创建一个新的
干净 workspace，不会复用失败实例。若连续失败，再把 task ID、时间和错误交给管理员。

noVNC 密码仍为 `osworld-public-evaluation`。协作者只访问 CloudFront 链接，不直接打开 worker
IP、5000 或 5910；也不需要修改本机 proxy。湾区 annotator 第一轮同样使用香港 worker，管理员
根据实测延迟再决定是否增加美国 worker pool。

以下 terminal/AWS 流程保留为管理员诊断与单人 fallback，普通协作者无需执行。

## 1. 标注前准备

在仓库根目录运行：

```bash
conda activate osworld-aws-dev
aws sso login --profile osworld-dev
aws sts get-caller-identity --profile osworld-dev
```

本地环境必须已经设置默认 annotation region 及其 region-scoped 资源：

```text
AWS_ANNOTATION_REGION=ap-east-1
AWS_AP_EAST_1_SUBNET_ID
AWS_AP_EAST_1_SECURITY_GROUP_ID
AWS_AP_EAST_1_AMI_ID
AWS_EC2_INSTANCE_PROFILE_NAME
ENABLE_TTL=true
DEFAULT_TTL_MINUTES=180
AWS_SCHEDULER_ROLE_ARN
```

Runner 默认使用香港 `ap-east-1` 和 SSM+SSH multiplexed connection。OSWorld 官方仓库原有的香港公共 AMI
已经不可访问，因此香港使用由 `us-east-1` 官方干净 AMI 跨区复制得到的私有加密 AMI；
metadata 同时记录 destination AMI、source AMI 和 distribution。旧 PowerPoint Web 的通用
`AWS_AMI_ID` 不会被复用。实例使用 `Project=OSWorld-Expert-Skill-Learning` 标签。

香港模式要求项目 Conda 环境中同时存在 AWS CLI、AWS Session Manager plugin、`ssh` 和
`ssh-keygen`。Runner 通过 SSM 临时注入一次性 SSH 公钥，只让 SSM 承载一条 SSH 连接，再由
SSH 在该连接内复用 API 与 noVNC；终端展示的 noVNC URL 因而是
`http://127.0.0.1:15910/vnc.html?...`，仅在端口已占用时回退到动态端口。URL 默认附加
`autoconnect=true&resize=scale&quality=0&compression=9`：只降低 noVNC 交互预览的带宽，
不会改变 guest 的 1920×1080 geometry 或最终 reference video 清晰度。一次性私钥只存在本机临时目录，并在 runner 退出
时删除；实例也会被终止。该路径不依赖香港 EC2 公网 IP、系统代理或公网入站规则。

香港链路首次打开可能需要 10–30 秒。Runner 在显示 URL 前必须已经验证 noVNC HTML 200、
WebSocket 101 和 RFB banner；如果终端已打印 `OSWorld is ready`，应等待首帧，不要连续刷新或
重复开多个标签页。不要删除 URL 中的低带宽参数；noVNC 设置面板如果改回较高画质，会显著
增加跨境交互延迟。固定 `15910` 让浏览器复用 noVNC 静态资源缓存，但无法消除后续画面更新
的跨境网络延迟。公网 5910 在当前大陆出口实测超时，不作为 fallback。

美国 fallback 仍可显式传入 `--aws-region us-east-1`；它继续读取原有
`AWS_SUBNET_ID/AWS_SECURITY_GROUP_ID` 并使用官方公共 AMI。香港只读取
`AWS_AP_EAST_1_*`，不会误用美国 subnet 或 security group。

对应 region 的 security group 必须是 OSWorld 专用资源。香港 SSM 模式不会查询
`checkip.amazonaws.com` 或修改 5000/5910 ingress。显式使用美国 public fallback 时，runner
才会获取当前公网 IPv4，并把 TCP 5000/5910 的公网规则收缩到当前地址 `/32`。不要传入共享
security group；public mode 的更新会撤销这两个端口上的旧公网 CIDR。

## 2. Review gate

正式标注只允许启动在 `pilot/reference_package_reviews.json` 中标记为 `approved` 的任务。
先按照 [`reviewer.md`](reviewer.md) 在
`pilot/review_packets/<reference-task-id>/review.json` 完成 package review，再运行 packet
collector 将决定同步到中央 review 文件。Approved packet 的 `TASK.md`、artifact preview 和
operator guide 也可继续作为 expert 标注前的单任务入口。

Pending 任务只能用于工程 smoke：

```bash
python scripts/python/record_reference_task.py \
  --reference-task-id reference-task-r01-001 \
  --allow-pending
```

`--allow-pending` 不会绕过 `revision_requested` 或 `rejected`，也不会允许缺少 review form 的
任务启动。

## 3. 生成或重建 task configs

LLM 首先生成不含可信路径和可执行命令的 setup blueprint；本地 assembler 再校验 artifact
SHA256，并注入标准 OSWorld `upload_file`、`open` actions：

```bash
source secret_keys.sh
conda run -n osworld-aws-dev python \
  scripts/python/generate_reference_task_configs.py
```

冻结输出位于：

```text
pilot/annotation_setup_blueprints.json
pilot/task_configs/<reference-task-id>.json
pilot/task_config_manifest.json
```

已有 blueprint 时不应再次付费调用 LLM：

```bash
conda run -n osworld-aws-dev python \
  scripts/python/generate_reference_task_configs.py \
  --blueprints-input \
    evaluation_examples/expert_skill_learning/pilot/annotation_setup_blueprints.json
```

## 4. 一键启动正式标注

```bash
python scripts/python/record_reference_task.py \
  --reference-task-id reference-task-r01-001
```

Runner 会按顺序完成：

1. 验证 review decision、task config、artifact 路径和 SHA256；
2. 验证 AWS SSO identity；香港模式跳过公网 ingress 更新；
3. 启动一台官方 OSWorld Ubuntu 实例、设置 TTL，并建立 SSM+SSH 复用隧道；
4. 上传 initial XLSX 到 `/home/user/Desktop`，用 LibreOffice Calc 打开；
5. 在本地终端显示 task instruction、ready-state checks、operator guide 和 noVNC URL；
6. 等待 expert 检查初始状态；此时尚未录制；
7. 第一次 Enter 后先启动带 monotonic timestamp 的 guest XInput，再启动 MP4；reference
   annotation 默认不抓周期截图，避免与 noVNC 争用跨境隧道；Portal 会等 FFmpeg 第一帧确认后
   才显示 recording，且保留当前 noVNC 连接，不应再次要求输入 VNC 密码；
8. 第二次 Enter 先立即停止录屏，再停止并回收输入日志；保留 raw MP4，把键盘和鼠标提示
   burn-in 到默认视频，
   再自动发送 `Ctrl+S`、下载最终 XLSX 并写结果包；
9. 无论成功、失败或 `Ctrl-C`，都在 `finally` 中请求终止实例；180 分钟 TTL 是异常兜底。

noVNC 默认密码：

```text
osworld-public-evaluation
```

Operator guide 只显示在运行脚本的本地终端，不会进入 noVNC 桌面，因此不会出现在录制
画面中。Guide 是参考，不要求 expert 逐字逐步照抄；允许使用同等正确且高效的 Calc 操作。

按键提示采用后处理，不会在 noVNC 中弹窗或遮挡 expert 操作。默认显示 `Ctrl+A`、
`Ctrl+Shift+V` 等快捷键，以及 `Enter`、`Tab`、方向键等特殊键；普通文字输入不会逐键显示。
提示位于视频底部中央，约保留 1.2 秒，快速连续操作最多显示最近两条。

鼠标提示同样采用后处理并显示在实际操作坐标附近：左键显示 `Left Click`，相邻两次左键
会合并为 `Double Click`，右键显示 `Right Click`，滚轮显示 `Scroll ↑/↓`。按下与释放位置
相差超过 10 px 时视为拖拽，不额外显示点击提示，因为拖拽轨迹本身在视频里可见。连续滚轮
事件会做短时间去抖，避免提示遮挡内容。

Reference annotation 使用独立的 guest FFmpeg recorder，不调用官方 OSWorld `/start_recording`：
实时编码使用 `ultrafast`，stderr 写入文件而不是无人读取的 pipe。停止后会比较 raw MP4 的
movie-header duration 与 guest monotonic 录制窗口；缺失超过 5 秒则 run 直接失败，不能把截断
视频当作正式 reference video。通用 OSWorld 实验录制路径保持不变。

## 5. Enter 的准确含义

- 第一次 Enter 之前：可以等待实例、打开 noVNC、缩放窗口、核对 artifact；这些内容不进入
  `recording.mp4`。
- 第一次 Enter 之后：终端会显示 `RECORDING IS ACTIVE`，此后才开始专家操作。
- 第二次 Enter：表示任务操作已经完成；runner 立即停止录制，再自动保存和回收 workbook。
- 不要在第一次 Enter 之前完成需要展示的 skill。
- 不要在第二次 Enter 之后继续编辑。

## 6. 标注结果

默认输出：

```text
results/reference_annotations/<reference-task-id>/<UTC-run-id>/
├── recording.mp4
├── recording_raw.mp4
├── recording_capture.ffmpeg.log
├── input_events.xinput.log
├── input_events.timestamped.jsonl
├── input_keymap.xmodmap
├── input_timing.json
├── key_events.jsonl
├── pointer_events.jsonl
├── key_overlay.ass
├── events.jsonl
├── episode_manifest.json
├── initial_state.png
├── recording_start.png
├── final_state.png
├── initial_artifact.xlsx
├── final_artifact.xlsx
├── reference_task_config.json
├── reference_package.json
├── reference_review.json
└── artifact_manifest_entry.json
```

默认仍保留 `initial_state.png`、`recording_start.png` 和 `final_state.png` 三个关键状态，但不创建
`frames/`。工程诊断时可显式传 `--sample-interval 5` 等正数重新启用周期截图；通用 OSWorld
实验 runner 与 `manual_explore.py` 的原有截图行为不受影响。

`recording.mp4` 是默认的带键盘和鼠标提示 reference video；`recording_raw.mp4` 是完全不带
提示的原片，用于质量排查和后续 ablation。`key_events.jsonl` 与
`pointer_events.jsonl` 是与视频 PTS 对齐的隐私过滤事件，`input_timing.json` 保存 guest
monotonic clock 的 provisional 和 calibrated 对齐点。最终时间轴使用录制停止时间减去 MP4
实际时长定位第一帧，避免 FFmpeg 启动耗时使提示落后；原始 XInput 文件继续保留作 provenance。第二位 annotator 可以直接
在本地观看视频并检查 `final_artifact.xlsx`，不需要在 AWS 实例里播放视频。

正式标注默认要求按键捕获和 burn-in 成功。仅工程调试时可以使用：

```bash
python scripts/python/record_reference_task.py \
  --reference-task-id reference-task-r01-001 \
  --no-key-overlay
```

`--no-input-events` 必须与 `--no-key-overlay` 一起使用，避免静默产出缺少输入提示的正式视频。

## 7. 故障处理

- SSO 过期：重新运行 `aws sso login --profile osworld-dev`。
- 香港 noVNC 一直 loading：先等待 30 秒，确认使用 runner 输出的 `127.0.0.1:15910`（或端口
  冲突时的动态端口），并确认
  `session-manager-plugin` 与 SSH 子进程仍在；不要用独立 SSM port-forward 直接转发 5910，
  noVNC 的并发 HTTP/WebSocket 连接可能全部挂起。详细诊断见根目录 `developer.md`。
- 美国 public fallback 的 noVNC HTML 可以打开但持续 loading：按照 `developer.md` 的公网
  WebSocket/proxy 流程排查；不要把 security group 改成 `0.0.0.0/0`。
- Artifact SHA256 mismatch：停止标注，确认 workbook 是否被人工替换；先更新并审核 manifest，
  不要用参数绕过。
- `recording.mp4` 或 `final_artifact.xlsx` 缺失：该 run 不算完成，但保留 failed/interrupted
  bundle 供排查。
- Overlay 生成失败：run 标记为 failed，但已经完成的 `recording_raw.mp4` 和输入日志会保留；
  不要把 raw video 静默当作正式 reference video。
- 紧急停止：在 runner 终端按 `Ctrl-C`；脚本会保存当前可用日志并请求终止实例。

当前代码已经通过本地 mock/unit tests。2026-08-11 的真实 AWS smoke 已完整验证
Enter-start → XInput/MP4 → Enter-stop → overlay burn-in → final XLSX/bundle → terminate 闭环；
实例最终为 `terminated`，EBS、ENI 和 TTL schedule 均无残留。大 MP4 回传可能较慢；只要
runner 未报错且 TCP 接收仍在推进，应等待其完成，不要提前关闭终端或实例。
