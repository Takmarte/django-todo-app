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



=======





## 🔐 JWT Authentication (For Learning Purposes)

The project includes JWT token authentication endpoints as examples to demonstrate how JWT works with Django REST Framework.

- Obtain token:  
  POST /api/token/  
  Body:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
- Refresh token:                                             
   POST /api/token/refresh/                                   
   Body:

   ```json
   {
     "refresh": "your_refresh_token"
   }


- Use the access token in requests:
   Authorization: Bearer <your_access_token>


Note: These endpoints are included for educational purposes and not fully integrated with the frontend views.

## 🛠️ Tech Stack

Django REST Framework

JWT (djangorestframework-simplejwt)

=======


## 🔍 Project Details
   This application is a simple but structured daily task management system built with Django. It allows users to create categorized task lists for each day, add subtasks, and track their completion status dynamically. The key components of the system are as    
follows:


🗂️ Category System
- Tasks are grouped under a hierarchical category structure.

- Each category can optionally have a parent category (self-referencing model).

- Categories are linked to daily task lists, enabling filtered task views per category.


✅ Daily To-Do Lists
- Each user can create a separate to-do list for each day.

- A daily list is associated with a specific category.

- Users can add tasks to each daily list, and these tasks are further divided into subtasks.


📌 Tasks and Subtasks
- Every daily to-do list contains multiple tasks (Todos).

- Each task can contain one or more subtasks (TodoItems).

- When all subtasks are marked as done, the parent task is automatically marked as finished.

- Tasks can be marked as private, in which case they are only visible to their owner.

- Admin users have access to all tasks, including private ones.


📈 Progress Tracking
- A progress bar is displayed for each task based on the completion percentage of its subtasks.

- This value is dynamically calculated using a custom progress method on the model.


⚙️ Dynamic Interaction with AJAX
- Key operations such as toggling task/subtask status, adding or deleting subtasks, and creating new tasks are performed without reloading the page.

- This enhances the user experience with real-time updates and responsiveness.

- Toggle buttons such as Done/Not Done and Finished (Yes/No) are handled asynchronously.

Interactive Features:

- Some pages include interactive collapsible forms for adding new subtasks or tasks.

- These forms are initially hidden and appear dynamically when the user clicks an “Add” or “+” button.

- Once a new task or subtask is added, it is appended to the list immediately using JavaScript, without refreshing the page.

- This approach provides a clean interface by avoiding clutter and only showing forms when needed.


