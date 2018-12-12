# todoList

#### Configuring and launching server
1. Go to project directory directory
1. edit (if needed) DATABASES configuration in *site_todoLst/settings.py*
2. create database with database name specified in *site_todoLst/settings.py* with proper permissions for database user specified in *site_todoLst/settings.py*:
  E.g. in database prompt:
  ```
  CREATE DATABASE <database_name> OWNER <username>;
  ```
3. configure database:
```
python manage.py migrate
```
4. Start server:
```
python manage.py runserver ip:port
```
(by default - internal ip and 8000 port)

#### Adding users with administrator privileges:
```
python manage.py createsuperuser --username <username>
```

#### site structure
/ - will redirect to authentification page (/sign_in) if not already logged in else to your task list (/task)

/sign_in - authentification page

/sign_up - registration page

/task - main page that allows you to view, filter,delete and edit task available to you as well as create new tasks.

Tips for task list managment:
 - to edit task description for any task from your task list - double clik on task descripion

 - only selected (by activating corresponding checkbox) tasks are deleted/updated. 







