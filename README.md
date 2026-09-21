# FG Warranty Management Platform

A Django-based warranty and repair service management platform developed as an independent project with mentorship.

The application is designed around a warranty/repair workflow connecting customers, technicians, administrators, repair requests, uploaded files, comments, notifications, and repair-status tracking.

> **Project status:** Development / local prototype.
>
> This repository represents the current development state of the project. It has not yet been deployed or fully tested as a production application.

## Features

### Authentication & Accounts

* Custom Django user model
* Role-based users:

  * Customer
  * Technician
  * Admin
  * Messenger Admin
* Password authentication
* Email-based login links
* SMS-based login verification
* Password reset by email
* Signed authentication and password-reset tokens
* Token expiration

### Warranty & Repair Workflow

* Customer repair requests
* Repair request status tracking
* Customer dashboard
* Device and warranty-related request data
* Comments associated with repair requests

### File Management

* Upload files associated with repair requests
* Image and document file handling
* Image preview in Django Admin
* Optional image compression
* S3-compatible object storage support

### Notifications

* Email notifications for new comments
* HTML and plain-text email templates
* Celery-based asynchronous email tasks
* Notification status tracking
* Role-based notification permissions

### Security & Infrastructure

* Django authentication and authorization
* Signed authentication tokens
* Token expiration
* Basic request rate limiting
* Environment-based configuration for secrets
* S3-compatible object storage integration

## Technology

* Python
* Django
* Django ORM
* SQLite for local development
* PostgreSQL-compatible architecture
* Celery
* Pillow
* boto3
* S3-compatible object storage
* HTML/CSS templates

## Project Structure

```text
warranty/
├── accounts/        # Users, authentication and account workflows
├── config/          # Django project configuration
├── files/           # Uploaded repair files
├── middleware/      # Request middleware and rate limiting
├── notifications/   # Notification models and Celery tasks
├── repairs/         # Warranty and repair workflow
├── media/           # Local uploaded files (not tracked by Git)
├── manage.py
├── .env.example     # Environment variable template
└── README.md
```

## Development Status

This project is currently maintained as a local development project.

The repository contains the application source code and Django migrations. Local database contents, uploaded media, credentials, Python cache files, and personal/local documents are intentionally excluded from version control.

Some application components still require further integration and testing before the project can be considered a complete deployable application.

In particular, the current development snapshot references a `comments` Django application that is not included in this repository yet.

### Planned Work

* Complete missing application integrations
* Complete automated test coverage
* Production database configuration
* Production object storage configuration
* Production security configuration
* Production deployment
* Deployment documentation
* Further frontend refinement
* Complete admin-panel functionality
* Additional logging and monitoring

## Local Development

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a local environment file:

```bash
cp .env.example .env
```

Configure the required environment variables in `.env`.

Apply migrations:

```bash
python manage.py migrate
```

Create an administrator:

```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

The development server normally runs at:

```text
http://127.0.0.1:8000/
```

> **Note:** The current repository is a development snapshot and may require additional configuration or missing components before it can run successfully.

## Database & Local Files

The local SQLite database is intentionally excluded from version control.

Uploaded files under `media/` are also excluded because they represent local/runtime data rather than application source code.

Django migrations are included in the repository so that database structure can be recreated independently of the local development database.

## Configuration

Secrets and environment-specific settings should be provided through `.env`.

The repository includes `.env.example` containing the expected environment variable names without real credentials.

Never commit:

* API keys
* Passwords
* Secret keys
* Object-storage credentials
* Email credentials
* Local databases
* Uploaded/private files

## License

No open-source license has been added at this stage.
