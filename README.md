# Architecture Patterns and Design Patterns - Practice Project

[![Tests](https://github.com/rzambrano1/architecture_and_design_patterns/actions/workflows/tests.yml/badge.svg)](https://github.com/rzambrano1/architecture_and_design_patterns/actions/workflows/tests.yml)
[![GitHub release](https://img.shields.io/github/v/release/rzambrano1/architecture_and_design_patterns)](https://github.com/rzambrano1/architecture_and_design_patterns/releases)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

A practice project implementing architecture patterns and design principles from modern software engineering literature. The code follows test-driven development (TDD), domain-driven design (DDD), and repository pattern implementations.

The code follows along examples from Percival et al (2020) and incorporates elements from Ayeva et al (2024) and Okken (2022).

## Motivation

As a data scientist focused on feature engineering, model design, experimentation, causal analysis, and inference/prediction, I find it valuable to strengthen my software development skills. This practice helps me:

- Write more efficient, maintainable, and readable code
- Better communicate and collaborate with software engineers, DevOps, and MLOps teams
- Apply software engineering best practices to data science workflows
- Build production-ready machine learning systems

## Learning Objectives

- **Domain-Driven Design**: Separating business logic from infrastructure concerns
- **Repository Pattern**: Abstracting data persistence
- **ORM Mapping**: Using SQLAlchemy with imperative mapping
- **Test-Driven Development**: Comprehensive test coverage with pytest
- **Continuous Integration**: Automated testing with GitHub Actions
- **Design Patterns**: Foundational Design Principles, Patterns from the Gang of Four, Modern Patterns

I am overlooking code documentation. In my code I include docstrings with detailed sections, including: Parameters, Returns, Raises, Warns, and Examples (compatible with doctest module). I am also not making use sphinx. I am omitting documentation to keep the code short.

## Project Structure
```
architecture-patterns-python/
├── src/
│   └── bactch_allocations/
|       ├── domain/
│       |   └── model.py           # Domain model (Batch, OrderLine)
|       ├── adapters/
│       |   ├── orm.py             # SQLAlchemy mappings
│       |   └── repository.py      # Repository pattern implementation
|       ├── entrypoints/
│       |   └── flask_app.py       # 
|       ├── service_layers/
│       |   └── service_layer.py   # 
│       └── config.py              # Database configuration
├── test/
│   ├── e2e
│   |   └── test_api.py
│   ├── integration
|   │   ├── test_orm.py            # ORM mapping tests
|   │   └── test_repository.py     # Repository tests
│   ├── unit
|   │   ├── test_allocate.py       # Allocation logic tests
|   │   ├── test_batches.py        # Batch entity tests
|   │   └── test_services.py       # 
|   └──conftest.py                 # Shared test fixtures
├── .env                           # Environment variables
├── Dockerfile
├── docker-compose.yml             # Light-weight orchestration 
├── pyproject.toml                 # Project configuration
└── tox.ini                        # Test automation
```

## Database Setup

This project uses PostgreSQL running in Docker for local development.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pip
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) for Windows

### Installation

1. Clone the repository:
```bash
git clone https://github.com/rzambrano1/architecture_and_design_patterns.git
cd architecture_and_design_patterns
```

2. Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
                        # source .venv/bin/activate  # macOS/Linux
```

3. Install dependencies:
```bash
pip install -e ".[dev]"
```

### Docker Quick Start

1. **Start the database:**
```bash
   docker-compose up -d
```

2. **Verify it's running:**
```bash
   docker-compose ps
```

3. **Stop the database:**
```bash
   docker-compose down
```

### Database Connection Details
- **Host**: localhost
- **Port**: 5432
- **Database**: allocation
- **User**: postgres
- **Password**: postgres
- **Connection String**: `postgresql://postgres:postgres@localhost:5432/allocation`

### Notes
- **Tests use SQLite** in-memory for speed (no Postgres needed)
- **Development uses Postgres** for production-like environment
- Data persists between container restarts
- Use `docker-compose down -v` to delete all data

## Running Tests

### Using pytest directly:
```bash
pytest
```

### Using tox (recommended):
```bash
# Run all tests
tox

# Run specific environment
tox -e py311        # Run tests on Python 3.11
tox -e lint         # Run code quality checks
tox -e fast_lint    # Run light-weight quality checks avoiding ruff
tox -e coverage     # Run tests with coverage report
tox -e format       # Auto-format code
```

### View coverage report:
```bash
tox -e coverage
start htmlcov/index.html  # Windows
                          # open htmlcov/index.html  # macOS/Linux
```

## Development Tools

- **Testing**: pytest, pytest-cov
- **Linting**: ruff, black, mypy
- **Automation**: tox
- **CI/CD**: GitHub Actions

## References

- Percival, H., Gregory, B. (2020). **Architecture Patterns with Python:** *Enabling Test-Driven Development, Domain-Driven Design, and Event-Driven Microservices*. O'Reilly.
- Ayeva, K., Kasampalis, S. (2024). **Mastering Python Design Patterns:** *Craft Essential Python Patterns by Following Core Design Principles* (3rd ed.). Packt Publishing.
- Okken, B. (2022). **Python Testing with pytest:** *Simple, Rapid, Effective, and Scalable* (2nd ed.). The Pragmatic Programmers.

## License

This is a learning project for educational purposes.

## Contributing

This is a personal learning project, but feedback and suggestions are welcome! Feel free to open an issue.

---

**Note**: This project is part of my ongoing learning journey in software architecture and design patterns.