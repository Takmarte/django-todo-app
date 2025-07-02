# 📂 To-Do App – Django Application

This is a standalone Django application within the larger project that provides users with the ability to manage personal to-do tasks. It allows authenticated users to add, update, categorize, and delete their own to-dos. Superusers can see all to-dos, regardless of ownership.

---

## 🔧 Features

- 📆 Create, update, and delete tasks
- 🔑 Mark tasks as private or public
- ⏰ Track deadlines and finished dates
- 📂 Categorize to-dos
- 🌟 Simple and styled UI using Bootstrap

---

## 🔍 Interface Overview

Below are the key pages of the todo_app interface. Each image is followed by a brief description. To display these screenshots properly in GitHub, place the images in a folder named `/screenshots/` at the root of your repository and reference them relatively.

### 🔑 Login Page
Enables users to log in with their credentials.

![Login](todo_app/screenshots/loginhtml.png)

### ✍️ Register Page
Lets users register a new account by entering a username and password.

![Register](todo_app/screenshots/registerhtml.png)

### 📄 All To-Dos
Lists to-dos for the logged-in user. Admins can see all tasks.

![All To-Dos](todo_app/screenshots/alltodoshtml.png)

### ➕ Create To-Do
Allows creation of a new to-do, category selection, and optional privacy marking.

![Create To-Do](todo_app/screenshots/createtodohtml.png)

### ✏️ Update To-Do
Update a task's title, description, deadline, or finished state.

![Update To-Do](todo_app/screenshots/updatehtml.png)

### 📂 Category View
Show tasks under a specific category.

![Category View](todo_app/screenshots/categoryviewhtml.png)

### ➕ Add Category
Users can define new categories.

![Add Category](todo_app/screenshots/newcategoryhtml.png)

### 👤 User Info Page
Displays current user details.

![User Info](todo_app/screenshots/userinformationhtml.png)

### ℹ️ About Page
Static information page about the app.

![About](todo_app/screenshots/abouthtml.png)

---

## 🚀 Usage

This app is part of a Django project. Make sure to run migrations and create a superuser before use:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 🌐 Notes

- By default, new to-dos are marked as private.
- Admin users can view and manage all to-dos, including private ones.
- The interface uses Bootstrap 5 for styling.

---

Feel free to customize the app and extend its functionality as needed!

