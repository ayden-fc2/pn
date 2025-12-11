import sqlite3
import os

# Ensure we are in the right directory or use absolute path
db_path = 'health_track.db'
if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit(1)

db = sqlite3.connect(db_path)
cursor = db.cursor()

print("--- 1. Checking get_latest_metric (Should use idx_metrics_user_type_date) ---")
# Query from MetricRepository.get_latest_metric
query1 = "EXPLAIN QUERY PLAN SELECT value FROM HealthMetrics WHERE user_id = 1 AND metric_type = 'Weight' ORDER BY recorded_date DESC LIMIT 1"
cursor.execute(query1)
for row in cursor.fetchall():
    print(row)

print("\n--- 2. Checking get_appointments (Should use idx_appointments_user_id) ---")
# Simple query on Appointments
query2 = "EXPLAIN QUERY PLAN SELECT * FROM Appointments WHERE user_id = 1"
cursor.execute(query2)
for row in cursor.fetchall():
    print(row)

print("\n--- 3. Checking get_monthly_stats (Complex case) ---")
# Query from MetricRepository.get_monthly_stats
query3 = "EXPLAIN QUERY PLAN SELECT metric_type FROM HealthMetrics WHERE user_id = 1 AND strftime('%Y-%m', recorded_date) = '2025-10' GROUP BY metric_type"
cursor.execute(query3)
for row in cursor.fetchall():
    print(row)

db.close()
