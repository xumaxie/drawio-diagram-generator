# AI 绘图文件生成器

一个面向交付结果的 draw.io skill。  
它不是只生成一段 XML，而是把自然语言需求转成可直接用 draw.io 打开的 `.drawio` 文件。

这套 skill 的主要工作流是：先分析需求、再生成图、最后复核和校验。

GitHub 仓库：
[xumaxie/drawio-diagram-generator](https://github.com/xumaxie/drawio-diagram-generator)

## 这个 skill 干什么

它主要解决一类很常见但很容易做糙的事情：

- 用户只给一段文本或者只有代码仓库，却想要一份 draw.io 图文件
- 用户已经有现成 XML，想继续修改
- 用户想根据代码结构、接口关系、系统流程、业务描述生成图

skill 的默认目标不是聊天回复，而是产出一个本地 `.drawio` 文件。

## 使用教程

下面给出几种常用安装方式。  
如果你只是本地自用，推荐直接复制目录。  
如果你准备开源发布，推荐用 GitHub 安装命令。

### 1. Codex 本地安装

将 skill 目录复制到 Codex 的 skills 目录：

```bash
mkdir -p ~/.codex/skills
cp -R ./drawio-diagram-generator ~/.codex/skills/
```

如果你的仓库里 skill 不在根目录，而是在当前这种结构下，可以用：

```bash
mkdir -p ~/.codex/skills
cp -R ./.codex/skills/drawio-diagram-generator ~/.codex/skills/
```

安装完成后，重启 Codex。

### 2. Codex 通过 GitHub 安装

如果你已经把它发布到 GitHub，可以在 Codex 里直接使用 `$skill-installer`：

```text
$skill-installer install https://github.com/xumaxie/drawio-diagram-generator/tree/main/.codex/skills/drawio-diagram-generator
```

如果你后面把这个 skill 单独放成仓库根目录，也可以直接安装对应目录 URL。

安装完成后，重启 Codex。

### 3. Claude Code / 兼容 Skills 协议的 Agent 安装

对于 Claude Code、Cursor、OpenClaw 或其他支持 skills 协议的 Agent，推荐使用 `npx skills add`：

```bash
npx skills add https://github.com/xumaxie/drawio-diagram-generator --skill drawio-diagram-generator
```

如果你把这个 skill 单独作为一个技能仓库发布，也可以使用更短的形式：

```bash
npx skills add xumaxie/drawio-diagram-generator@drawio-diagram-generator -g -y
```

说明：

- `--skill drawio-diagram-generator` 适合从一个多技能仓库中安装指定 skill
- `-g` 表示全局安装
- `-y` 表示跳过确认

### 4. 安装后怎么用

安装成功后，可以直接用自然语言触发，例如：

- “帮我生成一个 H5 登录流程图，输出成 `.drawio` 文件。”
- “根据这段系统说明画一张架构图，并保存成 draw.io 文件。”
- “基于我现有的 draw.io XML 增加一个风控节点，不要整图重画。”

## 核心特点

### 1. 先判断，再出图

如果需求不完整，它不会盲猜，而是先追问关键信息。  
这能显著减少“图画出来了，但业务意思不对”的情况。

### 2. 默认产出 `.drawio` 文件

它的默认交付物是文件，不是裸 XML 文本。  
也就是说，它更接近真实工作流，而不是一次性的 prompt 试玩。

### 3. 保留了后端里最值钱的三段式流程

这套 skill 参考了后端智能体中的三个阶段：

1. 分析需求
2. 生成 draw.io XML
3. 复核结构、布局、输出格式

这个流程比“单条 prompt 直接出图”稳定得多。

### 4. 支持继续修改现有 draw.io XML

如果用户已经有当前画布 XML，这个 skill 会优先基于现有图续改，而不是粗暴整图重画。

### 5. 带校验能力

skill 附带了一个轻量校验脚本，用来检查生成的 `.drawio` 文件是否具备基本可用性。

## 适用场景

这个 skill 适合以下任务：

- 流程图生成
- UML 图生成
- 系统架构图生成
- 时序图生成
- ER 图生成
- 泳道图生成
- 基于现有 draw.io XML 的增量修改
- 基于仓库、代码结构、接口说明、业务文档生成图

## 和普通 prompt 的区别

普通 prompt 的典型问题是：

- 信息不完整时也硬画
- 只会返回 XML，不会考虑落盘成文件
- 混用 JSON、XML、Markdown 代码块
- 前端或调用方不好接
- 图结构能看，结果却不一定能直接用

这套 skill 的重点是把“生成图”变成“交付图文件”：

- 有需求判断
- 有输出协议
- 有布局约束
- 有续改策略
- 有文件校验

## 工作流程

默认流程如下：

1. 判断用户需求是否足够清晰
2. 如果不清晰，先追问缺失信息
3. 如果信息足够，生成 draw.io XML
4. 将 XML 写入 `.drawio` 文件
5. 检查 XML 结构和基本布局
6. 用脚本校验文件可用性

## 目录结构

```text
drawio-diagram-generator/
├── README.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── prompt-snippets.md
│   ├── protocol.md
│   └── xml-template.md
└── scripts/
    └── validate_drawio_xml.py
```

## 目录说明

- `SKILL.md`
  skill 主说明，定义能力、工作流、输出模式和使用规则。

- `references/protocol.md`
  保留后端里的 `user` / `drawio` 双通道协议思想，适合对接前端或中间层。

- `references/xml-template.md`
  提供 draw.io XML 骨架、最小可用示例和布局规则。

- `references/prompt-snippets.md`
  提供分析、绘图、复核三个阶段的提示模板。

- `scripts/validate_drawio_xml.py`
  用来校验生成文件是否具备基本 draw.io 可用结构。

## 快速使用

典型使用方式：

1. 触发 skill
2. 输入绘图需求
3. 如信息不足，补充必要信息
4. 让 skill 生成并写出 `.drawio` 文件
5. 用 draw.io 打开结果文件

例如你可以这样提需求：

- “帮我生成一个 H5 登录流程图，输出成 `.drawio` 文件。”
- “根据这个系统模块说明，画一张架构图并保存成 draw.io 文件。”
- “基于我现有的 draw.io XML，增加一个风控节点，不要重画整张图。”

## 输出模式

虽然默认成果是 `.drawio` 文件，但 skill 仍然保留了几种模式，方便不同接入方式复用：

- 文件模式  
  默认模式，生成并保存 `.drawio` 文件。

- 原始 XML 模式  
  当用户明确要求只要 XML 时使用。

- 协议模式  
  当调用方需要结构化返回时，使用 `user` / `drawio` 协议包装结果。

## 设计原则

这个 skill 的核心设计原则只有几条：

- 默认交付文件，不默认交付聊天文本
- 信息不足先追问，不盲猜
- 输出格式要严格，避免 JSON/XML/Markdown 混乱
- 能续改现有图，就不要粗暴重画
- 能校验，就不要只靠“感觉能用”

## License

本项目采用 MIT License，详见 [LICENSE](./LICENSE)。
