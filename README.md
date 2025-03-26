# Task Management Setup Guide

## Overview
The Task Management API is a Django-based backend system that provides task management functionalities, including user and task creation, task assignment, list all the tasks, and retrieval of tasks assigned to users.

## Features
- User creation
- Task creation and retrieval
- Assigning tasks to multiple users
- Pagination for listing tasks
- Structured JSON responses

## Technology Stack
- **Backend**: Django, Django REST Framework (DRF)
- **Database**: PostgreSQL

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/task_management.git
cd task_management
```

### 2. Create a Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
1. Create a `.env` file in the project root:
   ```bash
   touch .env
   ```
2. Add the following content to `.env`:
   ```ini
   DATABASE_NAME=task_management
   DATABASE_USER=your_username
   DATABASE_PASSWORD=your_password
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   ```

### 5. Create and Configure the Database
```bash
psql -U your_username -d postgres -c "CREATE DATABASE task_management;"
```

### 6. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 8. Run the Server
```bash
python manage.py runserver
```

---

## API Endpoints

### 1. **User Creation**
- **Endpoint:** `POST /user/`
- **Description:** Create a new user.
- **Payload:**
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@example.com",
    "password": "securepassword",
    "mobile": "1234567890"
}
```
- **Response:**
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@example.com",
    "username": "johndoe_1678543210",
    "mobile": "1234567890"
}
```

### 2. **Create a Task**
- **Endpoint:** `POST /task/`
- **Description:** Creates a new task.
- **Payload:**
```json
{
    "name": "Fix Bug #123",
    "description": "Fix the login page bug",
    "task_type": "Bug",
    "status": "Pending"
}
```
- **Response:**
```json
{
    "id": 1,
    "name": "Fix Bug #123",
    "description": "Fix the login page bug",
    "task_type": "Bug",
    "status": "Pending",
    "assigned_users": []
}
```

### 3. **Assign a Task to Users**
- **Endpoint:** `PATCH /task/{task_id}/assign/`
- **Description:** Assigns a task to one or more users.
- **Payload:**
```json
{
    "assigned_users": [1, 2, 3]
}
```
- **Response:**
```json
{
    "assigned_users": [1, 2, 3]
}
```

### 4. **Get All Tasks**
- **Endpoint:** `GET /task/`
- **Description:** Retrieves all tasks with pagination.
- **Response:**
```json
{
    "tasks": [
        {
            "id": 1,
            "name": "Initial Setup",
            "description": "This task is for initial setup of the project",
            "created_at": "2025-03-26T07:13:28.524239Z",
            "completed_at": null,
            "task_type": "",
            "status": "Pending",
            "assigned_users": [2, 1, 3, 4, 5, 6]
        }
    ]
}
```

### 5. **Get Tasks Assigned to a User**
- **Endpoint:** `GET /user/{user_id}/tasks/`
- **Description:** Fetches all tasks assigned to a specific user.
- **Response:**
```json
{
    "email": "johndoe@example.com",
    "name": "John Doe",
    "tasks": [
        {
            "name": "Fix Bug #123",
            "description": "Fix the login page bug",
            "task_type": "Bug",
            "status": "Pending"
        }
    ]
}
```

---

## Error Handling
### Common Status Codes:
- `200 OK` – Successful requests
- `201 Created` – When a resource is successfully created
- `400 Bad Request` – Validation errors or incorrect payload
- `404 Not Found` – Resource not found

---

## Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch`).
3. Commit changes (`git commit -m 'Add new feature'`).
4. Push to GitHub (`git push origin feature-branch`).
5. Submit a pull request.

---


## Contact
For questions or support, contact:
- **Email:** rambackenddev@gmail.com
- **GitHub Issues:** [Create an issue](https://github.com/yourusername/task_management/issues)

