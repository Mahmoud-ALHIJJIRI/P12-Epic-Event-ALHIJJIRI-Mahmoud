# 🎉 Epic Events CRM CLI

Epic Events CRM is a command-line interface application that helps Epic Events manage clients, contracts, and event logistics more efficiently. Built with Python, PostgreSQL, and rich CLI tools, it ensures secure access, clean separation of logic, and user role permissions.
⸻

## 🚀 Features

	•	🔐 JWT-based Authentication
	•	👤 Role-Based Access (Commercial, Gestion, Support)
	•	📇 Client Management
	•	📃 Contract Management
	•	📅 Event Scheduling
	•	🔑 Password hashing with Argon2
	•	📊 Beautiful CLI display with rich
	•	🧱 Database migrations via Alembic
	•	📁 Clean folder structure with service layers



## 📁 Project Structure

```text
📁 Epic_events/
├── 📁 auth/                     # Authentication logic
│   ├── __init__.py
│   ├── permissions.py
│   └── utils.py
├── 📁 cli/                      # CLI command entrypoints
│   ├── __init__.py
│   ├── client.py
│   ├── contract.py
│   ├── event.py
│   └── user.py
├── 📁 service/                  # Business logic (services)
│   ├── __init__.py
│   ├── client_service.py
│   ├── contract_service.py
│   ├── event_service.py
│   └── user_service.py
├── __init__.py
├── config.py                   # Project configuration
├── database.py                 # DB connection/session
├── models.py                   # SQLAlchemy models
├── rich_styles.py              # Rich style for better CLI outputs
├── sentry.py 

📄 .env                          # Environment variables
📄 .gitignore
📄 main.py                      # CLI entry point
📄 Pipfile
📄 Pipfile.lock
📄 README.md                    # Project documentation
```


## ✅ Requirements
	•	Python 3.9 or newer
	•	PostgreSQL
	•	Pipenv


## 🧰 Setup Instructions

### 1. Clone the Repo
```bash
	git clone https://github.com/Mahmoud-ALHIJJIRI/P12-Epic-Event-ALHIJJIRI-Mahmoud
	cd epic-events-crm
```

---
### 2. Install Dependencies
```bash
	pipenv install
	pipenv shell
```
---
### 3. 🔧 Prepare Environment Variables

Create a `.env` file at the root and add:
```env
# PostgreSQL DB URL
DATABASE_URL=postgresql://postgres@localhost:5432/epic_event_db

# Secret key for JWT signing
SECRET_KEY=your_secure_random_string_here

# Token expiration (in minutes)
JWT_EXPIRATION_MINUTES=60

# Optional: Sentry DSN
SENTRY_DSN=your_sentry_dsn_here
```

Make sure to replace your_secret_key_here with a secure random string (e.g., using openssl rand -hex 32 or any password generator).

✅ Note: This .env file is automatically loaded by the application to configure the database and JWT authentication.

---

### 4. Configure PostgreSQL
```sql
-- in psql
CREATE DATABASE epic_event_db;
```

If using Alembic, also set the correct DB URL in `alembic.ini`:
```ini
sqlalchemy.url = postgresql://postgres@localhost:5432/epic_event_db
```
---

### 5. 🏗️ Initialize the Database
```bash
	python main.py
	python main.py --help # To list the commands's list
```
---

## 🔐 User Roles & Permissions

| Role       | Description & Permissions                                         |
|------------|------------------------------------------------------------------|
| Commercial | Can create/update their clients, contracts, and events           |
| Gestion    | Admin role. Can manage all users, contracts, and events          |
| Support    | Can view/update only events assigned to them                     |


---

## 🧪 Example Usage

```bash
	python main.py register-admin         # First user (gestion)
	python main.py login
	python main.py register-client        # Commercial only
	python main.py list-clients
	python main.py whoami
	python main.py logout
```
---


## ⚙️ Dev & Debug Notes
- JWT token is saved at `~/.epic_crm_token`
- To logout, delete that file or run:
  ```bash
  python main.py logout
  ```
- You can override the token file path using `.env`
---

## 📦 Pipenv Commands

```bash
	pipenv install             # Install dependencies
	pipenv shell               # Activate virtualenv
	pipenv run python main.py  # Run the app inside the virtualenv
```
---

## 📜 License

> This project is for educational and internal use at Epic Events.

---

# 🙋‍♂️ Author

### Mahmoud ALHIJJIRI
### GitHub: @Mahmoud-ALHIJJIRI