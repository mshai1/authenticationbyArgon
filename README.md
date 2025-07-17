# Flask User Management App

This is a simple Flask application designed to manage user records using an SQLite database. It is built using the Flask framework, SQLAlchemy for ORM, and includes basic user functionality such as adding, storing, and displaying user information.

## 🚀 Features

- Add new users with:
  - Full Name
  - Email Address
  - Password
  - Phone Number
  - Address
- Store user data securely in a SQLite database (`users-list.db`)
- Use SQLAlchemy for object-relational mapping (ORM)
- Separation of concerns using templates, static files, and instance directory

## 🛠 Tech Stack

- **Python 3**
- **Flask**
- **Flask SQLAlchemy**
- **HTML/CSS (Jinja templates)**

## 📁 Project Structure

myapp/
│
├── main.py # Entry point of the app
├── requirements.txt # Python dependencies
├── static/ # Static files like CSS, JS
├── templates/ # HTML templates
├── instance/ # Contains the SQLite DB (ignored in Git)
├── .venv/ # Virtual environment (ignored in Git)
└── .gitignore # Git ignore rules


## 📦 Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/your-username/authenticationbyArgon.git
cd authenticationbyArgon
```

2. Install dependencies

```
pip install -r requirements.txt
```

2. Run the application

```
python main.py
```

The app will be accessible at: http://127.0.0.1:5000/

💡 Notes
- Make sure instance/ and .venv/ are not pushed to your repo.

- The database file users-list.db is created inside the instance/ directory.

You can initialize the database using:

```
with app.app_context():
    db.create_all()
```

📄 License
This project is for educational purposes and does not include user authentication, input validation, or encryption. Feel free to expand and improve upon it.

🤝 Contributions
Pull requests and suggestions are welcome!
