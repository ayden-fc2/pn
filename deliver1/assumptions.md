# 超出题面描述的建模假设

本文档列出为完成概念设计而作出的合理补充假设，均不与题面冲突。

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
