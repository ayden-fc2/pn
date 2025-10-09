# 扩展 ER 图说明（覆盖细分要求）

本文基于 `../ProjectPN.description.zh.md` 的项目描述，解释 `er-diagram.puml` 中的建模决策，覆盖交付物第 2 条的全部细分要求。

## 实体类型与关键属性（每实体仅在图中展示一个关键键）
- User：`healthId`（唯一、关键键）；`name` 为复合属性（见下）。
- ContactEmail：`email`（关键键），`isVerified`。
- Phone：`phoneNumber`（关键键），`isVerified`。
- Provider：`licenseNumber`（关键键），`name`，`isVerified`。
- UserProvider（连接实体）：`userProviderId`（关键键），`isPrimaryCare`，`linkedAt`。
- FamilyGroup：`groupId`（关键键），`name`。
- FamilyMembership（连接实体）：`membershipId`（关键键），`role`，`joinedAt`。
- UserDelegation（用户-用户递归关系的连接实体）：`delegationId`（关键键），`createdAt`。
- Appointment：`appointmentId`（关键键），`dateTime`，`type`，`status`，`cancelReason?`。
- Challenge：`challengeId`（关键键），`goal`，`startDate`，`endDate`。
- ChallengeParticipation（连接实体）：`participationId`（关键键），`progressValue?`，`status`，`updatedAt`。
- Invitation：`invitationId`（关键键），`type`，`targetEmail?`，`targetPhone?`，`createdAt`，`completedAt?`，`expiresAt（派生）`，`status`。
- MonthlyReport：`reportId`（关键键），`month(YYYY-MM)`，`summary`，`stepsTotal（派生）`。
- HealthMetric：`metricId`（关键键），`metricDate`，`metricType`，`metricValue`。

## 关系类型（含角色）
- User — ContactEmail（has）。
- User — Phone（has）。
- User — UserProvider（links），Provider — UserProvider（linkedBy），并在 UserProvider 上标记 `isPrimaryCare`。
- User — FamilyMembership（member），FamilyGroup — FamilyMembership（includes）。
- User — UserDelegation：两条边分别标注角色 `guardian` 与 `dependent`，表示“用户管理/被管理”的递归关系。
- User — Appointment（books），Provider — Appointment（serves）。
- User — Challenge（creates）。
- Challenge — ChallengeParticipation（has），User — ChallengeParticipation（participates）。
- User — Invitation（sends），Invitation — Challenge（for，可选）。
- User — MonthlyReport（has），User — HealthMetric（records）。

## 属性类型分类
- 简单/复合：`User.name` 为复合属性，细分为 `firstName`、`lastName`（存储形式可并入一个字段或拆分，概念层标注为复合）。
- 单值/多值：`Phone` 对 `User` 单值（每用户至多一个），`ContactEmail` 对 `User` 多值。
- 存储/派生：`Invitation.expiresAt = createdAt + 15d`（派生）；`MonthlyReport.stepsTotal` 由 `HealthMetric` 聚合（派生）。

## 结构性约束（传统记法与 (min,max)）
- User — ContactEmail：1 对多（用户侧可为 0）
  - 传统：User（可选）—< ContactEmail（多，端可选）
  - (min,max)：User→Email (0,N)；Email→User (0,1)
- User — Phone：最多一部电话，双方均可选
  - 传统：User（0..1）— Phone（0..1）
  - (min,max)：User→Phone (0,1)；Phone→User (0,1)
- User — UserProvider：用户与提供者多对多
  - 传统：User 1 —< UserProvider >— 1 Provider
  - (min,max)：User→UserProvider (0,N)；Provider→UserProvider (0,N)
- User — FamilyMembership / FamilyGroup — FamilyMembership：多对多经连接实体实现
  - (min,max)：User→Membership (0,N)；Group→Membership (0,N)
- User — UserDelegation（递归）
  - (min,max)：guardianUser→Delegation (0,N)；dependentUser→Delegation (0,N)
- User — Appointment / Provider — Appointment：一对多
  - (min,max)：User→Appt (0,N)；Provider→Appt (0,N)
- User — Challenge（创建者）：一对多
  - (min,max)：User→Challenge (0,N)；Challenge→User (1,1)
- Challenge — ChallengeParticipation / User — ChallengeParticipation：多对多经连接实体
  - (min,max)：Challenge→Part (0,N)；User→Part (0,N)
- User — Invitation：一对多（发送）
  - (min,max)：User→Invitation (0,N)；Invitation→User (1,1)
- Invitation — Challenge：可选一对一
  - (min,max)：Invitation→Challenge (0,1)；Challenge→Invitation (0,N)
- User — MonthlyReport：一对多（按月）
  - (min,max)：User→Report (0,N)；Report→User (1,1)
- User — HealthMetric：一对多（原始指标）
  - (min,max)：User→Metric (0,N)；Metric→User (1,1)

## 特化/泛化层次（Provider）
- `Provider` 为超类，`Doctor`、`Specialist`、`Therapist` 为子类；公用关键键 `licenseNumber`。
- 继承语义：子类继承 Provider 的属性与语义（如 `isVerified`），在 ER 图中以父子泛化箭头表达。

## 关键键展示规范
- 图中每个实体仅展示一个关键键（以 `<<PK>>` 标注）。
- 其他候选键与唯一约束移至 `constraints.md` 说明并在实现时通过唯一索引/约束保证。

## 递归关系的角色
- 通过连接实体 `UserDelegation` 的两条外键边，分别命名为 `guardian` 与 `dependent`，满足“在递归关系上展示角色”的要求。

## 取消与过期规则（语义约束）
- 预约：仅允许在预约时间前 24 小时取消（在实现层用触发器或应用逻辑保证）。
- 邀请：有效期 15 天；`expiresAt` 为派生属性，数据库中可用生成列或视图表达。
