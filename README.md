# Subscription & Budget Optimizer

Subscription & Budget Optimizer is a small Python web app for tracking subscriptions, setting a monthly budget, and viewing a simple spending dashboard.

## Features

- User registration and login
- Add, edit, view, and delete subscriptions
- Set a monthly budget and warning threshold
- View a dashboard summary of subscription spending
- SQLite-based local storage

## Tech Stack

- Python
- Flask
- SQLite
- Pytest

## Project Structure

- `app.py` - main Flask application
- `main.py` - simple demo script for service testing
- `models/` - domain models
- `repositories/` - data access layer
- `services/` - business logic
- `templates/` - HTML templates
- `tests/` - test suite

## Run Locally

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
pip install flask
```

3. Start the app:

```bash
python app.py
```

4. Open `http://127.0.0.1:5000` in your browser.

## Run Tests

```bash
pytest
```
