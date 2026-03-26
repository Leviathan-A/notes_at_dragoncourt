# Obsidian 配置建议

## 1. 打开 Vault
1. 打开 Obsidian。
2. 选择 `Open folder as vault`。
3. 指向本仓库下的 `vault/` 目录。

## 2. 启用 Daily Notes
1. 进入 `Settings -> Core plugins`。
2. 打开 `Daily notes`。
3. 在 Daily notes 设置中将路径设为 `01-Daily`。
4. 日期格式建议：`YYYY-MM-DD`。

## 3. 设置 Templates 目录
1. 打开 `Templates` 核心插件。
2. 在插件设置中把模板目录指向 `Templates`。
3. 日报模板建议使用 `Templates/daily.md`。

## 4. 设置附件目录
1. 进入 `Settings -> Files and links`。
2. `Default location for new attachments` 设为 `In the folder specified below`。
3. 文件夹设置为 `Assets`。

## 5. 快捷键建议
- 为 `Open today's daily note` 绑定常用快捷键。
- 为 `Insert template` 绑定快捷键。
- 为 `Quick switcher` 绑定快捷键，便于快速跳转。

## 6. Graph View 建议
- 使用 Graph View 观察孤立笔记。
- 优先补充双链，降低孤岛节点数量。

## 7. tags 与 [[wikilinks]]
- 标签用于分类：例如 `#project` `#daily`。
- 双链用于关系：例如 `[[02-Projects/xxx]]`。
- 建议“链接优先于标签”。

## 8. Obsidian Git（可选）
1. 在社区插件里安装 `Obsidian Git`。
2. 推荐先手工熟悉 `pull -> edit -> push`，再启用自动化。
3. 自动 push/pull 频率不要过高，减少冲突概率。

## 9. CLI（可选）
- 可用系统终端执行 `vault/scripts/*` 脚本。
- 如需 URI 调用，可研究 `obsidian://` 协议与本地脚本联动。
