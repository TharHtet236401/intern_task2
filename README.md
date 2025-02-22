# Financial Transaction Tracker

A Django-based financial transaction tracking system that helps users manage their income, expenses, and budgets.

## Features

- Track income and expenses with categorization
- View transaction history with filtering options
- Export transactions to CSV
- Monthly budget management
- Financial analysis and reporting
- Interactive charts for expense/income visualization

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Setup Instructions

1. Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run database migrations:

```bash
python manage.py migrate
```

4. (Optional) Seed the database with sample transactions:

```bash
python manage.py seed_transactions
```

5. Start the development server:

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Project Structure

- `transaction/` - Main application directory
  - `models.py` - Database models for Transaction and Budget
  - `views.py` - View functions for handling requests
  - `forms.py` - Form definitions for data validation
  - `management/commands/` - Custom management commands
  - `templates/` - HTML templates
  - `migrations/` - Database migrations

## AI Usage Report

#HTMX
--For the frontend, since I had no experience with HTMX, I first used a simple template with basic CRUD functionality. After completing it, I tried converting it to HTMX using Cursor Composer and solved issues. Later, I noticed some changes in my backend code due to HTMX integration, so I worked on understanding and adjusting my backend accordingly.

#Chart
--Also i have not experinec with the chart.js.But, I stuided the basic function to know what kind of data to sent from backend.Then,I used code suggestions of Cursor to develop the chart backend functions.
