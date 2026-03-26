---
title: constructor-listener 常驻 Pod 部署与排障
type: project
tags: [project, k8s, argo, listener]
created: 2026-03-26
---

# constructor-listener 常驻 Pod 部署与排障

## 项目目标
- 将 `trigger_print_params.py` 能力并入 `constructor_backend` 常驻 listener Pod（node2）。
- 实现 `peek -> submit workflow` 的稳定触发链路，并保持限流与通知可观测。

## 背景与范围
- 运行模式：listener 只 `peek` 队列，不直接消费。
- 部署方式：`emptyDir + initContainer git clone`，去除 hostPath 依赖。
- 约束：滚动更新可行、问题可追溯、失败可快速止血和回滚。

## 里程碑
- [x] 常驻 listener 部署完成并可监听
- [x] `LISTENER_INFLIGHT_MODE=redis` 生效
- [x] 关闭任务状态上报（只观察不回写）
- [x] Feishu 通知恢复为“失败降级 warning，不阻断主流程”
- [x] semaphore 从历史结构迁移到 `configMapKeyRef`
- [ ] 修复执行阶段 `FileNotFoundError: /workspace/init_code_base`
- [ ] 完成端到端回归：`peek -> submit -> build pods -> package`

## 当前状态
- listener 与 workflow 提交链路可工作。
- semaphore 配置错误已修复并验证限流生效。
- 当前主要阻塞已下沉至构建执行环境准备（`init_code_base` 缺失）。

## 风险与阻塞
- 风险：执行环境初始化步骤不完整导致 workflow 运行失败。
- 阻塞：`construct_scripts` clone 成功，但运行阶段找不到 `/workspace/init_code_base`。

## 关键决策记录
- 日期：2026-03-25
- 决策：部署改为 Pod 内 clone（`emptyDir + initContainer`）。
- 影响：提升跨节点一致性，降低宿主机目录依赖风险。

- 日期：2026-03-25
- 决策：semaphore 改为 `configMapKeyRef`，并启用 `constructor-pods-semaphore/max-concurrent`。
- 影响：限流恢复且避免 `cannot get LockName for a Semaphore without a ConfigMapRef` 报错。

## 关联知识
- [[03-Knowledge/Argo Semaphore 配置兼容排障]]
- [[03-Knowledge/Listener Peek 模式稳定性排障清单]]

## 关联日报
- [[01-Daily/2026-03-25]]

## 参考原始记录
- [[05-Resources/constructor-listener_operation_record_20260325-原始记录]]
