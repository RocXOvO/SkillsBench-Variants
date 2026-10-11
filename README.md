# SkillsBench Variants

用于交接实验的两批冻结变体任务，以及 233 批的运行部署补充。

| 批次 | 原使用方法 | 变体数 | 原任务数 | P1 / P2 / P3 |
|---|---|---:|---:|---|
| 四方法批次 | Generic、SkillLearn、Trace、SkillRevise | 233 | 81 | 81 / 71 / 81 |
| 历史三方法批次 | CoEvoSkills、SPARK、SkillEvolver | 222 | 77 | 77 / 68 / 77 |

两批合计 455 个变体包、242 个唯一 ID，213 个 ID 重合；重合不代表文件版本相同。原任务包包含 public 输入、environment 构建资产、private grader、原测试及可用 solution，保持冻结文件结构与 SHA256。

- [冻结任务 Release](https://github.com/RocXOvO/SkillsBench-Variants/releases/tag/variant-datasets-20261011)：233 和 222 两批源文件、原 manifest 与校验记录。
- [部署补充 Release](https://github.com/RocXOvO/SkillsBench-Variants/releases/tag/deployment-supplement-20261012)：完整镜像导出、原运行器及依赖、固定 CLI、特殊评分入口和部署索引。
- [交接与运行说明](variants/infra/README.md)：文件分布、下载、路径恢复、Linux 环境准备和评分协议。接手跑实验从这里开始。
- [缺失清单逐项对应](variants/infra/metadata/REPORT-COVERAGE.json)：报告明确列出的 57 项和全部 233 项部署材料。
- [缺失清单交付对照表](variants/infra/docs/MISSING-FILES-ALIGNMENT.md)：按原报告逐项列出镜像所在包、评分入口与交付方案，配套完整 ID 和 SHA256 核查记录。

部署补充按原报告覆盖整个 233 批：48 项缺 grader 配方提供可执行评分镜像；TF-IDF P1/P2 明确为宿主机评分，并提供准确测量环境和启动工具；exoplanet P3 提供原目录外评分入口。报告未附完整 205 项计划，交付采用全 233 项覆盖，接入方可按已有冻结 skill 范围选取。

镜像包包含原部署引用及原评分器额外依赖，按 ID、文件与层哈希校验，不能只把 sha256 当 registry 拉取地址。GW P2 旧镜像已经不存在，本次交付历史完整配方重建的环境和新 ID；Court 三项保留原注册适配器已有的缓存镜像覆盖与版本证据。差异和测试范围见交接说明及机器可读索引。

在仓库根目录可一并下载并核验：

```sh
python3 variants/infra/tools/download.py --group all --output "$PWD/downloads"
```

只接手报告所述实验，使用 `--group 233` 下载 233 任务和全部部署补充；222 历史包单独保存。镜像文件放在 Release 分卷中，Git Code 保留说明、工具和清单；详细解压与部署命令见运行说明。

两份原归档的 25,174 个逻辑任务文件已经逐项核对大小、模式与 SHA256。原 Release 的 87 个分卷及配套文件保留。233 为 46 卷，222 为 41 卷，每卷最大 128 MiB。

当前仓库及 Release 公开；原 `package-record.json` 的 `repository_private: true` 保留归档创建时的历史状态。当前下载目录和权限记录见 `variants/infra/metadata/PACKAGES.json`。

[两批组成](variants/batches.json)、[原包记录](variants/package-record.json)、[原包 SHA256](variants/SHA256SUMS)、[233 文件验证](variants/validation-233.json)、[222 文件验证](variants/validation-222.json)。222 批的 SPARK 和 CoEvoSkills 历史结果各为 221 项，音频 P3 为历史排除项，源任务仍包含在 222 包中。本次交付未重跑这些方法或产生新的模型实验结果。
