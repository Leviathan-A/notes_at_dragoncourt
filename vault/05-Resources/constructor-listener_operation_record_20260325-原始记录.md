# constructor-listener 常驻 Pod 部署与排障记录（截至 2026-03-25）

## 1. 范围与目标
- 目标：将 `trigger_print_params.py` 相关能力并入 `constructor_backend` 的常驻 listener Pod，部署在 `node2`，并完成队列监听触发、限流、通知链路验证。
- 约束：listener 使用 `peek`（只观察队列，不直接消费队列），部署需支持滚动更新和可追溯排障。

## 1.1 维护规则
- 本文档作为 listener 部署变更主记录，后续每次相关改动都必须同步更新本文档（改动内容、原因、状态、结论）。

## 2. 代码修改记录（含原因）
| 顺序 | Commit | 改动内容 | 改动原因 | 状态 |
|---|---|---|---|---|
| 1 | `dbf063a` | 集成 listener 触发路径、API trigger 路由、Feishu 通知组件、node2 部署基础配置 | 将外部 trigger+容器内 trigger 方案改为常驻 listener 方案 | 已完成 |
| 2 | `4b8f2db` | 关闭 task 状态上报；配置真实 webhook | 满足“只观察不改任务状态”原则；修复占位 webhook 导致异常 | 已完成 |
| 3 | `d242e4f` | Deployment 从 `hostPath` 切换为 `emptyDir + initContainer git clone` | 去除对宿主机本地目录依赖，改为 Pod 内每次拉代码 | 已完成 |
| 4 | `8bc7785` | 恢复 listener 触发后的 Feishu 通知（通知失败仅 warning） | 保持触发主流程稳定，同时恢复通知能力 | 已完成 |
| 5 | `a27f19c` | 临时将 `ARGO_POD_SEMAPHORE_ENABLED=0` | 先止血：规避 Argo semaphore 结构不兼容导致的全量触发失败 | 已完成（历史临时） |
| 6 | `83275bf` | 正式修复 semaphore：workflow 改为 `configMapKeyRef`；部署增加 semaphore 配置键 | 正向恢复限流，避免“只能关闭 semaphore 才能运行” | 已完成（当前生效） |

## 3. 集群操作与步骤状态（含原因）
| 步骤 | 操作 | 结果/现象 | 原因/目的 | 当前状态 |
|---|---|---|---|---|
| 1 | 在 `argo` 部署 `constructor-listener`（node2） | Pod 可启动并监听 | 建立常驻 listener 基线 | 已完成 |
| 2 | `LISTENER_INFLIGHT_MODE` 调整为 `redis` | 触发门控稳定，跨重启可恢复 | 避免内存态/运行态计数抖动 | 已完成（当前生效） |
| 3 | 修复 Secret 占位值（GitLab/Redis/webhook） | 消除鉴权与通知占位异常 | 先恢复基础可用性 | 已完成 |
| 4 | 切换为 Pod 内 clone 代码 | 运行时不再依赖宿主机代码路径 | 满足“容器内拉代码”诉求 | 已完成（当前生效） |
| 5 | 关闭 task 上报（`LISTENER_TASK_REPORT_ENABLE=0`） | listener 不再写回任务状态 | 遵守“只观察不动手上报” | 已完成（当前生效） |
| 6 | 恢复 Feishu 通知 | 触发成功后发送通知；失败不阻断 | 保留可观测性 | 已完成（当前生效） |
| 7 | 打开 debug serial 强制（`LISTENER_DEBUG_FORCE_BUILD_SERIAL=1`） | 新任务 serial 变为 `9999` | 调试环境快速识别任务来源 | 已完成（当前生效） |
| 8 | 临时关闭 semaphore（止血） | 去除 `LockName/ConfigMapRef` 立即报错 | 让 workflow 先能进入执行阶段 | 已完成（历史） |
| 9 | 正式恢复 semaphore（正修） | 限流生效且不再报 `ConfigMapRef` 错误 | 满足“限流生效 + 功能正常” | 已完成（当前生效） |
| 10 | 清理 stale claim/inflight 并重触发 | 卡住任务可重新提交 | 修复历史异常残留锁态 | 已完成 |

## 4. Root Cause（先前问题根因）
### RC-1：workflow 触发后立即 `Error`，未创建执行 Pod
- 现象：`cannot get LockName for a Semaphore without a ConfigMapRef`
- 根因：workflow 的 semaphore 结构使用了旧格式（`name/limit`），与当前 Argo 控制器期望的 `configMapKeyRef` 不兼容。
- 修复：`83275bf` 改为 `configMapKeyRef`；创建 `ConfigMap/constructor-pods-semaphore` 并启用。
- 状态：已解决。

### RC-2：曾出现“触发成功但被判失败/重复触发”
- 现象：workflow 已提交但 listener 仍走失败分支，任务重复被扫到。
- 根因：通知异常（占位 webhook）抛错与触发主流程耦合，导致 `_trigger_decompose` 返回失败。
- 修复：真实 webhook + 通知异常降级为 warning（不阻断主流程）。
- 状态：已解决。

### RC-3：peek 阶段出现卡门控/卡 claim
- 现象：队列有任务但短期无法再次触发。
- 根因：历史失败留下 stale `claim/inflight` 键，叠加门控导致跳过。
- 修复：清理 stale 键并保留 redis inflight 模式。
- 状态：已解决（历史任务清理后恢复）。

### RC-4：当前遗留失败（非 semaphore）
- 现象：执行阶段 Pod `exit code 1`，日志 `FileNotFoundError: /workspace/init_code_base`。
- 根因：`construct_scripts` clone 成功，但运行环境未准备 `init_code_base`（准备步骤/来源缺失）。
- 状态：未解决（当前主要阻塞）。

## 5. 当前生效配置快照（listener）
- 部署方式：Pod 内 clone（`emptyDir + initContainer`）
- 节点：`node2`
- `LISTENER_INFLIGHT_MODE=redis`
- `LISTENER_TASK_REPORT_ENABLE=0`
- `LISTENER_DEBUG_FORCE_BUILD_SERIAL=1`
- `ARGO_POD_SEMAPHORE_ENABLED=1`
- `ARGO_POD_SEMAPHORE_CONFIGMAP_NAME=constructor-pods-semaphore`
- `ARGO_POD_SEMAPHORE_CONFIGMAP_KEY=max-concurrent`
- `ConfigMap/constructor-pods-semaphore`: `max-concurrent=6`
- Feishu webhook：已配置真实值（文档不明文展开）

## 6. 验证结论
### 6.1 Semaphore 正向验证（已通过）
- 使用两个 smoke workflow 共享同一 semaphore key（临时 key：`smoke-limit=1`）验证：
  - 第一个 workflow 先运行；
  - 第二个 workflow 显示等待锁：`Waiting for argo/ConfigMap/constructor-pods-semaphore/smoke-limit lock. Lock status: 0/1`；
  - 第一个结束后第二个自动开始。
- 说明：限流生效且机制正常。

### 6.2 主链路现状
- listener 可 `peek` 并提交 workflow；
- semaphore 配置错误已消除；
- 当前失败点已下沉到构建执行阶段（`/workspace/init_code_base` 缺失）。

## 7. 后续待办
- 修复 `init_code_base` 来源/准备步骤（workflow 执行脚本或工作区初始化逻辑）。
- 修复后执行一次端到端回归：`peek -> submit -> build pods -> package`。

## 8. 本地测试脚本补充（2026-03-25）
- 新增：`deploy/trigger_listener_no_redis.py`
- 目的：提供“**不经 Redis 队列**”的触发方式，直接调用 listener API：
  - `POST /api/v1/trigger/hostpath`
- 适用场景：排查镜像、初始化脚本、Argo 提交链路时，避免 Redis 队列状态干扰。
- 跨机器能力补充：
  - 支持 `--listener-url` 指定完整地址；
  - 支持 `--hosts` 多主机候选自动尝试；
  - 支持 `--discover-k8s` + `kubectl` 自动发现 `constructor-listener` Service IP；
  - 若首个端点不可达会自动切换到下一个候选。
