-- Users table
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    password TEXT NOT NULL, -- In a real app, this should be hashed
    address TEXT
);

-- Emails table (One-to-Many with Users)
CREATE TABLE IF NOT EXISTS Emails (
    email_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    email_address TEXT NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- PhoneNumbers table (One-to-Many with Users)
CREATE TABLE IF NOT EXISTS PhoneNumbers (
    phone_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    phone_number TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Providers table
CREATE TABLE IF NOT EXISTS Providers (
    provider_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialty TEXT
);

-- UserProviders table (Many-to-Many between Users and Providers)
CREATE TABLE IF NOT EXISTS UserProviders (
    user_id INTEGER NOT NULL,
    provider_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, provider_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (provider_id) REFERENCES Providers(provider_id) ON DELETE CASCADE
);

-- Appointments table
CREATE TABLE IF NOT EXISTS Appointments (
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    provider_id INTEGER NOT NULL,
    appointment_date DATETIME NOT NULL,
    appointment_type TEXT,
    status TEXT DEFAULT 'Scheduled', -- Scheduled, Completed, Cancelled
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (provider_id) REFERENCES Providers(provider_id) ON DELETE CASCADE
);

-- WellnessChallenges table
CREATE TABLE IF NOT EXISTS WellnessChallenges (
    challenge_id INTEGER PRIMARY KEY AUTOINCREMENT,
    creator_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (creator_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- UserChallenges table (Many-to-Many for participation)
CREATE TABLE IF NOT EXISTS UserChallenges (
    user_id INTEGER NOT NULL,
    challenge_id INTEGER NOT NULL,
    status TEXT DEFAULT 'Active', -- Active, Completed, Dropped
    PRIMARY KEY (user_id, challenge_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (challenge_id) REFERENCES WellnessChallenges(challenge_id) ON DELETE CASCADE
);

-- HealthMetrics table
CREATE TABLE IF NOT EXISTS HealthMetrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    metric_type TEXT NOT NULL, -- e.g., 'Weight', 'Blood Pressure', 'Steps'
    value REAL NOT NULL,
    unit TEXT,
    recorded_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);
