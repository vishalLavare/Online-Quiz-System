# Online Quiz System Backend

## 📸 UI Preview

### Login Screen


### Register Screen
![Online Quiz System Register](assets/screenshot2.png)

### Quiz Settings Screen
![Online Quiz System Settings](assets/screenshot3.png)

A complete REST API backend for an Online Quiz System built with **Python Flask** and **MySQL**.

## 🚀 Features

- **User Authentication**: Register and Login with JWT (JSON Web Tokens).
- **Quiz Management**: Fetch questions and options.
- **Submission**: Submit answers and prevent duplicate entries.
- **Scoring**: Instant score calculation using SQL aggregation.
- **Leaderboard**: Rank users by their performance.
- **Docker Support**: Easy setup with Docker Compose.

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Database**: MySQL
- **Auth**: Flask-JWT-Extended, Bcrypt
- **Containerization**: Docker, Docker Compose

## 📦 Project Structure

```text
.
├── app.py              # Main Flask application
├── db.py               # Database connection and initialization
├── schema.sql           # MySQL database schema and sample data
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker image configuration
├── docker-compose.yml   # Multi-container setup
└── README.md           # Instructions
```

## ⚙️ How to Run Locally

### Option 1: Using Docker (Recommended)

1. Ensure you have Docker and Docker Compose installed.
2. Run:
   ```bash
   docker-compose up --build
   ```
3. The API will be available at `http://localhost:5000`.

### Option 2: Manual Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Setup MySQL**:
   - Create a database named `quiz_db`.
   - Run the queries in `schema.sql` to create tables and insert sample data.
3. **Environment Variables**:
   Create a `.env` file (optional) or set variables:
   ```text
   DB_HOST=localhost
   DB_USER=your_user
   DB_PASSWORD=your_password
   DB_NAME=quiz_db
   JWT_SECRET_KEY=your_secret_key
   ```
4. **Run the App**:
   ```bash
   python app.py
   ```

## 📍 API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST   | `/register` | Register a new user | No |
| POST   | `/login` | Log in and get JWT token | No |
| GET    | `/questions` | Get all quiz questions | No |
| POST   | `/submit` | Submit answers | Yes (JWT) |
| GET    | `/score/{id}` | Get score for a user | No |
| GET    | `/leaderboard` | View user rankings | No |

## 🧪 Sample Payloads

### POST /register
```json
{
  "username": "john_doe",
  "password": "password123"
}
```

### POST /submit
**Header**: `Authorization: Bearer <your_token>`
```json
{
  "answers": [
    {"question_id": 1, "option_id": 3},
    {"question_id": 2, "option_id": 6}
  ]
}
```


