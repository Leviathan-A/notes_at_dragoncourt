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
- 当前主要阻塞转为运行态资源与占位问题（`app/interface` 回归受 `Insufficient memory` 与 semaphore 等待影响）。

## 本周增量（2026-03-30 ~ 2026-04-03）
- 已完成并部署的关键修复：
  - package 依赖补齐（`colcon`）与 pip TLS fallback（`e849318`、`95aa745`）。
  - Argo depends `task.completed` 语义修复并上线（`a6ce247`）。
  - code cache claim 回收与释放策略上线（`construct_scripts@3a6deed` + `constructor_backend@314eaf5`）。
  - `chain_service@f5d8906` 修复可选参数空值导致的 argparse 报错。
- 已完成的代码级架构改造（待集群完整回归）：
  - 单 Pod 总进程持锁（build_subtree 路径）。
  - 统一入口 action pipeline（subtree/module/package/plan-package）。
- 本周运行结果：
  - `sdk` 回归成功；
  - `app/interface` 仍受资源与 semaphore 占位影响，持续跟踪中。

## 风险与阻塞
- 风险：集群资源抖动与历史 Running workflow 占位导致回归收敛慢。
- 阻塞：`app` 调度受 `Insufficient memory`/节点不可调度影响，`interface` 存在 semaphore 等待。

## 关键决策记录
- 日期：2026-03-25
- 决策：部署改为 Pod 内 clone（`emptyDir + initContainer`）。
- 影响：提升跨节点一致性，降低宿主机目录依赖风险。

- 日期：2026-03-25
- 决策：semaphore 改为 `configMapKeyRef`，并启用 `constructor-pods-semaphore/max-concurrent`。
- 影响：限流恢复且避免 `cannot get LockName for a Semaphore without a ConfigMapRef` 报错。

## 关联知识
- [[03-Knowledge/Constructor Listener 常驻 Pod 部署通用步骤与经验]]
- [[03-Knowledge/Argo Semaphore 配置兼容排障]]
- [[03-Knowledge/Listener Peek 模式稳定性排障清单]]

## 关联日报
- [[01-Daily/2026-03-25]]
- [[01-Daily/2026-03-30]]
- [[01-Daily/2026-03-31]]
- [[01-Daily/2026-04-01]]
- [[01-Daily/2026-04-02]]
- [[01-Daily/2026-04-03]]

## 参考原始记录
- [[05-Resources/constructor-listener_operation_record_20260325-原始记录]]
