# AI-Powered Personal Finance Tracker

A comprehensive personal finance management system that leverages artificial intelligence to analyze spending habits, predict future expenses, and provide personalized budgeting strategies.

## Features

- 🤖 AI-powered expense analysis and prediction
- 📊 Interactive spending visualization
- 📱 Cross-platform mobile app (React Native)
- 💰 Personalized budgeting recommendations
- 📈 Financial decision impact simulator

## Tech Stack

### Backend

- Django (Python web framework)
- Django REST Framework (API)
- PostgreSQL (Database)
- Scikit-learn (Machine Learning)

### Frontend

- React Native (Mobile App)
- React Navigation
- React Native Charts

### ML Components

- Scikit-learn
- Pandas
- NumPy

## Project Structure

```
Personal_Finance_Tracker/
├── backend/           # Django backend
├── frontend/         # React Native mobile app
├── ml_models/        # Machine learning models
└── requirements.txt  # Python dependencies
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn
- Git

### Backend Setup

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd Personal_Finance_Tracker
   ```

2. Set up Python virtual environment:

   ```bash
   cd backend
   python -m venv venv
   ```

3. Activate the virtual environment:

   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Unix or MacOS:
     ```bash
     source venv/bin/activate
     ```

4. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables:

   ```bash
   cp .env.example .env
   # Edit .env file with your configurations
   ```

6. Run database migrations:

   ```bash
   python manage.py migrate
   ```

7. Create a superuser (optional):

   ```bash
   python manage.py createsuperuser
   ```

8. Initialize sample data (optional):

   ```bash
   python manage.py init_sample_data
   ```

9. Start the development server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd frontend/FinanceTrackerApp
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:

   ```bash
   npm start
   ```

4. Run on your preferred platform:
   - Press `a` for Android
   - Press `i` for iOS (requires MacOS)
   - Press `w` for web

## Development Guidelines

### Code Style

- Backend: Follow PEP 8 style guide for Python code
- Frontend: Follow ESLint and Prettier configurations
- Use meaningful variable and function names
- Write docstrings and comments for complex logic

### Git Workflow

1. Create a new branch for each feature/bugfix:

   ```bash
   git checkout -b feature/feature-name
   ```

2. Make your changes and commit with clear messages:

   ```bash
   git add .
   git commit -m "feat: add feature description"
   ```

3. Push your branch and create a pull request:
   ```bash
   git push origin feature/feature-name
   ```

### Testing

- Write unit tests for new features
- Run tests before committing:

  ```bash
  # Backend tests
  python manage.py test

  # Frontend tests
  npm test
  ```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

Please make sure to update tests as appropriate and follow the existing code style.

## License

MIT License
