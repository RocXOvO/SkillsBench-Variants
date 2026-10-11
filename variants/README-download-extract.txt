SkillsBench 变体源文件归档（2026-10-11）

233 个：Generic / SkillLearn / Trace / SkillRevise；81 个原任务，P1=81、P2=71、P3=81。
222 个：CoEvoSkills / SPARK / SkillEvolver 历史批次；77 个原任务，P1=77、P2=68、P3=77。
两批交集 213 个 ID，但相同 ID 不自动代表同一文件版本。

每批包含变体任务输入、环境及构建资产、评分器和可用的原始测试/solution。
222 批保留构造包及当时定位到的 public/grader 文件，逐文件来源、权限和 SHA256 见对应 MANIFEST。
这是源文件归档；历史修复评测并非统一协议，本次没有新增模型调用或评测。
历史选中结果数量：SPARK=221、CoEvoSkills=221、SkillEvolver=222、no_skill=222。
音频 P3 的 SPARK 和 CoEvoSkills 两格是历史排除项；该任务仍在 222 个源文件包中。

GitHub 单个 Release 资产小于 2 GiB；为便于上传重试，完整 gzip/tar 包切成最多 128 MiB 的二进制分卷。
233 批共有 46 卷，222 批共有 41 卷。下载同一批的全部 .chunk-*，不要分别解压分卷。
也可用 GitHub CLI 一次下载全部资产（私有仓库需登录）：

gh release download variant-datasets-20261011 --repo RocXOvO/SkillsBench-Variants --dir variant-datasets-20261011
cd variant-datasets-20261011

在 macOS/Linux 的同一目录中合并并校验：

cat variant-tasks-233-20261010.tar.gz.chunk-* > variant-tasks-233-20261010.tar.gz
cat variant-tasks-222-20261011.tar.gz.chunk-* > variant-tasks-222-20261011.tar.gz
shasum -a 256 -c SHA256SUMS

Linux 也可用 sha256sum -c SHA256SUMS。
校验通过后解压：

tar -xzf variant-tasks-233-20261010.tar.gz
tar -xzf variant-tasks-222-20261011.tar.gz

233 包目录：variant-tasks-233-20261010/tasks/<variant_id>/。
222 包目录：variant-tasks-222/tasks/<variant_id>/。
233 批的 edit-pdf 三个变体和 radar-vital-signs 两个变体将构建环境放在 public/Dockerfile、public/root/；其余使用 environment/。

归档含去重硬链接；请保留完整目录结构和文件权限。
两个完整包及分卷都保留在本机 output/variant-packages-20261011/。
