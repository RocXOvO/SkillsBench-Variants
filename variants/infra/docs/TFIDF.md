# TF-IDF P1/P2 宿主机协议

`grader_image=null` 是原设计：`private/deployment.json` 指定 `host-supervised-exclusive-api`，grader 不是 actor 容器入口。原评分器运行在 Linux 宿主机，候选 API 则在隔离容器测量。

| 变体 | 干净测量基础镜像 |
|---|---|
| `parallel-tfidf-search--p1--dev-401` | `sha256:f807d85f5de5b182990065f80974ef51d57c0e8f2f9be5b0391b0ba307a0f9c3` |
| `parallel-tfidf-search--p2--dev-401` | `sha256:0eaefb647eb7d40945a81b41862314f39a614d34f55b8b51f13782f4339a57ff` |

二者都在完整镜像导出中。不能直接将 null 改填为 solver 镜像后调用容器内 `test.sh`。宿主机需要 Bash、Python、Docker CLI、原源码与固定测量输入；上述两项的根目录恢复别名包括原 `entry_pins.json` 校验的全部文件。

## generation 和停止边界

使用准确干净基础镜像启动 generation：8 CPUs、4096 MiB、network=none、pids-limit=512、cap-drop=ALL、no-new-privileges、`/root/.codex` tmpfs；保持原 image Env/User/WorkingDir/Entrypoint/Volumes/OnBuild，只覆盖 Cmd 为 `sleep infinity`。容器名为 `rt-solver-` 加 16 位小写十六进制。挂载仅为可信 generation 清单中的公开输入、原 CLI 和冻结 skill，全部只读；不挂 private 评分输入和 Docker socket。

agent 写 `/root/workspace/parallel_solution.py`。结束后停止所有后代，保留容器；OOM 或控制异常属于工程失败。可信宿主机记录实际 bind mounts，格式为 `[[绝对宿主路径, 容器路径], ...]`，不能接受 agent 编写的清单。

原 `tfidf_added_p1_snapshot_PREPARE_20261003_r1.py:freeze_stopped` 验证停止状态、资源、准确 image 与挂载，扫描导出的 rootfs，然后 Docker commit；检查新 snapshot 的准确 Parent、配置、停止状态前后一致。mounted 输入不进入 commit，依赖和候选代码保留在 rootfs。`legacy/tfidf_snapshot.py` 是较早 bridge 网络版，正式 network=none 路线使用提供的 native snapshot helper。

## 可执行入口

在 README 的原生 Linux 环境中调用；工具不启动模型：

```sh
python3 variants/infra/tools/run_tfidf.py \
  --variant parallel-tfidf-search--p1--dev-401 \
  --solver-container "$SOLVER_CONTAINER" \
  --mounts "$PWD/trusted-generation-mounts.json" \
  --provider-env "$PWD/private-provider-scan.env" \
  --condition no_skill \
  --output-dir /data/amax/skillsbench-variants/runs/tfidf-p1-new-run \
  --exclusive-lock /data/amax/skillsbench-variants/runs/tfidf-measurement.lock
```

`private-provider-scan.env` 是本次模型凭据的私有扫描输入，权限 0600，原 helper 接口为单行 `OPENLUX_API_KEY=<本次凭据>`，至少 16 bytes。该值只供停止后已知凭据扫描，不进入 candidate 容器、不发请求，也不上传。若接入方用不同 provider，按其私有凭据治理把待扫描值传给该原接口，并在自己的适配器检查其他凭据；包内不含作者 API key。测试用随机扫描标记不代表真实实验已经完成凭据审计。

`--agent-timeout` 仅在 generation 的可信回执确认超时时使用。原评分器的 condition 枚举为 `no_skill/skillrevise/spark/skillevolver/coevoskills`；新的外部方法名称另存到接入方自己的实验回执，并按其协议建立映射，不能修改原科学文件或静默改写原冻结方法记录。

工具在一个外层 900 秒内完成停止后扫描、快照和原宿主评分，导出上限沿用原 10 GiB 加 tar overhead；不额外给正式评分一个新的 900 秒。已具备合格本次 snapshot 的适配器也可直接调用：

```sh
bash <task-root>/private/grader/test.sh \
  --deployment <trusted-deployment.json> \
  --run-dir <fresh-absolute-run-dir> \
  --exclusive-lock <shared-lock-file>
```

可信配置包含 `variant_id`、原 condition、bool `agent_timeout`、`runtime_image_id`、本次 `snapshot_receipt` 路径及该文件 `snapshot_sha256`。snapshot 必须是真实新停止容器生成，不能伪造 Parent 或复用历史输出；直接调用也必须由外层适配器限制完整 freeze+grade 总预算。

## 测量与结果

宿主机整个测量持有同一个非阻塞 flock；4 workers、top_k=10、8 CPUs、4096 MiB、3 repetitions、12 次 timed API calls 和 4 次不计入性能的 nonce challenge。原 index speedup 阈值 1.5、search 2.0，测量基础数据及 predicate 保持原文件与哈希。

正常完成写 `<run>/native/status.json` 的 `status=completed`、`grader_completed=true`、reward 0/1，以及 `native/reward.txt`；外层结果为 `<run>/grade-summary.json`。工程异常维持 `engineering_pending`、reward null、exit 75。原入口拒绝容器内调用。性能测量推荐原生宿主 Docker；嵌套 Docker 的停止超时不应作为候选 task score。

`run_tfidf.py` 保留本次停止 solver 与 snapshot 供审计，调用方按其实际容器 ID 和 snapshot receipt 清理。本包也提供原 `tfidf_added_p1_host_grade_PREPARE_20261003_r1.py:grade(j,m,out)`，它结合作者原正式适配器的严格扫描与 owned cleanup；需要复用该完整策略的接入方按其源码签名绑定自己的 job、guard 和凭据回执。
