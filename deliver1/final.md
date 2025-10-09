# Project Deliverable 1

> 第18小组 刘志锋  黄柏曛  时啟轩

### 一. 阶段目标

**1. 概念建模**：在严格语义下刻画实体/关系/约束，明确边界条件与信息需求，形成可验证的概念模型与假设集。

**2. 结构表达**：用扩展 ER 图严谨呈现特化/泛化、递归角色、键/属性类型及结构性约束，双记法（传统与(min,max)）一致且可推导参与度。

**3. 语义约束与一致性**：抽象业务规则为数据层可检查/可推理的约束（如主治唯一、24小时取消、15天过期），区分存储/派生并给出一致性策略。

**4. 可映射性与分析准备**：确保模型可无歧义映射到关系模式，支撑范式化与索引设计、事务边界与参照策略，为后续逻辑/物理设计与评估奠基。

### 二. ER图设计

![e5708af76fb646c397434c35b68cf8dd.svg](http://www.fivecheers.com/resource/blog/svg/e5708af7-6fb6-46c3-9743-4c35b68cf8dd.svg)

### 三、建模假设

1. 用户姓名为复合属性：拆分为 `firstName`、`lastName`，图中以 `name` 表示复合属性。
2. `Phone` 对用户为 0..1（每个账户最多一部电话），但电话记录可独立存在（用于邀请未注册用户）。
3. `ContactEmail` 可多对一关联到用户；邮箱记录也可独立存在（支持面向未注册用户的邀请）。
4. Provider 细分类型采用特化/泛化：`Doctor`、`Specialist`、`Therapist`；共用 `licenseNumber` 作为全局唯一键。
5. 用户-提供者关联 `UserProvider` 存储 `isPrimaryCare`；每用户在同一时间最多一条 `isPrimaryCare=TRUE` 的记录。
6. 家庭组通过 `FamilyGroup` 与 `FamilyMembership` 表达，成员角色如 `guardian`、`member` 等在 `role` 中体现。
7. 用户对用户的“代管”/“被代管”关系通过 `UserDelegation` 表达，允许多对多并显式角色标注。
8. 预约 `Appointment` 的 `status` 至少包含 `Scheduled` 与 `Cancelled`；取消原因以自由文本 `cancelReason` 记录并可枚举。
9. 邀请 `Invitation` 的 `expiresAt` 为派生属性：`createdAt + 15d`；过期与完成互斥。
10. 月度汇总 `MonthlyReport.stepsTotal` 由 `HealthMetric(metricType=Steps)` 对当月数据聚合得到；可作为物化或视图实现。
11. 进度 `ChallengeParticipation.progressValue` 的度量单位由挑战语义决定（如步数/里程/分钟），在实现层规范化。
12. 所有 UUID 类型键在概念层仅表示“系统生成的唯一标识符”。

### 四、ER图外的数据约束与附加键

1. 附加候选键（按实体）

   * User：无（`healthId` 为唯一身份标识）。
   * ContactEmail：无（`email` 已为主键）。
   * Phone：无（`phoneNumber` 已为主键）。
   * Provider：无（`licenseNumber` 为唯一标识）。
   * Doctor / Specialist / Therapist：无（继承 `Provider.licenseNumber`）。
   * UserProvider：`(userId, providerId)`。
   * FamilyGroup：无（`name` 允许重复）。
   * FamilyMembership：`(groupId, userId)`。
   * UserDelegation：`(guardianUserId, dependentUserId)`。
   * Appointment：`(userId, providerId, dateTime)`。
   * Challenge：无（避免对相同目标/日期的不同挑战过度约束）。
   * ChallengeParticipation：`(challengeId, userId)`。
   * Invitation：无（时间与目标组合不作为强唯一键）。
   * MonthlyReport：`(userId, month)`。
   * HealthMetric：无（若限定“同一用户/类型/日期唯一”才可作为候选键）。
2. 其他数据约束（ER 图难以充分表达）

   * Primary Care 唯一：同一用户同时最多一条 `isPrimaryCare=TRUE`（条件唯一）。
   * 预约取消窗口：仅允许在预约时间前 ≥24 小时取消；取消需记录原因。
   * 邀请有效期：`expiresAt = createdAt + 15 days`；逾期转为 `Expired`，完成后不可再接受。
   * 验证要求：未验证的 `email/phone` 不得用于关键功能；仅验证通过的 `Provider` 可被正式关联或设为主治。

### 五、困难与取舍

| 困难                        | 解决方案                                                                                                              |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| 递归关系的角色表达          | 采用连接实体 `UserDelegation`，以两条外键分别标注 `guardian`/`dependent` 角色，便于扩展权限元数据与多角色管理。 |
| Primary Care 唯一           | 使用条件唯一约束（同一用户 `isPrimaryCare=TRUE` 至多一条），并在应用层进行二次校验与冲突处理。                      |
| 邀请的 15 天有效期          | 概念层以派生属性表示；实现层通过定时任务/生成列/触发器统一维护过期转态（`Expired`）与不可再接受规则。               |
| 月度汇总派生                | `stepsTotal` 由 `HealthMetric` 聚合得到；在物化视图与实时聚合之间权衡性能与数据新鲜度。                           |
| 属性建模粒度                | 保持 `User.name` 为复合属性以支持国际化与检索；实现层可存储拆分字段（如 `firstName`/`lastName`）。              |
| 取消原因与状态枚举          | 采用“枚举 + 可选文本”折中设计，既保证统计一致性又保留描述灵活性。                                                   |
| 邀请目标（邮箱/电话）可悬置 | 允许 `email/phone` 脱钩以支持未注册邀请；制定数据治理（归档/清理）策略以控制参照完整性与存量数据。                  |
