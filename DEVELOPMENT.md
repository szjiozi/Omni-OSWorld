# 开发注意事项

## 开发模式

代码统一在本地修改，通过 Git 远端 `omni` 同步到计算节点，并在计算节点上运行和测试。

1. 在本地修改代码，提交后推送当前分支到 `omni`：

   ```bash
   git add <files>
   git commit -m "<message>"
   git push omni HEAD
   ```

2. 连接计算节点：

   ```bash
   ssh hkust-compute
   ```

3. 进入计算节点上的 Omni-OSWorld 仓库，切换到对应分支并同步代码：

   ```bash
   cd <Omni-OSWorld 仓库目录>
   git fetch omni
   git switch <branch>
   git pull --ff-only omni <branch>
   ```

4. 在计算节点仓库根目录加载 Daytona 环境变量，激活
   `osworld_env` 环境，然后运行所需命令：

   ```bash
   source daytona_key.sh
   conda activate osworld_env
   <command>
   ```

   `daytona_key.sh` 只保存在计算节点，不提交到 Git，也不要在日志中输出
   其中的密钥。测试脚本只应检查所需变量是否已设置。
