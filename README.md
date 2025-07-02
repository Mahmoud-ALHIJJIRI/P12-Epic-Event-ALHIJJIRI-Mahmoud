Here’s your updated README.md with a new section called 🔧 Prepare Environment Variables, instructing users to create a .env file properly:

⸻

🎉 Epic Events CRM CLI

Epic Events CRM is a command-line interface application designed to streamline how Epic Events manages clients, contracts, and events. Built with Python, PostgreSQL, and a clean service architecture, this tool ensures secure access, proper user roles, and effective data management.

⸻

🚀 Features
	•	🔐 JWT-based Authentication
	•	👤 Role-Based Access (Commercial, Gestion, Support)
	•	📇 Client Management
	•	📃 Contract Management
	•	📅 Event Scheduling
	•	🔑 Password hashing with Argon2
	•	📊 Beautiful CLI display with rich
	•	🧱 Database migrations via Alembic
	•	📁 Clean folder structure with service layers

⸻

📁 Project Structure

<pre>
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

📄 .env                          # Environment variables
📄 .gitignore
📄 main.py                      # CLI entry point
📄 Pipfile
📄 Pipfile.lock
📄 README.md                    # Project documentation
</pre>



⸻

✅ Requirements
	•	Python 3.9 or newer
	•	PostgreSQL
	•	Pipenv

⸻

🧰 Setup Instructions

1. Clone the Repo

git clone https://github.com/yourusername/epic-events-crm.git
cd epic-events-crm


⸻

2. Install Dependencies Using Pipenv

pipenv install
pipenv shell


⸻

3. 🔧 Prepare Environment Variables

Create a .env file at the project root and add the following variables:

# PostgreSQL DB URL
DATABASE_URL=postgresql://postgres@localhost:5432/epic_event_db

# Secret key for JWT
JWT_SECRET_KEY=your_secret_key_here

# Token expiration (in minutes)
JWT_EXPIRATION_MINUTES=60

Make sure to replace your_secret_key_here with a secure random string (e.g., using openssl rand -hex 32 or any password generator).

✅ Note: This .env file is automatically loaded by the application to configure the database and JWT authentication.

⸻

4. Configure PostgreSQL

-- In psql
CREATE DATABASE epic_event_db;

Also, update alembic.ini if using Alembic directly:

# Inside alembic.ini
sqlalchemy.url = postgresql://postgres@localhost:5432/epic_event_db


⸻

5. 🏗️ Initialize the Database

Run this command to auto-create the tables:

python main.py

Alternatively, using Alembic:

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
	•	JWT token is saved in ~/.epic_crm_token by default
	•	To logout, delete that file or run:

python main.py logout


	•	You can change the token path to a custom one for easier local development

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

⸻

Let me know if you’d like to include .env.example, unit test instructions, or Docker setup next!