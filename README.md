# 📊 Financial Transaction Tracker

A Django-based financial transaction tracking system that helps users manage their income, expenses, and budgets.

## ✨ Features

- Track income and expenses with categorization
- View transaction history with filtering options
- Export transactions to CSV
- Monthly budget management
- Financial analysis and reporting
- Interactive charts for expense/income visualization

## 🔧 Prerequisites

- Python 3.x
- pip (Python package installer)

## 🚀 Setup Instructions

### 1. Clone the repository:
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd financial-tracker
```

### 2. Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Run database migrations:
```bash
python manage.py migrate
```

### 5. (Optional) Seed the database with sample transactions:
```bash
python manage.py seed_transactions
```

### 6. Start the development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## 📁 Project Structure

- `transaction/` - Main application directory
  - `models.py` - Database models for Transaction and Budget
  - `views.py` - View functions for handling requests
  - `forms.py` - Form definitions for data validation
  - `management/commands/` - Custom management commands
  - `templates/` - HTML templates
  - `migrations/` - Database migrations

## 🤖 AI Usage Report

### #HTMX
--I became experienced in HTMX after completing the task 1. so , i create the backend for the sections of the dyanmic pages.And then implment by using AI Composer to send the htxm request from the frontend.

### #Chart
--I also had no experience with Chart.js, but I studied its basic functions to understand what kind of data needed to be sent from the backend. Then, I used code suggestions from Cursor to develop the backend functions for the chart.For backend complex logic for trend chart, I used AI composer to generate the code and tried so hard to understand the logic.

### #Ramdom 
--as I had no experience with generating mock data, I used Cursor Composer to generte the mock using random package to display the data in the frontend with certain criteria.I used random instead of faker library as it makes the data more realistic to the range i want to input and easy to understand and follwed along the AI suggestions.

### #Request 
--Although I try to modulate the css and js with separate files, but I had some issues with the htmx request also due to time constraint for me to do it.I will make sure to understand the usage of static files and modulate the css and js with separate files before interview.
