# 开发注意事项

## 开发模式

代码统一在本地修改，通过 Git fork 同步到计算节点，并只在计算节点的
`osworld_env` Conda 环境中运行和测试。本地 fork remote 名为 `omni`；
计算节点仓库中同一个 fork 通常名为 `origin`，执行同步命令前先用
`git remote -v` 确认。

1. 在本地修改代码，提交后推送当前分支到 `omni`：

   ```bash
   git add <files>
   git commit -m "<message>"
   git push omni HEAD
   ```

2. 连接登录节点并申请计算节点：

   ```bash
   ssh hkust-hpc2
   module load slurm
   srun -p i64m512u -n 4 --mem=8G --time=07:00:00 --pty bash
   ```

   如果 `module load slurm` 后仍找不到 `srun`，使用
   `/opt/slurm/bin/srun` 加相同参数。`ssh hkust-compute` 只在已有活动
   allocation 时可用；出现 `pam_slurm_adopt` 错误说明需要重新申请。

3. 在分配到的计算节点进入 Omni-OSWorld 仓库，切换到对应分支并同步代码：

   ```bash
   cd <Omni-OSWorld 仓库目录>
   git remote -v
   git fetch <fork-remote>
   git switch <branch>
   git pull --ff-only <fork-remote> <branch>
   ```

4. 在计算节点仓库根目录激活 `osworld_env`，加载 Daytona 环境变量，
   然后运行所需命令：

   ```bash
   source "$(conda info --base)/etc/profile.d/conda.sh"
   conda activate osworld_env
   source daytona_key.sh

   test "${CONDA_DEFAULT_ENV}" = "osworld_env"
   test -n "${DAYTONA_API_KEY:-}"
   test -n "${DAYTONA_OSWORLD_SNAPSHOT:-}"
   <command>
   ```

   `daytona_key.sh` 只保存在计算节点，不提交到 Git，也不要在日志中输出
   其中的密钥。每个新的计算节点 shell 都需要重新 `source`；测试脚本只应
   检查所需变量是否已设置。
