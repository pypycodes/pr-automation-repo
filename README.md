# PR Automation Repository

A comprehensive multi-file project for testing pull request automation and AI capabilities.

## Project Structure

```
pr-automation-repo/
├── api/
│   └── endpoints.py          # Flask API endpoints
├── config/
│   └── settings.py           # Application configuration
├── models/
│   └── user.py               # User data model
├── services/
│   └── pr_service.py         # PR business logic
├── utils/
│   └── helpers.py            # Utility functions
├── tests/
│   ├── test_app.py           # Original app tests
│   ├── test_user_model.py    # User model tests
│   └── test_pr_service.py    # PR service tests
├── app.py                    # Original simple app
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── Makefile                 # Development commands
└── README.md                # This file
```

## Features

- **Multi-file architecture**: Separate concerns across different modules
- **User management**: Complete user model with validation and roles
- **PR service**: Full pull request lifecycle management
- **REST API**: Flask-based API with multiple endpoints
- **Configuration management**: Environment-based settings
- **Comprehensive testing**: Unit tests for all major components
- **Development tools**: Linting, formatting, and test coverage

## Setup

1. **Install dependencies**:
   ```bash
   make install
   ```

2. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run the application**:
   ```bash
   make run
   ```

The API will be available at `http://localhost:5000`

## API Endpoints

- `GET /health` - Health check
- `POST /users` - Create a new user
- `POST /prs` - Create a new pull request
- `GET /prs` - List pull requests
- `POST /prs/{id}/reviewers` - Add reviewer to PR
- `POST /prs/{id}/comments` - Add comment to PR
- `GET /prs/stats` - Get PR statistics

## Testing

Run all tests:
```bash
make test
```

Run tests with coverage:
```bash
make test-cov
```

## Development

Format code:
```bash
make format
```

Run linting:
```bash
make lint
```

Clean up:
```bash
make clean
```

## Usage Examples

### Create a user via API
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "roles": ["developer"]
  }'
```

### Create a PR via API
```bash
curl -X POST http://localhost:5000/prs \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Add new feature",
    "description": "Implementing amazing new functionality",
    "author": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com"
    },
    "source_branch": "feature/new-feature",
    "target_branch": "main"
  }'
```

This project is designed to provide a realistic multi-file codebase for testing PR automation, code review, and AI-powered development tools.
