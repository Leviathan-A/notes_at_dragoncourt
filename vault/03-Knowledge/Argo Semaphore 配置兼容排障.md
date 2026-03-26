---
title: Argo Semaphore 配置兼容排障
type: knowledge
tags: [knowledge, argo, semaphore, k8s]
created: 2026-03-26
---

# Argo Semaphore 配置兼容排障

## 一句话定义
- 当 workflow 触发后立即报锁配置错误时，优先核查 semaphore 字段结构是否与当前 Argo 控制器版本兼容。

## 适用场景
- 错误包含：`cannot get LockName for a Semaphore without a ConfigMapRef`。
- 现象为 workflow 尚未创建执行 Pod 就进入 `Error`。

## 核心要点
- 历史配置中的 `name/limit` 结构在新控制器下可能不兼容。
- 推荐结构：`configMapKeyRef`，并显式维护 configmap 名称与 key。
- 需要配套确认：
  - `ARGO_POD_SEMAPHORE_ENABLED=1`
  - `ARGO_POD_SEMAPHORE_CONFIGMAP_NAME`
  - `ARGO_POD_SEMAPHORE_CONFIGMAP_KEY`

## 常见误区
- 误区 1：临时把 semaphore 关闭后就不再回修。
- 误区 2：只改 workflow，不改 deployment 环境变量。
- 误区 3：未做并发验证就宣布“限流恢复”。

## 实践案例
- constructor-listener 从临时止血 `ARGO_POD_SEMAPHORE_ENABLED=0` 过渡到正式修复，改为 `configMapKeyRef` 后恢复限流。
- 使用 smoke workflow + `smoke-limit=1` 验证第二个 workflow 进入 waiting，再在第一个结束后自动执行。

## 关联项目
- [[02-Projects/constructor-listener 常驻 Pod 部署与排障]]

## 相关概念
- [[03-Knowledge/Listener Peek 模式稳定性排障清单]]
- [[03-Knowledge/Git 冲突最小化策略]]

## 参考来源
- [[05-Resources/constructor-listener_operation_record_20260325-原始记录]]
