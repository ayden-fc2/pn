HealthTrack 技术路线图（简明）

一、总体目标
- 构建 HealthTrack 个人健康与保健平台的数据库与基础应用，实现数据采集、预约管理、挑战管理与检索。

二、阶段划分
- 阶段 1：需求分析与概念设计
  - 明确实体、关系、关键属性与约束；完成扩展 ER 图（含特化/泛化与 (min,max) 约束）。
- 阶段 2：逻辑设计与模式优化
  - E/R 到关系模式映射、范式化、索引与约束设计（PK/FK/候选键/唯一性/检查约束）。
- 阶段 3：物理实现与数据访问层
  - 在选定 DBMS（如 PostgreSQL/MySQL）上建库建表，编写迁移脚本；实现数据访问层（ORM 或 SQL）。
- 阶段 4：应用层与基础功能
  - 实现注册与验证状态记录、提供者关联/解绑、预约创建/取消、挑战创建/邀请/进度跟踪、月度汇总与搜索。
- 阶段 5：测试与部署
  - 单元/集成测试、数据种子、性能与安全检查；容器化与部署（可选）。

三、核心数据模型要点（摘要）
- 实体：User、ContactEmail、Phone、Provider、FamilyGroup、Appointment、Challenge、ChallengeParticipation、Invitation、MonthlyReport、HealthMetric（可扩展）。
- 关键约束：
  - User(HealthID) 唯一；每 User 至多一 Phone；User 可有多 Email（Email 需能记录 verified 状态）。
  - Provider(licenseNo) 唯一；User-Provider 多对多并带 verified 与 primaryCare 标记（每用户最多一位 primaryCare=TRUE）。
  - FamilyGroup 支持多用户与角色/权限。
  - Appointment 拥有唯一 Id，支持状态与取消原因，限制“开诊前 24 小时可取消”。
  - Challenge 拥有唯一 Id；Participation 记录用户、进度与状态；Invitation 记录发起与完成/过期时间与 15 天有效期规则。
  - MonthlyReport 关联 User+月份，支持派生与汇总字段。

四、关键功能流（应用层）
- 注册：创建 User，新增 Email/Phone 并标记 verified 状态（流程本身不在模式层实现）。
- 提供者管理：关联/解绑 Provider，设置/变更 primaryCare（保证每用户最多一位）。
- 预约：创建、查询、24 小时前取消并记录原因；支持按日期/提供者搜索。
- 挑战：创建、邀请（邮件/短信），接受/过期逻辑（15 天），参与进度上报与统计。
- 汇总与检索：按月生成/查询汇总；健康指标检索与统计。

五、技术选型（示例）
- DBMS：PostgreSQL（推荐）或 MySQL；迁移：Liquibase/Flyway 或 ORM 自带迁移。
- 应用：
  - 后端：Node.js + NestJS/Express 或 Python + FastAPI；ORM：Prisma/TypeORM 或 SQLAlchemy。
  - 前端：React/Next.js 或 Vue/Nuxt；UI：Ant Design/Material UI。
- 基础设施：Docker Compose 本地开发，生产可用容器化与 CI。

六、质量与合规
- 数据一致性：事务边界、外键与检查约束、唯一索引、延迟约束（如 15 天过期定时任务）。
- 性能：常用查询建立索引（按用户、日期、提供者、挑战 Id）、分页查询。
- 安全：最小权限、加密存储敏感信息、审计日志（关键操作）。
- 测试：迁移可回滚、数据工厂、端到端测试关键业务流程。

七、里程碑与交付
- M1：ER 概念模型与假设清单；
- M2：关系模式与 DDL 初版（含约束与索引）；
- M3：基础 API 与最小可用 GUI；
- M4：完整功能、测试与部署说明；
- M5：项目报告与演示。
