Absolutely! Here’s the full README.md you can copy and paste directly:

⸻


# 🎉 Epic Events CRM CLI

Epic Events CRM is a command-line interface application designed to streamline how Epic Events manages clients, contracts, and events. Built with Python, PostgreSQL, and a clean service architecture, this tool ensures secure access, proper user roles, and effective data management.

---

## 🚀 Features

- 🔐 JWT-based Authentication  
- 👤 Role-Based Access (Commercial, Gestion, Support)  
- 📇 Client Management  
- 📃 Contract Management  
- 📅 Event Scheduling  
- 🔑 Password hashing with Argon2  
- 📊 Beautiful CLI display with `rich`  
- 🧱 Database migrations via Alembic  
- 📁 Clean folder structure with service layers  

---

## 📁 Project Structure

Epic_events/
├── alembic/                  # DB migrations
├── alembic.ini               # Alembic config
├── auth/                     # Authentication logic
│   ├── service.py
│   ├── token.py
│   └── permissions.py
├── service/                  # Business logic (user, client, contract, event)
│   ├── user_service.py
│   ├── client_service.py
│   ├── contract_service.py
│   └── event_service.py
├── cli/                      # CLI commands
├── database.py               # DB connection/session
├── models.py                 # SQLAlchemy models
├── main.py                   # CLI entry point
├── .epic_crm_token           # Local token storage (hidden)
└── README.md                 # You’re here

---

## ✅ Requirements

- Python 3.9 or newer  
- PostgreSQL  
- [Pipenv](https://pipenv.pypa.io/en/latest/)  

---

## 🧰 Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/epic-events-crm.git
cd epic-events-crm

2. Install Dependencies Using Pipenv

pipenv install
pipenv shell

3. Configure PostgreSQL

Create the database in PostgreSQL:

psql -U postgres
CREATE DATABASE epic_event_db;

Update alembic.ini with the correct database URL:

# Inside alembic.ini
sqlalchemy.url = postgresql://postgres@localhost:5432/epic_event_db


⸻

🏗️ Initialize the Database

Run this command to auto-create the tables:

python main.py

Alternatively, if using Alembic:

alembic revision --autogenerate -m "Initial migration"
alembic upgrade head


⸻

🔐 User Roles & Permissions

Role	Description & Permissions
Commercial	Create/update their clients and contracts, create events
Gestion	Full access: manage users, contracts, events
Support	Can view/update only the events assigned to them


⸻

🧪 Example Usage

# Register the first user (Gestion recommended)
python main.py register_admin_user

# Login
python main.py login

# Register client (commercial only)
python main.py register_client

# List clients
python main.py list_clients

# View logged-in user
python main.py whoami

# Logout
python main.py logout


⸻

⚙️ Dev & Debug Notes
	•	JWT token is saved in ~/.epic_crm_token (default home dir)
	•	To logout, delete that file or use python main.py logout
	•	You can also change the token path to the project folder for convenience

⸻

📦 Pipenv Commands

pipenv install             # Install all dependencies
pipenv shell               # Enter virtualenv shell
pipenv run python main.py  # Run main.py with virtualenv


⸻

📜 License

This project is for educational and internal use at Epic Events.

⸻

🙋‍♂️ Author

Mahmoud ALHIJJIRI
GitHub: @Mahmoud-ALHIJJIRI

--- 

Let me know if you'd like to include screenshots, database diagrams, or deployment instructions too!