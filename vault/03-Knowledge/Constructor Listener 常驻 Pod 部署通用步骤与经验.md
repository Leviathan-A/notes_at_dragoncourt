---
title: Constructor Listener 常驻 Pod 部署通用步骤与经验
type: knowledge
tags: [knowledge, k8s, argo, listener, deploy]
created: 2026-03-26
---

# Constructor Listener 常驻 Pod 部署通用步骤与经验

## 一句话定义
- 这是一份可复用的部署 Runbook：把 `constructor_backend` 的常驻 listener Pod 从“代码更新”到“上线验证”完整走通，并附带高频故障的定位顺序。

## 适用范围
- 目标服务：`constructor-listener`（Argo 命名空间）
- 典型场景：
  - 分支有新提交，需要快速上线验证。
  - listener 触发链路异常，需要判断是“代码问题 / 配置问题 / 集群问题 / 节点问题”。
  - 需要在“只观察不改任务状态”模式下做稳定联调。

## 标准部署步骤（通用 SOP）
1. 本地代码同步
- 仓库切到目标分支（如 `chain_service`）。
- 执行 `git pull --ff-only`，避免产生额外 merge commit。
- 记录本次上线 commit（后续用于 pod 内核对）。

2. 部署前配置核对
- 核对 `deploy/constructor-listener.yaml` 中关键配置：
  - 镜像：`DOCKER_IMAGE`
  - 触发模式：`LISTENER_PEEK` / `LISTENER_PEEK_REPEAT`
  - inflight 模式：`LISTENER_INFLIGHT_MODE`
  - task 上报：`LISTENER_TASK_REPORT_ENABLE`
  - semaphore 开关与 key：`ARGO_POD_SEMAPHORE_*`
- 核对 Secret（尤其 GitLab Token、Redis、Webhook）是否为真实值，避免占位值覆盖。

3. 滚动重启部署
- 执行 `kubectl -n argo rollout restart deployment/constructor-listener`。
- 执行 `kubectl -n argo rollout status deployment/constructor-listener`，必须等到 success。

4. 上线后版本确认
- 查看新 Pod 是否在目标节点（例如 `node2`）。
- 进入 Pod 核对 `/workspace/src`：
  - 当前分支是否为目标分支。
  - `git rev-parse --short HEAD` 是否等于本地拉取到的 commit。

5. 触发链路验证（建议 direct）
- 优先使用 `deploy/trigger_listener_no_redis.py` 做直连触发，减少 Redis 干扰。
- 记录 `task_id` 与 `workflow_name`。
- 立刻核对：
  - workflow 是否成功创建。
  - 子 Pod 是否正常拉起。

6. 执行阶段验证
- 抽取失败 Pod 的 `main` 容器关键日志。
- 判断失败层级：
  - 提交前（listener）
  - prepare_workspace
  - build_subtree/download_and_package
  - 远端上传（MinIO）

7. 变更留痕
- 把“改动、原因、状态、结论、commit”同步到 deploy journal。
- 将关键结论沉淀到知识库，形成下一次可复用脚本化流程。

## 高频故障与优先定位顺序
1. `HTTP Basic Access denied`（init-clone-repo）
- 优先看 Secret 是否被占位值覆盖。
- 处理方式：修复 Secret 后重建 Pod。

2. `cannot get LockName for a Semaphore without a ConfigMapRef`
- 说明 workflow semaphore 结构与 Argo 控制器不兼容。
- 处理方式：改为 `configMapKeyRef`，并确认 ConfigMap key 存在。

3. `gnutls_handshake() failed`
- 不是鉴权失败，而是 Pod 到 GitLab 的 TLS/网络路径问题。
- 处理方式：按节点维度排查（node2/node3 对比），先确认是否节点网络异常。

4. `origin/<branch> is not a commit`（incremental-update）
- 常见于 `init_code_base` 增量更新阶段，目标分支在目标仓库不存在或未 fetch 到。
- 处理方式：确认该 repo 是否存在该分支；必要时切换到存在的基线分支或调整初始化策略。

5. clone 失败后误导日志
- 现象：clone 失败仍打印“cloned”，随后才在依赖文件缺失处失败。
- 处理方式：脚本必须 fail-fast（`set -euo pipefail` / `|| exit 1`）。

## 关键设计经验（可复用）
- 经验 1：先把触发链路和执行链路拆开验证。
  - 先证实 `listener -> workflow submit` 正常，再看执行面失败，排障速度会快很多。

- 经验 2：部署成功不等于代码生效。
  - 必须在 Pod 内做 commit 校验，否则容易误判“已经上线”。

- 经验 3：线上调试默认走 direct 触发。
  - Redis 队列会引入历史残留（claim/inflight/重复扫描），direct 更利于隔离变量。

- 经验 4：限流问题必须“正修”而不是长期关闭。
  - semaphore 关闭只能止血，最终还是要恢复正确结构并完成并发验证。

- 经验 5：日志路径必须按 `task_id` 归档。
  - 便于跨服务关联（listener 日志、workflow 日志、MinIO 上传对象）。

- 经验 6：部署文档要跟代码同频更新。
  - 每次改动都写原因和状态，能显著降低多人协作时的反复沟通成本。

## 建议的最小发布检查清单
- [ ] 本地分支已 fast-forward 到目标远端。
- [ ] listener Deployment 已 rollout success。
- [ ] 新 Pod 在预期节点，且 commit 已核对。
- [ ] direct 触发成功，拿到 `task_id/workflow_name`。
- [ ] 至少抽检 1 个子 Pod 日志，确认失败不在“基础配置层”。
- [ ] deploy journal 已更新（含 commit 与 root cause）。

## 关联笔记
- [[02-Projects/constructor-listener 常驻 Pod 部署与排障]]
- [[03-Knowledge/Argo Semaphore 配置兼容排障]]
- [[03-Knowledge/Listener Peek 模式稳定性排障清单]]
- [[05-Resources/constructor-listener_operation_record_20260325-原始记录]]
