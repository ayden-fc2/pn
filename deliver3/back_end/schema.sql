-- Users table: Stores the core information for each user of the health platform.
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique identifier for the user (health_id in design)
    first_name TEXT NOT NULL, -- User's first name
    last_name TEXT NOT NULL, -- User's last name
    password TEXT NOT NULL, -- Hashed password for authentication
    address TEXT -- User's physical address
);

-- Emails table: Stores email addresses associated with users.
CREATE TABLE IF NOT EXISTS Emails (
    email_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique identifier for the email record
    user_id INTEGER NOT NULL, -- Foreign key referencing the User
    email_address TEXT NOT NULL UNIQUE, -- The actual email address
    is_verified BOOLEAN DEFAULT 0, -- Whether the email has been verified
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- PhoneNumbers table: Stores phone numbers associated with users.
CREATE TABLE IF NOT EXISTS PhoneNumbers (
    phone_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique identifier for the phone record
    user_id INTEGER NOT NULL, -- Foreign key referencing the User
    phone_number TEXT NOT NULL, -- The phone number string
    is_verified BOOLEAN DEFAULT 0, -- Whether the phone number has been verified
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    CONSTRAINT unique_user_phone UNIQUE (user_id) -- Constraint: One phone number per user (as per design)
);

-- Providers table: Stores information about healthcare providers (Doctors, Specialists, etc.).
CREATE TABLE IF NOT EXISTS Providers (
    provider_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique identifier for the provider (license_number in design)
    name TEXT NOT NULL, -- Full name of the provider
    specialty TEXT, -- The medical specialty of the provider
    is_verified BOOLEAN DEFAULT 0 -- Whether the provider is verified
);

-- UserProviders table: Links users to their healthcare providers (Many-to-Many).
CREATE TABLE IF NOT EXISTS UserProviders (
    user_id INTEGER NOT NULL, -- Foreign key referencing the User
    provider_id INTEGER NOT NULL, -- Foreign key referencing the Provider
    is_primary_care BOOLEAN DEFAULT 0, -- Whether this provider is the user's primary care physician
    linked_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- When this relationship was established
    PRIMARY KEY (user_id, provider_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (provider_id) REFERENCES Providers(provider_id) ON DELETE CASCADE
);

-- Appointments table: Stores appointment details between users and providers.
CREATE TABLE IF NOT EXISTS Appointments (
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique identifier for the appointment
    user_id INTEGER NOT NULL, -- Foreign key referencing the User
    provider_id INTEGER NOT NULL, -- Foreign key referencing the Provider
    appointment_date DATETIME NOT NULL, -- The scheduled date and time
    appointment_type TEXT, -- Type of appointment (e.g., Checkup, Therapy)
    status TEXT DEFAULT 'Scheduled' CHECK(status IN ('Scheduled', 'Completed', 'Cancelled')), -- Status of the appointment
    memo TEXT, -- Optional notes or memo for the appointment
    cancel_reason TEXT, -- Reason for cancellation if status is Cancelled
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (provider_id) REFERENCES Providers(provider_id) ON DELETE CASCADE
);

-- WellnessChallenges table: Stores definitions of wellness challenges.
CREATE TABLE IF NOT EXISTS WellnessChallenges (
    challenge_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique identifier for the challenge
    creator_id INTEGER NOT NULL, -- Foreign key referencing the User who created the challenge
    name TEXT NOT NULL, -- Name of the challenge
    description TEXT, -- Detailed description
    goal TEXT, -- The specific goal of the challenge (e.g., "10000 steps")
    start_date DATE, -- When the challenge starts
    end_date DATE, -- When the challenge ends
    FOREIGN KEY (creator_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    CONSTRAINT check_dates CHECK (end_date >= start_date) -- Constraint: End date must be after start date
);

-- UserChallenges table: Tracks user participation in challenges.
CREATE TABLE IF NOT EXISTS UserChallenges (
    user_id INTEGER NOT NULL, -- Foreign key referencing the User
    challenge_id INTEGER NOT NULL, -- Foreign key referencing the Challenge
    status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Completed', 'Dropped')), -- Participation status
    progress_value REAL DEFAULT 0, -- Current progress value (e.g., number of steps taken)
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- Last update time
    PRIMARY KEY (user_id, challenge_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (challenge_id) REFERENCES WellnessChallenges(challenge_id) ON DELETE CASCADE
);

-- HealthMetrics table: Stores health data recorded by users.
CREATE TABLE IF NOT EXISTS HealthMetrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique identifier for the metric
    user_id INTEGER NOT NULL, -- Foreign key referencing the User
    metric_type TEXT NOT NULL, -- Type of metric (e.g., 'Weight', 'Blood Pressure', 'Steps')
    value REAL NOT NULL, -- The numerical value
    unit TEXT, -- Unit of measurement (e.g., 'kg', 'mmHg')
    recorded_date DATETIME DEFAULT CURRENT_TIMESTAMP, -- When the metric was recorded
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- FamilyGroup table: Represents a group of users (e.g., a family unit).
CREATE TABLE IF NOT EXISTS FamilyGroup (
    group_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique identifier for the group
    name TEXT NOT NULL -- Name of the family group
);

-- FamilyMembership table: Links users to family groups.
CREATE TABLE IF NOT EXISTS FamilyMembership (
    membership_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique identifier for the membership
    group_id INTEGER NOT NULL, -- Foreign key referencing the FamilyGroup
    user_id INTEGER NOT NULL, -- Foreign key referencing the User
    role TEXT, -- Role in the family (e.g., 'Admin', 'Member')
    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- When the user joined
    FOREIGN KEY (group_id) REFERENCES FamilyGroup(group_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    UNIQUE(group_id, user_id) -- Constraint: A user can be in a group only once
);

-- UserDelegation table: Manages guardian/dependent relationships.
CREATE TABLE IF NOT EXISTS UserDelegation (
    delegation_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique identifier for the delegation
    guardian_id INTEGER NOT NULL, -- Foreign key referencing the Guardian User
    dependent_id INTEGER NOT NULL, -- Foreign key referencing the Dependent User
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- When the delegation was created
    FOREIGN KEY (guardian_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (dependent_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    CHECK (guardian_id != dependent_id), -- Constraint: Guardian cannot be the dependent
    UNIQUE(guardian_id, dependent_id) -- Constraint: Unique pair
);

-- Invitation table: Manages invitations for challenges or family groups.
CREATE TABLE IF NOT EXISTS Invitation (
    invitation_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique identifier for the invitation
    sender_id INTEGER NOT NULL, -- Foreign key referencing the Sender User
    challenge_id INTEGER, -- Foreign key referencing a Challenge (nullable)
    type TEXT NOT NULL, -- Type of invitation (e.g., 'Family', 'Challenge')
    target_email TEXT, -- Email of the invitee
    target_phone TEXT, -- Phone of the invitee
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- Creation time
    status TEXT DEFAULT 'Pending' CHECK(status IN ('Pending', 'Accepted', 'Rejected', 'Expired')), -- Status
    FOREIGN KEY (sender_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (challenge_id) REFERENCES WellnessChallenges(challenge_id) ON DELETE CASCADE,
    CHECK (target_email IS NOT NULL OR target_phone IS NOT NULL) -- Constraint: At least one contact method required
);

-- MonthlyReport table: Stores generated monthly health summaries.
CREATE TABLE IF NOT EXISTS MonthlyReport (
    report_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique identifier for the report
    user_id INTEGER NOT NULL, -- Foreign key referencing the User
    month TEXT NOT NULL, -- The month the report covers (YYYY-MM)
    summary TEXT, -- Text summary of the report
    steps_total INTEGER DEFAULT 0, -- Total steps for the month
    generated_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- When the report was generated
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    UNIQUE(user_id, month) -- Constraint: One report per user per month
);

-- Partial unique index to ensure only one primary care provider per user
CREATE UNIQUE INDEX IF NOT EXISTS idx_user_primary_care 
ON UserProviders(user_id) 
WHERE is_primary_care = 1;
