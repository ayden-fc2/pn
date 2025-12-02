# Health Track API Documentation

Base URL: `http://127.0.0.1:5000`

## 1. Authentication

### Login
*   **URL**: `/login`
*   **Method**: `POST`
*   **Description**: Authenticates a user.
*   **Request Body**:
    ```json
    {
        "user_id": 1,
        "password": "password123"
    }
    ```
*   **Response (200 OK)**:
    ```json
    {
        "message": "Logged in successfully",
        "user": {
            "user_id": 1,
            "first_name": "John",
            "last_name": "Doe",
            ...
        }
    }
    ```
*   **Response (401 Unauthorized)**: `{"error": "Invalid credentials"}`

### Logout
*   **URL**: `/logout`
*   **Method**: `POST`
*   **Description**: Logs out the current user.
*   **Response**: `{"message": "Logged out successfully"}`

---

## 2. Account Management

**Note**: All account endpoints require the user to be logged in.

### Get Account Details
*   **URL**: `/account`
*   **Method**: `GET`
*   **Description**: Retrieves user profile, emails, phone numbers, and linked providers.
*   **Response**:
    ```json
    {
        "user": { ... },
        "emails": [ ... ],
        "phones": [ ... ],
        "providers": [
            {
                "provider_id": 1,
                "provider_name": "Dr. Smith",
                "specialty": "Cardiology"
            }
        ]
    }
    ```

### Get All Providers
*   **URL**: `/account/providers`
*   **Method**: `GET`
*   **Description**: Retrieves a list of all available healthcare providers.
*   **Response**:
    ```json
    [
        {
            "provider_id": 1,
            "provider_name": "Dr. Smith",
            "specialty": "Cardiology"
        }
    ]
    ```

### Update Profile
*   **URL**: `/account`
*   **Method**: `PUT`
*   **Request Body**:
    ```json
    {
        "first_name": "John",
        "last_name": "Doe",
        "address": "New Address 123"
    }
    ```
*   **Response**: `{"message": "Account updated"}`

### Manage Emails
*   **URL**: `/account/email`
*   **Method**: `POST` (Add) / `DELETE` (Remove)
*   **Request Body**: `{"email": "new@example.com"}`
*   **Response**: `{"message": "Email added"}` or `{"message": "Email deleted"}`

### Manage Phones
*   **URL**: `/account/phone`
*   **Method**: `POST` (Add) / `DELETE` (Remove)
*   **Request Body**: `{"phone": "555-9999"}`
*   **Response**: `{"message": "Phone added"}` or `{"message": "Phone deleted"}`

### Manage Providers
*   **URL**: `/account/provider`
*   **Method**: `POST` (Link) / `DELETE` (Unlink)
*   **Request Body**: `{"provider_id": 2}`
*   **Response**: `{"message": "Provider linked"}` or `{"message": "Provider unlinked"}`

---

## 3. Appointments

### List Appointments
*   **URL**: `/appointments`
*   **Method**: `GET`
*   **Response**:
    ```json
    [
        {
            "appointment_id": 1,
            "provider_name": "Dr. Emily White",
            "appointment_date": "2023-10-15 10:00:00",
            "date": "2023-10-15",
            "time": "10:00",
            "description": "Checkup",
            "status": "Completed",
            ...
        }
    ]
    ```

### Book Appointment
*   **URL**: `/appointments`
*   **Method**: `POST`
*   **Request Body**:
    ```json
    {
        "provider_id": 1,
        "date": "2023-12-25",
        "time": "10:00",
        "description": "Checkup"
    }
    ```
*   **Response**: `{"message": "Appointment booked"}`

### Cancel Appointment
*   **URL**: `/appointments/<appointment_id>`
*   **Method**: `DELETE`
*   **Response**: `{"message": "Appointment cancelled"}`

### Search Appointments
*   **URL**: `/search`
*   **Method**: `GET`
*   **Query Parameters**:
    *   `provider`: (Optional) Provider name partial match
    *   `type`: (Optional) Appointment type partial match
    *   `start_date`: (Optional) YYYY-MM-DD
    *   `end_date`: (Optional) YYYY-MM-DD
*   **Example**: `/search?provider=Emily&start_date=2023-01-01`

---

## 4. Wellness Challenges

### List Challenges
*   **URL**: `/challenges`
*   **Method**: `GET`
*   **Response**:
    ```json
    [
        {
            "challenge_id": 1,
            "title": "Morning Run",
            "description": "Run 5km every morning",
            "joined": true,
            ...
        }
    ]
    ```

### Create Challenge
*   **URL**: `/challenges`
*   **Method**: `POST`
*   **Request Body**:
    ```json
    {
        "name": "Morning Run",
        "description": "Run 5km every morning",
        "start_date": "2023-12-01",
        "end_date": "2023-12-31"
    }
    ```
*   **Response**: `{"message": "Challenge created"}`

### Join Challenge
*   **URL**: `/challenges/<challenge_id>/join`
*   **Method**: `POST`
*   **Response**: `{"message": "Joined challenge"}`

### Leave Challenge
*   **URL**: `/challenges/<challenge_id>/leave`
*   **Method**: `POST`
*   **Response**: `{"message": "Left challenge"}`

---

## 5. Summary & Analytics

### Dashboard Summary
*   **URL**: `/summary`
*   **Method**: `GET`
*   **Response**:
    ```json
    {
        "bmi": 22.5,
        "active_challenges": 2,
        "upcoming_appointments": 1
    }
    ```

### Monthly Summary
*   **URL**: `/summary/monthly`
*   **Method**: `GET`
*   **Query Parameters**: `month` (Format: YYYY-MM, defaults to current month)
*   **Response**:
    ```json
    {
        "month": "2023-11",
        "appointment_count": 2,
        "metrics_stats": [
            {
                "metric_type": "Weight",
                "avg_val": 75.5,
                "min_val": 75.0,
                "max_val": 76.0
            }
        ]
    }
    ```

### Global Analytics
*   **URL**: `/analytics`
*   **Method**: `GET`
*   **Description**: Returns the most popular challenge and the most active user.
*   **Response**:
    ```json
    {
        "most_popular_challenge": { "name": "10k Steps Daily", "participant_count": 4 },
        "most_active_user": { "first_name": "John", "last_name": "Doe", "record_count": 5 }
    }
    ```
