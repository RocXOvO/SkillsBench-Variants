# 运行部署交接

本目录与 `deployment-supplement-20261012` Release 配套，补充 233 批任务的运行部署。先下载冻结任务，再下载部署补充；二者必须同时保留。222 批作为独立历史数据集保存，本次部署核查以报告对应的 233 批为范围。

## 缺失清单如何对应

| 报告要求 | 交付材料 | 对应索引 |
|---|---|---|
| 48 项独立 grader 环境无 Dockerfile | 原镜像导出，覆盖 47 项；GW P2 提供历史完整构建上下文、固定基础镜像、重建镜像和验证记录 | `metadata/REPORT-COVERAGE.json`、`metadata/IMAGES.json` |
| TF-IDF P1/P2 的 grader_image 为空 | 两个准确的干净测量镜像、原宿主机评分器、停止后快照工具及宿主机启动命令 | `docs/TFIDF.md` |
| exoplanet P3 缺 private/grader/test.sh | 原外部评分源码、所需真实 pytest 镜像、可执行调用工具、挂载与结果协议 | `docs/INTERFACES.md` |
| 205 项的 236 个镜像引用无法获取 | 提供整个 233 批的镜像集合，以及实际原评分器额外引用的镜像 | `metadata/IMAGES.json`、Release 镜像分卷 |
| solver 到 grader 的交接协议 | 233 项原部署绑定、官方任务入口、已声明历史运行器版本、评分回调及依赖、特殊入口工具 | `metadata/DEPLOYMENT-233.json`、`docs/INTERFACES.md` |

镜像导出是报告明确接受的交付方式，因此无需用猜测的 Dockerfile 替代原环境。报告中的 6 项已有配方也包含在镜像与任务集合中。报告未附完整 205 项 ID 或 `PREPARED_PLAN.json`；本交付覆盖全部 233 项，并核对报告逐名列出的 57 项，没有声称验证接入方那份计划的哈希。

## 文件分布

```text
SkillsBench-Variants/             # Git 仓库：说明、工具和机器可读索引
  README.md
  variants/
    infra/
      README.md
      Dockerfile                 # 原辅助脚本所需 Python/Docker/宿主工具
      compose.yaml               # 可选：隔离的 Docker 测试命名空间
      tools/                     # 下载、路径恢复、镜像加载、特殊评分入口
      docs/                      # 运行与交接协议
      metadata/                  # 233 项绑定、报告对应、镜像和包哈希

downloads/                       # Release 下载到本机；不进入 Git
  variant-tasks-233-20261010.tar.gz
  variant-tasks-222-20261011.tar.gz
  variant-infra-materials-20261012.tar.gz
  variant-actor-runtime-20261012.tar.gz
  variant-environments-20261012.tar.zst
  variant-runtime-images-20261012.tar.gz

extracted/
  variant-tasks-233-20261010/tasks/<variant_id>/
  variant-tasks-222/tasks/<variant_id>/
  variant-infra-materials-20261012/
    runtime/original/            # 原源码与配置，按来源路径保存
    native-dependencies/original/# 原评分器固定依赖，包括离线 Maven 资产
    recipes/gw-p2-historical-context/
    metadata/
  variant-actor-runtime-20261012/  # 固定的 6 个原 CLI 运行时文件

workspace/rootfs/                # 工具还原的原绝对路径命名空间
  data/amax/
  home/amax/
workspace/prepared.json          # 本次还原回执
```

`tasks/<id>/public` 供 solver 使用；`private/grader` 及可信评分依赖仅供评分阶段。不要把整个 `tasks/<id>` 或补充包挂给受测 agent。task archive 里的扁平兼容副本和 `public` 副本是冻结内容的一部分，保留原结构；恢复工具处理原评分器需要的目录别名。

## 下载和还原

在仓库根目录执行，Python 工具只用标准库：

```sh
python3 variants/infra/tools/download.py --group all --output "$PWD/downloads"
mkdir -p extracted
tar -xzf downloads/variant-tasks-233-20261010.tar.gz -C extracted
tar -xzf downloads/variant-tasks-222-20261011.tar.gz -C extracted
tar -xzf downloads/variant-infra-materials-20261012.tar.gz -C extracted
tar -xzf downloads/variant-actor-runtime-20261012.tar.gz -C extracted
python3 variants/infra/tools/prepare_workspace.py \
  --manifest variants/infra/metadata/MANIFEST-233.json \
  --tasks extracted/variant-tasks-233-20261010/tasks \
  --materials extracted/variant-infra-materials-20261012 \
  --actor-runtime extracted/variant-actor-runtime-20261012 \
  --workspace "$PWD/workspace"
```

下载器按清单校验每卷和完整归档，支持中断后继续，临时空间最多多占一卷。只接手报告实验可用 `--group 233`；该组同时下载 233 任务及全部部署补充。`--group 222` 只下载历史任务包。镜像归档不解压成任务目录。`.tar.zst` 采用 2 GiB 窗口的标准 zstd 无损压缩，工具先在宿主机解压再送入 Docker；不能直接使用 Docker 的默认 zstd 解码窗口。宿主机需 zstd 1.4.8+，解码额外预留约 2 GiB 内存；建议正式主机至少 24 GiB RAM。

先克隆 `https://github.com/RocXOvO/SkillsBench-Variants.git` 并进入仓库根目录。Git 中的 `PACKAGES.json` 是完整发布目录，补充归档里的副本工具与本仓库配套使用；独立验证回执保存在 Git 的 `metadata/VALIDATION.json` 及 Release 配套 JSON 中。

## 推荐运行环境：独立 Linux/amd64 主机或虚拟机

原环境为 Linux/amd64、Docker 29.5.0、containerd 镜像存储。任务预算最多 8 CPUs、16 GiB 内存，GPU 数为 0；给主机额外留出 Docker 与宿主工具的资源。建议预留至少 500 GB 磁盘，含下载、完整镜像存储、路径还原及实验输出；并发数量另按任务预算计算。宿主机安装 Python 3.11+、Bash、GNU coreutils、util-linux（含 `prlimit`）、tar 、zstd 和 Docker CLI。MAC/ARM 本机可以下载和校验，正式测量在 Linux/amd64 执行。

containerd 存储保留这些原 OCI 镜像 ID；不能把归档转换成经典存储镜像后仍声称同一原 ID。参见 [Docker containerd 镜像存储说明](https://docs.docker.com/engine/storage/containerd/)。本包的 Docker 版本和配置来源于原服务器与空引擎导入验证。

本包交付并验证 Linux/amd64 的完整执行图。少数原多架构索引还引用服务器上已不存在的其他架构或 attestation；这些不属于本次执行平台。导入命令固定 `--platform linux/amd64`，不声称提供 ARM 镜像。

在**专用于本次复现的新 Linux 主机**，建立原运行器需要的命名空间：

```sh
export PYTHONDONTWRITEBYTECODE=1
sudo mkdir -p /data/amax /home/amax
sudo mount --bind "$PWD/workspace/rootfs/data/amax" /data/amax
sudo mount --bind "$PWD/workspace/rootfs/home/amax" /home/amax
python3 variants/infra/tools/load_images.py \
  --catalog variants/infra/metadata/IMAGES.json \
  --archive downloads/variant-environments-20261012.tar.zst \
  --archive downloads/variant-runtime-images-20261012.tar.gz \
  --receipt "$PWD/workspace/images-loaded.json"
```

已有同名目录含其他工作时，改用新的虚拟机。这里的两处挂载让原源码保持不变，包括源码里固定的路径、哈希与本地镜像别名。导入工具核验完整包、架构和每个镜像 ID，然后恢复原别名；这些别名不是公开 registry 拉取地址。

## 可选的隔离 Docker 命名空间

`compose.yaml` 提供固定 Docker 29.5.0 的独立引擎，适合导入核验和普通容器评分。TF-IDF 的正式性能测量使用上面的原生 Linux 宿主机路线；本次并发进行镜像导出等重 I/O 时，嵌套及共享宿主环境都曾出现停止容器超时。正式性能测量应在空闲的独立原生主机执行；容器控制异常保留工程状态，不能作为候选任务分数。

```sh
set -o pipefail
docker image load --platform linux/amd64 --input downloads/variant-runtime-images-20261012.tar.gz
export VARIANTS_WORKSPACE="$PWD/workspace"
export VARIANTS_DOWNLOADS="$PWD/downloads"
export VARIANTS_DOCKER_GID="$(id -g)"
cd variants/infra
docker compose -p skillsbench-variants up -d engine
zstd -dc --long=31 "$VARIANTS_DOWNLOADS/variant-environments-20261012.tar.zst" | docker compose -p skillsbench-variants exec -T engine docker image load --platform linux/amd64
docker compose -p skillsbench-variants exec -T engine docker image load --platform linux/amd64 --input /downloads/variant-runtime-images-20261012.tar.gz
docker compose -p skillsbench-variants run --rm controller tools/load_images.py --verify-only \
  --catalog /infra/metadata/IMAGES.json \
  --archive /downloads/variant-environments-20261012.tar.zst \
  --archive /downloads/variant-runtime-images-20261012.tar.gz \
  --receipt /data/amax/skillsbench-variants/runs/images-loaded.json
```

engine 用独立存储和 Unix socket；controller 带 `prlimit` 等原辅助工具。此引擎可运行容器，不需要作者服务器。不要把 engine socket 挂到 solver。完成本轮后用同一项目名 `docker compose down`；需要保留复现镜像时保留该项目的数据卷。

## 交给实验适配器的材料

先用 `tools/inspect_task.py` 查看准确 ID。`ENTRYPOINTS-233.json` 给出全部 233 项的权威来源记录、任务内入口文件、捕获范围和实际镜像配置；232 项有任务内 `private/grader/test.sh`，exoplanet P3 使用本包外部入口。`DEPLOYMENT-233.json` 包含原 solver/grader、有效评分镜像、预算、public 文件与输出绑定、评分模式、历史运行器校验值、原回调及特殊入口。历史运行器源码位于补充包 `runtime/original/`；CLI 版本为 `codex-cli 0.147.0`。

报告已经冻结的 SkillRevise/VISE skill 与 gpt-6-sol 的调用、成本账本属于接入方的实验适配器；报告明确不要求作者重新生成 skill 或提供 API 密钥。本包提供作者侧的运行环境和部署协议。接入方调用自己的模型后，必须停止所有 agent 后代，按对应任务规则冻结产物，再调用原 grader，并给本次运行保存新的回执。原历史队列的 `__main__` 带历史调度路径，禁止作为新的批处理启动命令。原完整 formal 入口还带作者历史模型、方法与 seal 的限制；接入方使用自己的 generation 适配器，按本包索引绑定对应的停止产物捕获与原科学评分 API，不能把历史 gpt-5.5 调度函数当作 gpt-6-sol 的新实验启动器。

空的 manifest `output_roots` 或 `grader_image` 不意味着可以采用通用猜测。以具体原评分器及特殊部署协议为准。评分工程失败保持 `reward=null`，任务正常完成失败才是 `reward=0`。完整规则见 [评分交接](docs/INTERFACES.md) 和 [TF-IDF 宿主机协议](docs/TFIDF.md)。

## 版本与验证

两批任务 archive 保持原 SHA256。已声明的 17 个历史 runner 版本、37 个 helper 版本，以及 10 项扩展实际启动记录补查得到的 2 个额外 runner 版本均已恢复。记录见 `HISTORICAL-PIN-COVERAGE.json`；逐文件补充索引见 `SOURCE-FILES.json`。验证记录分别说明文件与依赖完整性、镜像图校验、空引擎导入、特殊入口真实评分；不能把文件校验等同于 205 项的新模型实验全部跑完。

GW P2 的历史镜像 `20bcd779…` 已不存在，交付的 `3b50e63f…` 从原历史 Dockerfile、固定基础镜像和一致的公开 GWF 构建，评分器与科学文件保持冻结，并通过评分对照。Court 三项原注册评分器本就使用已合格的缓存镜像覆盖历史缺失 ID；保留原映射与版本证明。上述差异都在 `IMAGES.json` 中记录，不声称恢复了旧镜像字节身份。

原始任务和部署源码保持字节与哈希，宿主调用设置 `PYTHONDONTWRITEBYTECODE=1`，避免导入时在冻结树中新增缓存。10 项 Bike/Edit-PDF/Paratransit/UC-P3 的实际 launch 记录已逐字段与冻结 cell 核对；Bike 的两个历史恢复脚本只作来源证据，新实验使用官方 grader 入口，不运行它们的历史恢复 main。

最终补充包已经用完整 233 任务归档执行路径恢复，实际还原并逐文件核验 19,373 个文件，包含 6,377 个原运行部署及依赖文件。`metadata/validation/` 保存各检查的范围和回执，`metadata/VALIDATION.json` 汇总发布验收。镜像格式、导入和特殊评分入口的检查分别记录，未开展 205 项新模型实验。

镜像扫描中出现的公开测试夹具按原基础镜像层、文件 SHA256 和上游来源逐项核对；仅接受明确证明的文件，不跳过整个依赖目录。来源证据在 `metadata/validation/public-image-fixture-evidence.json`。`audits/verify_image_export.py` 保留实际使用的离线镜像图与文件扫描程序；如需独立复查，先从 `IMAGES.json` 为对应归档取出 `image_ids`，写成 `{"image_ids": [...]}` 的选择文件，然后执行：

```sh
python3 variants/infra/audits/verify_image_export.py \
  downloads/variant-environments-20261012.tar.zst \
  workspace/main-image-selection.json \
  workspace/main-image-audit.json \
  variants/infra/metadata/validation/public-image-fixture-evidence.json
```
