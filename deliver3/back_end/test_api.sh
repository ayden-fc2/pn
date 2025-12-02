#!/bin/bash

BASE_URL="http://127.0.0.1:5000"
COOKIE_FILE="cookies.txt"

echo "--- 1. Login ---"
curl -s -c $COOKIE_FILE -X POST -H "Content-Type: application/json" -d '{"user_id": 1, "password": "password123"}' $BASE_URL/login
echo -e "\n"

echo "--- 2. Get Account ---"
curl -s -b $COOKIE_FILE $BASE_URL/account
echo -e "\n"

echo "--- 3. Get Appointments ---"
curl -s -b $COOKIE_FILE $BASE_URL/appointments
echo -e "\n"

echo "--- 4. Get Challenges ---"
curl -s -b $COOKIE_FILE $BASE_URL/challenges
echo -e "\n"

echo "--- 5. Monthly Summary (2023-11) ---"
curl -s -b $COOKIE_FILE "$BASE_URL/summary/monthly?month=2023-11"
echo -e "\n"

echo "--- 6. Analytics ---"
curl -s -b $COOKIE_FILE $BASE_URL/analytics
echo -e "\n"

echo "--- 7. Logout ---"
curl -s -b $COOKIE_FILE -X POST $BASE_URL/logout
echo -e "\n"

rm $COOKIE_FILE
