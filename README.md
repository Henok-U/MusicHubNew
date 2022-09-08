# MuiscHubNew

Pet project for itechart intership

Check out full [documentation](https://musichubnew.readthedocs.io/en/latest/)

Visit production [server](http://3.71.253.142/).

# Prerequisites

- [Docker](https://www.docker.com/)
- [Python](https://www.python.org/downloads/)

# Initialize the project

Start the postgres container for local development:
WINDOWS:

```bash
docker-compose up
```

Create virtual enviroment and install requirements:

```bash
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
```

Make migrations and create super user

```bash
python manage.py migrate && python manage.py createsuperuser
```

Run development server and go to <http://localhost:8000/> :

```bash
python manage.py runserver
```
