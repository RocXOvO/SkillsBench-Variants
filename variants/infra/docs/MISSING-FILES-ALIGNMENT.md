# 与部署缺失清单逐项对齐

依据用户提供的《SkillsBench-Variants 部署缺失清单》（2026-10-12），逐项核对其完整 ID、已发布镜像、任务文件、原运行器与评分入口。清单明确列出的 57 项全部对应，未发现交付索引遗漏。完整 ID、镜像 SHA256、归档、入口及预算见 [REPORT-ALIGNMENT.json](../metadata/REPORT-ALIGNMENT.json)。

| 清单要求 | 已交付方案 | 数量与说明 |
|---|---|---|
| 独立 grader 环境缺 Dockerfile | 镜像导出；GW P2 另提供原历史完整构建上下文 | 48 项：47 项原镜像，1 项明确记录的新 ID 重建镜像 |
| TF-IDF P1/P2 grader_image 为空 | 原宿主机评分 API、准确干净测量镜像、快照与启动工具 | 2 项，按 [TF-IDF 协议](TFIDF.md) 执行；原 null 不改写成猜测的独立 grader |
| exoplanet P3 缺 test.sh | 原外部评分源码、调用工具、真实 pytest 镜像与产物协议 | 1 项，按 [外部入口说明](INTERFACES.md#exoplanet-p3) 执行 |
| 236 个非空镜像引用无法获取 | 交付整个 233 父集合的镜像及原评分器额外依赖 | 父集合 268 个原引用中 267 个保留原 ID，GW P2 用记录的新重建 ID；总共交付 282 个镜像 |
| solver → grader 交接 | 原运行器、权威源 manifest、逐任务 public/产物/入口与预算绑定 | [233 项部署绑定](../metadata/DEPLOYMENT-233.json)、[233 项入口](../metadata/ENTRYPOINTS-233.json)、[交接说明](INTERFACES.md) |
| 原已有 grader Dockerfile | 冻结任务内配方及其原镜像 | 清单中的 6 项原样保留 |

报告没有附完整 205 项 ID 或 PREPARED_PLAN.json。本次采用完整 233 父集合覆盖，核对报告逐名列出的 57 项，不声称核验接入方未提供的计划哈希。类别存在重叠，不能把数量相加当作受影响总数。

## 下载位置与使用顺序

- [原任务 Release](https://github.com/RocXOvO/SkillsBench-Variants/releases/tag/variant-datasets-20261011)：`variant-tasks-233-20261010.tar.gz`，任务相对路径为 `variant-tasks-233-20261010/tasks/<variant_id>/`。222 历史批次独立保存。
- [部署补充 Release](https://github.com/RocXOvO/SkillsBench-Variants/releases/tag/deployment-supplement-20261012)：A = `variant-environments-20261012.tar.zst`，B = `variant-runtime-images-20261012.tar.gz`；另有 `variant-infra-materials-20261012.tar.gz` 原源码/依赖/重建上下文、`variant-actor-runtime-20261012.tar.gz` 固定 CLI。
- 镜像表中的 ID 是本地导入后的标识；下载采用 [PACKAGES.json](../metadata/PACKAGES.json) 中的分卷 URL 和 SHA256。按 [部署 README](../README.md) 下载、恢复路径并加载镜像。

在仓库根目录执行：

```sh
python3 variants/infra/tools/download.py --group 233 --output "$PWD/downloads"
```

## 逐项对应

下表镜像 SHA256 显示前 12 位便于阅读，完整值在配套 JSON。TF-IDF 列出的镜像供停止后快照的干净测量容器使用，宿主机执行原评分 API。

| 变体 ID | 清单分类 | 交付方案 | 实际评分/测量镜像 | 所在包 |
|---|---|---|---|---|
| `adaptive-cruise-control--p2--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `6e24bd675a73` | A |
| `adaptive-cruise-control--p3--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `4d8b22d75356` | A |
| `dynamic-object-aware-egomotion--p3--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `5fd5ebca1b43` | A |
| `earthquake-phase-association--p2--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `4322be448a54` | A |
| `econ-detrending-correlation--p2--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `604ce6cadf77` | A |
| `econ-detrending-correlation--p3--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `604ce6cadf77` | A |
| `edit-pdf--p1--sr-ext-401` | 独立评分环境缺配方 | 原镜像导出 | `aff87a250bec` | A |
| `edit-pdf--p2--sr-ext-401` | 独立评分环境缺配方 | 原镜像导出 | `aff87a250bec` | A |
| `edit-pdf--p3--sr-ext-401` | 独立评分环境缺配方 | 原镜像导出 | `aff87a250bec` | A |
| `energy-market-pricing--p1--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `7bc36553a8a4` | A |
| `energy-market-pricing--p2--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `7bc36553a8a4` | A |
| `energy-market-pricing--p3--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `8b84079f8af2` | A |
| `energy-unit-commitment--p1--sr-ext-401` | 独立评分环境缺配方 | 原镜像导出 | `cb32e79f73b9` | A |
| `energy-unit-commitment--p2--sr-ext-401` | 独立评分环境缺配方 | 原镜像导出 | `f91526bae7f2` | A |
| `energy-unit-commitment--p3--sr-ext-401` | 独立评分环境缺配方 | 原镜像导出 | `c00df5d3e639` | A |
| `enterprise-information-search--p3--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `78387bc3881b` | A |
| `glm-lake-mendota--p2--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `521d61f4065c` | A |
| `gravitational-wave-detection--p2--dev-401` | 独立评分环境缺配方 | 历史配方重建 + 镜像 | `3b50e63f024f` | A |
| `gravitational-wave-detection--p3--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `85ce1ec62407` | A |
| `grid-dispatch-operator--p1--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `3056539247c3` | A |
| `grid-dispatch-operator--p3--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `193628227d5f` | A |
| `hvac-control--p1--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `ac6e0a588ecc` | A |
| `hvac-control--p3--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `ac6e0a588ecc` | A |
| `invoice-fraud-detection--p2--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `71cab6d86da8` | A |
| `manufacturing-fjsp-optimization--p1--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `78387bc3881b` | A |
| `manufacturing-fjsp-optimization--p2--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `78387bc3881b` | A |
| `manufacturing-fjsp-optimization--p3--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `78387bc3881b` | A |
| `mars-clouds-clustering--p2--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `b44b0c494656` | A |
| `multilingual-video-dubbing--p3--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `b234145d73be` | A |
| `organize-messy-files--p1--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `059c319f94e6` | A |
| `parallel-tfidf-search--p1--dev-401` | 宿主机评分环境 | 宿主评分器 + 干净测量镜像 | `f807d85f5de5` | A |
| `parallel-tfidf-search--p2--dev-401` | 宿主机评分环境 | 宿主评分器 + 干净测量镜像 | `0eaefb647eb7` | A |
| `paratransit-routing--p1--sr-ext-401` | 独立评分环境缺配方 | 原镜像导出 | `66b3643fa54f` | A |
| `paratransit-routing--p2--sr-ext-401` | 独立评分环境缺配方 | 原镜像导出 | `d2c0e3df752e` | A |
| `paratransit-routing--p3--sr-ext-401` | 独立评分环境缺配方 | 原镜像导出 | `8f4e6e5057e7` | A |
| `pddl-tpp-planning--p1--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `78387bc3881b` | A |
| `pddl-tpp-planning--p2--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `78387bc3881b` | A |
| `pddl-tpp-planning--p3--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `78387bc3881b` | A |
| `protein-expression-analysis--p1--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `9239cd663e69` | A |
| `protein-expression-analysis--p2--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `ad39e0b8b738` | A |
| `protein-expression-analysis--p3--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `a8bdd5014942` | A |
| `r2r-mpc-control--p1--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `ac6e0a588ecc` | A |
| `r2r-mpc-control--p2--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `ac6e0a588ecc` | A |
| `r2r-mpc-control--p3--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `ac6e0a588ecc` | A |
| `radar-vital-signs--p1--sr-ext-401` | 独立评分环境缺配方 | 原镜像导出 | `7b3b710d9f0e` | A |
| `radar-vital-signs--p3--sr-ext-401` | 独立评分环境缺配方 | 原镜像导出 | `7b3b710d9f0e` | A |
| `reserves-at-risk-calc--p1--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `16320073cc01` | A |
| `reserves-at-risk-calc--p2--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `310b87ac824a` | A |
| `reserves-at-risk-calc--p3--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `19b261fdc205` | A |
| `threejs-to-obj--p2--dev-401` | 独立评分环境缺配方 | 原镜像导出 | `3ed589a2899c` | A |
| `exoplanet-detection-period--p3--dev-401` | 缺评分入口 | 原外部入口 + 实际评分镜像 | `ec75d3c7acc4` | A |
| `exoplanet-detection-period--p1--dev-401` | 原已有配方 | 原镜像导出 | `dfcbe4c22f6f` | A |
| `offer-letter-generator--p1--dev-401` | 原已有配方 | 原镜像导出 | `3a950e522609` | A |
| `offer-letter-generator--p2--dev-401` | 原已有配方 | 原镜像导出 | `f10edcb93f94` | A |
| `paper-anonymizer--p2--dev-401` | 原已有配方 | 原镜像导出 | `ba84acf395a8` | A |
| `quantum-numerical-simulation--p1--dev-401` | 原已有配方 | 原镜像导出 | `c3b03fec281e` | A |
| `quantum-numerical-simulation--p2--dev-401` | 原已有配方 | 原镜像导出 | `c3b03fec281e` | A |

## 交接边界与验证记录

233 项的 agent/verifier 预算均已绑定到原公开配置与原计划来源；manifest 的空字段不覆盖权威预算。运行器、回调及固定依赖放在素材包，路径与文件哈希见 SOURCE-FILES.json。评分正常完成的错误答案为 0，依赖/容器控制等工程失败为 null。

GW P2 旧镜像已不存在：交付原完整配方、固定基础镜像、输入资产和经评分对照验证的新镜像；差异见 [GW-P2-REBUILD.json](../metadata/GW-P2-REBUILD.json)。Court 三项的历史 native 镜像按原注册评分器使用合格缓存环境，映射见 IMAGES.json；原计划仍存在的镜像同时保留。

既有验收覆盖 19,373 个真实恢复文件、282 个镜像的图/文件/层校验及空引擎导入后的元数据核对，并包含 TF-IDF 两项、GW P2 和 exoplanet P3 的真实评分对照；范围见 [VALIDATION.json](../metadata/VALIDATION.json)。整集空引擎导入没有解包所有 RootFS，不代表已执行全部 233 个 grader。本次对齐没有启动新的模型实验。

清单已明确 gpt-6-sol 调用、冻结 skill 接入与成本账本属于接手方适配器；交付原运行部署材料，不需要作者提供 API 凭据或重新生成 skill。
