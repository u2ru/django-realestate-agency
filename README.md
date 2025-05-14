# Activate virtual environment

For Linux/Mac:

```bash
source venv/bin/activate
```

For Windows:

```bash
.\venv\Scripts\activate
```

Install Requirements:

```bash
pip install -r requirements.txt
```

# Run server

```bash
python manage.py runserver
```

# Exit virtual environment

```bash
deactivate
```

# Run make migrations

```bash
python manage.py makemigrations
```

# Run migrations

```bash
python manage.py migrate
```

# Create superuser

```bash
python manage.py createsuperuser
```

# generating po files

```bash
python manage.py makemessages -l ka --extension=html --ignore="venv/*"
python manage.py makemessages -l ru --extension=html --ignore="venv/*"
```

# compile po files

```bash
python manage.py compilemessages
```

# collect static files

```bash
python manage.py collectstatic
```
