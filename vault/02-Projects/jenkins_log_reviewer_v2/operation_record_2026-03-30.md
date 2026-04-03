# Jenkins Log Reviewer v2 Operation Record (2026-03-30)

## 1. Scope and Objective
- Project: `jenkins_log_reviewer_v2`
- Goal: 构建 Jenkins 日志异步分析服务，并将 clang issue 回写到 GitLab MR；限制评论噪声，满足 K8s 常驻服务运行适配。
- Environment: 本地开发环境（CST），目标运行环境为 K8s 常驻容器。
- Constraints:
  - 以最小提交集为主，仅保留核心服务代码。
  - 日志解析建议流程保留 API 占位，先打通评论闭环。
  - MR 行内评论需按文件与行号精准落点。

## 2. Code Changes (with reason)
| Step | Commit | Files | Change | Reason | Status |
|---|---|---|---|---|---|
| 1 | `9831196` | `app/*`, `README.md`, `Dockerfile`, `.env.example`, `requirements.txt` | 初始化 v2 主链路：回调入队、Jenkins 拉日志、clang 解析、建议生成、GitLab 评论 | 完成 2.0 主体工程骨架与核心功能闭环 | completed |
| 2 | `357c428` | `app/main.py`, `app/pipeline_service.py`, `Dockerfile`, `README.md` | 增加 `livez/readyz` 与服务就绪判定；容器非 root 运行 | 提升 K8s 运行兼容性与探针对接能力 | completed |
| 3 | `554ca39` | `app/config.py`, `app/gitlab_client.py`, `app/pipeline_service.py`, `.env.example`, `README.md` | 增加评论上限配置；超限时仅发 MR 汇总评论 | 控制 MR 评论噪声，避免大量逐行评论影响评审 | completed |
| 4 | `572792d` | `app/pipeline_service.py` | 上限判断改为强制按 `error+warning` 总量统计 | 严格符合“20个 error+warning 上限”的业务规则 | completed |

## 3. Operations Timeline
| Time | Operation | Target | Result | Status |
|---|---|---|---|---|
| 2026-03-30 11:30-15:30 CST | 建立独立仓库并实现 v2 主链路 | 本地 git repo `jenkins_log_reviewer_v2` | 功能可运行，任务异步处理链路打通 | completed |
| 2026-03-30 15:40-16:00 CST | 真实 MR 行评论联调 | GitLab MR `dockers!7` | 使用有效 token 成功创建 line discussion（discussion_id=`10419a4ae150b2e05b82c5b72d4f80eb915e983d`） | completed |
| 2026-03-30 16:00-16:20 CST | K8s 适配收敛 | 服务探针/容器运行方式 | 增加 `livez/readyz`，就绪逻辑可用，容器非 root | completed |
| 2026-03-30 16:40-17:00 CST | 评论上限策略落地 | `pipeline_service` + `gitlab_client` | 超过 20 条时停止逐文件评论，仅发 MR 汇总说明 | completed |
| 2026-03-30 17:03 CST | 回归验证 | `unittest` | `Ran 17 tests ... OK` | completed |

## 4. Root Cause Analysis
### Issue-1: MR 评论过多导致评审噪声
- Symptom: 当日志 issue 数量较多时，MR 出现大量逐行评论，评审可读性下降。
- Direct cause: 每条 issue 均执行逐文件评论，无阈值保护。
- Root cause: 缺少“评论预算/上限”策略，未区分高噪声场景与常规场景。
- Fix: 新增 `ISSUE_COMMENT_LIMIT`（默认 20）；超过上限时改为 MR 汇总评论，并引导查看 Jenkins 日志。
- Verification: 单测覆盖超限场景；服务逻辑验证通过。
- Status: resolved

### Issue-2: K8s 健康探针对接信息不足
- Symptom: 工程仅有 `/healthz`，无法区分“存活”与“就绪”。
- Direct cause: 缺少 `livez/readyz` 分离端点。
- Root cause: 早期实现偏功能闭环，未补齐平台运行约定接口。
- Fix: 增加 `/livez` 与 `/readyz`；`readyz` 依赖 worker 启动状态。
- Verification: 路由存在性验证 + 单测回归通过。
- Status: resolved

## 5. Current Effective Configuration Snapshot
- Runtime mode: FastAPI + asyncio worker queue（进程内队列）
- Health endpoints: `/healthz`, `/livez`, `/readyz`
- Comment policy:
  - `ISSUE_COMMENT_LIMIT=20`
  - `error+warning` 总数超限 -> MR 汇总评论（不逐行）
- Suggestion API:
  - `SUGGESTION_API_URL=http://10.129.59.108:8088/v1/chat/completions`
  - `SUGGESTION_MODEL=Kimi-Linear-48B-A3B-Instruct`
- Security posture: 容器使用非 root 用户运行
- Active branch/commit: `master` @ `572792d`
- Push state: 本地提交完成，尚未执行远端 push（local-only）

## 6. Verification Evidence
- Unit test:
  - Command: `python3 -m unittest discover -s tests -p 'test_*.py' -q`
  - Result: `Ran 17 tests ... OK`
- MR comment E2E (历史验证):
  - Target MR: `https://gitlab.desaysv.com/ida/ad_alg_dev/codes/platform/develop_env/dockers/-/merge_requests/7`
  - Evidence: 成功创建 line discussion（`discussion_id=10419a4ae150b2e05b82c5b72d4f80eb915e983d`）

## 7. Open Items
- Item: 将 `xxx` 联系人替换为真实值并配置到环境变量/模板中。
- Next action: 增加 `CONTACT_OWNER` 配置并用于超限汇总评论文案。
- Owner: `lcz`

- Item: 上线前在目标 K8s 环境执行真实 webhook 回归。
- Next action: 使用测试 Jenkins job 回调服务，校验异步处理与 MR 评论。
- Owner: `lcz`
