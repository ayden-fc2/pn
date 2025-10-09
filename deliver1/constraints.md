# ER 图外的附加数据约束与附加键

## 附加键（候选键）与唯一性
- User：`healthId`（主键）；候选键：无（假设健康 ID 即唯一身份标识）。
- ContactEmail：`email`（主键）；允许唯一。
- Phone：`phoneNumber`（主键）；允许唯一。
- Provider：`licenseNumber`（主键）；候选键：`(name, licenseNumber)` 仅信息性，不构成唯一性；如需，可约束 `licenseNumber` 唯一。
- UserProvider：唯一性 `(userId, providerId)`；且 `isPrimaryCare=TRUE` 在同一 `userId` 上至多一条（部分唯一约束）。
- FamilyGroup：`groupId`（主键）；`name` 可重复。
- FamilyMembership：唯一性 `(groupId, userId)`，避免重复入组；`membershipId` 为技术键。
- UserDelegation：唯一性 `(guardianUserId, dependentUserId)`，避免重复授权。
- Appointment：`appointmentId`（主键）；可选唯一 `(userId, providerId, dateTime)` 以防重复预约。
- Challenge：`challengeId`（主键）。
- ChallengeParticipation：唯一性 `(challengeId, userId)`。
- Invitation：业务去重可选 `(targetEmail/targetPhone, createdAt±ε)`；不强制唯一。
- MonthlyReport：唯一性 `(userId, month)`。
- HealthMetric：可选唯一 `(userId, metricType, metricDate, <time-bucket>)`。

## 参照完整性与参与约束
- 所有连接实体的外键均为必须存在（内侧 (1,1)）。
- `Phone` 与 `ContactEmail` 允许悬置（用于未注册邀请），若与 `User` 关联则外键有效。
- `Invitation` → `Challenge` 为可选外键（邀请可仅用于共享数据）。

## 业务规则（语义约束）
- 预约取消时间：仅允许在 `Appointment.dateTime - 24h` 之前取消。
- Primary care 唯一性：每 `User` 同时仅允许一位 `isPrimaryCare=TRUE`。
- 邀请有效期：`expiresAt = createdAt + 15 days`；过期后状态自动转为 `Expired`。
- 参与唯一：`ChallengeParticipation` 针对 `(challengeId, userId)` 唯一。
- 月报唯一：每用户每月最多一份 `MonthlyReport`（`(userId, month)` 唯一）。

## 索引建议（实现层）
- 高频检索：`Appointment(userId, dateTime)`、`Appointment(providerId, dateTime)`、`ChallengeParticipation(challengeId)`、`Invitation(status, createdAt)`、`HealthMetric(userId, metricType, metricDate)`。
- 唯一索引：参见上节的唯一性约束。
