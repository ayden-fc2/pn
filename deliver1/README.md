# Deliverable 1 工作目录

本目录围绕 `ProjectPN.description.zh.md` 的项目描述，完成 `Project Deliverable 1.zh.md` 的全部期望内容（1-5），并严格满足第 2 项的细分要求。

## 目录结构
- README.md（本说明）
- er-diagram.puml（PlantUML 扩展 ER 图）
- er-notes.md（ER 图要素说明：实体/关系/属性/角色/约束）
- assumptions.md（超出描述的建模假设）
- constraints.md（ER 图外的数据约束与附加键）
- difficulties.md（本阶段遇到的困难与取舍）

## 本阶段目标（对应交付物 1）
1. 概述目标：完成概念层的数据库设计并清晰记录假设、约束与难点。
2. 扩展 ER 图：满足 E/R 符号、特化/泛化层次、实体/关系/属性、角色、关键键、结构性约束（传统与 (min,max)）等细分要求。
3. 记录与规范：明确所有超出题面描述的假设；列出 ER 图表达之外的约束与附加键；整理困难与设计权衡。

## 如何渲染 ER 图
- 推荐使用 VS Code + PlantUML 插件，或命令行 PlantUML：
  - 命令行示例：`plantuml -tsvg er-diagram.puml`
  - 生成文件：`er-diagram.svg` 或 `er-diagram.png`

## 参考
- 题面：`../ProjectPN.description.zh.md`
- 交付要求：`../Project Deliverable 1.zh.md`
