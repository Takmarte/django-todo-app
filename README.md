# Django Training Practice Project

This repository contains a simple backend practice project developed as part of my internship training. The goal of this work is to reinforce my understanding of backend development using Python and the Django framework.

## 🎯 Purpose

- To gain hands-on experience with Django  
- To improve my understanding of Python in a real project structure  
- To practice essential backend concepts such as routing, views, templates, and models

## 🛠️ Technologies Used

- Python 3.13.2  
- Django 5.x  
- HTML (Django Templates)  
- SQLite (Default Django Database)

## 📁 Project Structure

The project follows the standard Django layout:

```
/project_root
├── manage.py
├── /project_name/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── /app_name/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
└── db.sqlite3
```

## 🚀 How to Run Locally

1. **Clone the repository (in the terminal):**
   ```bash
   git clone https://github.com/Takmarte/djangoproject.git
   cd djangoproject
   ```

2. **(Optional) Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required packages:**
   ```bash
   pip install django
   ```

4. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

5. **Open your browser and visit:**
   ```
   http://127.0.0.1:8000/
   ```

## 📝 Notes

- This project is built for educational purposes only.  
- It was created as part of my internship to improve backend development skills using Django.