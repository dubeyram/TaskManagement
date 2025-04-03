# Task Management Setup Guide

## Overview
The Task Management API is a Django-based backend system that provides task management functionalities, including user and task creation, task assignment, list all the tasks, and retrieval of tasks assigned to users.

## Features
- User creation
- Task creation and retrieval
- Assigning tasks to multiple users
- Pagination for listing tasks
- Structured JSON responses
- Implemented Signals to log user creation, task creation, and task assigned to users
- Implemented Celery for asynchronous task creation
- Implemented Celery Beat for periodic reminder emails to users

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
### 9. Run Celery
```bash
celery -A task_management worker -l info
```

### 10. Run Celery Beat
```bash
celery -A task_management beat -l info
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


### 4. **Get All Tasks (Paginated)**
- **Endpoint:** `GET /task/?page=1&page_size=5`
- **Description:** Retrieves all tasks with pagination.
- **Response:**
```json
{
    "count": 100,
    "total_pages": 20,
    "current_page": 1,
    "next_page": 2,
    "previous_page": null,
    "results": [
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

## Postman Collection
- The Postman collection for this API can be found [here](https://ramgopaldubey.postman.co/workspace/RamGopal-Dubey's-Workspace~2669db3a-425a-4b2e-8e33-384c031cc97a/collection/43448931-b53e329c-6048-4a1a-a56e-5de35d74ca15?action=share&creator=43448931&active-environment=43448931-94367d10-6f2b-4b8e-9854-5a51e7f66342).
- **Important:** Select the environment as **local** while using the API.


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

