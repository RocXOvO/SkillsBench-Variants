# solver 与 grader 的交接

`metadata/DEPLOYMENT-233.json` 按 `variant_id` 给出全量绑定。先读取 `original_cell` 的 public 文件、工作目录、image 和输出规则，再读取 `deployment_mode`、`native_profile` 与 `special_entry`。预算以冻结 `public/task.toml` 和对应 `input-plan-r2.json` 的绑定为依据，索引保存有效预算；manifest 空字段不能覆盖这些预算。

## 原运行器与评分回调

`original_runner_sha256` 与 `original_runner_package_paths` 指向补充包里的准确历史版本；`original_helper_pins` 与 `HISTORICAL-PIN-COVERAGE.json` 对应辅助文件。所有原源码保留原 bytes，不直接改写路径或 pin。原 API 需要的绝对路径由 `prepare_workspace.py` 与挂载命名空间恢复。

76 项为原运行器内置评分，154 项要求保留停止后的 actor 并调用对应原评分器；另有 2 项 TF-IDF 宿主机协议及 1 项 exoplanet P3 外部协议。142 个注册 profile 的完整字段与资源 pin 在 `NATIVE-PROFILES.json`。其余保留 actor 的任务使用相应原分支或单独回调，以索引对应的源运行器及任务内官方入口为准。`ENTRYPOINTS-233.json` 同时记录这类入口的文件哈希和原 source manifest；未给 runner pin 的历史行保留该事实，不用同名脚本猜测历史版本。

注册回调入口位于：

```text
/home/amax/spark-native-work/self-evo-skillsbench-20260926-r1/server_queue/
  ordinary-skill-233-20261009-r1/native_registered_dispatcher_r5.py
```

模块的 `profiles()`、`callback_module(row)` 返回准确原回调，包括 Court 缓存评分环境覆盖；常用回调签名是 `grade_after_actor(row, freeze, actor_receipt_path, attempt_dir, entry)`。`row` 是原计划行加准确 `evaluation_contract`，`freeze` 是接入方本次冻结输入记录，`actor_receipt_path` 是本次停止后的 solver 回执，`attempt_dir` 为新目录，`entry` 是原注册记录。各 profile 在调用前检查完整契约、源码、资源和产物边界。不要只取原 `grade_ready_*.py` 后跳过注册适配器已经规定的修复或覆盖。

原队列调度器和创建 seal 是历史方法运行的记录，不是新实验的现成授权。接入方保存自己的冻结 skill、模型参数、generation 超时、resource 约束、真实 container ID、停止状态、输入/输出哈希、评分命令与新 reward 回执。私有测试、truth、reference 及评分源码均不挂给 solver。

## exoplanet P3

任务冻结 `private/grader` 只有两个文件；原评分入口在目录外，提供外部入口满足缺失清单要求。不要在冻结目录里插入新 `test.sh` 破坏原树哈希。

停止健康的 solver，保留 `skillsbench-variants.variant=exoplanet-detection-period--p3--dev-401` 标签，然后在还原命名空间中执行：

```sh
python3 variants/infra/tools/grade_exoplanet_p3.py \
  --solver-container "$SOLVER_CONTAINER" \
  --output-dir /data/amax/skillsbench-variants/runs/exoplanet-new-run
```

该工具调用原 `grade_ready_exoplanet_p3.py:one`，仅捕获 `/root/period.txt`。实际评分镜像为 `ec75d3c7…`，别名 `transfer-financial-grader:direct-r1`，它与 manifest 的 solver 镜像不同，加载工具会恢复别名。

| 项目 | 固定协议 |
|---|---|
| private/grader | `/tests:ro` |
| 冻结产物 | `/capture/root/period.txt`，capture 目录只读 |
| 事件观察器 | `/observer/jpg_phase_record.py:ro` |
| 工作目录、资源 | `/tmp`，1 CPU，8192 MiB，断网、只读 rootfs，128 MiB `/tmp` |
| 环境 | `PYTHONPATH=/observer`、`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` |
| 命令 | `python3 -B -m pytest -c /dev/null --rootdir=/tests --confcutdir=/tests -p no:cacheprovider -p jpg_phase_record --assert=plain /tests/test_outputs.py` |
| 完成证据 | 4 个原测试、12 个 setup/call/teardown 事件、真实容器状态与退出码 |
| 结果 | 新输出目录 `exoplanet-evaluation/result.json`，`status=valid` 时 reward 为 0/1；工程异常 null |
| 总预算 | 捕获、启动、测试、发布及 cleanup 共 240 秒 |

## GW P2

solver 保持原 `99678fc2…`；评分使用已记录的历史配方重建镜像 `3b50e63f…`。这个专用入口负责把已记录的旧缺失镜像引用改为重建环境，优先于仍保留旧 ID 的历史脚本。停止健康 solver 并保留同名变体标签后：

```sh
python3 variants/infra/tools/grade_gw_p2.py \
  --solver-container "$SOLVER_CONTAINER" \
  --output-dir /data/amax/skillsbench-variants/runs/gw-p2-new-run
```

用原停止产物捕获器冻结 `/root/detection_results.csv`，不在 solver 中执行新代码。private grader 只读挂到 `/opt/grader`、冻结 CSV 目录到 `/capture:ro`、日志目录到 `/logs/verifier:rw`。评分工作目录 `/root`，8 CPUs、8192 MiB，断网、只读 rootfs；命令为 `python -I /opt/grader/run.py`。总预算 240 秒，正常结果为 `logs/committed.json` 的 `status=completed`、reward 0/1，并核对 `logs/reward.txt`。有效正确输出完成 9 个原测试；缺产物是原评分器明确的有效 0 分，工程失败不可变成 0。

`recipes/gw-p2-historical-context/` 含完整历史 Dockerfile 与 GWF。如需重建，先恢复 `reviewed-transfer-gw-public:compat-r3` 到记录的固定基础镜像，再执行 `docker build --pull=false --network=none`，保存本次新 ID；Dockerfile 和输入相同不保证获得历史 ID。

## 结果记录

接入方保存新 run 的输出，分清任务失败与工程失败：原评分器已经完成的错误答案是 0；超时、镜像/文件漂移、容器控制失败、依赖缺失或无法完成要求的测试是 null/工程状态。新的 run 目录不可复用历史结果或覆盖之前的运行。
