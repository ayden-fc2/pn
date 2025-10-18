-- HealthTrack Personal Wellness Platform - Logical Schema (Phase 2)
-- SQL dialect: ANSI-ish (validated best on PostgreSQL 14+). Replace CHECK/partial indexes as needed for your RDBMS.

-- =========================
-- 1) Core entities
-- =========================
CREATE TABLE "User" (
  health_id        VARCHAR(64) PRIMARY KEY,
  first_name       VARCHAR(100) NOT NULL,
  last_name        VARCHAR(100) NOT NULL
);

CREATE TABLE ContactEmail (
  email            VARCHAR(320) PRIMARY KEY,
  is_verified      BOOLEAN NOT NULL DEFAULT FALSE,
  user_health_id   VARCHAR(64) NULL REFERENCES "User"(health_id) ON DELETE SET NULL
);

CREATE TABLE Phone (
  phone_number     VARCHAR(32) PRIMARY KEY,
  is_verified      BOOLEAN NOT NULL DEFAULT FALSE,
  user_health_id   VARCHAR(64) NULL REFERENCES "User"(health_id) ON DELETE SET NULL,
  CONSTRAINT uq_phone_per_user UNIQUE (user_health_id)
);

CREATE TABLE Provider (
  license_number   VARCHAR(64) PRIMARY KEY,
  name             VARCHAR(200) NOT NULL,
  is_verified      BOOLEAN NOT NULL DEFAULT FALSE
);

-- Class Table Inheritance for Provider subtypes
CREATE TABLE Doctor (
  license_number   VARCHAR(64) PRIMARY KEY,
  CONSTRAINT fk_doctor_provider FOREIGN KEY (license_number) REFERENCES Provider(license_number) ON DELETE CASCADE
);

CREATE TABLE Specialist (
  license_number   VARCHAR(64) PRIMARY KEY,
  CONSTRAINT fk_specialist_provider FOREIGN KEY (license_number) REFERENCES Provider(license_number) ON DELETE CASCADE
);

CREATE TABLE Therapist (
  license_number   VARCHAR(64) PRIMARY KEY,
  CONSTRAINT fk_therapist_provider FOREIGN KEY (license_number) REFERENCES Provider(license_number) ON DELETE CASCADE
);

-- =========================
-- 2) User and Provider linking
-- =========================
CREATE TABLE UserProvider (
  user_provider_id UUID PRIMARY KEY,
  user_health_id   VARCHAR(64) NOT NULL REFERENCES "User"(health_id) ON DELETE CASCADE,
  provider_license_number VARCHAR(64) NOT NULL REFERENCES Provider(license_number) ON DELETE RESTRICT,
  is_primary_care  BOOLEAN NOT NULL DEFAULT FALSE,
  linked_at        TIMESTAMP NOT NULL,
  CONSTRAINT uq_user_provider UNIQUE (user_health_id, provider_license_number)
);

-- Conditional uniqueness (per-user at most one primary care)
-- PostgreSQL example (comment out if not supported by your DB):
-- CREATE UNIQUE INDEX uq_primary_care_once ON UserProvider(user_health_id) WHERE is_primary_care;

-- Portable alternative: a partial enforcement via CHECK + trigger can be used.

-- =========================
-- 3) Family grouping
-- =========================
CREATE TABLE FamilyGroup (
  group_id   UUID PRIMARY KEY,
  name       VARCHAR(200) NOT NULL
);

CREATE TABLE FamilyMembership (
  membership_id  UUID PRIMARY KEY,
  group_id       UUID NOT NULL REFERENCES FamilyGroup(group_id) ON DELETE CASCADE,
  user_health_id VARCHAR(64) NOT NULL REFERENCES "User"(health_id) ON DELETE CASCADE,
  role           VARCHAR(50) NOT NULL,
  joined_at      TIMESTAMP NOT NULL,
  CONSTRAINT uq_group_user UNIQUE (group_id, user_health_id),
  CONSTRAINT chk_role_not_empty CHECK (role <> '')
);

-- =========================
-- 4) User recursive delegation
-- =========================
CREATE TABLE UserDelegation (
  delegation_id          UUID PRIMARY KEY,
  guardian_user_health_id  VARCHAR(64) NOT NULL REFERENCES "User"(health_id) ON DELETE RESTRICT,
  dependent_user_health_id VARCHAR(64) NOT NULL REFERENCES "User"(health_id) ON DELETE RESTRICT,
  created_at            TIMESTAMP NOT NULL,
  CONSTRAINT uq_guardian_dependent UNIQUE (guardian_user_health_id, dependent_user_health_id),
  CONSTRAINT chk_guardian_ne_dependent CHECK (guardian_user_health_id <> dependent_user_health_id)
);

-- =========================
-- 5) Appointments
-- =========================
CREATE TABLE Appointment (
  appointment_id   UUID PRIMARY KEY,
  user_health_id   VARCHAR(64) NOT NULL REFERENCES "User"(health_id) ON DELETE CASCADE,
  provider_license_number VARCHAR(64) NOT NULL REFERENCES Provider(license_number) ON DELETE RESTRICT,
  date_time        TIMESTAMP NOT NULL,
  type             VARCHAR(20) NOT NULL,
  memo             TEXT NULL,
  status           VARCHAR(20) NOT NULL,
  cancel_reason    VARCHAR(500) NULL,
  CONSTRAINT uq_user_provider_datetime UNIQUE (user_health_id, provider_license_number, date_time),
  CONSTRAINT chk_type CHECK (type IN ('InPerson','Virtual')),
  CONSTRAINT chk_status CHECK (status IN ('Scheduled','Cancelled'))
);
-- Business rule (24h cancellation window) to be enforced in application layer and/or trigger

-- =========================
-- 6) Challenges and participation
-- =========================
CREATE TABLE Challenge (
  challenge_id   UUID PRIMARY KEY,
  creator_user_health_id VARCHAR(64) NOT NULL REFERENCES "User"(health_id) ON DELETE CASCADE,
  goal           VARCHAR(500) NOT NULL,
  start_date     DATE NOT NULL,
  end_date       DATE NOT NULL,
  CONSTRAINT chk_dates CHECK (end_date >= start_date)
);

CREATE TABLE ChallengeParticipation (
  participation_id UUID PRIMARY KEY,
  challenge_id     UUID NOT NULL REFERENCES Challenge(challenge_id) ON DELETE CASCADE,
  user_health_id   VARCHAR(64) NOT NULL REFERENCES "User"(health_id) ON DELETE CASCADE,
  progress_value   DECIMAL(18,4) NULL,
  status           VARCHAR(20) NOT NULL,
  updated_at       TIMESTAMP NOT NULL,
  CONSTRAINT uq_challenge_user UNIQUE (challenge_id, user_health_id),
  CONSTRAINT chk_participation_status CHECK (status IN ('Invited','Joined','Completed','Declined'))
);

-- =========================
-- 7) Invitations
-- =========================
CREATE TABLE Invitation (
  invitation_id   UUID PRIMARY KEY,
  sender_user_health_id VARCHAR(64) NOT NULL REFERENCES "User"(health_id) ON DELETE CASCADE,
  challenge_id     UUID NULL REFERENCES Challenge(challenge_id) ON DELETE SET NULL,
  type             VARCHAR(20) NOT NULL,
  target_email     VARCHAR(320) NULL,
  target_phone     VARCHAR(32) NULL,
  created_at       TIMESTAMP NOT NULL,
  completed_at     TIMESTAMP NULL,
  expires_at       TIMESTAMP NULL,
  status           VARCHAR(20) NOT NULL,
  CONSTRAINT chk_inv_type CHECK (type IN ('Challenge','ShareData')),
  CONSTRAINT chk_inv_status CHECK (status IN ('Pending','Accepted','Expired','Cancelled')),
  CONSTRAINT chk_inv_target_at_least_one CHECK (
    (target_email IS NOT NULL AND length(trim(target_email))>0) OR
    (target_phone IS NOT NULL AND length(trim(target_phone))>0)
  )
);
-- Derived: expires_at = created_at + interval '15 days' (use generated column/trigger or compute in view)

-- =========================
-- 8) Reports and metrics
-- =========================
CREATE TABLE MonthlyReport (
  report_id       UUID PRIMARY KEY,
  user_health_id  VARCHAR(64) NOT NULL REFERENCES "User"(health_id) ON DELETE CASCADE,
  month           CHAR(7) NOT NULL, -- YYYY-MM
  summary         TEXT NOT NULL,
  steps_total     INTEGER NULL
);
-- Candidate key (user, month) if required:
-- CREATE UNIQUE INDEX uq_user_month ON MonthlyReport(user_health_id, month);

CREATE TABLE HealthMetric (
  metric_id     UUID PRIMARY KEY,
  user_health_id VARCHAR(64) NOT NULL REFERENCES "User"(health_id) ON DELETE CASCADE,
  metric_date   DATE NOT NULL,
  metric_type   VARCHAR(30) NOT NULL,
  metric_value  DECIMAL(18,4) NOT NULL,
  CONSTRAINT chk_metric_type CHECK (metric_type IN ('Steps','HeartRate'))
);
-- Optional uniqueness per user/type/date:
-- CREATE UNIQUE INDEX uq_metric_user_type_date ON HealthMetric(user_health_id, metric_type, metric_date);

-- =========================
-- 9) Helpful indexes
-- =========================
CREATE INDEX idx_email_user ON ContactEmail(user_health_id);
CREATE INDEX idx_phone_user ON Phone(user_health_id);
CREATE INDEX idx_up_user ON UserProvider(user_health_id);
CREATE INDEX idx_up_provider ON UserProvider(provider_license_number);
CREATE INDEX idx_appt_user_datetime ON Appointment(user_health_id, date_time DESC);
CREATE INDEX idx_appt_provider_datetime ON Appointment(provider_license_number, date_time DESC);
CREATE INDEX idx_participation_user ON ChallengeParticipation(user_health_id);
CREATE INDEX idx_inv_sender ON Invitation(sender_user_health_id);
CREATE INDEX idx_metric_user_date ON HealthMetric(user_health_id, metric_date DESC);
