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
1. 概念建模：在严格语义下刻画实体/关系/约束，明确边界条件与信息需求，形成可验证的概念模型与假设集。
2. 结构表达：用扩展 ER 图严谨呈现特化/泛化、递归角色、键/属性类型及结构性约束，双记法（传统与(min,max)）一致且可推导参与度。
3. 语义约束与一致性：抽象业务规则为数据层可检查/可推理的约束（如主治唯一、24小时取消、15天过期），区分存储/派生并给出一致性策略。
4. 可映射性与分析准备：确保模型可无歧义映射到关系模式，支撑范式化与索引设计、事务边界与参照策略，为后续逻辑/物理设计与评估奠基。
## 如何渲染 ER 图
- 推荐使用 VS Code + PlantUML 插件，或命令行 PlantUML：
  - 命令行示例：`plantuml -tsvg er-diagram.puml`
  - 生成文件：`er-diagram.svg` 或 `er-diagram.png`

## 参考
- 题面：`../ProjectPN.description.zh.md`
- 交付要求：`../Project Deliverable 1.zh.md`
