---
title: Listener Peek 模式稳定性排障清单
type: knowledge
tags: [knowledge, listener, redis, workflow]
created: 2026-03-26
---

# Listener Peek 模式稳定性排障清单

## 一句话定义
- 针对“listener 只 peek 队列并触发 workflow”模式的稳定性检查清单，用于快速定位触发失败、重复触发、门控卡住问题。

## 适用场景
- workflow 已提交但被错误判定失败。
- 同一任务重复被扫到或长时间无法再次触发。
- 通知链路异常影响主流程判断。

## 核心要点
- 主流程与通知解耦：通知失败只 warning，不应让触发返回失败。
- inflight 建议使用 redis：跨重启恢复更稳定。
- 关闭 task 上报以符合“只观察不回写”原则。
- 出现历史残留时，优先检查/清理 stale `claim/inflight` 键。
- 调试期可开启固定 serial（如 `9999`）便于识别来源。

## 常见误区
- 误区 1：把通知失败当主链路失败。
- 误区 2：忽略历史门控键残留，导致“看起来没问题但不触发”。
- 误区 3：只看 listener 日志，不看 workflow 执行阶段依赖准备。

## 实践案例
- 触发链路修复后，失败点下沉至执行阶段，出现 `FileNotFoundError: /workspace/init_code_base`，说明问题已从“提交阶段”转到“运行环境准备阶段”。

## 关联项目
- [[02-Projects/constructor-listener 常驻 Pod 部署与排障]]

## 相关概念
- [[03-Knowledge/Argo Semaphore 配置兼容排障]]

## 参考来源
- [[05-Resources/constructor-listener_operation_record_20260325-原始记录]]
