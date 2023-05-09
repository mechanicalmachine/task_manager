# task_manager
Simple app for managing background tasks via API.

## Installation

- Pull code to you machine
- Install requirements: `pip install -r requirements.txt`
- Make migrations: `python manage.py migrate`
- Run message broker: `docker-compose up -d`
- Run server: `python manage.py migrate`
- Create superuser: `python manage.py createsuperuser`
- Open admin site in browser: `http://127.0.0.1:8000/admin`
- Use api methods as at explained further

## Examples

First, you need to create a user. You can yse management command or admin site for that.
Then you can find user token in admin site. You should use this token for all requests.

NOTE: as a task name you should pass task reference like `task_manager.tasks.task_one` not just a task name.

For task creation you can use following curl request:
```bash
curl --location --request POST 'http://127.0.0.1:8000/tasks/' \
  --header 'Authorization: Token YOUR-TOKEN}' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "name": "task_manager.tasks.task_one",
    "params": {
        "param1": 1,
        "param2": 2
    },
    "options": {
        "retry": 200,
        "delay": 1
    }
}'
```

For retrieving tasks list based on their name you can use following curl request:
```bash
curl --location --request GET 'http://127.0.0.1:8000/tasks?name=task_manager.tasks.task_one' \
  --header 'Authorization: Token YOUR-TOKEN' \
  --header 'Content-Type: application/json'
```

For task retrieving you can use following curl request:
```bash
curl --location --request GET 'http://127.0.0.1:8000/tasks/{task_id}' \
  --header 'Authorization: Token YOUR-TOKEN' \
  --header 'Content-Type: application/json'
```

For task cancellation you can use following curl request:
```bash
curl --location --request POST 'http://127.0.0.1:8000/tasks/{task_id}/cancel' \
  --header 'Authorization: Token YOUR-TOKEN' \
  --header 'Content-Type: application/json'
```

## Admin site

You can find list of all task, detailed task information etc. in admin interface.

You can also select few tasks and cancel them at the same time using admin actions.
