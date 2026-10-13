# 中华医学会参考文献样式：中文文献附英文对照

一个供 Zotero 使用的开放 CSL 样式，针对《中华神经科杂志》等中华医学会期刊的**顺序编码制**参考文献格式。核心功能：中文文献自动输出中文条目 + 英文对照，**只编号一次**；原本为英文的文献仍只输出英文条目。

> 版本：0.1.0（测试版）。基于 Zotero 中文社区“中华医学会”样式（韩小土、Zeping Lee）的著录规则，补充英文对照部分。采用 CSL-M 扩展及 `original-*` 字段；请使用 Zotero 7 及其内置的 citeproc-js 引擎。未在作者本人的 Zotero/Word 图形界面实测，个别版本可能有兼容性差异。样式不会翻译文献，英文元数据需要录入。

## 一、安装

1. 下载 `chinese-medical-bilingual.csl`。
2. Zotero → 编辑 → 设置 → 引用 → 样式 → `+` → 选取 `.csl` 文件。
3. 在 Word 的 Zotero 工具栏点 **Document Preferences**，选择“中华医学会（中文文献附英文对照）”，再点 **Refresh**。
4. 若出现“不是有效的 CSL 1.0.2 样式”一类提示，原因可能是 CSL-M 双语言扩展；Zotero 中文社区已有类似样式，也有此提示。请核查 Zotero 版本和实际输出；不要在无法识别样式时强行继续。
5. 首次切换样式时最好备份 Word 文档。将 Zotero 条目的“语言”填为 `zh-CN`（中文）或 `en-US`（英文）。

## 二、中文文献怎么填

在 Zotero 的期刊文章条目中，按普通方法填写中文**标题、作者、期刊名称、日期、卷、期、页码、DOI**；“语言”填写 `zh-CN`。

然后在 **“额外”（Extra）** 字段添加英文元数据，完整示例见 `samples/zotero-extra.txt`：

```text
Original Author: Lin,|| Zhi Qiang
Original Author: Li,|| Xiao Bo
Original Author: Huang,|| Shun Xiang
Original Author: Zhao,|| Hua Dong
Original Author: Liu,|| Lei
Original Author: Cao,|| Wan Qian
Original Author: Liu,|| Xin
Original Author: Tang,|| Bei Sha
Original Author: Zhang,|| Ru Xu
Original Title: Genetic and clinical features of sorbitol dehydrogenase gene-related Charcot-Marie-Tooth disease in Chinese population
Original Container Title Short: Chin J Neurol
Original Container Title: Chinese Journal of Neurology
```

- 每位英文作者单占一行，格式为 `Original Author: 姓,|| 名`；逗号非常重要。为了生成 `Lin ZQ`，名的拼音音节写作 `Zhi Qiang`，而不是 `Zhiqiang`。
- 作者应尽量录入全部实际作者，样式会自动截取前 3 位，超过 3 位中文加“等”、英文加 `et al.`。
- `Original Title` 是正式英文题名；`Original Container Title Short` 是标准英文期刊缩写；`Original Container Title` 是英文全称，当英文缩写为空时可回退使用。
- DOI、年份、卷、期、页码无需在 Extra 重复输入。
- 为避免生成内容不全的英文条目，只有 `Original Author` 和 `Original Title` **同时存在**时才生成英文对照。英文期刊缩写也建议完整填写。
- 如果某中文文献没有以上英文元数据，仅显示中文条目。样式**不会自动翻译**。

## 三、预期输出示例

```text
[7] 林志强, 李小波, 黄顺祥, 等. 中国人山梨醇脱氢酶基因相关腓骨肌萎缩症的基因型-表型分析[J]. 中华神经科杂志, 2020, 53(11): 882-887. DOI: 10.3760/cma.j.cn113694-20200511-00343.
    Lin ZQ, Li XB, Huang SX, et al. Genetic and clinical features of sorbitol dehydrogenase gene-related Charcot-Marie-Tooth disease in Chinese population[J]. Chin J Neurol, 2020, 53(11): 882-887. DOI: 10.3760/cma.j.cn113694-20200511-00343.
```

编号 `[7]` 仅用于演示，实际编号由 Zotero 按正文首次引用顺序确定。Word 内的悬挂缩进及行距还需要按期刊排版要求检查。

## 四、测试方法与已知限制

- `tests/references.json` 覆盖中文双语、英文单语、无译文，以及英文题名或作者单边缺失的情况。
- `tests/smoke_test.py` 检查 XML 格式、引用字段、双布局结构；如果安装 Pandoc，还通过**只用于测试的单布局副本**运行实际渲染冒烟测试。可运行 `python tests/smoke_test.py`。
- Pandoc **不支持 CSL-M 多布局**：直接拿正式样式运行 Pandoc 可能报 `Multiple layout elements present in bibliography`，不代表 Zotero 不能安装。
- `Original Author` 的 Extra 语法与中英双语布局依赖 Zotero 的 CSL-M 支持。当前测试验证了模拟器单布局时中文+英文对照的格式，正式双布局尚未进行真实 Zotero/Word 端到端测试。
- 样式优先支持**期刊论文**；图书、会议、网页等类型提供基本输出，但尚未逐类型核对《中华神经科杂志》编辑部全部细则。
- 避免混用 Zotero 不同语言写法：`Chinese`、`English`、`中文` 等通常不足以驱动 CSL-M 的语言布局选择。

## 五、来源与许可证

衍生自：<https://github.com/zotero-chinese/styles/blob/main/src/中华医学会/中华医学会.csl>（原作者：韩小土；贡献者：Zeping Lee），并借鉴 Zotero 中文社区使用 `original-*` 字段为中文文献追加英文对照行的公共样式实现。

本样式及本仓库的文档以 **Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)** 许可发布。保留原作者和链接，修改、传播时应遵守署名、相同方式共享要求。许可证信息见 `LICENSE.md`。

如用于正式投稿，请以期刊最新投稿规范及论文实际 Word 输出为最终检查依据。
