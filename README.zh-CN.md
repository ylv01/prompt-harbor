<p align="center"><img src="assets/brand/hero.svg" width="900" alt="PromptHarbor：理解任务，选择模型，汇合成果"></p>
<p align="center">
  <a href="LICENSE"><img src="assets/badges/license.svg" alt="Apache 2.0 许可证"></a>
  <a href="CHANGELOG.md"><img src="assets/badges/version.svg" alt="版本 0.2.1"></a>
  <a href="skills/promptharbor/SKILL.md"><img src="assets/badges/skill.svg" alt="Agent Skill"></a>
  <a href="docs/COVERAGE.md"><img src="assets/badges/data.svg" alt="模型数据 2026-09-29"></a>
</p>
<p align="center"><b>给它一个问题，它给你最值得考虑的 Top 3 模型。<br>给它一个工程，它帮你拆分、分配模型，并把成果带回主窗口。</b></p>
<p align="center"><a href="README.md">English</a> · 简体中文</p>

PromptHarbor 是一个 Agent Skill：识别普通 Prompt 的**领域、子领域和具体任务**，
结合任务评测与社区实测，默认给出 **Top 3、简洁理由和资源要求**，由用户根据已有
订阅、额度和工具自由选择。遇到较长工程时，每个部分也给出 Top 3；先约定接口，再拆分前端、后端、
数据库等工作，在当前窗口输出可直接复制的提示词。用户交给相应模型，最后把结果
带回主窗口检查、拼接和验收。

宿主 Agent 负责语义理解和联网研究，本地脚本负责可复查的筛选、排序与交接验证。

## 两种用法

**输出长这样：**“设计一个有交互的落地页。我已有 GPT-6 Sol、Kimi K3、DeepSeek V4.1 Flash。”

| Top 3 | 简洁理由 | 选择时看什么 |
|---|---|---|
| GPT-6 Sol | 当前快照的同组 WebDev 评测提供较强支持 | 已有账号的工具权限与额度 |
| Kimi K3 | WebDev 结果加上带作品的视觉网页社区记录 | 风格是否合适、可用额度；同时保留反面反馈 |
| DeepSeek V4.1 Flash | 有同组任务评测，可作为第三个可用选择 | 实际部署、成本与交互验收 |

这是限定上述资源的视觉设计示例，依据与日期见[完整输出](examples/frontend-output.md)。
不提供资源清单时，先给更广范围的 Top 3；提供后重新筛选。

**单个问题：**“检查我的 Python 股票回测有没有未来函数。”

识别为量化金融 + 代码分析，检索有关代码实现的能力证据，同时说明：编程评测不能
证明量化研究能力或收益。然后给出候选、证据链接、是否值得切换，以及时间切分、
成本、信息泄漏等验证方法。

**完整工程：**“帮我制作一个图书管理系统，包括评分和书评。”

| 部分 | 如何选择 | 交接边界 |
|---|---|---|
| 前端 | 根据任务评测与社区反馈给出 Top 3 | 页面、状态、类型化 API 客户端 |
| 数据库 | 保留示例声明的当前模型 GPT-6 Sol | 表结构、约束、种子数据与验证 SQL |
| 后端 | 给出 Top 3，用户选择一个遵循契约的模型 | API、事务、统一错误结构 |
| 测试 | 没有切换证据时保留当前模型 | 真实端到端流程与执行记录 |
| 集成 | 主窗口 | 检查接口、拼接文件、修复冲突、运行验收 |

选择任何候选都沿用同一份接口与验收标准。多个部分可以复用同一个模型。

完整示例含 [项目定义](examples/library-system/project.json)、
[共享接口](examples/library-system/contracts/interfaces.md) 和
[四份生成提示词](examples/library-system/handoffs/PLAN.md)。前端和数据库可先开始，
后端接收数据库交付后继续，测试接收全部实现，最终由主窗口集成。

## 安装

下载或克隆仓库，在仓库根目录运行：

```powershell
python scripts/install.py --host codex
```

安装器遵循 `CODEX_HOME`，未设置时使用用户目录下的 `.codex/skills`。
已有同名目录时拒绝覆盖。安装后重新加载技能或开启新对话。

```sh
python scripts/install.py --host claude
python scripts/install.py --dest /path/to/your/skills
```

也可以直接复制 `skills/promptharbor` 到兼容宿主的技能目录。脚本需要 Python 3.10+；
宿主直接阅读 Skill 和 JSON 证据不需要 Python。不同宿主的发现机制有所不同，安装
Skill 并不意味着它自动拦截所有消息。

## 开始使用

在支持 Skill 的宿主中输入：

```text
使用 $promptharbor。本对话后续我发送普通问题时，先识别任务并给出 Top 3 模型、理由和依据。
如果是工程项目，每个部分也给出 Top 3，并在当前窗口输出可复制的完整提示词。
我会把其他模型的成果带回来，由本窗口负责集成与验收。
```

随后直接发问题即可。单次使用也可以写：

```text
$promptharbor 这个任务适合什么模型：用 Lean 完成下面这个定理的证明。
```

工程交接提示词包括目标、接口版本、依赖、文件归属、验收标准和交付回执。
用户把提示词发给选择的模型，再将完整文件和回执带回。主窗口会检查实际成果并在
获准的工作区内集成。项目不自动登录其他平台、不自动调用付费 API，也不自动
切换当前模型。

## 本地试用与验证

```sh
python skills/promptharbor/scripts/harbor.py validate
python skills/promptharbor/scripts/harbor.py recommend --job examples/frontend.json
python skills/promptharbor/scripts/harbor.py recommend --job examples/backtest.json
python skills/promptharbor/scripts/harbor.py recommend --prompt "总结这段视频"
python skills/promptharbor/scripts/project.py compile --project examples/library-system/project.json --out out/handoffs
python -m unittest discover -s tests -v
```

`--prompt` 只是明确标注低置信度的中英文关键词降级模式。任意普通 Prompt 的语义
分类和工程拆分由宿主 Agent 完成，脚本不伪装成一个内置的语义模型。
推荐流程可通过 [结构化 job](skills/promptharbor/references/job-format.md) 复现。

复现历史示例时可加 `--as-of 2026-09-29`；当前建议应省略它，不能用旧日期绕过
过期检查。数据过期时可能不返回推荐。

## 依据与社区评价

当前快照包含 **49 个细分任务、11 个模型、50 条证据、22 个来源引用**。

- 区分官方能力声明、供应商测评、独立评测、社区作品报告、亲历反馈与推断。
- 保存模型版本、推理档位、工具环境、评测版本、指标、日期与局限。
- 不把综合榜单当作细分任务排名；不把长上下文容量当作可靠召回能力。
- 遇到未覆盖的模型或任务，宿主联网补充；离线时明确只基于已有快照。
- 写作风格、量化策略、形式化证明等任务需要各自的验证，不能套用邻近领域分数。

[覆盖表与证据缺口](docs/COVERAGE.md) · [调研记录](docs/RESEARCH.md) ·
[判断方法](skills/promptharbor/references/evidence.md) ·
[更新流程](skills/promptharbor/references/refresh.md)

社区权重默认：**前端实现与视觉设计 30%、多数写作任务 25%、一般任务 15%、
金融/医疗/法律任务 5%**。这些是可调整的初始策略，并非实验得出的最优比例。
有作品和提示词的报告权重高于个人感受；同源转载不重复加权；负面反馈会减分，
未知日期会折扣并限期失效。Arena 这类系统化人类偏好评测归入独立评测，避免重复计算。

Kimi K3 已纳入[公开网页作品记录](https://neuralhub.dev/ai-test-results)和
[有正反意见的前端使用反馈](https://www.reddit.com/r/kimi/comments/1vconet/is_kimi_k3_actually_good_or_was_it_overhyped/)。
这些证据影响视觉网页任务的推荐；“页面好看”“按设计稿还原”“后端正确”分别判断。
详见[社区权重规则](skills/promptharbor/references/community.md)和
[按已有模型筛选的前端示例](examples/frontend.json)。

更新机制包含过期检查与每周 GitHub 工作流，生成待复核报告，由维护者审核新证据。

## 使用边界

- **Top 3 随任务和资源变化。** 用户可限定已有模型；有依据的候选不足三个时，说明缺口。
- **“现在”需要新证据。** 联网时检查版本、可用性并补充新模型；离线时使用标明日期的快照。
- **推荐要经过具体任务验收。** 创意偏好、设计还原、代码正确性各有标准；跨模型盲测的推荐准确率尚未建立。
- **用户选择，主窗口集成。** 提示词由用户转交；接口契约和真实测试决定成果能否拼接。模型名称、API 单价不能替代账号权益、额度和总成本检查。

## 项目结构

```text
skills/promptharbor/    可独立安装的 Skill、证据、脚本与说明
examples/              单问题与完整工程交接示例
tests/                 筛选逻辑、工程依赖与交付验证
evals/                 宿主 Agent 行为评估用例
assets/                原创 Logo、头像、社交预览与 badges
scripts/               安装、打包、文档与时效性检查
docs/                  调研、设计、覆盖范围与发布说明
.github/               CI、维护报告与贡献模板
```

## 发布与贡献

```sh
python scripts/check_repo.py
python scripts/freshness.py
python scripts/package_skill.py
```

ZIP 安装包输出到 `dist/`。
参考 [贡献说明](CONTRIBUTING.md)、[品牌素材](assets/brand/README.md) 与
[发布步骤](docs/RELEASING.md)。

## 许可证

原创代码、文档、数据整理与美术采用 [Apache License 2.0](LICENSE)。第三方资料和
模型权重保持各自条款，详见 [来源声明](THIRD_PARTY.md)。本项目不代表任何模型
厂商或评测机构。
