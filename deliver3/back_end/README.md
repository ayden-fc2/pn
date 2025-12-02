# Health Track Backend

## Setup & Run

1.  **Install Dependencies**:
    ```bash
    cd back_end
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **Initialize Database**:
    The database `health_track.db` is already initialized. To reset it:
    ```bash
    python3 -c "from app import init_db; init_db()"
    ```

3.  **Run Application**:
    ```bash
    python main.py
    ```
    The server will start at `http://127.0.0.1:5000`.

## API Endpoints (Menu Implementation)

### Authentication
*   `POST /api/login`: Login (Body: `{"user_id": 1, "password": "password123"}`)
*   `POST /api/logout`: Sign Out

### Account Info
*   `GET /api/account`: Get user details, emails, phones, providers.
*   `PUT /api/account`: Update user details.
*   `POST /api/account/email`: Add email.
*   `DELETE /api/account/email`: Remove email.
*   (Similar for phone and provider)

### Appointments
*   `GET /api/appointments`: List appointments.
*   `POST /api/appointments`: Book appointment.

### Wellness Challenges
*   `GET /api/challenges`: List challenges.
*   `POST /api/challenges`: Create challenge.
*   `POST /api/challenges/join`: Join challenge.

### Summary & Search
*   `GET /api/summary/monthly?month=YYYY-MM`: Monthly Health Summary.
*   `GET /api/search?provider=...&type=...`: Search Records.

### Analytics
*   `GET /api/analytics`: Most participants challenge, Most active user.
