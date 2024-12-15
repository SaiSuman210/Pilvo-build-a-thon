# Pilvo-build-a-thon

This is a Flask-based web application for monitoring and displaying the status of various services. It includes features for user authentication, service management, incident logging, and real-time status updates using WebSocket and Socket.IO. The application also supports organization-specific public status pages.

## Features

- User Authentication (Register, Login, Logout)
- Service Management (Add, Update, Delete)
- Incident Logging for Services
- Real-Time Status Updates via WebSocket
- Organization-Specific Public Status Pages
- API Endpoint for External Status Checks

## Requirements

- Python 3.7+
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-SocketIO
- Flask-Migrate
- Eventlet
- Redis

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/status_page_app.git
   cd status_page_app
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Redis:**
   For macOS:
   ```bash
   brew install redis
   brew services start redis
   ```
   For Ubuntu:
   ```bash
   sudo apt-get update
   sudo apt-get install redis-server
   sudo service redis-server start
   ```

5. **Run Database Migrations:**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Create an Admin User:**
   ```bash
   flask shell
   ```

   Inside the Flask shell:
   ```python
   from app import db
   from models import User
   from werkzeug.security import generate_password_hash

   admin_user = User(username='admin', password=generate_password_hash('adminpassword'), organization_id=1)
   db.session.add(admin_user)
   db.session.commit()
   ```

## Running the Application

1. **Run the Flask Application:**
   ```bash
   python app.py
   ```

2. **Access the Application:**
   Open your web browser and navigate to `http://localhost:5000`.

## Usage

### User Authentication

- **Register**: Create a new user account.
- **Login**: Log in to an existing account.
- **Logout**: Log out of the current session.

### Service Management

- **Add Service**: Add a new service with a name and status.
- **Update Service**: Update the status of an existing service.
- **Log Incident**: Log an incident for a service with a description and status.

### Public Status Pages

- Access the public status page for an organization by navigating to `/public/<organization_id>`.

### API Endpoint

- Check the status of services for an organization by making a GET request to `/api/status/<organization_id>`.

## File Structure

```
/status_page_app
  /static
    favicon.ico
  /templates
    base.html
    index.html
    login.html
    public.html
    register.html
  app.py
  config.py
  models.py
  requirements.txt
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes or improvements.

## Contact

For any questions or inquiries, please contact [saisuman.910@gmail.com].