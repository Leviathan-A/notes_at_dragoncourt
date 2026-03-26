# 个人知识库（Obsidian + Git）

## 1. 项目目标
这是一个可长期使用的个人知识库基础设施：
- Obsidian 作为主界面
- Git 作为同步与版本管理层
- 支持日报、项目笔记、知识沉淀、多设备协作
- 预留本地 AI 输出 Markdown 草稿能力

## 2. 目录结构说明
```text
vault/
  00-Inbox/
  01-Daily/
  02-Projects/
  03-Knowledge/
  04-Areas/
  05-Resources/
  90-Indexes/
  Templates/
  Assets/
  scripts/
  docs/
```

## 3. Linux 初始化步骤
1. 进入仓库根目录。
2. 执行：
   - `python3 vault/scripts/init_vault.py`
3. 用 Obsidian 打开 `vault/`。
4. 在 Obsidian 中按 `vault/docs/obsidian-setup.md` 完成设置。

## 4. Windows 初始化步骤
1. 进入仓库目录（PowerShell）。
2. 执行：
   - `python vault/scripts/init_vault.py`
3. 用 Obsidian 打开 `vault/`。
4. 按 `vault/docs/obsidian-setup.md` 完成设置。

## 5. Git 同步工作流
推荐流程：**先 pull，再编辑，再 push**。
默认不自动 push，由脚本手工触发。

Linux:
- `bash vault/scripts/pull.sh`
- `bash vault/scripts/push.sh`
- `bash vault/scripts/sync.sh`

Windows:
- `powershell -ExecutionPolicy Bypass -File vault/scripts/pull.ps1`
- `powershell -ExecutionPolicy Bypass -File vault/scripts/push.ps1`
- `powershell -ExecutionPolicy Bypass -File vault/scripts/sync.ps1`

## 6. 每日使用流程
1. 创建日报：
   - `python3 vault/scripts/new_daily.py`
2. 记录当天行动、阻塞、洞察。
3. 把日报双链到项目和知识页。
4. 下班前执行同步脚本。

## 7. 冲突处理指南
- 多设备编辑前先 `pull --rebase`。
- 冲突优先在 Markdown 中手工合并，再重新提交。
- 最易冲突文件：同一天日报、同一项目页、同一索引页。
- 不建议同步 workspace 布局类文件（已在 `.gitignore` 处理）。

## 8. Obsidian 使用建议
- 用 `90-Indexes/Home.md` 作为入口。
- 用模板创建新笔记，减少结构漂移。
- 双链优先于标签；标签用于分类，链接用于关系。

## 9. 可选插件建议
- Dataview（索引增强）
- Obsidian Git（可选自动同步）
- Templater（高级模板逻辑，可选）

## 10. 后续 AI 接入方式
见 `vault/docs/ai-integration.md`。
建议模式：AI 生成草稿，人审后再补链路并提交。

## 手工步骤
以下步骤需要你手工完成：
1. 安装并打开 Obsidian，选择 `vault/` 目录。
2. 配置 Git 远程仓库地址与认证（本仓库不写死远程、用户名、token）。
3. 在多设备分别执行首次 `git pull`。
4. 可选安装 Dataview / Obsidian Git 插件。
5. 若使用 direnv，请在本机执行 `direnv allow`。
