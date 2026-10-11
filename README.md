# SkillsBench Variants

两批 SkillsBench 实验变体源文件，合计 455 个变体包。

| 批次 | 使用方法 | 变体数 | 原任务数 | P1 / P2 / P3 | 完整压缩包大小 |
|---|---|---:|---:|---|---:|
| 四方法批次 | Generic、SkillLearn、Trace、SkillRevise | 233 | 81 | 81 / 71 / 81 | 6.06 GB |
| 三方法历史批次 | CoEvoSkills、SPARK、SkillEvolver | 222 | 77 | 77 / 68 / 77 | 5.49 GB |

[下载两批变体及文件清单](https://github.com/RocXOvO/SkillsBench-Variants/releases/tag/variant-datasets-20261011)。233 批为 46 卷，222 批为 41 卷，每卷最多 128 MiB。

归档包含任务输入、环境与构建资产、评分器和可用的源测试、solution。对应 Release 中的 `MANIFEST-233.json`、`MANIFEST-222.json` 记录逐文件来源、权限与 SHA256。

## 下载与解压

```sh
gh release download variant-datasets-20261011 --repo RocXOvO/SkillsBench-Variants --dir variant-datasets-20261011
cd variant-datasets-20261011
cat variant-tasks-233-20261010.tar.gz.chunk-* > variant-tasks-233-20261010.tar.gz
cat variant-tasks-222-20261011.tar.gz.chunk-* > variant-tasks-222-20261011.tar.gz
shasum -a 256 -c SHA256SUMS
tar -xzf variant-tasks-233-20261010.tar.gz
tar -xzf variant-tasks-222-20261011.tar.gz
```

先合并同一批的全部分卷，再校验和解压。Linux 可使用 `sha256sum -c SHA256SUMS`。详细说明见 [README-download-extract.txt](variants/README-download-extract.txt)。

## 校验与来源

两份完整包的 25,174 个任务文件均已核对 SHA256、大小和权限；Release 中 87 个分卷与配套清单也完成了 SHA256 校验。

- [两批组成与 ID 差异](variants/batches.json)：共有 213 个 ID，分别独有 20 和 9 个；相同 ID 不自动代表相同文件版本。
- [压缩包及附件记录](variants/package-record.json)与 [SHA256SUMS](variants/SHA256SUMS)。
- [233 批校验报告](variants/validation-233.json)与 [222 批校验报告](variants/validation-222.json)。

222 批保留历史构造包及当时定位到的 public/grader 阶段。SPARK 和 CoEvoSkills 的历史结果各为 221 项，音频 P3 是历史排除项，但该任务仍包含在 222 个源文件包中。该归档记录源文件来源，本次没有新增模型调用或评测。
