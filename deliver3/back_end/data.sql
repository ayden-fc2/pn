-- Insert Users
INSERT INTO Users (first_name, last_name, password, address) VALUES 
('John', 'Doe', 'password123', '123 Main St'),
('Jane', 'Smith', 'securepass', '456 Oak Ave'),
('Alice', 'Johnson', 'alicepass', '789 Pine Ln'),
('Bob', 'Brown', 'bobpass', '321 Elm St'),
('Charlie', 'Davis', 'charliepass', '654 Maple Dr'),
('Diana', 'Evans', 'dianapass', '987 Cedar Rd'),
('Frank', 'Green', 'frankpass', '159 Birch Blvd'),
('Grace', 'Hill', 'gracepass', '753 Walnut Way'),
('Henry', 'Irwin', 'henrypass', '852 Spruce St'),
('Ivy', 'Jones', 'ivypass', '951 Fir Ave');

-- Insert Emails
INSERT INTO Emails (user_id, email_address, is_verified) VALUES 
(1, 'john.doe@example.com', 1),
(1, 'john.d@work.com', 0),
(2, 'jane.smith@example.com', 1),
(3, 'alice.j@example.com', 1),
(4, 'bob.brown@example.com', 1),
(5, 'charlie.d@example.com', 1),
(6, 'diana.e@example.com', 1),
(7, 'frank.g@example.com', 0),
(8, 'grace.h@example.com', 1),
(9, 'henry.i@example.com', 1),
(10, 'ivy.j@example.com', 1);

-- Insert PhoneNumbers
INSERT INTO PhoneNumbers (user_id, phone_number, is_verified) VALUES 
(1, '555-0101', 1),
(2, '555-0102', 1),
(3, '555-0103', 1),
(4, '555-0104', 0),
(5, '555-0105', 1),
(6, '555-0106', 1),
(7, '555-0107', 0),
(8, '555-0108', 1),
(9, '555-0109', 1),
(10, '555-0110', 1);

-- Insert Providers
INSERT INTO Providers (name, specialty, is_verified) VALUES 
('Dr. Emily White', 'Cardiology', 1),
('Dr. Michael Green', 'General Practice', 1),
('Dr. Sarah Black', 'Dermatology', 1),
('Dr. David Blue', 'Orthopedics', 1),
('Dr. Lisa Grey', 'Pediatrics', 1),
('Dr. Tom Brown', 'Neurology', 1),
('Dr. James Wilson', 'Oncology', 1),
('Dr. Patricia Moore', 'Psychiatry', 1),
('Dr. Robert Taylor', 'Urology', 1),
('Dr. Jennifer Anderson', 'Endocrinology', 0),
('Dr. William Thomas', 'Gastroenterology', 1),
('Dr. Elizabeth Jackson', 'Rheumatology', 0),
('Dr. Christopher White', 'Pulmonology', 1),
('Dr. Jessica Harris', 'Nephrology', 0),
('Dr. Daniel Martin', 'Ophthalmology', 1);

-- Insert UserProviders
INSERT INTO UserProviders (user_id, provider_id, is_primary_care) VALUES 
(1, 1, 0), (1, 2, 1),
(2, 2, 1), (2, 3, 0),
(3, 1, 0), (3, 4, 0),
(4, 2, 1),
(5, 5, 1),
(6, 6, 0),
(7, 2, 1),
(8, 3, 0),
(9, 4, 1),
(10, 1, 0);

-- Insert Appointments
INSERT INTO Appointments (user_id, provider_id, appointment_date, appointment_type, status, memo) VALUES 
(1, 1, '2025-10-15 10:00:00', 'Checkup', 'Completed', 'Annual checkup'),
(1, 2, '2025-11-01 14:30:00', 'Flu Shot', 'Completed', NULL),
(2, 2, '2025-10-20 09:00:00', 'Consultation', 'Completed', 'Skin rash'),
(3, 4, '2026-12-05 11:00:00', 'Therapy', 'Scheduled', 'Monthly session'),
(4, 2, '2025-11-10 15:00:00', 'Checkup', 'Completed', NULL),
(1, 1, '2026-12-01 10:00:00', 'Follow-up', 'Scheduled', 'Follow up on blood pressure'),
(2, 3, '2026-12-10 13:00:00', 'Skin Check', 'Scheduled', 'Routine check'),
(5, 5, '2025-12-15 09:00:00', 'Vaccination', 'Scheduled', 'Kids vaccination'),
(6, 6, '2025-12-20 14:00:00', 'MRI', 'Scheduled', 'Headache check'),
(7, 2, '2025-12-22 10:30:00', 'General', 'Scheduled', NULL),
(8, 3, '2025-12-25 11:00:00', 'Consultation', 'Scheduled', 'Acne'),
(9, 4, '2026-01-05 09:30:00', 'Surgery', 'Scheduled', 'Knee surgery'),
(10, 1, '2026-01-10 15:00:00', 'Checkup', 'Scheduled', 'Heart monitor');

-- Insert WellnessChallenges
INSERT INTO WellnessChallenges (creator_id, name, description, goal, start_date, end_date) VALUES 
(1, '10k Steps Daily', 'Walk 10,000 steps every day for a month', '10000 steps/day', '2025-11-01', '2026-11-30'),
(2, 'No Sugar November', 'Avoid added sugar for the whole month', '0g added sugar', '2025-11-01', '2026-11-30'),
(3, 'Yoga Morning', 'Do 20 mins of yoga every morning', '20 mins/day', '2025-12-01', '2026-12-31'),
(5, 'Marathon Training', 'Run 5km every other day', '5km run', '2026-01-01', '2026-06-01'),
(6, 'Meditation', 'Meditate for 10 mins daily', '10 mins/day', '2026-01-01', '2026-12-31');

-- Insert UserChallenges
INSERT INTO UserChallenges (user_id, challenge_id, status, progress_value) VALUES 
(1, 1, 'Completed', 300000),
(2, 1, 'Completed', 310000),
(3, 1, 'Active', 50000),
(4, 1, 'Dropped', 10000),
(2, 2, 'Completed', 30),
(1, 2, 'Active', 15),
(3, 3, 'Active', 5),
(5, 4, 'Active', 10),
(6, 5, 'Active', 20),
(7, 1, 'Active', 5000),
(8, 2, 'Active', 5),
(9, 3, 'Active', 2),
(10, 4, 'Active', 0);

-- Insert HealthMetrics
-- User 1 (John)
INSERT INTO HealthMetrics (user_id, metric_type, value, unit, recorded_date) VALUES 
(1, 'Weight', 80.5, 'kg', '2025-10-01 08:00:00'),
(1, 'Weight', 80.0, 'kg', '2025-10-15 08:00:00'),
(1, 'Weight', 79.5, 'kg', '2025-11-01 08:00:00'),
(1, 'Height', 180, 'cm', '2025-10-01 08:00:00'), -- Added Height for BMI
(1, 'Blood Pressure', 120, 'mmHg', '2025-10-01 08:05:00'), -- Systolic
(1, 'Blood Pressure', 118, 'mmHg', '2025-11-01 08:05:00'),
(1, 'Steps', 8000, 'count', '2025-10-01 20:00:00'),
(1, 'Steps', 9500, 'count', '2025-10-02 20:00:00'),
(1, 'Steps', 10200, 'count', '2025-10-03 20:00:00'),
(1, 'Steps', 7500, 'count', '2025-11-01 20:00:00'),
(1, 'Steps', 11000, 'count', '2025-11-02 20:00:00');

-- User 2 (Jane)
INSERT INTO HealthMetrics (user_id, metric_type, value, unit, recorded_date) VALUES 
(2, 'Weight', 65.0, 'kg', '2025-10-05 07:00:00'),
(2, 'Weight', 64.5, 'kg', '2025-11-05 07:00:00'),
(2, 'Height', 165, 'cm', '2025-10-05 07:00:00'), -- Added Height for BMI
(2, 'Steps', 10500, 'count', '2025-11-01 20:00:00'),
(2, 'Steps', 11000, 'count', '2025-11-02 20:00:00');

-- User 3 (Alice)
INSERT INTO HealthMetrics (user_id, metric_type, value, unit, recorded_date) VALUES 
(3, 'Steps', 5000, 'count', '2025-11-01 18:00:00'),
(3, 'Height', 170, 'cm', '2025-11-01 18:00:00'),
(3, 'Weight', 70.0, 'kg', '2025-11-01 18:00:00');

-- User 5 (Charlie)
INSERT INTO HealthMetrics (user_id, metric_type, value, unit, recorded_date) VALUES 
(5, 'Run Distance', 5.2, 'km', '2026-01-02 07:00:00'),
(5, 'Height', 175, 'cm', '2026-01-02 07:00:00'),
(5, 'Weight', 75.0, 'kg', '2026-01-02 07:00:00');

-- Family Groups
INSERT INTO FamilyGroup (name) VALUES ('Doe Family'), ('Smith Family');

-- Family Memberships
INSERT INTO FamilyMembership (group_id, user_id, role) VALUES 
(1, 1, 'Admin'), -- John
(1, 3, 'Member'), -- Alice
(2, 2, 'Admin'), -- Jane
(2, 4, 'Member'); -- Bob

-- User Delegations
INSERT INTO UserDelegation (guardian_id, dependent_id) VALUES 
(1, 3), -- John -> Alice
(2, 4), -- Jane -> Bob
(5, 6); -- Charlie -> Diana

-- Invitations
INSERT INTO Invitation (sender_id, challenge_id, type, target_email, status) VALUES 
(1, 1, 'Challenge', 'bob.brown@example.com', 'Pending'),
(2, 2, 'Challenge', 'alice.j@example.com', 'Accepted'),
(3, 3, 'Challenge', 'john.doe@example.com', 'Rejected'),
(5, 4, 'Challenge', 'frank.g@example.com', 'Pending'),
(6, 5, 'Challenge', 'grace.h@example.com', 'Pending'),
(1, NULL, 'Family', 'henry.i@example.com', 'Pending'), -- Family invite
(2, NULL, 'Delegation', 'ivy.j@example.com', 'Pending'), -- Delegation invite
(2, 2, 'Challenge', 'john.doe@example.com', 'Pending'), -- Invite John to Jane's challenge
(3, NULL, 'Family', 'jane.smith@example.com', 'Pending'); -- Invite Jane to Alice's family

-- Monthly Reports
INSERT INTO MonthlyReport (user_id, month, summary, steps_total) VALUES 
(1, '2025-10', 'Avg Weight: 80.2kg. Avg BP: 120 mmHg. Total Steps: 27700. Appointments: 1.', 27700),
(1, '2025-11', 'Avg Weight: 79.5kg. Avg BP: 118 mmHg. Total Steps: 18500. Appointments: 2.', 18500),
(2, '2025-10', 'Avg Weight: 65.0kg. Appointments: 1.', 0),
(2, '2025-11', 'Avg Weight: 64.5kg. Total Steps: 21500. Appointments: 1.', 21500),
(3, '2025-11', 'Total Steps: 5000.', 5000),
(5, '2026-01', 'Great start to the year.', 200000);
