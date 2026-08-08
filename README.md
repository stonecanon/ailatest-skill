# AIlatest skill

一个面向科研、写作、绘图、数据处理和其他实用工作流的公开 Skill 合集。每个 Skill 都保持独立目录，既可以单独安装，也可以在这个仓库中持续维护和学习 GitHub 协作。

## 当前收录

| Skill | 方向 | 用途 |
| --- | --- | --- |
| [`draw-process-flowchart`](skills/draw-process-flowchart/) | 科研绘图 | 绘制可变阶段的论文级流程图，并导出 PNG、SVG、PDF |
| [`design-natural-science-fund-figures`](skills/design-natural-science-fund-figures/) | 科研绘图 | 生成基金技术路线图、研究逻辑图并核查图文一致性 |
| [`write-natural-science-fund-proposals`](skills/write-natural-science-fund-proposals/) | 科研写作 | 围绕科学问题组织基金正文、证据链与终稿核查 |

后续 Skill 会继续按用途加入 `skills/`，例如科研写作、文献整理、数据分析、图表制作和其他实验性工具。

配套示意图：[`科研证据链流程图`](examples/draw-process-flowchart/)、[`基金绘图工作链`](examples/design-natural-science-fund-figures/)、[`基金写作核心逻辑`](examples/write-natural-science-fund-proposals/)。

## 快速使用

在 Codex 中，将需要使用的 Skill 目录复制到本地 Skill 目录：

```bash
cp -R skills/draw-process-flowchart "$HOME/.codex/skills/draw-process-flowchart"
```

然后调用：

```text
$draw-process-flowchart
```

也可以直接克隆整个合集：

```bash
git clone https://github.com/stonecanon/ailatest-skill.git
```

## 仓库结构

```text
skills/                         # 可直接调用的 Skill
examples/                       # 重构后的示意图和最小示例
LICENSE                         # MIT License
```

每个 Skill 目录建议包含：

```text
SKILL.md                        # 主说明与工作流程
agents/openai.yaml              # Codex 显示名称与默认提示词
references/                     # 风格、方法或领域参考
scripts/                        # 可复现的脚本
```

## 公开仓库安全规则

- 不提交 API key、访问 token、密码、私钥、Cookie 或个人配置文件；
- 不提交本机绝对路径、个人邮箱、临时目录和带身份信息的日志；
- 示例图使用重新设计的内容和数据，不上传个人论文截图或原始资料；
- 上传前检查文本、脚本、SVG、PDF 元数据和 Git 历史中的隐私信息。

## 维护方式

新增 Skill 时，在 `skills/<skill-name>/` 建立独立目录，并补充一个不含个人信息的 README 或示例。提交前运行对应 Skill 的校验脚本，再使用清晰的 commit message 推送到 `main`。
