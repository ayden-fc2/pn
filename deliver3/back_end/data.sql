-- Insert Users
INSERT INTO Users (first_name, last_name, password, address) VALUES 
('John', 'Doe', 'password123', '123 Main St'),
('Jane', 'Smith', 'securepass', '456 Oak Ave'),
('Alice', 'Johnson', 'alicepass', '789 Pine Ln'),
('Bob', 'Brown', 'bobpass', '321 Elm St');

-- Insert Emails
INSERT INTO Emails (user_id, email_address) VALUES 
(1, 'john.doe@example.com'),
(1, 'john.d@work.com'),
(2, 'jane.smith@example.com'),
(3, 'alice.j@example.com'),
(4, 'bob.brown@example.com');

-- Insert PhoneNumbers
INSERT INTO PhoneNumbers (user_id, phone_number) VALUES 
(1, '555-0101'),
(2, '555-0102'),
(3, '555-0103'),
(4, '555-0104');

-- Insert Providers
INSERT INTO Providers (name, specialty) VALUES 
('Dr. Emily White', 'Cardiology'),
('Dr. Michael Green', 'General Practice'),
('Dr. Sarah Black', 'Dermatology'),
('Dr. David Blue', 'Orthopedics');

-- Insert UserProviders
INSERT INTO UserProviders (user_id, provider_id) VALUES 
(1, 1), (1, 2),
(2, 2), (2, 3),
(3, 1), (3, 4),
(4, 2);

-- Insert Appointments
INSERT INTO Appointments (user_id, provider_id, appointment_date, appointment_type, status) VALUES 
(1, 1, '2023-10-15 10:00:00', 'Checkup', 'Completed'),
(1, 2, '2023-11-01 14:30:00', 'Flu Shot', 'Completed'),
(2, 2, '2023-10-20 09:00:00', 'Consultation', 'Completed'),
(3, 4, '2023-12-05 11:00:00', 'Therapy', 'Scheduled'),
(4, 2, '2023-11-10 15:00:00', 'Checkup', 'Completed'),
(1, 1, '2023-12-01 10:00:00', 'Follow-up', 'Scheduled'),
(2, 3, '2023-12-10 13:00:00', 'Skin Check', 'Scheduled');

-- Insert WellnessChallenges
INSERT INTO WellnessChallenges (creator_id, name, description, start_date, end_date) VALUES 
(1, '10k Steps Daily', 'Walk 10,000 steps every day for a month', '2023-11-01', '2023-11-30'),
(2, 'No Sugar November', 'Avoid added sugar for the whole month', '2023-11-01', '2023-11-30'),
(3, 'Yoga Morning', 'Do 20 mins of yoga every morning', '2023-12-01', '2023-12-31');

-- Insert UserChallenges
INSERT INTO UserChallenges (user_id, challenge_id, status) VALUES 
(1, 1, 'Completed'),
(2, 1, 'Completed'),
(3, 1, 'Active'),
(4, 1, 'Dropped'),
(2, 2, 'Completed'),
(1, 2, 'Active'),
(3, 3, 'Active');

-- Insert HealthMetrics
-- User 1 (John)
INSERT INTO HealthMetrics (user_id, metric_type, value, unit, recorded_date) VALUES 
(1, 'Weight', 80.5, 'kg', '2023-10-01 08:00:00'),
(1, 'Weight', 80.0, 'kg', '2023-10-15 08:00:00'),
(1, 'Weight', 79.5, 'kg', '2023-11-01 08:00:00'),
(1, 'Blood Pressure', 120, 'mmHg', '2023-10-01 08:05:00'), -- Systolic
(1, 'Blood Pressure', 118, 'mmHg', '2023-11-01 08:05:00');

-- User 2 (Jane)
INSERT INTO HealthMetrics (user_id, metric_type, value, unit, recorded_date) VALUES 
(2, 'Weight', 65.0, 'kg', '2023-10-05 07:00:00'),
(2, 'Weight', 64.5, 'kg', '2023-11-05 07:00:00'),
(2, 'Steps', 10500, 'count', '2023-11-01 20:00:00'),
(2, 'Steps', 11000, 'count', '2023-11-02 20:00:00');

-- User 3 (Alice)
INSERT INTO HealthMetrics (user_id, metric_type, value, unit, recorded_date) VALUES 
(3, 'Steps', 5000, 'count', '2023-11-01 18:00:00');
